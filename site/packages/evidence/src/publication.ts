import { z } from "zod";
import { EvidenceVersionSchema } from "./graph.ts";

// Les deux objets publiés par le site.
//
// Un POST est un article d'étude : long, dense, adossé à une chaîne de
// preuves complète dérivée des registres de l'étude (chemin
// « sources → définitions → observations → transformations → résultats »).
// Une NOTE est un message court et sourcé, destiné à être partagé par une
// URL non devinable : la chaîne y est souvent minuscule (un chiffre, la page
// de la source), mais elle est là.

const Slug = z.string().regex(/^[a-z0-9][a-z0-9-]*$/);

export const StudySchema = z.object({
  slug: Slug,
  name: z.string().min(1),
  question: z.string().optional(),
});

export const PostSchema = z.object({
  slug: Slug,
  title: z.string().min(1),
  subtitle: z.string().optional(),
  date: z.string().date(),
  summary: z.string().optional(),
  study: StudySchema,
  version: EvidenceVersionSchema.default({}),
});

// Une note vit dans le dépôt sous un slug lisible ; son URL publique porte un
// JETON dérivé du slug et d'un secret de build (HMAC) — le dépôt, public, ne
// révèle donc pas les adresses partagées. Le jeton n'est jamais listé.
export const NoteTokenSchema = z.string().regex(/^[a-z0-9]{24}$/);

export const NoteSchema = z.object({
  slug: Slug,
  title: z.string().min(1),
  date: z.string().date(),
  context: z.string().optional(),
  version: EvidenceVersionSchema.default({}),
});

export type Study = z.infer<typeof StudySchema>;
export type Post = z.infer<typeof PostSchema>;
export type Note = z.infer<typeof NoteSchema>;

// Manifeste des fichiers d'une publication : chemin logique servi par le
// site → fichier d'origine sur le disque (au build seulement).
export const FileManifestEntrySchema = z.object({
  path: z.string().min(1),
  from: z.string().min(1),
  size: z.number().int().nonnegative(),
  mime: z.string().min(1),
  hosted: z.enum(["asset", "object-store", "none"]),
});

export const FileManifestSchema = z.array(FileManifestEntrySchema);

export type FileManifestEntry = z.infer<typeof FileManifestEntrySchema>;
export type FileManifest = z.infer<typeof FileManifestSchema>;
