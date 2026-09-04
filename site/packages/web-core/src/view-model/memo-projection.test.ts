import { describe, expect, it, vi } from "vitest";
import { memoProjection } from "./memo-projection.ts";

describe("memoProjection", () => {
  it("returns the same ViewModel reference for the same snapshot reference", () => {
    const project = vi.fn((s: { title: string }) => ({ label: s.title }));
    const memoized = memoProjection(project);
    const snapshot = { title: "a" };
    expect(memoized(snapshot)).toBe(memoized(snapshot));
    expect(project).toHaveBeenCalledTimes(1);
  });

  it("projects again for a new snapshot reference", () => {
    const memoized = memoProjection((s: { title: string }) => ({
      label: s.title,
    }));
    const first = memoized({ title: "a" });
    const second = memoized({ title: "b" });
    expect(first).not.toBe(second);
    expect(second.label).toBe("b");
  });
});
