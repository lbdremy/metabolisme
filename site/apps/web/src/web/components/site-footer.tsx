import { Eye } from "lucide-react";
import { Logo } from "~/web/components/ui/logo";
import type { ReviewMode } from "~/web/modules/posts/use-review-mode";

// Pied de page : le logo seul, centré. Trois clics rapprochés dessus
// basculent le mode relecture (les posts en attente de relecture
// réapparaissent dans l'index) ; le bandeau qui suit dit que le mode est
// actif et permet d'en sortir.
export function SiteFooter({ review }: { review: ReviewMode }) {
  return (
    <footer className="mx-auto flex max-w-3xl flex-col items-center gap-3 px-6 pb-14 pt-6">
      <button
        type="button"
        onClick={review.onLogoTap}
        aria-label="Métabolisme"
        className="rounded-full p-1 opacity-60 transition-opacity hover:opacity-100"
      >
        <Logo size={20} />
      </button>
      {review.enabled && (
        <p className="inline-flex items-center gap-2 rounded-full border border-rule bg-white/60 px-3 py-1 font-sans text-[0.72rem] text-ink-2">
          <Eye aria-hidden className="size-3.5 text-ink-3" />
          Articles en attente de relecture : visibles
          <button
            type="button"
            onClick={review.disable}
            className="underline decoration-1 underline-offset-2 hover:text-ink"
          >
            masquer
          </button>
        </p>
      )}
    </footer>
  );
}
