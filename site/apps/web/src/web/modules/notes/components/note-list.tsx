import { Link } from "@tanstack/react-router";
import { ArrowRight } from "lucide-react";
import { conceptionStatus, type Note } from "~/contracts/evidence";
import { frenchSpacing } from "~/web/lib/french-spacing";
import { formatDate } from "~/web/modules/evidence/model/format";
import { InReviewBadge } from "~/web/modules/posts/components/in-review-badge";

export type CollectedNote = { readonly token: string; readonly note: Note };

// La liste des articles de conception : un par ligne, dans l'ordre de
// lecture du recueil (position), pas dans l'ordre des dates — le numéro est
// la position dans le recueil, il ne change pas quand une partie est
// masquée. Le lien mène à l'adresse à jeton de l'article. La page qui la
// porte dit déjà leur type.
export function NoteList({ notes }: { notes: ReadonlyArray<CollectedNote> }) {
  return (
    <ol className="divide-y divide-rule">
      {notes.map(({ token, note }) => (
        <li key={token} className="py-7 first:pt-0">
          <Link to="/notes/$token" params={{ token }} className="group flex gap-5">
            <span
              aria-hidden
              className="mt-1 w-6 shrink-0 font-sans text-[0.8rem] font-semibold tabular-nums text-ink-3"
            >
              {String(note.collection?.position ?? 0).padStart(2, "0")}
            </span>
            <span className="block">
              <span className="flex flex-wrap items-center gap-2 font-sans text-[0.72rem] font-semibold uppercase tracking-wider text-ink-3">
                <span>{formatDate(note.date)}</span>
                {conceptionStatus(note) === "in_review" && <InReviewBadge />}
              </span>
              <span className="mt-2 block font-sans text-[1.35rem] font-bold leading-tight tracking-tight text-ink group-hover:underline group-hover:decoration-2 group-hover:underline-offset-4">
                {frenchSpacing(note.title)}
              </span>
              {note.context !== undefined && (
                <span className="mt-2 block font-serif text-[0.95rem] leading-relaxed text-ink-2">
                  {frenchSpacing(note.context.trim())}
                </span>
              )}
              <span className="mt-3 inline-flex items-center gap-1 font-sans text-[0.8rem] font-medium text-ink">
                Lire, avec la chaîne de preuves
                <ArrowRight
                  aria-hidden
                  className="size-3.5 transition-transform group-hover:translate-x-0.5"
                />
              </span>
            </span>
          </Link>
        </li>
      ))}
    </ol>
  );
}
