import { z } from "zod";
import { EvidenceVersionSchema } from "./graph.ts";

// Les objets publiés par le site.
//
// Un POST est un ARTICLE DE RECHERCHE : il établit l'existant, adossé à une
// chaîne de preuves complète dérivée des registres de l'étude (chemin
// « sources → définitions → observations → transformations → résultats »).
// Une NOTE est un message court et sourcé, destiné à être partagé par une
// URL non devinable : la chaîne y est souvent minuscule (un chiffre, la page
// de la source), mais elle est là. Les notes du recueil « conception » sont
// des ARTICLES DE CONCEPTION : elles conçoivent un système métabolique et
// portent surtout des valeurs, choix et propositions (méthode, « Deux
// disciplines, une chaîne de preuves »).

const Slug = z.string().regex(/^[a-z0-9][a-z0-9-]*$/);

// Statut de publication d'un post. « in_review » : l'article est en ligne à
// son adresse, mais ABSENT de l'index — il attend la relecture de l'auteur.
// Ce n'est pas un secret (l'URL suffit), c'est un tri : la page d'accueil ne
// présente que ce qui a été relu.
export const PublicationStatusSchema = z.enum(["published", "in_review"]);

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
  status: PublicationStatusSchema.default("published"),
  version: EvidenceVersionSchema.default({}),
});

// Une note vit dans le dépôt sous un slug lisible ; son URL publique porte un
// JETON dérivé du slug et d'un secret de build (HMAC) — le dépôt, public, ne
// révèle donc pas les adresses partagées. Le jeton n'est jamais listé.
export const NoteTokenSchema = z.string().regex(/^[a-z0-9]{24}$/);

// Un RECUEIL de notes : plusieurs notes écrites pour être lues ensemble.
// Il donne au site de quoi servir un sommaire à une adresse unique. Le seul
// recueil que le site présente est celui des articles de conception
// (CONCEPTION_COLLECTION) ; un autre recueil ne change rien au régime de ses
// notes — jeton, noindex, absence de l'accueil.
export const NoteCollectionSchema = z.object({
  slug: Slug,
  title: z.string().min(1),
  position: z.number().int().positive(),
});

export const NoteSchema = z.object({
  slug: Slug,
  title: z.string().min(1),
  date: z.string().date(),
  context: z.string().optional(),
  collection: NoteCollectionSchema.optional(),
  // Pour un article de conception seulement : « published » le fait entrer
  // à l'accueil et dans l'index des moteurs. Absent, il est EN RELECTURE —
  // servi à son jeton, montré au seul mode relecture. Une conception ne
  // devient publique que par une décision écrite dans note.yaml.
  status: PublicationStatusSchema.optional(),
  // L'adresse LISIBLE d'un article de conception publié : /conception/<slug>.
  // Absente, c'est le slug du dossier. Elle ne sert qu'une fois l'article
  // publié — en relecture, seul le jeton y mène ; le dossier, lui, ne se
  // renomme pas (le jeton en dérive, et des liens sont déjà partagés).
  public_slug: Slug.optional(),
  version: EvidenceVersionSchema.default({}),
});

export type PublicationStatus = z.infer<typeof PublicationStatusSchema>;
export type Study = z.infer<typeof StudySchema>;
export type Post = z.infer<typeof PostSchema>;
export type NoteCollection = z.infer<typeof NoteCollectionSchema>;
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
