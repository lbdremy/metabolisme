import { describe, expect, it } from "vitest";
import { selectCollection } from "./collection.ts";
import type { Note } from "./publication.ts";

function note(slug: string, collection?: { slug: string; position: number }): Note {
  return {
    slug,
    title: slug,
    date: "2026-09-20",
    version: {},
    ...(collection === undefined
      ? {}
      : {
          collection: {
            slug: collection.slug,
            title: "Livret 2027",
            position: collection.position,
          },
        }),
  };
}

const entries = [
  { token: "c", note: note("troisieme", { slug: "livret", position: 3 }) },
  { token: "x", note: note("hors-recueil") },
  { token: "a", note: note("premiere", { slug: "livret", position: 1 }) },
  { token: "y", note: note("autre-recueil", { slug: "dossier", position: 1 }) },
  { token: "b", note: note("deuxieme", { slug: "livret", position: 2 }) },
];

describe("selectCollection", () => {
  it("ne retient que les notes du recueil demandé", () => {
    expect(selectCollection(entries, "livret").map((entry) => entry.token)).not.toContain("x");
    expect(selectCollection(entries, "livret").map((entry) => entry.token)).not.toContain("y");
  });

  it("les ordonne par position, pas par date ni par jeton", () => {
    expect(selectCollection(entries, "livret").map((entry) => entry.token)).toEqual([
      "a",
      "b",
      "c",
    ]);
  });

  it("rend une liste vide pour un recueil inconnu", () => {
    expect(selectCollection(entries, "inexistant")).toEqual([]);
  });
});
