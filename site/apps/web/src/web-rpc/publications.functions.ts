import { notFound } from "@tanstack/react-router";
import { createServerFn } from "@tanstack/react-start";
import { z } from "zod";
import { NoteTokenSchema, selectConception, type Post } from "~/contracts/evidence";
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

// Les ARTICLES DE CONCEPTION publiés, dans l'ordre de lecture du recueil —
// l'accueil et le sommaire de la conception les présentent comme les posts.
// Les notes hors recueil ne sont jamais listées : seul leur jeton y mène.
export const listConception = createServerFn({ method: "GET" }).handler(() =>
  selectConception(notes(), "published").map((entry) => ({
    token: entry.token,
    note: entry.note,
  })),
);

// Les articles de conception en relecture — demandés explicitement quand le
// mode relecture est actif, comme les posts en relecture.
export const listConceptionInReview = createServerFn({ method: "GET" }).handler(() =>
  selectConception(notes(), "in_review").map((entry) => ({
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
