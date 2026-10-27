// Typographie française à l'affichage : l'espace avant « ; : ? ! » et
// après « « », avant « » » devient insécable, pour que la ponctuation ne
// tombe jamais seule en début de ligne. Le texte source n'est pas modifié.
const BEFORE = / ([;:?!»])/g;
const AFTER = /« /g;

export function frenchSpacing(text: string): string {
  return text.replace(BEFORE, " $1").replace(AFTER, "« ");
}
