import { createFileRoute, Link } from "@tanstack/react-router";
import { Link as LinkIcon } from "lucide-react";
import { SiteFooter } from "~/web/components/site-footer";
import { CopyButton } from "~/web/components/ui/copy-button";
import { Wordmark } from "~/web/components/ui/logo";
import { NoteList } from "~/web/modules/notes/components/note-list";
import { useReviewMode } from "~/web/modules/posts/use-review-mode";
import { listCollection } from "~/web-rpc/public";

// Le sommaire du livret : la seule page du site qui liste des notes.
//
// Elle ne change rien à leur régime — chacune garde son adresse à jeton et son
// noindex — mais elle donne une adresse UNIQUE à partager avec le groupe de
// travail, au lieu de dix liens. Elle est donc elle-même hors index : pas de
// lien depuis l'accueil ni depuis la méthode, et « noindex, nofollow ».
export const Route = createFileRoute("/livret")({
  loader: () => listCollection({ data: { collection: "livret" } }),
  head: () => ({
    meta: [
      { name: "robots", content: "noindex, nofollow" },
      { title: "Livret 2027 — notes Métabolisme" },
    ],
  }),
  component: LivretPage,
});

function LivretPage() {
  const notes = Route.useLoaderData();
  const review = useReviewMode();

  return (
    <div className="min-h-screen">
      <header className="mx-auto flex max-w-3xl items-center justify-between px-6 pt-8">
        <Link to="/">
          <Wordmark />
        </Link>
        <nav className="font-sans text-[0.85rem] text-ink-2">
          <Link to="/methode" className="hover:underline">
            La méthode
          </Link>
        </nav>
      </header>
      <main className="mx-auto max-w-3xl px-6 pb-24 pt-14">
        <section className="border-b border-rule pb-10">
          <p className="flex items-center gap-2 font-sans text-[0.75rem] font-semibold uppercase tracking-wider text-ink-3">
            Recueil de notes
            <CopyButton
              label="Copier le lien de ce sommaire"
              copiedLabel="Lien copié"
              icon={LinkIcon}
              getText={() => window.location.href.split("?")[0] ?? window.location.href}
              className="-my-1"
            />
          </p>
          <h1 className="mt-3 font-sans text-[2.2rem] font-bold leading-[1.08] tracking-tight text-ink sm:text-[2.6rem]">
            Livret 2027
          </h1>
          <p className="mt-5 max-w-[60ch] font-serif text-[1.15rem] leading-relaxed text-ink-2">
            Dix notes écrites pour être lues ensemble : deux mécanismes de conception, trois droits,
            la préemption des rentes de position, la forme urbaine, et la liste de ce qui reste à
            instruire. Ce sont des <strong className="text-ink">textes de travail</strong> — la
            plupart de ce qu'ils affirment est encore valeur, choix ou interprétation, et le panneau
            de droite le dit nœud par nœud plutôt que de le déguiser en résultat.
          </p>
          <p className="mt-4 max-w-[60ch] font-sans text-[0.85rem] leading-relaxed text-ink-3">
            Cette page n'est référencée nulle part : elle existe pour être partagée telle quelle,
            avec les adresses des notes qu'elle rassemble.
          </p>
        </section>
        <section className="pt-10">
          {notes.length === 0 ? (
            <p className="font-sans text-ink-3">Aucune note dans ce recueil.</p>
          ) : (
            <NoteList notes={notes} />
          )}
        </section>
      </main>
      <SiteFooter review={review} />
    </div>
  );
}
