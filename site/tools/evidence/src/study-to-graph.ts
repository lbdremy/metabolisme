import { z } from "zod";
import {
  EvidenceGraphSchema,
  NODE_TYPES,
  type ComputedNode,
  type EvidenceFile,
  type EvidenceGraph,
  type EvidenceNode,
  type EvidenceVersion,
  type FileManifest,
} from "@metabolisme/evidence";
import { languageOf, mimeOf } from "./mime.ts";

// Dérivation pure : les quatre registres d'une étude (méthode INTRO §7-§10)
// deviennent un graphe de preuves au contrat du site, plus le manifeste des
// fichiers à publier (sources figées, code, sorties). Aucune I/O ici : la
// taille des fichiers est fournie par l'appelant.

// Ce qu'on accepte des registres YAML d'une étude — un sous-ensemble tolérant
// (SubsetModel) : des champs inconnus ne cassent pas la dérivation.
const Loose = z.object({}).loose();

// Un champ textuel facultatif d'un registre : absent, null, ou parfois un
// nombre (une année) — tout ce qui n'est pas une chaîne est normalisé.
const optionalText = z
  .union([z.string(), z.number(), z.null()])
  .optional()
  .transform((value) => (value === null || value === undefined ? undefined : String(value)));

const RegistrySource = z
  .object({
    id: z.string(),
    publisher: z.string(),
    title: z.string(),
    source_url: z.string(),
    dataset_id: optionalText,
    publication_date: optionalText,
    retrieved_at: optionalText,
    geographic_scope: optionalText,
    temporal_scope: optionalText,
    license: optionalText,
    notes: optionalText,
    local_file: optionalText,
    checksum: optionalText,
    files: z
      .array(z.object({ path: z.string(), checksum: optionalText }))
      .nullable()
      .optional(),
    // Une copie figée peut être conservée pour vérification sans être servie
    // par le site (droits de redistribution non établis) : l'URL d'origine
    // reste, le fichier n'est pas publié.
    redistributable: z.boolean().optional(),
  })
  .loose();

const RegistryDefinition = z
  .object({
    id: z.string(),
    term: z.string(),
    source: optionalText,
    // Une notion construite par l'étude dépend du choix qui la formule,
    // en plus de la source qui l'ancre (INTRO §8 : ne pas présenter une
    // construction comme une citation).
    constructed_by: optionalText,
    url: optionalText,
    last_updated: optionalText,
    definition: z.string(),
    caveats: z
      .array(z.string())
      .nullable()
      .optional()
      .transform((v) => v ?? []),
  })
  .loose();

// Une hypothèse du registre est un paramètre chiffré (valeur centrale,
// plage, unité) ou une hypothèse qualitative (`statement`) — jamais ni l'un
// ni l'autre, jamais un paramètre incomplet.
const RegistryHypothesis = z
  .object({
    id: z.string(),
    name: z.string(),
    description: z.string(),
    central_value: z.number().optional(),
    plausible_range: z.tuple([z.number(), z.number()]).optional(),
    unit: z.string().optional(),
    statement: optionalText,
    confidence: z.enum(["low", "medium", "high"]),
    justification: z.array(z.string()).default([]),
    limitations: z.array(z.string()).default([]),
    affects: z.array(z.string()).default([]),
  })
  .loose();

const RegistryClaim = z
  .object({
    id: z.string(),
    type: z.enum(NODE_TYPES),
    title: z.string(),
    depends_on: z.array(z.string()).default([]),
    limitations: z.array(z.string()).default([]),
    notes: optionalText,
    produced_by: optionalText,
    output: optionalText,
  })
  .loose();

export type StudyRegistries = {
  sources: unknown[];
  definitions: unknown[];
  hypotheses: unknown[];
  claims: unknown[];
};

export type FileStat = { size: number } | null;

export type StudyToGraphOptions = {
  // Préfixe des chemins d'origine dans le dépôt (ex. « logement/ »).
  studyPrefix: string;
  version: EvidenceVersion;
  // Taille d'un fichier de l'étude, ou null s'il n'existe pas.
  statFile: (repoPath: string) => FileStat;
  // Au-delà, un fichier ne peut pas être un asset statique du CDN.
  maxAssetBytes: number;
};

function basename(path: string): string {
  return path.split("/").at(-1) ?? path;
}

function trimTitle(text: string): string {
  return text.replace(/\s+/g, " ").trim();
}

export function studyToGraph(
  registries: StudyRegistries,
  options: StudyToGraphOptions,
): { graph: EvidenceGraph; files: FileManifest } {
  const nodes: EvidenceNode[] = [];
  const files: FileManifest = [];
  const seenFiles = new Set<string>();

  function publish(
    logicalPath: string,
    studyRelativePath: string,
    checksum: string | undefined,
    redistributable = true,
  ): EvidenceFile {
    const repoPath = `${options.studyPrefix}${studyRelativePath}`;
    const stat = options.statFile(repoPath);
    const size = stat?.size ?? 0;
    const hosted: EvidenceFile["hosted"] =
      stat === null || !redistributable
        ? "none"
        : size > options.maxAssetBytes
          ? "object-store"
          : "asset";
    if (!seenFiles.has(logicalPath) && hosted !== "none") {
      seenFiles.add(logicalPath);
      files.push({ path: logicalPath, from: repoPath, size, mime: mimeOf(logicalPath), hosted });
    }
    const file: EvidenceFile = {
      path: logicalPath,
      name: basename(studyRelativePath),
      mime: mimeOf(logicalPath),
      size,
      hosted,
    };
    if (checksum !== undefined) file.checksum = checksum;
    return file;
  }

  for (const raw of registries.sources) {
    const source = RegistrySource.parse(raw);
    const attached = [
      ...(source.local_file === undefined
        ? []
        : [{ path: source.local_file, checksum: source.checksum }]),
      ...(source.files ?? []),
    ];
    nodes.push({
      id: source.id,
      type: "source",
      title: trimTitle(source.title),
      depends_on: [],
      limitations: [],
      ...(source.notes === undefined ? {} : { notes: source.notes.trim() }),
      publisher: source.publisher,
      source_url: source.source_url,
      ...(source.dataset_id === undefined ? {} : { dataset_id: source.dataset_id }),
      ...(source.publication_date === undefined
        ? {}
        : { publication_date: source.publication_date }),
      ...(source.retrieved_at === undefined ? {} : { retrieved_at: source.retrieved_at }),
      ...(source.geographic_scope === undefined
        ? {}
        : { geographic_scope: source.geographic_scope }),
      ...(source.temporal_scope === undefined ? {} : { temporal_scope: source.temporal_scope }),
      ...(source.license === undefined ? {} : { license: source.license }),
      files: attached.map((file) =>
        publish(
          `sources/${basename(file.path)}`,
          file.path,
          file.checksum,
          source.redistributable !== false,
        ),
      ),
    });
  }

  for (const raw of registries.definitions) {
    const definition = RegistryDefinition.parse(raw);
    nodes.push({
      id: definition.id,
      type: "definition",
      title: trimTitle(definition.term),
      depends_on: [
        ...(definition.source === undefined ? [] : [definition.source]),
        ...(definition.constructed_by === undefined ? [] : [definition.constructed_by]),
      ],
      limitations: [],
      term: definition.term,
      definition: definition.definition.trim(),
      ...(definition.url === undefined ? {} : { url: definition.url }),
      ...(definition.last_updated === undefined ? {} : { last_updated: definition.last_updated }),
      caveats: definition.caveats,
    });
  }

  for (const raw of registries.hypotheses) {
    const hypothesis = RegistryHypothesis.parse(raw);
    const numeric = [hypothesis.central_value, hypothesis.plausible_range, hypothesis.unit];
    const quantified = numeric.every((field) => field !== undefined);
    if (!quantified && numeric.some((field) => field !== undefined)) {
      throw new Error(
        `${hypothesis.id} : paramètre incomplet (valeur centrale, plage et unité vont ensemble)`,
      );
    }
    if (!quantified && hypothesis.statement === undefined) {
      throw new Error(
        `${hypothesis.id} : une hypothèse est un paramètre chiffré ou porte un énoncé (statement)`,
      );
    }
    nodes.push({
      id: hypothesis.id,
      type: "hypothesis",
      title: trimTitle(hypothesis.description),
      depends_on: hypothesis.justification,
      limitations: hypothesis.limitations,
      name: hypothesis.name,
      ...(hypothesis.central_value === undefined
        ? {}
        : { central_value: hypothesis.central_value }),
      ...(hypothesis.plausible_range === undefined
        ? {}
        : { plausible_range: hypothesis.plausible_range }),
      ...(hypothesis.unit === undefined ? {} : { unit: hypothesis.unit }),
      ...(hypothesis.statement === undefined ? {} : { statement: hypothesis.statement.trim() }),
      confidence: hypothesis.confidence,
      affects: hypothesis.affects,
    });
  }

  for (const raw of registries.claims) {
    const claim = RegistryClaim.parse(raw);
    const base = {
      id: claim.id,
      title: trimTitle(claim.title),
      depends_on: claim.depends_on,
      limitations: claim.limitations,
      ...(claim.notes === undefined ? {} : { notes: claim.notes.trim() }),
    };
    if (claim.type === "transformation" || claim.type === "measure" || claim.type === "result") {
      const computed: ComputedNode = { ...base, type: claim.type };
      if (claim.produced_by !== undefined) {
        publish(`code/${claim.produced_by}`, claim.produced_by, undefined);
        computed.produced_by = {
          path: `code/${claim.produced_by}`,
          repo_path: `${options.studyPrefix}${claim.produced_by}`,
          language: languageOf(claim.produced_by),
        };
      }
      if (claim.output !== undefined) {
        publish(`data/${basename(claim.output)}`, claim.output, undefined);
        computed.output = {
          path: `data/${basename(claim.output)}`,
          repo_path: `${options.studyPrefix}${claim.output}`,
        };
      }
      nodes.push(computed);
    } else if (
      claim.type === "source" ||
      claim.type === "definition" ||
      claim.type === "hypothesis" ||
      claim.type === "observation"
    ) {
      // Les S/D/H vivent dans leurs registres ; une observation du graphe n'a
      // pas de localisateur (le registre claims.yaml n'en porte pas).
      if (claim.type === "observation") {
        nodes.push({ ...base, type: "observation", locators: [] });
      } else {
        throw new Error(`${claim.id} : un nœud ${claim.type} doit venir de son registre`);
      }
    } else {
      nodes.push({ ...base, type: claim.type });
    }
  }

  // Garantit le contrat (défauts, formats) avant écriture.
  const graph = EvidenceGraphSchema.parse({ nodes, version: options.version });
  return { graph, files };
}

// Garde-fou de lecture des registres : un YAML qui n'est pas une liste est
// une erreur d'auteur, pas un cas à rattraper.
export function asList(name: string, value: unknown): unknown[] {
  const parsed = z.array(Loose).safeParse(value ?? []);
  if (!parsed.success) throw new Error(`${name} : liste attendue`);
  return parsed.data;
}
