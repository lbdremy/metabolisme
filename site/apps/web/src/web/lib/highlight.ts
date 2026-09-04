import { createHighlighterCore, type HighlighterCore } from "@shikijs/core";
import { createJavaScriptRegexEngine } from "@shikijs/engine-javascript";

// Coloration syntaxique (shiki, grammaires embarquées) : chargée à la demande
// — la première ouverture d'un fichier de code paie l'import, pas le site.
// Port navigateur pur : aucune API React ici.

let instance: Promise<HighlighterCore> | null = null;

function highlighter(): Promise<HighlighterCore> {
  instance ??= createHighlighterCore({
    themes: [import("@shikijs/themes/github-light")],
    langs: [
      import("@shikijs/langs/python"),
      import("@shikijs/langs/yaml"),
      import("@shikijs/langs/json"),
      import("@shikijs/langs/typescript"),
    ],
    engine: createJavaScriptRegexEngine(),
  });
  return instance;
}

const KNOWN = new Set(["python", "yaml", "json", "typescript"]);

export async function highlightToHtml(code: string, language: string): Promise<string> {
  const core = await highlighter();
  return core.codeToHtml(code, {
    lang: KNOWN.has(language) ? language : "text",
    theme: "github-light",
  });
}
