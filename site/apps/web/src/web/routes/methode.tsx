import { createFileRoute } from "@tanstack/react-router";
import Markdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { SiteFooter } from "~/web/components/site-footer";
import { SiteHeader } from "~/web/components/site-header";
import { useReviewMode } from "~/web/modules/posts/use-review-mode";
import { getPage } from "~/web-rpc/public";

// La méthode (INTRO.md du dépôt), rendue telle quelle.
export const Route = createFileRoute("/methode")({
  loader: () => getPage({ data: { slug: "methode" } }),
  head: () => ({ meta: [{ title: "La méthode — Métabolisme" }] }),
  component: MethodPage,
});

function MethodPage() {
  const { markdown } = Route.useLoaderData();
  const review = useReviewMode();
  return (
    <div className="min-h-screen">
      <SiteHeader />
      <main className="mx-auto max-w-[72ch] px-6 py-12">
        <div className="prose-reading">
          <Markdown remarkPlugins={[remarkGfm]}>{markdown}</Markdown>
        </div>
      </main>
      <SiteFooter review={review} />
    </div>
  );
}
