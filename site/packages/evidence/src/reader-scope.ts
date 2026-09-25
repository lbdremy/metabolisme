import type { Note, NoteCollection, Post, PublicationStatus, Study } from "./publication.ts";

// Ce que le serveur MCP donne à lire — sélection pure.
//
// Tous les posts, relus ou en relecture (ils sont déjà servis à leur
// adresse). Parmi les notes, SEULEMENT celles des recueils ouverts (le livret) :
// une note isolée reste un message privé, lisible par son seul jeton. Le
// markdown et les graphes sont ceux du site, jamais une copie.

export const READER_COLLECTIONS: readonly string[] = ["livret"];

export type ReadableKind = "post" | "note";

export type Readable = {
  readonly kind: ReadableKind;
  readonly slug: string;
  readonly title: string;
  readonly date: string;
  readonly path: string;
  // Dossier de contenu (/content/<posts|notes>/<id>/) : le slug d'un post,
  // le jeton d'une note.
  readonly contentId: string;
  readonly markdown: string;
  readonly subtitle?: string;
  readonly summary?: string;
  readonly context?: string;
  readonly status?: PublicationStatus;
  readonly study?: Study;
  readonly collection?: NoteCollection;
};

type PostEntry = { readonly post: Post; readonly markdown: string };
type NoteEntry = { readonly token: string; readonly note: Note; readonly markdown: string };

function fromPost({ post, markdown }: PostEntry): Readable {
  return {
    kind: "post",
    slug: post.slug,
    title: post.title,
    date: post.date,
    path: `/posts/${post.slug}`,
    contentId: post.slug,
    markdown,
    status: post.status,
    study: post.study,
    ...(post.subtitle === undefined ? {} : { subtitle: post.subtitle }),
    ...(post.summary === undefined ? {} : { summary: post.summary.trim() }),
  };
}

function fromNote({ token, note, markdown }: NoteEntry): Readable {
  return {
    kind: "note",
    slug: note.slug,
    title: note.title,
    date: note.date,
    path: `/notes/${token}`,
    contentId: token,
    markdown,
    ...(note.context === undefined ? {} : { context: note.context.trim() }),
    ...(note.collection === undefined ? {} : { collection: note.collection }),
  };
}

export function selectReadable(
  posts: ReadonlyArray<PostEntry>,
  notes: ReadonlyArray<NoteEntry>,
  collections: ReadonlyArray<string> = READER_COLLECTIONS,
): Readable[] {
  const open = new Set(collections);
  const collected = notes
    .flatMap((entry) => {
      const collection = entry.note.collection;
      return collection !== undefined && open.has(collection.slug) ? [{ entry, collection }] : [];
    })
    .toSorted(
      (a, b) =>
        a.collection.slug.localeCompare(b.collection.slug) ||
        a.collection.position - b.collection.position,
    );
  const byDate = posts.toSorted((a, b) => b.post.date.localeCompare(a.post.date));
  return [...byDate.map(fromPost), ...collected.map(({ entry }) => fromNote(entry))];
}
