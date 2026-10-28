import { createFileRoute } from "@tanstack/react-router";
import { SiteFooter } from "~/web/components/site-footer";
import { SiteHeader } from "~/web/components/site-header";
import { TwoDisciplines } from "~/web/modules/artefacts/components/two-disciplines";
import { useReviewMode } from "~/web/modules/posts/use-review-mode";

// L'accueil présente le programme et ses deux disciplines ; les articles sont
// listés chacun sur le sommaire de son type (/recherche, /conception).
export const Route = createFileRoute("/")({
  component: HomePage,
});

function HomePage() {
  const review = useReviewMode();

  return (
    <div className="min-h-screen">
      <SiteHeader />
      <main className="mx-auto max-w-3xl px-6 pb-24 pt-14">
        <section className="border-b border-rule pb-10">
          <h1 className="font-sans text-[2.2rem] font-bold leading-[1.08] tracking-tight text-ink sm:text-[2.8rem]">
            Concevoir des institutions à partir des conditions réelles.
          </h1>
          <p className="mt-5 max-w-[60ch] font-serif text-[1.15rem] leading-relaxed text-ink-2">
            Métabolisme est un programme de recherche et de conception : il établit l'existant —
            logements vacants, coûts, revenus, rentes, flux — et conçoit à partir de lui des
            systèmes économiques et institutionnels. Tout est publié avec sa{" "}
            <strong className="text-ink">chaîne de preuves exécutable</strong> : chaque chiffre
            renvoie à sa source, son calcul, ses hypothèses, et chaque choix est nommé comme tel.
          </p>
        </section>

        <TwoDisciplines />
      </main>
      <SiteFooter review={review} />
    </div>
  );
}
