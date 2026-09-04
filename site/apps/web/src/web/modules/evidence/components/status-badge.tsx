import type { NodeType } from "~/contracts/evidence";
import { Badge } from "~/web/components/ui/badge";
import { Tooltip } from "~/web/components/ui/tooltip";
import { STATUS } from "../model/status";

// Le statut épistémique d'un nœud, en couleur de la charte. Compact : la
// lettre seule ; complet : lettre + libellé.
export function StatusBadge({
  type,
  compact = false,
  className,
}: {
  type: NodeType;
  compact?: boolean;
  className?: string;
}) {
  const status = STATUS[type];
  return (
    <Tooltip content={status.hint}>
      <Badge tone="accent" color={status.cssVar} className={className}>
        {compact ? status.letter : `${status.letter} · ${status.label}`}
      </Badge>
    </Tooltip>
  );
}

export function StatusDot({ type, className }: { type: NodeType; className?: string }) {
  return (
    <span
      aria-hidden
      className={className ?? "inline-block size-2 rounded-full"}
      style={{ backgroundColor: STATUS[type].cssVar }}
    />
  );
}
