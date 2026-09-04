import { Link as LinkIcon } from "lucide-react";
import type { Note } from "~/contracts/evidence";
import { CopyButton } from "~/web/components/ui/copy-button";
import { formatDate } from "~/web/modules/evidence/model/format";
import { VersionLine } from "~/web/modules/posts/components/post-header";

// En-tête d'une note partagée : titre, date, contexte d'envoi, et le lien
// à copier — c'est lui qui se partage, la note n'est listée nulle part.
export function NoteHeader({ note }: { note: Note }) {
  return (
    <header>
      <p className="flex items-center gap-2 font-sans text-[0.75rem] font-semibold uppercase tracking-wider text-ink-3">
        Note · {formatDate(note.date)}
        <CopyButton
          label="Copier le lien de cette note"
          copiedLabel="Lien copié"
          icon={LinkIcon}
          getText={() => window.location.href.split("?")[0] ?? window.location.href}
          className="-my-1"
        />
      </p>
      <h1 className="mt-3 font-sans text-[1.7rem] font-bold leading-[1.15] tracking-tight text-ink sm:text-[2rem]">
        {note.title}
      </h1>
      {note.context !== undefined && (
        <p className="mt-3 font-serif text-[1rem] italic leading-relaxed text-ink-2">
          {note.context.trim()}
        </p>
      )}
      <VersionLine version={note.version} />
    </header>
  );
}
