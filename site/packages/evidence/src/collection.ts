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
