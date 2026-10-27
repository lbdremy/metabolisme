import { describe, expect, it } from "vitest";
import {
  conceptionStatus,
  isPublishedConception,
  selectCollection,
  selectConception,
} from "./collection.ts";
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

function conception(slug: string, position: number, status?: Note["status"]): Note {
  return {
    ...note(slug, { slug: "conception", position }),
    ...(status === undefined ? {} : { status }),
  };
}

const designs = [
  { token: "r", note: conception("relue", 2, "published") },
  { token: "s", note: conception("sans-statut", 1) },
  { token: "e", note: conception("en-relecture", 3, "in_review") },
  { token: "z", note: { ...note("note-isolee"), status: "published" as const } },
];

describe("articles de conception", () => {
  it("sont en relecture tant que note.yaml ne dit pas « published »", () => {
    expect(conceptionStatus(conception("sans-statut", 1))).toBe("in_review");
  });

  it("ne sont publics que s'ils sont du recueil conception ET publiés", () => {
    expect(
      designs.filter((entry) => isPublishedConception(entry.note)).map((e) => e.token),
    ).toEqual(["r"]);
  });

  it("se sélectionnent par statut, dans l'ordre du recueil", () => {
    expect(selectConception(designs, "in_review").map((entry) => entry.token)).toEqual(["s", "e"]);
    expect(selectConception(designs, "published").map((entry) => entry.token)).toEqual(["r"]);
  });
});
