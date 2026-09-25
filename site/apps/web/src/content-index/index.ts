import { contentIndex } from "virtual:content-index";
import { NoteSchema, PostSchema, type Note, type Post } from "~/contracts/evidence";

// L'index du contenu, figé au build par vite-plugins/content-assets et
// validé ici, à la frontière : serveur seulement (le Worker n'a pas de
// système de fichiers). Il ne porte que les métadonnées et le markdown —
// graphe et fichiers sont des assets statiques.
//
// Trois lecteurs : les fonctions RPC des pages, le plan du site
// (sitemap.xml) et le serveur MCP.

export type IndexedPost = { readonly post: Post; readonly markdown: string };
// `token` est aussi l'identifiant du dossier de contenu de la note
// (/content/notes/<token>/…).
export type IndexedNote = {
  readonly token: string;
  readonly note: Note;
  readonly markdown: string;
};
export type IndexedPage = { readonly slug: string; readonly markdown: string };

export function indexedPosts(): IndexedPost[] {
  return contentIndex.posts.flatMap((entry) => {
    const parsed = PostSchema.safeParse(entry.post);
    // Un post.json invalide ne doit pas rendre toute la liste inaccessible.
    return parsed.success ? [{ post: parsed.data, markdown: entry.markdown }] : [];
  });
}

export function indexedNotes(): IndexedNote[] {
  return contentIndex.notes.flatMap((entry) => {
    const parsed = NoteSchema.safeParse(entry.note);
    return parsed.success
      ? [{ token: entry.token, note: parsed.data, markdown: entry.markdown }]
      : [];
  });
}

export function indexedPage(slug: string): IndexedPage | undefined {
  return contentIndex.pages.find((candidate) => candidate.slug === slug);
}

// Le jeton qui ouvre le serveur MCP (/mcp/<jeton>).
export function mcpToken(): string {
  return contentIndex.mcpToken;
}
