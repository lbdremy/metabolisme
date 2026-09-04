import type { EvidenceNode } from "~/contracts/evidence";
import { cn } from "~/web/lib/cn";
import { STATUS } from "../model/status";

// Un nœud cité dans le panneau : identifiant coloré + titre tronqué, cliquable
// pour l'ouvrir. C'est l'unité de navigation dans la chaîne.
export function NodeChip({
  node,
  onOpen,
  active = false,
  showTitle = true,
}: {
  node: EvidenceNode;
  onOpen: (id: string) => void;
  active?: boolean;
  showTitle?: boolean;
}) {
  const status = STATUS[node.type];
  return (
    <button
      type="button"
      onClick={() => onOpen(node.id)}
      aria-current={active || undefined}
      className={cn(
        "group flex w-full items-start gap-2 rounded-md border border-rule bg-white/60 px-2.5 py-1.5 text-left",
        "font-sans text-[0.8rem] leading-snug transition-colors hover:border-rule-2 hover:bg-white",
        active && "border-ink bg-white",
      )}
    >
      <span
        className="mt-0.5 shrink-0 rounded px-1 py-px font-mono text-[0.68rem] font-semibold text-white"
        style={{ backgroundColor: status.cssVar }}
      >
        {node.id}
      </span>
      {showTitle && (
        <span className="line-clamp-2 text-ink-2 group-hover:text-ink">{node.title}</span>
      )}
    </button>
  );
}
