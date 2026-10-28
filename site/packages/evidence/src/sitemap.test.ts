import { describe, expect, it } from "vitest";
import type { Note, Post } from "./publication.ts";
import { renderSitemap, sitemapEntries } from "./sitemap.ts";

function post(slug: string, date: string, status: Post["status"] = "published"): Post {
  return {
    slug,
    title: slug,
    date,
    study: { slug: "logement", name: "Logement" },
    status,
    version: {},
  };
}

describe("sitemapEntries", () => {
  it("liste l'accueil, la méthode, la recherche puis ses posts relus, du plus récent au plus ancien", () => {
    const entries = sitemapEntries([post("ancien", "2026-08-01"), post("recent", "2026-09-10")]);
    expect(entries.map((entry) => entry.path)).toEqual([
      "/",
      "/methode",
      "/recherche",
      "/posts/recent",
      "/posts/ancien",
      "/conception",
    ]);
  });

  it("laisse les posts en relecture hors du plan", () => {
    const entries = sitemapEntries([
      post("relu", "2026-08-01"),
      post("en-relecture", "2026-09-10", "in_review"),
    ]);
    expect(entries.map((entry) => entry.path)).not.toContain("/posts/en-relecture");
  });

  it("date l'accueil du dernier post relu", () => {
    const entries = sitemapEntries([
      post("relu", "2026-08-01"),
      post("en-relecture", "2026-09-10", "in_review"),
    ]);
    expect(entries[0]).toEqual({ path: "/", lastmod: "2026-08-01" });
  });

  it("sans post relu, l'accueil n'a pas de date", () => {
    expect(sitemapEntries([])[0]).toEqual({ path: "/" });
  });
});

function design(slug: string, date: string, status?: Note["status"]): Note {
  return {
    slug,
    title: slug,
    date,
    collection: { slug: "conception", title: "Conception", position: 1 },
    ...(status === undefined ? {} : { status }),
    version: {},
  };
}

describe("sitemapEntries — articles de conception", () => {
  const notes = [
    { token: "pub", note: design("publiee", "2026-10-20", "published") },
    { token: "rel", note: design("en-relecture", "2026-10-25") },
    {
      token: "iso",
      note: {
        slug: "isolee",
        title: "isolee",
        date: "2026-10-26",
        status: "published",
        version: {},
      } as Note,
    },
  ];

  it("ajoute les seuls articles de conception publiés, à leur adresse lisible", () => {
    const paths = sitemapEntries([], notes).map((entry) => entry.path);
    expect(paths).toContain("/conception/publiee");
    expect(paths).not.toContain("/notes/pub");
    expect(paths).not.toContain("/notes/rel");
    expect(paths).not.toContain("/notes/iso");
  });

  it("date l'accueil de la publication la plus récente, recherche ou conception", () => {
    expect(sitemapEntries([post("relu", "2026-08-01")], notes)[0]).toEqual({
      path: "/",
      lastmod: "2026-10-20",
    });
  });
});

describe("renderSitemap", () => {
  it("produit des URL absolues sans double barre", () => {
    const xml = renderSitemap("https://metabolisme.dev/", [
      { path: "/posts/x", lastmod: "2026-09-10" },
    ]);
    expect(xml).toContain(
      "<url><loc>https://metabolisme.dev/posts/x</loc><lastmod>2026-09-10</lastmod></url>",
    );
    expect(xml.startsWith('<?xml version="1.0" encoding="UTF-8"?>')).toBe(true);
  });

  it("échappe les caractères XML", () => {
    expect(renderSitemap("https://a.b", [{ path: "/?a=1&b=2" }])).toContain(
      "https://a.b/?a=1&amp;b=2",
    );
  });
});
