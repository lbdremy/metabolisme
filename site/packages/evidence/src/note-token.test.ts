import { describe, expect, it } from "vitest";
import { deriveNoteToken } from "./note-token.ts";
import { NoteTokenSchema } from "./publication.ts";

describe("deriveNoteToken", () => {
  it("is deterministic, secret-dependent and well-formed", async () => {
    const a = await deriveNoteToken("secret", "ma-note");
    expect(a).toBe(await deriveNoteToken("secret", "ma-note"));
    expect(a).not.toBe(await deriveNoteToken("autre", "ma-note"));
    expect(a).not.toBe(await deriveNoteToken("secret", "ma-note-2"));
    expect(NoteTokenSchema.safeParse(a).success).toBe(true);
  });
});
