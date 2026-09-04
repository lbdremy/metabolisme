import { Check, Copy, type LucideIcon } from "lucide-react";
import { useCopyToClipboard } from "~/web/hooks/use-copy-to-clipboard";
import { cn } from "~/web/lib/cn";
import { Tooltip } from "./tooltip";

// Bouton de copie du design system : icône + tooltip, qui bascule sur le
// libellé de confirmation (et une coche) pendant deux secondes après la copie.
// Le texte à copier est fourni paresseusement (getText) au moment du clic.

export function CopyButton({
  label,
  copiedLabel,
  getText,
  icon: Icon = Copy,
  className,
}: {
  label: string;
  copiedLabel: string;
  getText: () => string;
  icon?: LucideIcon;
  className?: string;
}) {
  const { copied, copy } = useCopyToClipboard();
  const Glyph = copied ? Check : Icon;

  return (
    <Tooltip content={copied ? copiedLabel : label}>
      <button
        type="button"
        aria-label={label}
        data-slot="copy-button"
        data-copied={copied || undefined}
        onClick={() => copy(getText())}
        className={cn(
          "rounded-md p-1.5 text-ink-3 transition-colors hover:bg-paper-2 hover:text-ink",
          copied && "text-status-transformation hover:text-status-transformation",
          className,
        )}
      >
        <Glyph aria-hidden className="size-4" />
      </button>
    </Tooltip>
  );
}
