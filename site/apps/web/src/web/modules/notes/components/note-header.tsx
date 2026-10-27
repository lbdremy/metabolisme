import { Link } from "@tanstack/react-router";
import { Link as LinkIcon } from "lucide-react";
import { conceptionStatus, isConception, type Note } from "~/contracts/evidence";
import { CopyButton } from "~/web/components/ui/copy-button";
import { ArtefactKindBadge } from "~/web/modules/artefacts/components/artefact-kind-badge";
import { frenchSpacing } from "~/web/lib/french-spacing";
import { formatDate } from "~/web/modules/evidence/model/format";
import { InReviewBadge } from "~/web/modules/posts/components/in-review-badge";
import { VersionLine } from "~/web/modules/posts/components/post-header";

// En-tête d'une note : titre, date, contexte, et le lien à copier. Un
// article de conception porte en plus son type, son statut et le chemin du
// sommaire ; une note isolée reste un message partagé par lien.
export function NoteHeader({ note }: { note: Note }) {
  const design = isConception(note);
  return (
    <header>
      <p className="flex flex-wrap items-center gap-2 font-sans text-[0.75rem] font-semibold uppercase tracking-wider text-ink-3">
        {design ? <ArtefactKindBadge kind="design" /> : <span>Note</span>}
        <span>{formatDate(note.date)}</span>
        {design && conceptionStatus(note) === "in_review" && <InReviewBadge />}
        <CopyButton
          label={design ? "Copier le lien de cet article" : "Copier le lien de cette note"}
          copiedLabel="Lien copié"
          icon={LinkIcon}
          getText={() => window.location.href.split("?")[0] ?? window.location.href}
          className="-my-1"
        />
      </p>
      <h1 className="mt-3 font-sans text-[1.7rem] font-bold leading-[1.15] tracking-tight text-ink sm:text-[2rem]">
        {frenchSpacing(note.title)}
      </h1>
      {note.context !== undefined && (
        <p className="mt-3 font-serif text-[1rem] italic leading-relaxed text-ink-2">
          {frenchSpacing(note.context.trim())}
        </p>
      )}
      {design && (
        <p className="mt-3 font-sans text-[0.8rem] text-ink-3">
          Article de conception : il porte surtout des valeurs, des choix et des propositions, et
          dit nœud par nœud ce qui reste à établir.{" "}
          <Link to="/conception" className="text-ink underline decoration-1 underline-offset-2">
            Tous les articles de conception
          </Link>
        </p>
      )}
      <VersionLine version={note.version} />
    </header>
  );
}
