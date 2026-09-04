import { z } from "zod";
import { EvidenceVersionSchema, StudySchema } from "@metabolisme/evidence";

// post.yaml : la partie écrite à la main d'un post. Tout le reste du dossier
// (post.json, article.md, graph.json, files.json) est généré par build-posts.
export const PostConfigSchema = z.object({
  slug: z.string().regex(/^[a-z0-9][a-z0-9-]*$/),
  title: z.string().min(1),
  subtitle: z.string().optional(),
  date: z.string().date(),
  summary: z.string().optional(),
  study: StudySchema.extend({
    // Dossier de l'étude, relatif à la racine du dépôt (ex. « logement »).
    dir: z.string().min(1),
  }),
  // Article Markdown, relatif au dossier de l'étude.
  article: z.string().min(1),
  version: EvidenceVersionSchema.default({}),
});

export type PostConfig = z.infer<typeof PostConfigSchema>;

// L'article garde son texte tel quel, sauf le titre H1 initial et, s'il le
// suit immédiatement, le sous-titre en gras : la page les porte déjà dans son
// en-tête.
export function stripLeadingTitle(markdown: string): string {
  return markdown.replace(/^\s*# [^\n]*\n+/, "").replace(/^\*\*[^\n]*\*\*\n+/, "");
}
