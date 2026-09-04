import type { LucideIcon } from "lucide-react";
import { cn } from "~/web/lib/cn";
import { Tooltip } from "./tooltip";

// Bouton icône du design system : tooltip obligatoire (c'est son libellé).
export function IconButton({
  icon: Icon,
  label,
  onClick,
  className,
  disabled,
}: {
  icon: LucideIcon;
  label: string;
  onClick: () => void;
  className?: string;
  disabled?: boolean;
}) {
  return (
    <Tooltip content={label}>
      <button
        type="button"
        aria-label={label}
        disabled={disabled}
        onClick={onClick}
        className={cn(
          "rounded-md p-1.5 text-ink-3 transition-colors hover:bg-paper-2 hover:text-ink",
          "disabled:cursor-not-allowed disabled:opacity-40 disabled:hover:bg-transparent",
          className,
        )}
      >
        <Icon aria-hidden className="size-4" />
      </button>
    </Tooltip>
  );
}
