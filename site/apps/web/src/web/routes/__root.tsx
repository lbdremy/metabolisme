/// <reference types="vite/client" />
import { createRootRoute, HeadContent, Link, Outlet, Scripts } from "@tanstack/react-router";
import type { ReactNode } from "react";
import appCss from "~/styles.css?url";
import { Wordmark } from "~/web/components/ui/logo";

export const Route = createRootRoute({
  head: () => ({
    meta: [
      { charSet: "utf-8" },
      { name: "viewport", content: "width=device-width, initial-scale=1" },
      { title: "Métabolisme" },
      {
        name: "description",
        content:
          "Concevoir des institutions à partir des conditions matérielles, avec des chaînes de preuves exécutables.",
      },
    ],
    links: [
      { rel: "stylesheet", href: appCss },
      { rel: "icon", type: "image/png", href: "/favicon.png" },
    ],
  }),
  component: RootComponent,
  notFoundComponent: NotFound,
});

function RootComponent() {
  return (
    <RootDocument>
      <Outlet />
    </RootDocument>
  );
}

function NotFound() {
  return (
    <main className="mx-auto max-w-2xl px-6 py-24 text-center">
      <Wordmark />
      <p className="mt-8 font-sans text-ink-2">Cette page n'existe pas.</p>
      <Link to="/" className="mt-4 inline-block font-sans text-sm underline">
        Retour à l'accueil
      </Link>
    </main>
  );
}

function RootDocument({ children }: { children: ReactNode }) {
  return (
    <html lang="fr">
      <head>
        <HeadContent />
      </head>
      <body className="min-h-screen bg-paper text-ink">
        {children}
        <Scripts />
      </body>
    </html>
  );
}
