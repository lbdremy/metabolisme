import { describe, expect, it } from "vitest";
import { deriveMcpToken, tokensMatch } from "./mcp-token.ts";
import { deriveNoteToken } from "./note-token.ts";

describe("deriveMcpToken", () => {
  it("est stable et dépend du secret", async () => {
    expect(await deriveMcpToken("a")).toBe(await deriveMcpToken("a"));
    expect(await deriveMcpToken("a")).not.toBe(await deriveMcpToken("b"));
  });

  it("a la forme d'un jeton de note sans pouvoir en être un", async () => {
    const token = await deriveMcpToken("secret");
    expect(token).toMatch(/^[a-z0-9]{24}$/);
    expect(token).not.toBe(await deriveNoteToken("secret", "mcp"));
  });
});

describe("tokensMatch", () => {
  it("n'accepte que le jeton exact", () => {
    expect(tokensMatch("abc", "abc")).toBe(true);
    expect(tokensMatch("abc", "abd")).toBe(false);
    expect(tokensMatch("abc", "ab")).toBe(false);
    expect(tokensMatch("abc", "")).toBe(false);
  });
});
