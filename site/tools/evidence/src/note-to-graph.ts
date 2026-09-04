import { z } from "zod";
import {
  collectAnchoredIds,
  danglingReferences,
  EvidenceGraphSchema,
  NODE_TYPES,
  NodeIdSchema,
  type EvidenceGraph,
  type EvidenceNode,
  type EvidenceVersion,
  type FileManifest,
} from "@metabolisme/evidence";
import { mimeOf } from "./mime.ts";

// Dérivation pure d'une note : evidence.yaml (écrit à la main, au plus près
// du contrat du graphe mais avec des raccourcis d'auteur) → graphe + manifeste.
//
// Raccourcis acceptés :
//   - une source liste ses fichiers par chemin relatif au dossier de la note
//     (« sources/datalab-395.pdf ») ; taille, type et empreinte sont calculés ;
//   - une observation localise sa lecture (fichier, page, citation) ;
//   - un résultat peut donner sa formule et sa valeur en clair, sans code.

const Files = z.array(z.string().min(1)).default([]);

const AuthoredSource = z.object({
  id: NodeIdSchema,
  type: z.literal("source"),
  title: z.string().min(1),
  publisher: z.string().min(1),
  source_url: z.string().min(1),
  dataset_id: z.string().optional(),
  publication_date: z.string().optional(),
  retrieved_at: z.string().optional(),
  geographic_scope: z.string().optional(),
  temporal_scope: z.string().optional(),
  license: z.string().optional(),
  notes: z.string().optional(),
  files: Files,
  depends_on: z.array(NodeIdSchema).default([]),
  limitations: z.array(NodeIdSchema).default([]),
});

// Tout autre nœud passe tel quel dans le contrat (validé en sortie).
const AuthoredOther = z
  .object({
    id: NodeIdSchema,
    type: z.enum(NODE_TYPES).exclude(["source"]),
  })
  .loose();

const AuthoredNode = z.union([AuthoredSource, AuthoredOther]);

export const AuthoredEvidenceSchema = z.object({
  nodes: z.array(AuthoredNode),
});

export type AttachedFile = {
  readonly size: number;
  readonly checksum: string;
};

export type NoteToGraphOptions = {
  version: EvidenceVersion;
  // Lecture d'un fichier joint (chemin relatif au dossier de la note), ou
  // null s'il manque.
  readFile: (relativePath: string) => AttachedFile | null;
  // Préfixe de dépôt du dossier de la note (pour le manifeste).
  notePrefix: string;
};

export type NoteProblem = { readonly kind: string; readonly message: string };

export function noteToGraph(
  authored: unknown,
  markdown: string,
  options: NoteToGraphOptions,
): { graph: EvidenceGraph; files: FileManifest; problems: NoteProblem[] } {
  const problems: NoteProblem[] = [];
  const parsed = AuthoredEvidenceSchema.parse(authored);
  const files: FileManifest = [];
  const nodes: EvidenceNode[] = [];

  for (const node of parsed.nodes) {
    if (node.type !== "source") {
      // Raccourci d'auteur : une définition prend son terme pour titre.
      const withTitle =
        node.type === "definition" && !("title" in node) && typeof node["term"] === "string"
          ? { ...node, title: node["term"] }
          : node;
      nodes.push(withTitle as EvidenceNode);
      continue;
    }
    const { files: attached, ...rest } = node;
    nodes.push({
      ...rest,
      files: attached.map((relativePath) => {
        const read = options.readFile(relativePath);
        if (read === null) {
          problems.push({
            kind: "missing-file",
            message: `${node.id} : ${relativePath} introuvable`,
          });
        }
        const name = relativePath.split("/").at(-1) ?? relativePath;
        files.push({
          path: relativePath,
          from: `${options.notePrefix}${relativePath}`,
          size: read?.size ?? 0,
          mime: mimeOf(relativePath),
          hosted: read === null ? "none" : "asset",
        });
        return {
          path: relativePath,
          name,
          mime: mimeOf(relativePath),
          size: read?.size ?? 0,
          ...(read === null ? {} : { checksum: read.checksum }),
          hosted: read === null ? ("none" as const) : ("asset" as const),
        };
      }),
    });
  }

  const graph = EvidenceGraphSchema.parse({ nodes, version: options.version });

  for (const { from, to } of danglingReferences(graph)) {
    problems.push({ kind: "dangling", message: `${from} dépend de ${to}, absent du graphe` });
  }
  const ids = new Set(graph.nodes.map((node) => node.id));
  for (const id of collectAnchoredIds(markdown)) {
    if (!ids.has(id)) {
      problems.push({ kind: "unknown-anchor", message: `la note cite ${id}, absent du graphe` });
    }
  }
  const anchored = new Set(collectAnchoredIds(markdown));
  for (const node of graph.nodes) {
    // Chaque localisateur doit viser un fichier d'une source amont.
    if (node.type === "observation") {
      const upstreamFiles = new Set(
        node.depends_on.flatMap((dep) => {
          const source = graph.nodes.find((candidate) => candidate.id === dep);
          return source?.type === "source" ? source.files.map((file) => file.path) : [];
        }),
      );
      for (const locator of node.locators) {
        if (locator.file !== undefined && !upstreamFiles.has(locator.file)) {
          problems.push({
            kind: "locator",
            message: `${node.id} localise ${locator.file}, qui n'est joint à aucune de ses sources`,
          });
        }
      }
    }
    if (node.type === "source" && node.files.length === 0) {
      problems.push({ kind: "no-file", message: `${node.id} n'a aucun fichier figé` });
    }
  }
  // Un nœud que le texte ne cite pas et dont rien ne dépend est orphelin.
  const referenced = new Set(
    graph.nodes.flatMap((node) => [...node.depends_on, ...node.limitations]),
  );
  for (const node of graph.nodes) {
    if (!anchored.has(node.id) && !referenced.has(node.id)) {
      problems.push({ kind: "orphan", message: `${node.id} n'est ni cité par la note ni utilisé` });
    }
  }

  return { graph, files, problems };
}
