import type { Readable, ReadableKind } from "./reader-scope.ts";

// Recherche plein texte dans les publications lisibles — fonction pure.
//
// Insensible à la casse et aux accents (« preemption » trouve
// « préemption »). Une publication répond si TOUS les mots de la requête y
// figurent (titre ou texte) ; elle est classée par nombre d'occurrences et
// renvoyée avec quelques extraits, pour que le lecteur choisisse quoi ouvrir.

export type SearchHit = {
  readonly kind: ReadableKind;
  readonly slug: string;
  readonly title: string;
  readonly occurrences: number;
  readonly excerpts: readonly string[];
};

export type SearchOptions = {
  readonly kind?: ReadableKind;
  readonly limit?: number;
  readonly excerptsPerHit?: number;
  readonly excerptRadius?: number;
};

// Replie chaque caractère sans en changer la longueur (sans accent,
// minuscule) : les
// positions du texte replié sont celles du texte d'origine, ce qui
// permet d'extraire les passages tels qu'écrits.
export function foldText(text: string): string {
  let out = "";
  for (const char of text) {
    const folded = char.normalize("NFD").replace(/\p{M}/gu, "").toLowerCase();
    out += folded.length === char.length ? folded : char;
  }
  return out;
}

function occurrencesOf(haystack: string, needle: string): number[] {
  const positions: number[] = [];
  let from = haystack.indexOf(needle);
  while (from !== -1) {
    positions.push(from);
    from = haystack.indexOf(needle, from + needle.length);
  }
  return positions;
}

function excerptAt(text: string, position: number, length: number, radius: number): string {
  const start = Math.max(0, position - radius);
  const end = Math.min(text.length, position + length + radius);
  const body = text.slice(start, end).replace(/\s+/g, " ").trim();
  return `${start > 0 ? "…" : ""}${body}${end < text.length ? "…" : ""}`;
}

export function searchReadables(
  readables: ReadonlyArray<Readable>,
  query: string,
  options: SearchOptions = {},
): SearchHit[] {
  const { kind, limit = 20, excerptsPerHit = 3, excerptRadius = 160 } = options;
  const terms = [
    ...new Set(
      foldText(query)
        .split(/\s+/)
        .filter((term) => term.length > 0),
    ),
  ];
  if (terms.length === 0) return [];
  const hits: SearchHit[] = [];
  for (const readable of readables) {
    if (kind !== undefined && readable.kind !== kind) continue;
    const title = foldText(readable.title);
    const body = foldText(readable.markdown);
    const perTerm = terms.map((term) => ({
      term,
      inTitle: title.includes(term),
      positions: occurrencesOf(body, term),
    }));
    if (perTerm.some((entry) => !entry.inTitle && entry.positions.length === 0)) continue;
    const occurrences = perTerm.reduce(
      (sum, entry) => sum + entry.positions.length + (entry.inTitle ? 1 : 0),
      0,
    );
    // Les premiers passages de chaque mot, sans extraits qui se recouvrent.
    const anchors = perTerm
      .flatMap((entry) =>
        entry.positions.map((position) => ({ position, length: entry.term.length })),
      )
      .toSorted((a, b) => a.position - b.position);
    const excerpts: string[] = [];
    let lastEnd = -1;
    for (const anchor of anchors) {
      if (excerpts.length >= excerptsPerHit) break;
      if (anchor.position < lastEnd) continue;
      excerpts.push(excerptAt(readable.markdown, anchor.position, anchor.length, excerptRadius));
      lastEnd = anchor.position + anchor.length + excerptRadius;
    }
    hits.push({
      kind: readable.kind,
      slug: readable.slug,
      title: readable.title,
      occurrences,
      excerpts,
    });
  }
  return hits.toSorted((a, b) => b.occurrences - a.occurrences).slice(0, limit);
}
