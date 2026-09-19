import { useCallback, useEffect, useRef, useState } from "react";
import { NO_TAPS, registerTap, type TapSequence } from "./model/review-mode";

// Hook ViewModel du mode relecture : l'horloge, le stockage du navigateur et
// le compteur de clics — la reconnaissance du geste, elle, est pure.

const STORAGE_KEY = "metabolisme.review-mode";

function read(): boolean {
  try {
    return window.localStorage.getItem(STORAGE_KEY) === "on";
  } catch {
    // Stockage refusé (navigation privée, réglage strict) : le mode existe
    // pour la session, il ne survivra simplement pas au rechargement.
    return false;
  }
}

function write(enabled: boolean): void {
  try {
    if (enabled) window.localStorage.setItem(STORAGE_KEY, "on");
    else window.localStorage.removeItem(STORAGE_KEY);
  } catch {
    /* idem */
  }
}

export type ReviewMode = {
  readonly enabled: boolean;
  readonly onLogoTap: () => void;
  readonly disable: () => void;
};

export function useReviewMode(): ReviewMode {
  const [enabled, setEnabled] = useState(false);
  const enabledRef = useRef(false);
  const taps = useRef<TapSequence>(NO_TAPS);

  const apply = useCallback((next: boolean) => {
    enabledRef.current = next;
    setEnabled(next);
    write(next);
  }, []);

  // Le serveur ne connaît pas le choix du lecteur : il est lu après
  // hydratation, sinon les deux rendus divergent.
  useEffect(() => {
    const stored = read();
    if (stored) {
      enabledRef.current = true;
      setEnabled(true);
    }
  }, []);

  const onLogoTap = useCallback(() => {
    const result = registerTap(taps.current, Date.now());
    taps.current = result.sequence;
    if (result.completed) apply(!enabledRef.current);
  }, [apply]);

  const disable = useCallback(() => {
    apply(false);
  }, [apply]);

  return { enabled, onLogoTap, disable };
}
