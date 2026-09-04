import { describe, expect, it } from "vitest";
import { danglingReferences, indexGraph, upstreamChain, upstreamSources } from "./graph-index.ts";
import { EvidenceGraphSchema } from "./graph.ts";

const graph = EvidenceGraphSchema.parse({
  nodes: [
    { id: "S-01", type: "source", title: "s", publisher: "INSEE", source_url: "https://x" },
    { id: "S-02", type: "source", title: "s2", publisher: "SDES", source_url: "https://y" },
    { id: "O-01", type: "observation", title: "o", depends_on: ["S-01"] },
    { id: "T-01", type: "transformation", title: "t", depends_on: ["O-01"] },
    { id: "L-01", type: "limit", title: "l" },
    {
      id: "R-01",
      type: "result",
      title: "r",
      depends_on: ["T-01", "S-02"],
      limitations: ["L-01"],
    },
    { id: "I-01", type: "interpretation", title: "i", depends_on: ["R-01"] },
  ],
});

describe("indexGraph", () => {
  const index = indexGraph(graph);

  it("resolves nodes and reverse edges", () => {
    expect(index.byId.get("R-01")?.type).toBe("result");
    expect(index.dependents.get("R-01")).toEqual(["I-01"]);
    expect(index.dependents.get("S-01")).toEqual(["O-01"]);
    expect(index.limitedNodes.get("L-01")).toEqual(["R-01"]);
  });

  it("walks the upstream chain breadth-first, each node once", () => {
    expect(upstreamChain(index, "I-01")).toEqual([
      { id: "R-01", depth: 1 },
      { id: "T-01", depth: 2 },
      { id: "S-02", depth: 2 },
      { id: "O-01", depth: 3 },
      { id: "S-01", depth: 4 },
    ]);
    expect(upstreamSources(index, "I-01")).toEqual(["S-02", "S-01"]);
    expect(upstreamChain(index, "S-01")).toEqual([]);
  });
});

describe("danglingReferences", () => {
  it("is empty on a closed graph and lists broken edges otherwise", () => {
    expect(danglingReferences(graph)).toEqual([]);
    const broken = EvidenceGraphSchema.parse({
      nodes: [
        { id: "R-01", type: "result", title: "r", depends_on: ["T-09"], limitations: ["L-07"] },
      ],
    });
    expect(danglingReferences(broken)).toEqual([
      { from: "R-01", to: "T-09" },
      { from: "R-01", to: "L-07" },
    ]);
  });
});
