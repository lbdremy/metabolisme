import { describe, expect, it } from "vitest";
import { EvidenceGraphSchema } from "~/contracts/evidence";
import { createEvidenceExplorerModel } from "./evidence-explorer-model";

const graph = EvidenceGraphSchema.parse({
  nodes: [
    { id: "S-01", type: "source", title: "s", publisher: "p", source_url: "u", files: [] },
    { id: "O-01", type: "observation", title: "o", depends_on: ["S-01"] },
    { id: "R-01", type: "result", title: "r", depends_on: ["O-01"] },
  ],
});

async function ready() {
  const model = createEvidenceExplorerModel();
  await model.load(() => Promise.resolve(graph));
  return model;
}

describe("evidence explorer model", () => {
  it("loads the graph once and exposes the index", async () => {
    const model = await ready();
    const vm = model.toViewModel(model.getSnapshot());
    expect(vm.graphStatus).toBe("ready");
    expect(vm.isKnown("R-01")).toBe(true);
    expect(vm.isKnown("R-09")).toBe(false);
    await model.load(() => Promise.reject(new Error("no")));
    expect(model.toViewModel(model.getSnapshot()).graphStatus).toBe("ready");
  });

  it("reports a loading failure", async () => {
    const model = createEvidenceExplorerModel();
    await model.load(() => Promise.reject(new Error("HTTP 500")));
    const vm = model.toViewModel(model.getSnapshot());
    expect(vm.graphStatus).toBe("error");
    expect(vm.errorMessage).toBe("HTTP 500");
  });

  it("keeps a trail of visited nodes, truncating on a revisit", async () => {
    const model = await ready();
    model.visit("R-01");
    model.visit("O-01");
    model.visit("S-01");
    expect(model.toViewModel(model.getSnapshot()).trail.map((n) => n.id)).toEqual([
      "R-01",
      "O-01",
      "S-01",
    ]);
    expect(model.previous()).toBe("O-01");
    model.visit("O-01");
    expect(model.toViewModel(model.getSnapshot()).trail.map((n) => n.id)).toEqual(["R-01", "O-01"]);
    expect(model.toViewModel(model.getSnapshot()).chain.map((s) => s.id)).toEqual(["S-01"]);
    model.visit(null);
    expect(model.toViewModel(model.getSnapshot()).trail).toEqual([]);
    expect(model.previous()).toBeNull();
  });

  it("flags an unknown selected id and resets the open file on navigation", async () => {
    const model = await ready();
    model.visit("R-99");
    expect(model.toViewModel(model.getSnapshot()).selectedMissing).toBe(true);
    model.visit("S-01");
    model.openFile(
      "S-01",
      { path: "sources/x.pdf", name: "x.pdf", mime: "application/pdf", size: 1, hosted: "asset" },
      3,
    );
    expect(model.toViewModel(model.getSnapshot()).openFile?.page).toBe(3);
    model.visit("O-01");
    expect(model.toViewModel(model.getSnapshot()).openFile).toBeNull();
  });

  it("projects the same view model for the same snapshot", async () => {
    const model = await ready();
    const snapshot = model.getSnapshot();
    expect(model.toViewModel(snapshot)).toBe(model.toViewModel(snapshot));
  });
});
