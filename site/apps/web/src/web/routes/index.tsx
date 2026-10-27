import { createFileRoute, Link } from "@tanstack/react-router";
import { useEffect, useMemo, useState } from "react";
import type { Post } from "~/contracts/evidence";
import { SiteFooter } from "~/web/components/site-footer";
import { SiteHeader } from "~/web/components/site-header";
import { ArtefactKindBadge } from "~/web/modules/artefacts/components/artefact-kind-badge";
import { TwoDisciplines } from "~/web/modules/artefacts/components/two-disciplines";
import { NoteList, type CollectedNote } from "~/web/modules/notes/components/note-list";
import { PostList } from "~/web/modules/posts/components/post-list";
import { useReviewMode } from "~/web/modules/posts/use-review-mode";
import {
  listConception,
  listConceptionInReview,
  listPosts,
  listPostsInReview,
} from "~/web-rpc/public";

export const Route = createFileRoute("/")({
  loader: async () => {
    const [posts, designs] = await Promise.all([listPosts(), listConception()]);
    return { posts, designs };
  },
  component: HomePage,
});

function HomePage() {
  const { posts: published, designs: publishedDesigns } = Route.useLoaderData();
  const review = useReviewMode();
  const [postsInReview, setPostsInReview] = useState<ReadonlyArray<Post>>([]);
  const [designsInReview, setDesignsInReview] = useState<ReadonlyArray<CollectedNote>>([]);

  // Ce qui attend la relecture n'est pas dans la réponse de la page : il est
  // demandé à part, seulement quand le mode est actif.
  useEffect(() => {
    if (!review.enabled) {
      setPostsInReview([]);
      setDesignsInReview([]);
      return;
    }
    let current = true;
    void Promise.all([listPostsInReview(), listConceptionInReview()]).then(([posts, designs]) => {
      if (!current) return;
      setPostsInReview(posts);
      setDesignsInReview(designs);
    });
    return () => {
      current = false;
    };
  }, [review.enabled]);

  const posts = useMemo(
    () => [...published, ...postsInReview].toSorted((a, b) => b.date.localeCompare(a.date)),
    [published, postsInReview],
  );
  const designs = useMemo(
    () =>
      [...publishedDesigns, ...designsInReview].toSorted(
        (a, b) => (a.note.collection?.position ?? 0) - (b.note.collection?.position ?? 0),
      ),
    [publishedDesigns, designsInReview],
  );

  return (
    <div className="min-h-screen">
      <SiteHeader />
      <main className="mx-auto max-w-3xl px-6 pb-24 pt-14">
        <section className="border-b border-rule pb-10">
          <h1 className="font-sans text-[2.2rem] font-bold leading-[1.08] tracking-tight text-ink sm:text-[2.8rem]">
            Concevoir des institutions à partir des conditions réelles.
          </h1>
          <p className="mt-5 max-w-[60ch] font-serif text-[1.15rem] leading-relaxed text-ink-2">
            Métabolisme est un programme de recherche et de conception : il établit l'existant —
            logements vacants, coûts, revenus, rentes, flux — et conçoit à partir de lui des
            systèmes économiques et institutionnels. Tout est publié avec sa{" "}
            <strong className="text-ink">chaîne de preuves exécutable</strong> : chaque chiffre
            renvoie à sa source, son calcul, ses hypothèses, et chaque choix est nommé comme tel.
          </p>
        </section>

        <TwoDisciplines />

        <section id="recherche" aria-labelledby="titre-recherche" className="scroll-mt-8 pt-12">
          <SectionTitle id="titre-recherche" kind="research" title="Établir l'existant" />
          <div className="mt-8">
            {posts.length === 0 ? (
              <p className="font-sans text-ink-3">
                Aucun article de recherche publié pour l'instant.
              </p>
            ) : (
              <PostList posts={posts} />
            )}
          </div>
        </section>

        <section
          id="conception"
          aria-labelledby="titre-conception"
          className="mt-6 scroll-mt-8 border-t border-rule pt-12"
        >
          <SectionTitle
            id="titre-conception"
            kind="design"
            title="Concevoir des systèmes métaboliques"
          />
          <div className="mt-8">
            {designs.length === 0 ? (
              <p className="max-w-[60ch] font-serif text-[1rem] leading-relaxed text-ink-3">
                Les premiers articles de conception sont en relecture. Ils paraîtront ici un par un.
              </p>
            ) : (
              <NoteList notes={designs} />
            )}
          </div>
          <p className="mt-8 font-sans text-[0.85rem]">
            <Link to="/conception" className="text-ink underline decoration-1 underline-offset-2">
              Le sommaire de la conception, dans l'ordre de lecture
            </Link>
          </p>
        </section>
      </main>
      <SiteFooter review={review} />
    </div>
  );
}

function SectionTitle({
  id,
  kind,
  title,
}: {
  id: string;
  kind: "research" | "design";
  title: string;
}) {
  return (
    <div>
      <ArtefactKindBadge kind={kind} />
      <h2
        id={id}
        className="mt-3 font-sans text-[1.6rem] font-bold leading-tight tracking-tight text-ink"
      >
        {title}
      </h2>
    </div>
  );
}
