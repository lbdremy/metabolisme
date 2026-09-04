import { createFileRoute, Link } from "@tanstack/react-router";
import { Wordmark } from "~/web/components/ui/logo";
import { PostList } from "~/web/modules/posts/components/post-list";
import { listPosts } from "~/web-rpc/public";

export const Route = createFileRoute("/")({
  loader: () => listPosts(),
  component: HomePage,
});

function HomePage() {
  const posts = Route.useLoaderData();

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
          <h1 className="font-sans text-[2.2rem] font-bold leading-[1.08] tracking-tight text-ink sm:text-[2.8rem]">
            Concevoir des institutions à partir des conditions réelles.
          </h1>
          <p className="mt-5 max-w-[60ch] font-serif text-[1.15rem] leading-relaxed text-ink-2">
            Métabolisme est un programme de recherche : des systèmes économiques et institutionnels
            pensés depuis le matériel — logements vacants, coûts, revenus, flux — et publiés avec
            leur <strong className="text-ink">chaîne de preuves exécutable</strong>. Chaque chiffre
            renvoie à sa source, son calcul, ses hypothèses. Tout est contestable, parce que tout
            est inspectable.
          </p>
        </section>
        <section className="pt-10">
          {posts.length === 0 ? (
            <p className="font-sans text-ink-3">Aucun article publié pour l'instant.</p>
          ) : (
            <PostList posts={posts} />
          )}
        </section>
      </main>
    </div>
  );
}
