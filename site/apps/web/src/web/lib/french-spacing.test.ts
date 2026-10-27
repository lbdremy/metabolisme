import { describe, expect, it } from "vitest";
import { frenchSpacing } from "./french-spacing";

describe("frenchSpacing", () => {
  it("rend insécable l'espace avant la ponctuation haute", () => {
    expect(frenchSpacing("deux mécanismes ; un troisième : la commande ?")).toBe(
      "deux mécanismes ; un troisième : la commande ?",
    );
  });

  it("rend insécables les espaces intérieurs des guillemets", () => {
    expect(frenchSpacing("« Reconnaître une rente »")).toBe("« Reconnaître une rente »");
  });

  it("laisse intact un texte sans ponctuation haute", () => {
    expect(frenchSpacing("Établir l'existant")).toBe("Établir l'existant");
  });
});
