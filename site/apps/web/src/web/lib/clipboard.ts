import { err, ok, type BrowserCapabilityError, type Result } from "@metabolisme/web-core";

// Port presse-papier : l'API navigateur reste derrière ce contrat (doctrine —
// jamais de navigator.* dans un composant feuille).

export type ClipboardPort = {
  writeText: (text: string) => Promise<Result<void, BrowserCapabilityError>>;
};

export function createNavigatorClipboardPort(): ClipboardPort {
  return {
    async writeText(text) {
      if (typeof navigator === "undefined" || navigator.clipboard === undefined) {
        return err({
          code: "clipboard/not-supported",
          message: "Le presse-papier n'est pas disponible dans ce navigateur.",
          severity: "warning",
          recoverable: true,
          capability: "clipboard",
          reason: "not-supported",
        });
      }
      try {
        await navigator.clipboard.writeText(text);
        return ok(undefined);
      } catch (cause) {
        return err({
          code: "clipboard/write-failed",
          message: "La copie dans le presse-papier a échoué.",
          severity: "warning",
          recoverable: true,
          capability: "clipboard",
          reason: "permission-denied",
          cause,
        });
      }
    },
  };
}

export function createFakeClipboardPort(): ClipboardPort & { texts: string[] } {
  const texts: string[] = [];
  return {
    texts,
    writeText(text) {
      texts.push(text);
      return Promise.resolve(ok(undefined));
    },
  };
}
