import { NODE_ID_PATTERN } from "./graph.ts";

// Ancres de preuve dans un texte Markdown.
//
// Deux façons de relier un passage au graphe :
//   - explicite : un lien dont l'URL est « ev:R-07 » — le passage entier
//     (un chiffre, une phrase) devient l'ancre ;
//   - implicite : un identifiant nu dans le texte (« … 194 488 logements
//     (R-07) … ») — l'identifiant lui-même devient l'ancre, s'il existe
//     dans le graphe.
// Les deux mènent au même endroit : le panneau, ouvert sur ce nœud.

export const EVIDENCE_SCHEME = "ev:";

export function evidenceHref(id: string): string {
  return `${EVIDENCE_SCHEME}${id}`;
}

// L'identifiant visé par un href, ou null si ce n'est pas une ancre de preuve.
export function parseEvidenceHref(href: string | undefined): string | null {
  if (href === undefined || !href.startsWith(EVIDENCE_SCHEME)) return null;
  const id = href.slice(EVIDENCE_SCHEME.length);
  return NODE_ID_PATTERN.test(id) ? id : null;
}

// Identifiants nus dans un texte : « S-01/S-02 », « (R-01, I-01) », « H-12 ».
// Les frontières \b évitent d'attraper « ZE-01 » ou « F-23 » (pas un statut).
const BARE_ID = /\b([SDOTMHRIVCPL]-\d{2,3})\b/g;

export type TextSegment = { kind: "text"; text: string } | { kind: "anchor"; id: string };

// Découpe un texte en segments texte / ancre, pour les identifiants connus
// seulement : un « L-01 » qui n'existe pas dans le graphe reste du texte.
export function splitBareIds(text: string, known: (id: string) => boolean): TextSegment[] {
  const segments: TextSegment[] = [];
  let cursor = 0;
  for (const match of text.matchAll(BARE_ID)) {
    const id = match[1];
    if (id === undefined || !known(id)) continue;
    const start = match.index;
    if (start > cursor) segments.push({ kind: "text", text: text.slice(cursor, start) });
    segments.push({ kind: "anchor", id });
    cursor = start + id.length;
  }
  if (cursor < text.length) segments.push({ kind: "text", text: text.slice(cursor) });
  return segments;
}

// Tous les identifiants ancrés dans un document (explicites et nus), sans
// doublon, dans l'ordre d'apparition — pour vérifier qu'une note ne cite pas
// un nœud absent de son graphe.
export function collectAnchoredIds(markdown: string): string[] {
  const ids = new Set<string>();
  for (const match of markdown.matchAll(/\(ev:([SDOTMHRIVCPL]-\d{2,3})\)/g)) {
    if (match[1] !== undefined) ids.add(match[1]);
  }
  for (const match of markdown.matchAll(BARE_ID)) {
    if (match[1] !== undefined) ids.add(match[1]);
  }
  return [...ids];
}
