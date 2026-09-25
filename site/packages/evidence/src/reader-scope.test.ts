import { describe, expect, it } from "vitest";
import type { Note, Post } from "./publication.ts";
import { selectReadable } from "./reader-scope.ts";

function post(slug: string, date: string, status: Post["status"]): Post {
  return {
    slug,
    title: slug,
    date,
    study: { slug: "logement", name: "Logement" },
    status,
    version: {},
  };
}

function note(slug: string, collection?: { slug: string; position: number }): Note {
  return {
    slug,
    title: slug,
    date: "2026-09-20",
    version: {},
    ...(collection === undefined
      ? {}
      : { collection: { slug: collection.slug, title: "Recueil", position: collection.position } }),
  };
}

const posts = [
  { post: post("ancien", "2026-08-01", "published"), markdown: "a" },
  { post: post("en-relecture", "2026-09-10", "in_review"), markdown: "b" },
];

const notes = [
  { token: "tok-2", note: note("livret-deux", { slug: "livret", position: 2 }), markdown: "n2" },
  { token: "tok-p", note: note("note-privee"), markdown: "secret" },
  { token: "tok-1", note: note("livret-un", { slug: "livret", position: 1 }), markdown: "n1" },
  { token: "tok-d", note: note("dossier", { slug: "autre", position: 1 }), markdown: "d" },
];

describe("selectReadable", () => {
  const readable = selectReadable(posts, notes);
  const slugs = readable.map((entry) => entry.slug);

  it("donne tous les posts, relus ou en relecture, du plus récent au plus ancien", () => {
    expect(slugs.slice(0, 2)).toEqual(["en-relecture", "ancien"]);
    expect(readable[0]?.status).toBe("in_review");
  });

  it("donne les notes du livret dans l'ordre du recueil", () => {
    expect(slugs.slice(2)).toEqual(["livret-un", "livret-deux"]);
  });

  it("ne donne jamais une note hors recueil ni celle d'un recueil fermé", () => {
    expect(slugs).not.toContain("note-privee");
    expect(slugs).not.toContain("dossier");
    expect(readable.map((entry) => entry.markdown)).not.toContain("secret");
  });

  it("adresse un post par son slug et une note par son jeton", () => {
    expect(readable.find((entry) => entry.slug === "ancien")).toMatchObject({
      path: "/posts/ancien",
      contentId: "ancien",
    });
    expect(readable.find((entry) => entry.slug === "livret-un")).toMatchObject({
      path: "/notes/tok-1",
      contentId: "tok-1",
    });
  });

  it("n'ouvre que les recueils demandés", () => {
    expect(selectReadable([], notes, ["autre"]).map((entry) => entry.slug)).toEqual(["dossier"]);
    expect(selectReadable([], notes, [])).toEqual([]);
  });
});
