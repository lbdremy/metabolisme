import { describe, expect, it, vi } from "vitest";
import { createModelStore } from "./create-model-store.ts";

type Snapshot = {
  count: number;
  profile: { name: string };
};

const initial: Snapshot = { count: 0, profile: { name: "a" } };

describe("createModelStore", () => {
  it("returns the same snapshot reference between mutations", () => {
    const store = createModelStore<Snapshot>({ ...initial });
    expect(store.getSnapshot()).toBe(store.getSnapshot());
  });

  it("replaces the snapshot reference on update", () => {
    const store = createModelStore<Snapshot>({ ...initial });
    const before = store.getSnapshot();
    store.update((draft) => {
      draft.count = 1;
    });
    const after = store.getSnapshot();
    expect(after).not.toBe(before);
    expect(after.count).toBe(1);
    expect(before.count).toBe(0);
  });

  it("keeps structural sharing for untouched branches", () => {
    const store = createModelStore<Snapshot>({ ...initial });
    const before = store.getSnapshot();
    store.update((draft) => {
      draft.count = 1;
    });
    expect(store.getSnapshot().profile).toBe(before.profile);
  });

  it("notifies subscribers on update and stops after unsubscribe", () => {
    const store = createModelStore<Snapshot>({ ...initial });
    const listener = vi.fn();
    const unsubscribe = store.subscribe(listener);
    store.update((draft) => {
      draft.count = 1;
    });
    expect(listener).toHaveBeenCalledTimes(1);
    unsubscribe();
    store.update((draft) => {
      draft.count = 2;
    });
    expect(listener).toHaveBeenCalledTimes(1);
  });

  it("emits JSON patches when an observer is registered", () => {
    const onPatches = vi.fn();
    const store = createModelStore<Snapshot>({ ...initial }, { onPatches });
    store.update((draft) => {
      draft.count = 5;
    });
    expect(onPatches).toHaveBeenCalledTimes(1);
    const [patches, inversePatches] = onPatches.mock.calls[0] as [unknown[], unknown[]];
    expect(patches).toHaveLength(1);
    expect(inversePatches).toHaveLength(1);
  });

  it("freezes snapshots in dev: in-place mutation throws", () => {
    const store = createModelStore<Snapshot>({ ...initial });
    store.update((draft) => {
      draft.count = 1;
    });
    const snapshot = store.getSnapshot();
    expect(() => {
      (snapshot as { count: number }).count = 99;
    }).toThrow();
  });
});
