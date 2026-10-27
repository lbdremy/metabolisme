import type { Note, PublicationStatus } from "./publication.ts";

// Sélection pure d'un RECUEIL de notes, et du recueil des articles de
// conception.
//
// L'ordre est celui que le recueil déclare (`position`), pas celui des
// dates : ces notes sont écrites pour être lues dans un ordre.

export type CollectedNote<T> = { readonly token: string; readonly note: Note } & T;

export function selectCollection<T extends { readonly token: string; readonly note: Note }>(
  notes: ReadonlyArray<T>,
  collection: string,
): T[] {
  return notes
    .filter((entry) => entry.note.collection?.slug === collection)
    .toSorted((a, b) => (a.note.collection?.position ?? 0) - (b.note.collection?.position ?? 0));
}

// Le recueil des ARTICLES DE CONCEPTION — l'autre type d'artefact du site,
// à côté des articles de recherche (les posts).
export const CONCEPTION_COLLECTION = "conception";

export function isConception(note: Note): boolean {
  return note.collection?.slug === CONCEPTION_COLLECTION;
}

// Un article de conception sans statut est en relecture : il ne devient
// public que si note.yaml le dit.
export function conceptionStatus(note: Note): PublicationStatus {
  return note.status ?? "in_review";
}

export function isPublishedConception(note: Note): boolean {
  return isConception(note) && conceptionStatus(note) === "published";
}

// Les articles de conception d'un statut donné, dans l'ordre de lecture.
export function selectConception<T extends { readonly token: string; readonly note: Note }>(
  notes: ReadonlyArray<T>,
  status: PublicationStatus,
): T[] {
  return selectCollection(notes, CONCEPTION_COLLECTION).filter(
    (entry) => conceptionStatus(entry.note) === status,
  );
}

// Le slug lisible d'un article de conception : `public_slug` s'il est
// donné, le slug du dossier sinon.
export function conceptionSlug(note: Note): string {
  return note.public_slug ?? note.slug;
}

// L'adresse canonique d'une note. Un article de conception PUBLIÉ est
// durable : il a une adresse lisible, et son jeton y redirige. Tout le reste
// — conception en relecture, note isolée — n'a que son jeton.
export function notePath(entry: { readonly token: string; readonly note: Note }): string {
  return isPublishedConception(entry.note)
    ? `/conception/${conceptionSlug(entry.note)}`
    : `/notes/${entry.token}`;
}

// Deux articles de conception ne peuvent pas revendiquer la même adresse
// lisible : le build refuse, plutôt que de servir l'un à la place de l'autre.
export function duplicateConceptionSlugs(notes: ReadonlyArray<Note>): string[] {
  const seen = new Map<string, number>();
  for (const note of notes) {
    if (!isConception(note)) continue;
    const slug = conceptionSlug(note);
    seen.set(slug, (seen.get(slug) ?? 0) + 1);
  }
  return [...seen]
    .filter(([, count]) => count > 1)
    .map(([slug]) => slug)
    .toSorted();
}
