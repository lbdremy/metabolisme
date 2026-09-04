import { notFound } from "@tanstack/react-router";
import { createServerFn } from "@tanstack/react-start";
import { z } from "zod";
import { contentIndex } from "virtual:content-index";
import {
  NoteSchema,
  NoteTokenSchema,
  PostSchema,
  type Note,
  type Post,
} from "~/contracts/evidence";

// L'index est figé au build par vite-plugins/content-assets : le runtime de
// déploiement n'a pas de système de fichiers. Il ne porte que les
// métadonnées — article, graphe et fichiers sont des assets statiques.

type IndexedPost = { readonly post: Post; readonly markdown: string };
type IndexedNote = { readonly token: string; readonly note: Note; readonly markdown: string };

function posts(): IndexedPost[] {
  return contentIndex.posts.flatMap((entry) => {
    const parsed = PostSchema.safeParse(entry.post);
    // Un post.json invalide ne doit pas rendre toute la liste inaccessible.
    return parsed.success ? [{ post: parsed.data, markdown: entry.markdown }] : [];
  });
}

function notes(): IndexedNote[] {
  return contentIndex.notes.flatMap((entry) => {
    const parsed = NoteSchema.safeParse(entry.note);
    return parsed.success
      ? [{ token: entry.token, note: parsed.data, markdown: entry.markdown }]
      : [];
  });
}

export const listPosts = createServerFn({ method: "GET" }).handler(() =>
  posts()
    .map((entry) => entry.post)
    .toSorted((a, b) => b.date.localeCompare(a.date)),
);

const SlugInput = z.object({ slug: z.string().min(1) });

export const getPost = createServerFn({ method: "GET" })
  .validator(SlugInput)
  .handler(({ data }) => {
    const entry = posts().find((candidate) => candidate.post.slug === data.slug);
    if (entry === undefined) {
      throw notFound();
    }
    return entry;
  });

// Les notes ne sont jamais listées : seule une URL complète (jeton) y mène.
// Un jeton mal formé est une page inexistante, pas une erreur serveur.
const TokenInput = z.object({ token: z.string().min(1) });

export const getNote = createServerFn({ method: "GET" })
  .validator(TokenInput)
  .handler(({ data }) => {
    const entry = NoteTokenSchema.safeParse(data.token).success
      ? notes().find((candidate) => candidate.token === data.token)
      : undefined;
    if (entry === undefined) {
      throw notFound();
    }
    return entry;
  });

const PageInput = z.object({ slug: z.string().regex(/^[a-z0-9-]+$/) });

export const getPage = createServerFn({ method: "GET" })
  .validator(PageInput)
  .handler(({ data }) => {
    const page = contentIndex.pages.find((candidate) => candidate.slug === data.slug);
    if (page === undefined) {
      throw notFound();
    }
    return page;
  });
