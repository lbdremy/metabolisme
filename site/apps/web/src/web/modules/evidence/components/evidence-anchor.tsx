import type { ReactNode } from "react";
import { nodeTypeOfId } from "~/contracts/evidence";
import { cn } from "~/web/lib/cn";
import { STATUS } from "../model/status";

// L'ancre de preuve dans le texte : le passage (un chiffre, une phrase) ou
// l'identifiant nu, souligné de la couleur de son statut. C'est un vrai lien
// vers l'état d'URL du nœud (?n=R-07) — il se partage, marche sans script,
// et se coupe en fin de ligne comme du texte (un bouton ne le ferait pas) ;
// avec script, le clic ouvre le panneau sans recharger la page.
export function EvidenceAnchor({
  id,
  active,
  ready,
  onOpen,
  children,
}: {
  id: string;
  active: boolean;
  ready: boolean;
  onOpen: (id: string) => void;
  children: ReactNode;
}) {
  const type = nodeTypeOfId(id);
  const color = type === null ? "var(--color-ink-3)" : STATUS[type].cssVar;
  const bare = typeof children === "string" && children === id;
  return (
    <a
      href={`?n=${id}`}
      data-evidence={id}
      data-active={active || undefined}
      aria-disabled={!ready || undefined}
      onClick={(event) => {
        event.preventDefault();
        if (ready) onOpen(id);
      }}
      title={type === null ? id : `${id} — ${STATUS[type].label}`}
      style={{ "--anchor": color } as React.CSSProperties}
      className={cn(
        "rounded-sm transition-colors",
        !ready && "cursor-default",
        bare
          ? "mx-px px-1 font-mono text-[0.72em] font-semibold text-[var(--anchor)] outline outline-1 -outline-offset-1 outline-[color-mix(in_oklab,var(--anchor)_40%,transparent)] hover:bg-[color-mix(in_oklab,var(--anchor)_12%,transparent)]"
          : "underline decoration-[var(--anchor)] decoration-2 underline-offset-[0.2em] hover:bg-[color-mix(in_oklab,var(--anchor)_12%,transparent)]",
        active && "bg-[color-mix(in_oklab,var(--anchor)_18%,transparent)]",
      )}
    >
      {children}
    </a>
  );
}
