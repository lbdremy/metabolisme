import { createFileRoute } from "@tanstack/react-router";
import { Link as LinkIcon } from "lucide-react";
import { useEffect, useMemo, useState } from "react";
import { z } from "zod";
import { SiteFooter } from "~/web/components/site-footer";
import { SiteHeader } from "~/web/components/site-header";
import { CopyButton } from "~/web/components/ui/copy-button";
import { ArtefactKindBadge } from "~/web/modules/artefacts/components/artefact-kind-badge";
import { NoteList, type CollectedNote } from "~/web/modules/notes/components/note-list";
import { useReviewMode } from "~/web/modules/posts/use-review-mode";
import { listConception, listConceptionInReview } from "~/web-rpc/public";

// `?relecture=1` montre aussi ce qui est en relecture, sans activer le mode
// pour tout le site : c'est l'adresse qui se partage avec ceux qui relisent
// (l'ancien sommaire /livret y mène). Ce n'est pas un secret, c'est un tri.
const SearchSchema = z.object({
  relecture: z.coerce.boolean().optional().catch(undefined),
});

// Le sommaire des articles de conception, dans l'ordre de lecture du
// recueil. Seuls les articles publiés y figurent d'office.
export const Route = createFileRoute("/conception")({
  validateSearch: SearchSchema,
  loader: () => listConception(),
  head: () => ({ meta: [{ title: "Conception — Métabolisme" }] }),
  component: ConceptionPage,
});

function ConceptionPage() {
  const published = Route.useLoaderData();
  const { relecture } = Route.useSearch();
  const review = useReviewMode();
  const showReview = review.enabled || relecture === true;
  const [inReview, setInReview] = useState<ReadonlyArray<CollectedNote>>([]);

  useEffect(() => {
    if (!showReview) {
      setInReview([]);
      return;
    }
    let current = true;
    void listConceptionInReview().then((list) => {
      if (current) setInReview(list);
    });
    return () => {
      current = false;
    };
  }, [showReview]);

  const designs = useMemo(
    () =>
      [...published, ...inReview].toSorted(
        (a, b) => (a.note.collection?.position ?? 0) - (b.note.collection?.position ?? 0),
      ),
    [published, inReview],
  );

  return (
    <div className="min-h-screen">
      <SiteHeader />
      <main className="mx-auto max-w-3xl px-6 pb-24 pt-14">
        <section className="border-b border-rule pb-10">
          <p className="flex items-center gap-2">
            <ArtefactKindBadge kind="design" />
            <CopyButton
              label="Copier le lien de ce sommaire"
              copiedLabel="Lien copié"
              icon={LinkIcon}
              getText={() => window.location.href}
              className="-my-1"
            />
          </p>
          <h1 className="mt-3 font-sans text-[2.2rem] font-bold leading-[1.08] tracking-tight text-ink sm:text-[2.6rem]">
            Concevoir des systèmes métaboliques
          </h1>
          <p className="mt-5 max-w-[60ch] font-serif text-[1.15rem] leading-relaxed text-ink-2">
            La conception métabolique dessine des institutions qui vivent comme un organisme : elles
            captent une ressource dans leur milieu, la transforment en patrimoine durable plutôt
            qu'en dépense consommée, et s'entretiennent d'elles-mêmes. Chaque article en propose
            une, avec sa <strong className="text-ink">chaîne de preuves</strong> : les faits sont
            sourcés, les valeurs et les choix nommés comme tels.
          </p>
        </section>
        <section className="pt-10">
          {designs.length === 0 ? (
            <p className="max-w-[60ch] font-serif text-[1rem] leading-relaxed text-ink-3">
              Les premiers articles de conception sont en relecture. Ils paraîtront ici un par un.
            </p>
          ) : (
            <NoteList notes={designs} />
          )}
        </section>
      </main>
      <SiteFooter review={review} />
    </div>
  );
}
