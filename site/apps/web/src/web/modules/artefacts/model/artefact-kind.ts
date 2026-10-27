// Les deux types d'articles du site, qui relèvent des deux disciplines de la
// méthode (« Deux disciplines, une chaîne de preuves ») : établir l'existant,
// concevoir un système métabolique.
//
// Chaque type emprunte la couleur du statut qui le porte dans le graphe : le
// résultat (R) pour la recherche, la proposition (P) pour la conception. Le
// lecteur retrouve ainsi dans la liste le code qu'il lit dans le panneau.

export type ArtefactKind = "research" | "design";

export type ArtefactKindInfo = {
  readonly label: string;
  readonly plural: string;
  readonly color: string;
  readonly discipline: string;
  readonly question: string;
  readonly carries: string;
};

export const ARTEFACT_KINDS: Readonly<Record<ArtefactKind, ArtefactKindInfo>> = {
  research: {
    label: "Recherche",
    plural: "Recherches",
    color: "var(--color-status-result)",
    discipline: "Établir l'existant",
    question: "Qu'est-ce qui est, et comment le sait-on ?",
    carries:
      "Des observations, des calculs et des résultats, reproductibles depuis les sources figées.",
  },
  design: {
    label: "Conception",
    plural: "Conception",
    color: "var(--color-status-proposal)",
    discipline: "Concevoir un système métabolique",
    question: "Qu'est-ce qui pourrait être, et est-ce que cela tiendrait ?",
    carries:
      "Des valeurs, des choix et des propositions, assumés comme tels et adossés aux faits établis.",
  },
};
