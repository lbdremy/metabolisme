import { describe, expect, it } from "vitest";
import { detectDelimiter, previewCsv } from "./csv-preview";

describe("detectDelimiter", () => {
  it("picks the delimiter that splits every line the same way", () => {
    expect(detectDelimiter("a;b;c\n1;2;3\n4;5;6")).toBe(";");
    expect(detectDelimiter("a,b\n1,2")).toBe(",");
    expect(detectDelimiter("a\tb\n1\t2")).toBe("\t");
    expect(detectDelimiter("solo\nline")).toBe(",");
  });
});

describe("previewCsv", () => {
  it("parses quoted cells and drops a partial last line of a cut sample", () => {
    const sample = 'code;libellé;n\n01;"Ain; plaine";3\n02;"Aisne ""x""";4\n03;Allie';
    const preview = previewCsv(sample, { maxRows: 10, complete: false });
    expect(preview.header).toEqual(["code", "libellé", "n"]);
    expect(preview.rows).toEqual([
      ["01", "Ain; plaine", "3"],
      ["02", 'Aisne "x"', "4"],
    ]);
    expect(preview.truncated).toBe(true);
  });

  it("keeps every line of a complete sample and caps the rows", () => {
    const preview = previewCsv("a,b\n1,2\n3,4\n5,6\n", { maxRows: 2, complete: true });
    expect(preview.rows).toEqual([
      ["1", "2"],
      ["3", "4"],
    ]);
    expect(preview.truncated).toBe(true);
    expect(previewCsv("a,b\n1,2\n", { maxRows: 2, complete: true }).truncated).toBe(false);
  });
});
