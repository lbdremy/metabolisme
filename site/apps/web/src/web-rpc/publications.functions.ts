import { notFound } from "@tanstack/react-router";
import { createServerFn } from "@tanstack/react-start";
import { z } from "zod";
import { NoteTokenSchema, selectCollection, type Post } from "~/contracts/evidence";
import { indexedNotes as notes, indexedPage, indexedPosts as posts } from "~/content-index";

function byDateDescending(list: ReadonlyArray<Post>): Post[] {
  return list.toSorted((a, b) => b.date.localeCompare(a.date));
}

// L'index ne porte que les posts relus. Un post « en relecture » reste
// servi à son adresse (getPost ne filtre pas) : il est hors de la liste,
// pas hors du site.
export const listPosts = createServerFn({ method: "GET" }).handler(() =>
  byDateDescending(
    posts()
      .map((entry) => entry.post)
      .filter((post) => post.status === "published"),
  ),
);

// La liste des posts en attente de relecture — demandée explicitement par
// l'accueil quand le mode relecture est actif.
export const listPostsInReview = createServerFn({ method: "GET" }).handler(() =>
  byDateDescending(
    posts()
      .map((entry) => entry.post)
      .filter((post) => post.status === "in_review"),
  ),
);

// Un RECUEIL de notes : le seul endroit du site où des notes sont listées,
// et il faut en connaître l'adresse. Le régime des notes ne change pas —
// chacune garde son jeton, son noindex et son absence de l'accueil ; c'est le
// SOMMAIRE qui se partage, à la place de dix liens. Les notes hors recueil ne
// sont toujours accessibles que par leur jeton.
const CollectionInput = z.object({ collection: z.string().min(1) });

export const listCollection = createServerFn({ method: "GET" })
  .validator(CollectionInput)
  .handler(({ data }) =>
    selectCollection(notes(), data.collection).map((entry) => ({
      token: entry.token,
      note: entry.note,
    })),
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
    const page = indexedPage(data.slug);
    if (page === undefined) {
      throw notFound();
    }
    return page;
  });
