import type { ReactNode } from "react";
import { tv } from "tailwind-variants";

// Pastille du design system. Le `tone` est une couleur de la charte, sans
// vocabulaire produit : le mapping statut → couleur vit dans le module qui
// connaît les statuts.

const badge = tv({
  base: "inline-flex items-center gap-1 rounded-full px-2 py-0.5 font-sans text-[0.7rem] font-semibold uppercase tracking-wider",
  variants: {
    tone: {
      neutral: "bg-paper-2 text-ink-2",
      accent: "text-white",
      outline: "border border-current bg-transparent",
    },
  },
  defaultVariants: {
    tone: "neutral",
  },
});

export function Badge({
  tone = "neutral",
  color,
  className,
  children,
}: {
  tone?: "neutral" | "accent" | "outline";
  // Couleur CSS appliquée en fond (accent) ou en texte (outline).
  color?: string | undefined;
  className?: string | undefined;
  children: ReactNode;
}) {
  const style =
    color === undefined ? undefined : tone === "accent" ? { backgroundColor: color } : { color };
  return (
    <span data-slot="badge" data-tone={tone} className={badge({ tone, className })} style={style}>
      {children}
    </span>
  );
}
