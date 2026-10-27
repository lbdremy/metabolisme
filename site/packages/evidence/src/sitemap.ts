import { isPublishedConception, notePath } from "./collection.ts";
import type { Note, Post } from "./publication.ts";

// Plan du site pour les moteurs (sitemap.xml) — fonction pure.
//
// Il ne liste que ce que l'accueil présente : l'accueil, la méthode, les
// articles de recherche relus (posts), le sommaire de la conception et les
// articles de conception publiés. Ce qui est en relecture est servi à son
// adresse mais signalé noindex ; les autres notes restent hors index — leur
// adresse se transmet, elle ne se découvre pas.

export type SitemapEntry = {
  readonly path: string;
  readonly lastmod?: string;
};

export function sitemapEntries(
  posts: ReadonlyArray<Post>,
  notes: ReadonlyArray<{ readonly token: string; readonly note: Note }> = [],
): SitemapEntry[] {
  const published = posts
    .filter((post) => post.status === "published")
    .toSorted((a, b) => b.date.localeCompare(a.date));
  const designs = notes
    .filter((entry) => isPublishedConception(entry.note))
    .toSorted((a, b) => b.note.date.localeCompare(a.note.date));
  const latest = [published[0]?.date, designs[0]?.note.date]
    .filter((date): date is string => date !== undefined)
    .toSorted()
    .at(-1);
  return [
    latest === undefined ? { path: "/" } : { path: "/", lastmod: latest },
    { path: "/methode" },
    ...published.map((post) => ({ path: `/posts/${post.slug}`, lastmod: post.date })),
    { path: "/conception" },
    ...designs.map((entry) => ({ path: notePath(entry), lastmod: entry.note.date })),
  ];
}

function escapeXml(text: string): string {
  return text
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&apos;");
}

export function renderSitemap(origin: string, entries: ReadonlyArray<SitemapEntry>): string {
  const base = origin.replace(/\/+$/, "");
  const urls = entries.map((entry) => {
    const lastmod = entry.lastmod === undefined ? "" : `<lastmod>${entry.lastmod}</lastmod>`;
    return `  <url><loc>${escapeXml(base + entry.path)}</loc>${lastmod}</url>`;
  });
  return [
    '<?xml version="1.0" encoding="UTF-8"?>',
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ...urls,
    "</urlset>",
    "",
  ].join("\n");
}
