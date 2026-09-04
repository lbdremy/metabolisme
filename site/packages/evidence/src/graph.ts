import { z } from "zod";

// Contrat du graphe de preuves (méthode Métabolisme, INTRO §4 et §10).
//
// C'est LE format commun aux deux objets publiés par le site : un post (le
// graphe est dérivé des registres d'une étude — sources.yaml, definitions.yaml,
// hypotheses.yaml, claims.yaml) et une note (le graphe est écrit à la main,
// beaucoup plus court). Le panneau d'exploration ne connaît que ce contrat.
//
// Chaque nœud porte un statut épistémique (S, D, O, T, M, H, R, I, V, C, P,
// L) : c'est ce qui empêche de présenter une hypothèse comme une donnée ou un
// choix normatif comme une conclusion. Les identifiants sont la clé des
// relations (depends_on, limitations) et la cible des ancres dans le texte.

export const NODE_TYPES = [
  "source",
  "definition",
  "observation",
  "transformation",
  "measure",
  "hypothesis",
  "result",
  "interpretation",
  "value",
  "choice",
  "proposal",
  "limit",
] as const;

export type NodeType = (typeof NODE_TYPES)[number];

export const NODE_PREFIX: Record<NodeType, string> = {
  source: "S",
  definition: "D",
  observation: "O",
  transformation: "T",
  measure: "M",
  hypothesis: "H",
  result: "R",
  interpretation: "I",
  value: "V",
  choice: "C",
  proposal: "P",
  limit: "L",
};

export const NODE_TYPE_BY_PREFIX: Record<string, NodeType> = Object.fromEntries(
  (Object.entries(NODE_PREFIX) as [NodeType, string][]).map(([type, prefix]) => [prefix, type]),
);

// Identifiant d'un nœud : préfixe de statut + numéro (S-01, R-14, L-26…).
export const NODE_ID_PATTERN = /^[SDOTMHRIVCPL]-\d{2,3}$/;
export const NodeIdSchema = z.string().regex(NODE_ID_PATTERN);

// Un fichier rattaché au graphe (source figée, code, sortie de calcul). Le
// chemin est LOGIQUE, relatif au dossier de contenu de la publication
// (« sources/insee-focus-359.xlsx », « code/src/logement/core/parc.py »).
// `hosted` dit comment le site le sert : asset statique, stockage objet pour
// les fichiers trop lourds pour le CDN, ou pas du tout (fichier non
// redistribuable — seule l'URL d'origine reste).
export const EvidenceFileSchema = z.object({
  path: z.string().min(1),
  name: z.string().min(1),
  mime: z.string().min(1),
  size: z.number().int().nonnegative(),
  checksum: z
    .string()
    .regex(/^sha256:[0-9a-f]{64}$/)
    .optional(),
  hosted: z.enum(["asset", "object-store", "none"]),
});

// Où regarder dans un fichier source pour retrouver une observation : page
// d'un PDF, feuille d'un classeur, section d'une page, et la citation exacte.
export const LocatorSchema = z.object({
  file: z.string().min(1).optional(),
  page: z.number().int().positive().optional(),
  sheet: z.string().min(1).optional(),
  table: z.string().min(1).optional(),
  section: z.string().min(1).optional(),
  quote: z.string().min(1).optional(),
  url: z.string().url().optional(),
});

const NodeBase = z.object({
  id: NodeIdSchema,
  title: z.string().min(1),
  depends_on: z.array(NodeIdSchema).default([]),
  limitations: z.array(NodeIdSchema).default([]),
  notes: z.string().optional(),
});

export const SourceNodeSchema = NodeBase.extend({
  type: z.literal("source"),
  publisher: z.string().min(1),
  source_url: z.string().min(1),
  dataset_id: z.string().optional(),
  publication_date: z.string().optional(),
  retrieved_at: z.string().optional(),
  geographic_scope: z.string().optional(),
  temporal_scope: z.string().optional(),
  license: z.string().optional(),
  files: z.array(EvidenceFileSchema).default([]),
});

export const DefinitionNodeSchema = NodeBase.extend({
  type: z.literal("definition"),
  term: z.string().min(1),
  definition: z.string().min(1),
  url: z.string().optional(),
  last_updated: z.string().optional(),
  caveats: z.array(z.string()).default([]),
});

// Une hypothèse est soit un PARAMÈTRE (valeur centrale, plage plausible,
// unité — INTRO §9), soit une hypothèse QUALITATIVE (une relation ou une
// hypothèse directrice, portée par `statement`, sans valeur numérique). La
// dérivation (study-to-graph) exige l'une ou l'autre forme ; le contrat les
// accepte toutes deux pour que le panneau sache les afficher.
export const HypothesisNodeSchema = NodeBase.extend({
  type: z.literal("hypothesis"),
  name: z.string().min(1),
  central_value: z.number().optional(),
  plausible_range: z.tuple([z.number(), z.number()]).optional(),
  unit: z.string().min(1).optional(),
  statement: z.string().min(1).optional(),
  confidence: z.enum(["low", "medium", "high"]),
  affects: z.array(NodeIdSchema).default([]),
});

// Un paramètre chiffré porte ses trois champs numériques ensemble.
export function isQuantifiedHypothesis(node: z.infer<typeof HypothesisNodeSchema>): node is z.infer<
  typeof HypothesisNodeSchema
> & {
  central_value: number;
  plausible_range: [number, number];
  unit: string;
} {
  return (
    node.central_value !== undefined &&
    node.plausible_range !== undefined &&
    node.unit !== undefined
  );
}

// Une observation peut porter la valeur lue et l'endroit exact où la lire.
export const ObservationNodeSchema = NodeBase.extend({
  type: z.literal("observation"),
  value: z.string().optional(),
  locators: z.array(LocatorSchema).default([]),
});

// Référence au code qui produit un nœud (chemin logique dans les fichiers de
// la publication + chemin d'origine dans le dépôt de l'étude).
export const CodeRefSchema = z.object({
  path: z.string().min(1),
  repo_path: z.string().min(1),
  language: z.string().min(1),
});

export const DataRefSchema = z.object({
  path: z.string().min(1),
  repo_path: z.string().min(1),
});

const ComputedBase = NodeBase.extend({
  produced_by: CodeRefSchema.optional(),
  output: DataRefSchema.optional(),
  // Une note peut donner le calcul en clair (formule + valeur) sans code.
  value: z.string().optional(),
  formula: z.string().optional(),
});

export const TransformationNodeSchema = ComputedBase.extend({ type: z.literal("transformation") });
export const MeasureNodeSchema = ComputedBase.extend({ type: z.literal("measure") });
export const ResultNodeSchema = ComputedBase.extend({ type: z.literal("result") });

export const InterpretationNodeSchema = NodeBase.extend({ type: z.literal("interpretation") });
export const ValueNodeSchema = NodeBase.extend({ type: z.literal("value") });
export const ChoiceNodeSchema = NodeBase.extend({ type: z.literal("choice") });
export const ProposalNodeSchema = NodeBase.extend({ type: z.literal("proposal") });
export const LimitNodeSchema = NodeBase.extend({ type: z.literal("limit") });

export const EvidenceNodeSchema = z.discriminatedUnion("type", [
  SourceNodeSchema,
  DefinitionNodeSchema,
  HypothesisNodeSchema,
  ObservationNodeSchema,
  TransformationNodeSchema,
  MeasureNodeSchema,
  ResultNodeSchema,
  InterpretationNodeSchema,
  ValueNodeSchema,
  ChoiceNodeSchema,
  ProposalNodeSchema,
  LimitNodeSchema,
]);

// La version du raisonnement à laquelle le graphe est rattaché (INTRO §6.1 :
// chaque publication renvoie à un commit ou un tag).
export const EvidenceVersionSchema = z.object({
  repo_url: z.string().optional(),
  tag: z.string().optional(),
  commit: z.string().optional(),
  evidence_doc: z.string().optional(),
});

export const EvidenceGraphSchema = z.object({
  nodes: z.array(EvidenceNodeSchema),
  version: EvidenceVersionSchema.default({}),
});

export type EvidenceFile = z.infer<typeof EvidenceFileSchema>;
export type Locator = z.infer<typeof LocatorSchema>;
export type CodeRef = z.infer<typeof CodeRefSchema>;
export type DataRef = z.infer<typeof DataRefSchema>;
export type SourceNode = z.infer<typeof SourceNodeSchema>;
export type DefinitionNode = z.infer<typeof DefinitionNodeSchema>;
export type HypothesisNode = z.infer<typeof HypothesisNodeSchema>;
export type ObservationNode = z.infer<typeof ObservationNodeSchema>;
export type TransformationNode = z.infer<typeof TransformationNodeSchema>;
export type MeasureNode = z.infer<typeof MeasureNodeSchema>;
export type ResultNode = z.infer<typeof ResultNodeSchema>;
export type ComputedNode = TransformationNode | MeasureNode | ResultNode;
export type EvidenceNode = z.infer<typeof EvidenceNodeSchema>;
export type EvidenceVersion = z.infer<typeof EvidenceVersionSchema>;
export type EvidenceGraph = z.infer<typeof EvidenceGraphSchema>;

export function nodeTypeOfId(id: string): NodeType | null {
  const prefix = id.split("-")[0];
  return prefix === undefined ? null : (NODE_TYPE_BY_PREFIX[prefix] ?? null);
}
