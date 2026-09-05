import { describe, expect, it } from "vitest";
import { danglingReferences } from "@metabolisme/evidence";
import { studyToGraph } from "./study-to-graph.ts";

const registries = {
  sources: [
    {
      id: "S-01",
      publisher: "INSEE",
      title: "Parc de logements\n  au 1er janvier",
      source_url: "https://insee.fr/x",
      publication_date: "2025-09-17",
      retrieved_at: "2026-08-03",
      local_file: "data/raw/insee.xlsx",
      checksum: "sha256:" + "a".repeat(64),
      notes: "note\n",
    },
    {
      id: "S-05",
      publisher: "MTE",
      title: "LOVAC",
      source_url: "https://data.gouv.fr/lovac",
      files: [
        { path: "data/raw/lovac-communes.csv", checksum: "sha256:" + "b".repeat(64) },
        { path: "data/raw/lovac-big.csv" },
      ],
    },
  ],
  definitions: [
    { id: "D-01", term: "logement", source: "S-01", definition: "Un local…", caveats: ["c1"] },
    {
      id: "D-02",
      term: "captivité (notion construite)",
      source: "S-01",
      constructed_by: "C-01",
      definition: "Notion de l'étude…",
    },
  ],
  hypotheses: [
    {
      id: "H-06",
      name: "threshold",
      description: "Seuil",
      central_value: 2,
      plausible_range: [1, 3],
      unit: "years",
      confidence: "medium",
      justification: ["S-05"],
      affects: ["R-02"],
    },
    {
      id: "H-01",
      name: "framing",
      description: "Hypothèse directrice",
      statement: "Là où l'infrastructure n'est pas substituable, le prix se décorrèle du coût.",
      confidence: "low",
      justification: ["D-01"],
      limitations: ["L-01"],
    },
  ],
  claims: [
    { id: "O-01", type: "observation", title: "obs", depends_on: ["S-01", "D-01"] },
    {
      id: "T-01",
      type: "transformation",
      title: "t",
      depends_on: ["O-01"],
      produced_by: "src/logement/core/parc.py",
    },
    {
      id: "R-02",
      type: "result",
      title: "r",
      depends_on: ["T-01", "H-06"],
      produced_by: "src/logement/shell/build.py",
      output: "data/processed/vacance.json",
      limitations: ["L-01"],
    },
    { id: "L-01", type: "limit", title: "l" },
    { id: "C-01", type: "choice", title: "c" },
    { id: "I-01", type: "interpretation", title: "i", depends_on: ["R-02"] },
  ],
};

const sizes: Record<string, number> = {
  "logement/data/raw/insee.xlsx": 1000,
  "logement/data/raw/lovac-communes.csv": 7_000_000,
  "logement/data/raw/lovac-big.csv": 90_000_000,
  "logement/src/logement/core/parc.py": 3000,
  "logement/src/logement/shell/build.py": 9000,
  "logement/data/processed/vacance.json": 4000,
};

const { graph, files } = studyToGraph(registries, {
  studyPrefix: "logement/",
  version: { tag: "v1" },
  statFile: (path) => (path in sizes ? { size: sizes[path] ?? 0 } : null),
  maxAssetBytes: 25_000_000,
});

describe("studyToGraph", () => {
  it("maps every registry into one closed graph", () => {
    expect(graph.nodes.map((n) => n.id)).toEqual([
      "S-01",
      "S-05",
      "D-01",
      "D-02",
      "H-06",
      "H-01",
      "O-01",
      "T-01",
      "R-02",
      "L-01",
      "C-01",
      "I-01",
    ]);
    expect(danglingReferences(graph)).toEqual([]);
    expect(graph.version).toEqual({ tag: "v1" });
  });

  it("normalises titles and attaches source files with hosting decided by size", () => {
    const s01 = graph.nodes.find((n) => n.id === "S-01");
    expect(s01?.title).toBe("Parc de logements au 1er janvier");
    expect(s01?.type === "source" && s01.files).toEqual([
      {
        path: "sources/insee.xlsx",
        name: "insee.xlsx",
        mime: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        size: 1000,
        checksum: "sha256:" + "a".repeat(64),
        hosted: "asset",
      },
    ]);
    const s05 = graph.nodes.find((n) => n.id === "S-05");
    expect(s05?.type === "source" && s05.files.map((f) => f.hosted)).toEqual([
      "asset",
      "object-store",
    ]);
  });

  it("links definitions to their source and hypotheses to their justification", () => {
    expect(graph.nodes.find((n) => n.id === "D-01")?.depends_on).toEqual(["S-01"]);
    expect(graph.nodes.find((n) => n.id === "H-06")?.depends_on).toEqual(["S-05"]);
  });

  it("accepts a qualitative hypothesis (statement, no numeric parameter)", () => {
    const h01 = graph.nodes.find((n) => n.id === "H-01");
    expect(h01?.type === "hypothesis" && h01.statement).toMatch(/substituable/);
    expect(h01?.type === "hypothesis" && h01.central_value).toBeUndefined();
    expect(h01?.limitations).toEqual(["L-01"]);
  });

  it("links a constructed notion to the choice that formulates it", () => {
    expect(graph.nodes.find((n) => n.id === "D-02")?.depends_on).toEqual(["S-01", "C-01"]);
  });

  it("keeps a non-redistributable file out of the manifest but on the node", () => {
    const { graph: g, files: f } = studyToGraph(
      {
        ...registries,
        sources: [{ ...registries.sources[0], redistributable: false }],
        claims: [],
        definitions: [],
        hypotheses: [],
      },
      { studyPrefix: "logement/", version: {}, statFile: () => ({ size: 10 }), maxAssetBytes: 100 },
    );
    const s01 = g.nodes[0];
    expect(s01?.type === "source" && s01.files[0]?.hosted).toBe("none");
    expect(f).toEqual([]);
  });

  it("rejects a hypothesis that is neither a full parameter nor a statement", () => {
    const broken = (extra: object) =>
      studyToGraph(
        {
          ...registries,
          claims: [],
          definitions: [],
          hypotheses: [{ id: "H-09", name: "x", description: "x", confidence: "low", ...extra }],
        },
        { studyPrefix: "s/", version: {}, statFile: () => null, maxAssetBytes: 1 },
      );
    expect(() => broken({})).toThrow(/statement/);
    expect(() => broken({ central_value: 1 })).toThrow(/incomplet/);
  });

  it("publishes code and outputs once each, with repo paths", () => {
    const r02 = graph.nodes.find((n) => n.id === "R-02");
    expect(r02?.type === "result" && r02.produced_by).toEqual({
      path: "code/src/logement/shell/build.py",
      repo_path: "logement/src/logement/shell/build.py",
      language: "python",
    });
    expect(r02?.type === "result" && r02.output).toEqual({
      path: "data/vacance.json",
      repo_path: "logement/data/processed/vacance.json",
    });
    expect(files.map((f) => f.path)).toEqual([
      "sources/insee.xlsx",
      "sources/lovac-communes.csv",
      "sources/lovac-big.csv",
      "code/src/logement/core/parc.py",
      "code/src/logement/shell/build.py",
      "data/vacance.json",
    ]);
    expect(files.find((f) => f.path === "sources/lovac-big.csv")?.hosted).toBe("object-store");
  });

  it("marks a missing file as not hosted rather than failing", () => {
    const { graph: g } = studyToGraph(
      { ...registries, claims: [], definitions: [], hypotheses: [] },
      {
        studyPrefix: "logement/",
        version: {},
        statFile: () => null,
        maxAssetBytes: 1,
      },
    );
    const s01 = g.nodes[0];
    expect(s01?.type === "source" && s01.files[0]?.hosted).toBe("none");
  });
});
