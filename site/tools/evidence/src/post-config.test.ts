import { describe, expect, it } from "vitest";
import { stripLeadingTitle } from "./post-config.ts";

describe("stripLeadingTitle", () => {
  it("drops the H1 and a bold subtitle line that follows it", () => {
    expect(stripLeadingTitle("# Titre\n\n**Sous-titre.**\n\n*Intro*\n")).toBe("*Intro*\n");
    expect(stripLeadingTitle("# Titre\n\nTexte **gras** ici\n")).toBe("Texte **gras** ici\n");
    expect(stripLeadingTitle("Pas de titre\n")).toBe("Pas de titre\n");
  });
});
