import { describe, expect, it } from "vitest";
import type { Readable } from "./reader-scope.ts";
import { foldText, searchReadables } from "./text-search.ts";

function readable(
  slug: string,
  title: string,
  markdown: string,
  kind: Readable["kind"] = "post",
): Readable {
  return { kind, slug, title, date: "2026-09-01", path: `/${slug}`, contentId: slug, markdown };
}

const corpus = [
  readable("a", "Rente autoroutière", "La préemption de la rente. Préemption encore."),
  readable("b", "Logement", "Le parc social et la PRÉEMPTION foncière."),
  readable("c", "Information", "Rien à voir.", "note"),
];

describe("foldText", () => {
  it("retire accents et casse sans changer la longueur", () => {
    expect(foldText("Préemption ÉTÉ")).toBe("preemption ete");
    expect(foldText("Œuvre 😀 é").length).toBe("Œuvre 😀 é".length);
  });
});

describe("searchReadables", () => {
  it("trouve sans tenir compte des accents ni de la casse, les plus denses d'abord", () => {
    const hits = searchReadables(corpus, "preemption");
    expect(hits.map((hit) => hit.slug)).toEqual(["a", "b"]);
    expect(hits[0]?.occurrences).toBe(2);
  });

  it("exige tous les mots, dans le titre ou le texte", () => {
    expect(searchReadables(corpus, "préemption autoroutière").map((hit) => hit.slug)).toEqual([
      "a",
    ]);
    expect(searchReadables(corpus, "préemption absent")).toEqual([]);
  });

  it("filtre par type et borne le nombre de résultats", () => {
    expect(searchReadables(corpus, "rien", { kind: "post" })).toEqual([]);
    expect(searchReadables(corpus, "rien", { kind: "note" }).map((hit) => hit.slug)).toEqual(["c"]);
    expect(searchReadables(corpus, "la", { limit: 1 })).toHaveLength(1);
  });

  it("renvoie des extraits tels qu'écrits, sans chevauchement", () => {
    const [hit] = searchReadables(corpus, "préemption", { excerptRadius: 5 });
    expect(hit?.excerpts[0]).toContain("préemption");
    expect(hit?.excerpts).toHaveLength(2);
  });

  it("une requête vide ne renvoie rien", () => {
    expect(searchReadables(corpus, "   ")).toEqual([]);
  });
});
