import { describe, expect, it } from "vitest";
import { formatBytes, formatDate, viewerKindOf } from "./format";

describe("format", () => {
  it("formats sizes and dates in French", () => {
    expect(formatBytes(900)).toBe("900 o");
    expect(formatBytes(52_462)).toBe("51 Ko");
    expect(formatBytes(3_007_255)).toBe("2.9 Mo");
    expect(formatDate("2026-08-10")).toBe("10 août 2026");
    expect(formatDate("2025")).toBe("2025");
  });

  it("chooses a viewer from the mime type", () => {
    expect(viewerKindOf("application/pdf", "x.pdf")).toBe("pdf");
    expect(viewerKindOf("text/csv; charset=utf-8", "x.csv")).toBe("csv");
    expect(viewerKindOf("text/x-python; charset=utf-8", "x.py")).toBe("code");
    expect(viewerKindOf("application/zip", "x.zip")).toBe("download");
    expect(viewerKindOf("application/xml; charset=utf-8", "x.xml")).toBe("text");
  });
});
