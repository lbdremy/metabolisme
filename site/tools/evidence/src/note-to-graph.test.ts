import { describe, expect, it } from "vitest";
import { noteToGraph } from "./note-to-graph.ts";

const authored = {
  nodes: [
    {
      id: "S-01",
      type: "source",
      title: "Datalab 395",
      publisher: "SDES",
      source_url: "https://sdes",
      files: ["sources/datalab-395.pdf"],
    },
    {
      id: "O-01",
      type: "observation",
      title: "5,4 M",
      value: "5 396 300",
      depends_on: ["S-01"],
      locators: [{ file: "sources/datalab-395.pdf", page: 1, quote: "5,4 millions" }],
    },
    { id: "I-01", type: "interpretation", title: "gros parc", depends_on: ["O-01"] },
  ],
};

const options = {
  version: {},
  notePrefix: "",
  readFile: (path: string) =>
    path === "sources/datalab-395.pdf" ? { size: 10, checksum: "sha256:" + "c".repeat(64) } : null,
};

describe("noteToGraph", () => {
  it("attaches files with computed metadata and reports no problem on a sound note", () => {
    const { graph, files, problems } = noteToGraph(authored, "[5,4 M](ev:O-01) (I-01)", options);
    expect(problems).toEqual([]);
    expect(files).toEqual([
      {
        path: "sources/datalab-395.pdf",
        from: "sources/datalab-395.pdf",
        size: 10,
        mime: "application/pdf",
        hosted: "asset",
      },
    ]);
    const source = graph.nodes[0];
    expect(source?.type === "source" && source.files[0]?.checksum).toBe("sha256:" + "c".repeat(64));
  });

  it("reports missing files, dangling references, unknown anchors and orphans", () => {
    const broken = {
      nodes: [
        { ...authored.nodes[0], files: ["sources/nope.pdf"] },
        { ...authored.nodes[1], depends_on: ["S-09"] },
        { id: "L-01", type: "limit", title: "unused" },
      ],
    };
    const { problems } = noteToGraph(broken, "[x](ev:O-01) et R-05", options);
    expect(problems.map((p) => p.kind)).toEqual([
      "missing-file",
      "dangling",
      "unknown-anchor",
      "locator",
      "orphan",
      "orphan",
    ]);
  });
});
