import { describe, expect, it } from "vitest";
import { collectAnchoredIds, parseEvidenceHref, splitBareIds } from "./anchors.ts";

describe("parseEvidenceHref", () => {
  it("accepts ev: hrefs with a valid id only", () => {
    expect(parseEvidenceHref("ev:R-07")).toBe("R-07");
    expect(parseEvidenceHref("ev:R-123")).toBe("R-123");
    expect(parseEvidenceHref("ev:ZE-01")).toBeNull();
    expect(parseEvidenceHref("https://insee.fr")).toBeNull();
    expect(parseEvidenceHref(undefined)).toBeNull();
  });
});

const known = (id: string) => ["S-01", "S-02", "R-01"].includes(id);

describe("splitBareIds", () => {
  it("turns known ids into anchors and leaves the rest as text", () => {
    expect(splitBareIds("vacants (S-01/S-02) et L-01.", known)).toEqual([
      { kind: "text", text: "vacants (" },
      { kind: "anchor", id: "S-01" },
      { kind: "text", text: "/" },
      { kind: "anchor", id: "S-02" },
      { kind: "text", text: ") et L-01." },
    ]);
  });

  it("does not match ids glued to other letters", () => {
    expect(splitBareIds("ZE-01 et F-23 et R-01", known)).toEqual([
      { kind: "text", text: "ZE-01 et F-23 et " },
      { kind: "anchor", id: "R-01" },
    ]);
  });

  it("returns a single text segment when nothing matches", () => {
    expect(splitBareIds("rien", known)).toEqual([{ kind: "text", text: "rien" }]);
  });
});

describe("collectAnchoredIds", () => {
  it("collects explicit and bare ids once, in order", () => {
    expect(collectAnchoredIds("[5,4 M](ev:O-01) soit 15,9 % (O-02, O-01) ev:S-01")).toEqual([
      "O-01",
      "O-02",
      "S-01",
    ]);
  });
});
