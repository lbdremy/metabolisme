import { Link } from "@tanstack/react-router";
import { Wordmark } from "~/web/components/ui/logo";

// L'en-tête des pages de sommaire : le logo, et les deux types d'articles
// avant la méthode qui les distingue.
export function SiteHeader() {
  return (
    <header className="mx-auto flex max-w-3xl items-center justify-between px-6 pt-8">
      <Link to="/">
        <Wordmark />
      </Link>
      <nav className="flex items-center gap-5 font-sans text-[0.85rem] text-ink-2">
        <Link to="/recherche" className="hover:underline">
          Recherches
        </Link>
        <Link to="/conception" className="hover:underline">
          Conception
        </Link>
        <Link to="/methode" className="hover:underline">
          La méthode
        </Link>
      </nav>
    </header>
  );
}
