import { McpServer } from "@modelcontextprotocol/server";
import { z } from "zod";
import {
  indexGraph,
  NODE_TYPES,
  NodeIdSchema,
  searchReadables,
  walkChain,
  type EvidenceGraph,
  type Readable,
} from "~/contracts/evidence";

// Le serveur MCP de Métabolisme : LECTURE SEULE.
//
// Il donne à un assistant (Claude) ce que le site donne à un lecteur : les
// posts (relus ou en relecture), les notes du livret, la méthode, et pour
// chaque publication son graphe de preuves. Rien ne s'écrit, rien ne sort du
// périmètre choisi par `selectReadable` — une note isolée n'y est jamais.
//
// Une instance par requête (serveur sans état) : le contenu est l'index figé
// au build, les graphes des assets statiques lus à la demande.

export type McpContent = {
  readonly origin: string;
  readonly readables: ReadonlyArray<Readable>;
  readonly method: string | undefined;
  readonly loadGraph: (readable: Readable) => Promise<EvidenceGraph>;
};

const INSTRUCTIONS = `Métabolisme est un programme de recherche : concevoir des institutions et des systèmes économiques à partir des conditions matérielles réelles, publiés comme des CHAÎNES DE PREUVES exécutables (read_method pour la méthode complète).

Deux objets :
- les POSTS, articles d'étude (logement, monopoles, autoroutes…), statut « published » (relu) ou « in_review » (en attente de relecture de l'auteur — le dire quand on le cite) ;
- les NOTES du recueil « Livret 2027 », doctrine d'un groupe de travail, à lire dans l'ordre de leur position. Elles portent surtout des valeurs, choix et propositions : ne pas les présenter comme des résultats d'étude.

Chaque publication a un graphe de preuves. Les nœuds ont un statut épistémique (préfixe de l'identifiant) : S source, D définition, O observation, T transformation, M mesure, H hypothèse, R résultat, I interprétation, V valeur, C choix, P proposition, L limite. Le texte ancre ses chiffres sur des nœuds : [passage](ev:R-07) ou (R-07). Pour vérifier une affirmation, remonter la chaîne (walk_graph, direction upstream) jusqu'aux sources et leurs localisateurs (page, citation) ; pour mesurer ce qu'une hypothèse ou une source porte, descendre (downstream).

Citer une publication par son adresse : ${"`url`"} dans les réponses des outils.`;

const READ_ONLY = { readOnlyHint: true, destructiveHint: false, idempotentHint: true } as const;

const KindSchema = z.enum(["post", "note"]);

function json(data: unknown, indent: number | undefined = 2) {
  return { content: [{ type: "text" as const, text: JSON.stringify(data, null, indent) }] };
}

function failure(message: string) {
  return { isError: true, content: [{ type: "text" as const, text: message }] };
}

function describe(readable: Readable, origin: string) {
  return {
    kind: readable.kind,
    slug: readable.slug,
    title: readable.title,
    ...(readable.subtitle === undefined ? {} : { subtitle: readable.subtitle }),
    date: readable.date,
    ...(readable.status === undefined ? {} : { status: readable.status }),
    ...(readable.study === undefined ? {} : { study: readable.study }),
    ...(readable.collection === undefined ? {} : { collection: readable.collection }),
    ...(readable.summary === undefined ? {} : { summary: readable.summary }),
    ...(readable.context === undefined ? {} : { context: readable.context }),
    url: origin + readable.path,
  };
}

export function createMetabolismeMcpServer(content: McpContent): McpServer {
  const { origin, readables } = content;
  const server = new McpServer(
    { name: "metabolisme", title: "Métabolisme", version: "1.0.0" },
    { instructions: INSTRUCTIONS },
  );

  const find = (slug: string, kind?: "post" | "note") =>
    readables.find((entry) => entry.slug === slug && (kind === undefined || entry.kind === kind));
  const unknown = (slug: string) =>
    failure(`Aucune publication « ${slug} ». list_publications donne les slugs disponibles.`);

  async function graphOf(readable: Readable) {
    try {
      return await content.loadGraph(readable);
    } catch (error) {
      return error instanceof Error ? error : new Error(String(error));
    }
  }

  server.registerTool(
    "list_publications",
    {
      title: "Lister les publications",
      description:
        "Liste les posts (articles d'étude) et les notes du Livret 2027 : slug, titre, date, statut (posts), position dans le recueil (notes), résumé, adresse. Point de départ pour choisir quoi lire.",
      inputSchema: z.object({
        kind: KindSchema.optional().describe("post ou note ; absent = les deux"),
        status: z
          .enum(["published", "in_review"])
          .optional()
          .describe("posts seulement : relus ou en attente de relecture"),
      }),
      annotations: READ_ONLY,
    },
    ({ kind, status }) =>
      json(
        readables
          .filter((entry) => kind === undefined || entry.kind === kind)
          .filter((entry) => status === undefined || entry.status === status)
          .map((entry) => describe(entry, origin)),
      ),
  );

  server.registerTool(
    "read_publication",
    {
      title: "Lire une publication",
      description:
        "Renvoie les métadonnées puis le texte intégral (Markdown) d'un post ou d'une note. Les ancres [passage](ev:R-07) et (R-07) renvoient aux nœuds du graphe de preuves (get_graph, walk_graph).",
      inputSchema: z.object({
        slug: z.string().min(1),
        kind: KindSchema.optional().describe("à préciser seulement si un slug est ambigu"),
      }),
      annotations: READ_ONLY,
    },
    ({ slug, kind }) => {
      const readable = find(slug, kind);
      if (readable === undefined) return unknown(slug);
      return {
        content: [
          { type: "text" as const, text: JSON.stringify(describe(readable, origin), null, 2) },
          { type: "text" as const, text: readable.markdown },
        ],
      };
    },
  );

  server.registerTool(
    "get_graph",
    {
      title: "Graphe de preuves (JSON)",
      description:
        "Renvoie le graphe de preuves d'une publication en JSON : { slug, version, node_count, nodes }. Chaque nœud a id, type, title, depends_on, limitations et les champs de son statut (sources : éditeur, URL, fichiers figés et empreintes ; observations : valeur et localisateurs page/citation ; hypothèses : valeur centrale et plage ; résultats : formule, code, sortie). Le graphe d'un post peut dépasser 300 Ko : filtrer par `types` ou `ids` quand c'est possible.",
      inputSchema: z.object({
        slug: z.string().min(1),
        kind: KindSchema.optional(),
        types: z.array(z.enum(NODE_TYPES)).optional().describe("ne garder que ces statuts"),
        ids: z.array(NodeIdSchema).optional().describe("ne garder que ces nœuds (ex. R-07)"),
      }),
      annotations: READ_ONLY,
    },
    async ({ slug, kind, types, ids }) => {
      const readable = find(slug, kind);
      if (readable === undefined) return unknown(slug);
      const graph = await graphOf(readable);
      if (graph instanceof Error) return failure(graph.message);
      const keepTypes = types === undefined ? undefined : new Set<string>(types);
      const keepIds = ids === undefined ? undefined : new Set<string>(ids);
      const nodes = graph.nodes.filter(
        (node) =>
          (keepTypes === undefined || keepTypes.has(node.type)) &&
          (keepIds === undefined || keepIds.has(node.id)),
      );
      return json(
        { slug: readable.slug, version: graph.version, node_count: graph.nodes.length, nodes },
        undefined,
      );
    },
  );

  server.registerTool(
    "walk_graph",
    {
      title: "Parcourir le graphe",
      description:
        "Parcourt le graphe de preuves depuis un nœud, en largeur. upstream : ce dont il dépend, jusqu'aux sources (vérifier une affirmation). downstream : ce qui s'appuie sur lui (ce qu'une source ou une hypothèse fausse ferait tomber). Renvoie le nœud de départ, chaque nœud atteint avec sa profondeur, et les limites déclarées en chemin.",
      inputSchema: z.object({
        slug: z.string().min(1),
        kind: KindSchema.optional(),
        node_id: NodeIdSchema.describe("nœud de départ, ex. R-07"),
        direction: z.enum(["upstream", "downstream"]).default("upstream"),
        max_depth: z.number().int().min(1).optional().describe("absent = toute la chaîne"),
      }),
      annotations: READ_ONLY,
    },
    async ({ slug, kind, node_id, direction, max_depth }) => {
      const readable = find(slug, kind);
      if (readable === undefined) return unknown(slug);
      const graph = await graphOf(readable);
      if (graph instanceof Error) return failure(graph.message);
      const index = indexGraph(graph);
      const root = index.byId.get(node_id);
      if (root === undefined) {
        return failure(`Aucun nœud ${node_id} dans le graphe de « ${readable.slug} ».`);
      }
      const steps = walkChain(index, node_id, direction, max_depth).map((step) => ({
        depth: step.depth,
        node: index.byId.get(step.id),
      }));
      const reached = [
        root,
        ...steps.flatMap((step) => (step.node === undefined ? [] : [step.node])),
      ];
      const limitIds = [...new Set(reached.flatMap((node) => node.limitations))];
      const limits = limitIds.flatMap((id) => {
        const node = index.byId.get(id);
        return node === undefined ? [] : [node];
      });
      return json({ slug: readable.slug, direction, root, steps, limits }, undefined);
    },
  );

  server.registerTool(
    "search",
    {
      title: "Rechercher",
      description:
        "Recherche plein texte dans les posts et les notes du livret, insensible à la casse et aux accents. Tous les mots doivent figurer. Renvoie les publications les plus denses d'abord, avec des extraits.",
      inputSchema: z.object({
        query: z.string().min(1),
        kind: KindSchema.optional(),
        limit: z.number().int().min(1).max(50).default(10),
      }),
      annotations: READ_ONLY,
    },
    ({ query, kind, limit }) =>
      json(
        searchReadables(readables, query, { limit, ...(kind === undefined ? {} : { kind }) }).map(
          (hit) => {
            const readable = find(hit.slug, hit.kind);
            return { ...hit, url: readable === undefined ? undefined : origin + readable.path };
          },
        ),
      ),
  );

  server.registerTool(
    "read_method",
    {
      title: "Lire la méthode",
      description:
        "Renvoie la méthode Métabolisme (la chaîne de preuves exécutable) : statuts des nœuds, graphe, règles pour les agents. À lire pour interpréter un graphe ou juger une publication.",
      annotations: READ_ONLY,
    },
    () =>
      content.method === undefined
        ? failure("La méthode n'est pas dans ce déploiement.")
        : { content: [{ type: "text" as const, text: content.method }] },
  );

  return server;
}
