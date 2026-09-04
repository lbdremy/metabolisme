import { Tooltip as BaseTooltip } from "@base-ui-components/react/tooltip";
import type { ReactElement, ReactNode } from "react";

// Tooltip du design system : primitive Base UI, apparence maison.
// L'élément déclencheur est fourni tel quel via `children` (render prop
// Base UI) — le composant n'impose ni balise ni styles au déclencheur.

export function Tooltip({
  content,
  children,
}: {
  content: ReactNode;
  children: ReactElement<Record<string, unknown>>;
}) {
  return (
    <BaseTooltip.Root>
      <BaseTooltip.Trigger render={children} />
      <BaseTooltip.Portal>
        <BaseTooltip.Positioner sideOffset={6}>
          <BaseTooltip.Popup
            data-slot="tooltip"
            className="z-50 rounded-md bg-ink px-2 py-1 font-sans text-xs text-paper shadow-md"
          >
            {content}
          </BaseTooltip.Popup>
        </BaseTooltip.Positioner>
      </BaseTooltip.Portal>
    </BaseTooltip.Root>
  );
}
