import { useEffect, useRef, useState } from "react";
import { createNavigatorClipboardPort, type ClipboardPort } from "~/web/lib/clipboard";

// Hook générique : copie un texte et expose un état « copié » éphémère pour le
// retour visuel (tooltip). Adaptateur React pur au-dessus du port presse-papier.

const RESET_AFTER_MS = 2000;

export function useCopyToClipboard(args?: { port?: ClipboardPort }): {
  copied: boolean;
  copy: (text: string) => void;
} {
  const portRef = useRef<ClipboardPort | null>(null);
  portRef.current ??= args?.port ?? createNavigatorClipboardPort();
  const [copied, setCopied] = useState(false);
  const timerRef = useRef<ReturnType<typeof setTimeout> | null>(null);

  useEffect(() => {
    return () => {
      if (timerRef.current !== null) clearTimeout(timerRef.current);
    };
  }, []);

  const copy = (text: string) => {
    void portRef.current?.writeText(text).then((result) => {
      if (!result.ok) return;
      setCopied(true);
      if (timerRef.current !== null) clearTimeout(timerRef.current);
      timerRef.current = setTimeout(() => setCopied(false), RESET_AFTER_MS);
    });
  };

  return { copied, copy };
}
