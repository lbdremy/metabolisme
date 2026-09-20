import type { Note } from "./publication.ts";

// Sélection pure d'un RECUEIL de notes.
//
// Un recueil ne change pas le régime des notes : chacune garde son jeton, son
// noindex et son absence de l'accueil. Il donne seulement au site de quoi
// servir un sommaire à une adresse unique. L'ordre est celui que le recueil
// déclare (`position`), pas celui des dates : ces notes sont écrites pour être
// lues dans un ordre.

export type CollectedNote<T> = { readonly token: string; readonly note: Note } & T;

export function selectCollection<T extends { readonly token: string; readonly note: Note }>(
  notes: ReadonlyArray<T>,
  collection: string,
): T[] {
  return notes
    .filter((entry) => entry.note.collection?.slug === collection)
    .toSorted((a, b) => (a.note.collection?.position ?? 0) - (b.note.collection?.position ?? 0));
}
