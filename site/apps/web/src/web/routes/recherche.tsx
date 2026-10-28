import { createFileRoute } from "@tanstack/react-router";
import { Link as LinkIcon } from "lucide-react";
import { useEffect, useMemo, useState } from "react";
import { z } from "zod";
import type { Post } from "~/contracts/evidence";
import { SiteFooter } from "~/web/components/site-footer";
import { SiteHeader } from "~/web/components/site-header";
import { CopyButton } from "~/web/components/ui/copy-button";
import { ArtefactKindBadge } from "~/web/modules/artefacts/components/artefact-kind-badge";
import { PostList } from "~/web/modules/posts/components/post-list";
import { useReviewMode } from "~/web/modules/posts/use-review-mode";
import { listPosts, listPostsInReview } from "~/web-rpc/public";

// `?relecture=1` montre aussi ce qui est en relecture, comme sur /conception.
const SearchSchema = z.object({
  relecture: z.coerce.boolean().optional().catch(undefined),
});

// Le sommaire des articles de recherche, du plus récent au plus ancien.
// Seuls les articles relus y figurent d'office.
export const Route = createFileRoute("/recherche")({
  validateSearch: SearchSchema,
  loader: () => listPosts(),
  head: () => ({ meta: [{ title: "Recherche — Métabolisme" }] }),
  component: ResearchPage,
});

function ResearchPage() {
  const published = Route.useLoaderData();
  const { relecture } = Route.useSearch();
  const review = useReviewMode();
  const showReview = review.enabled || relecture === true;
  const [inReview, setInReview] = useState<ReadonlyArray<Post>>([]);

  useEffect(() => {
    if (!showReview) {
      setInReview([]);
      return;
    }
    let current = true;
    void listPostsInReview().then((list) => {
      if (current) setInReview(list);
    });
    return () => {
      current = false;
    };
  }, [showReview]);

  const posts = useMemo(
    () => [...published, ...inReview].toSorted((a, b) => b.date.localeCompare(a.date)),
    [published, inReview],
  );

  return (
    <div className="min-h-screen">
      <SiteHeader />
      <main className="mx-auto max-w-3xl px-6 pb-24 pt-14">
        <section className="border-b border-rule pb-10">
          <p className="flex items-center gap-2">
            <ArtefactKindBadge kind="research" />
            <CopyButton
              label="Copier le lien de ce sommaire"
              copiedLabel="Lien copié"
              icon={LinkIcon}
              getText={() => window.location.href}
              className="-my-1"
            />
          </p>
          <h1 className="mt-3 font-sans text-[2.2rem] font-bold leading-[1.08] tracking-tight text-ink sm:text-[2.6rem]">
            Établir l'existant
          </h1>
          <p className="mt-5 max-w-[60ch] font-serif text-[1.15rem] leading-relaxed text-ink-2">
            La recherche établit ce qui est : logements vacants, coûts, revenus, rentes, flux.
            Chaque article part de sources figées et publie sa{" "}
            <strong className="text-ink">chaîne de preuves exécutable</strong> : chaque chiffre
            renvoie à sa source, son calcul et ses hypothèses, et se rejoue depuis les données.
          </p>
        </section>
        <section className="pt-10">
          {posts.length === 0 ? (
            <p className="font-sans text-ink-3">
              Aucun article de recherche publié pour l'instant.
            </p>
          ) : (
            <PostList posts={posts} />
          )}
        </section>
      </main>
      <SiteFooter review={review} />
    </div>
  );
}
