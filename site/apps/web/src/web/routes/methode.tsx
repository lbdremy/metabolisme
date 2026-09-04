import { createFileRoute, Link } from "@tanstack/react-router";
import Markdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { Wordmark } from "~/web/components/ui/logo";
import { getPage } from "~/web-rpc/public";

// La méthode (INTRO.md du dépôt), rendue telle quelle.
export const Route = createFileRoute("/methode")({
  loader: () => getPage({ data: { slug: "methode" } }),
  head: () => ({ meta: [{ title: "La méthode — Métabolisme" }] }),
  component: MethodPage,
});

function MethodPage() {
  const { markdown } = Route.useLoaderData();
  return (
    <div className="min-h-screen">
      <header className="sticky top-0 z-30 flex h-12 items-center border-b border-rule bg-paper/95 px-6 backdrop-blur">
        <Link to="/">
          <Wordmark />
        </Link>
      </header>
      <main className="mx-auto max-w-[72ch] px-6 py-12">
        <div className="prose-reading">
          <Markdown remarkPlugins={[remarkGfm]}>{markdown}</Markdown>
        </div>
      </main>
    </div>
  );
}
