import type { NodeType } from "~/contracts/evidence";

// Vocabulaire d'affichage des statuts épistémiques (INTRO §4) et leur
// couleur dans la charte — la couleur est un jeton CSS, jamais un hex ici.

export type StatusDisplay = {
  readonly letter: string;
  readonly label: string;
  readonly plural: string;
  readonly cssVar: string;
  readonly hint: string;
};

export const STATUS: Record<NodeType, StatusDisplay> = {
  source: {
    letter: "S",
    label: "Source",
    plural: "Sources",
    cssVar: "var(--color-status-source)",
    hint: "Document, base ou fichier d'origine, figé et sommé",
  },
  definition: {
    letter: "D",
    label: "Définition",
    plural: "Définitions",
    cssVar: "var(--color-status-definition)",
    hint: "Définition statistique, juridique ou conceptuelle retenue",
  },
  observation: {
    letter: "O",
    label: "Observation",
    plural: "Observations",
    cssVar: "var(--color-status-observation)",
    hint: "Fait directement lu dans une source",
  },
  transformation: {
    letter: "T",
    label: "Transformation",
    plural: "Transformations",
    cssVar: "var(--color-status-transformation)",
    hint: "Opération appliquée aux données (code)",
  },
  measure: {
    letter: "M",
    label: "Mesure",
    plural: "Mesures",
    cssVar: "var(--color-status-measure)",
    hint: "Indicateur directement calculé",
  },
  hypothesis: {
    letter: "H",
    label: "Hypothèse",
    plural: "Hypothèses",
    cssVar: "var(--color-status-hypothesis)",
    hint: "Valeur ou relation introduite dans le modèle, avec sa plage plausible",
  },
  result: {
    letter: "R",
    label: "Résultat",
    plural: "Résultats",
    cssVar: "var(--color-status-result)",
    hint: "Sortie produite par un calcul ou un scénario",
  },
  interpretation: {
    letter: "I",
    label: "Interprétation",
    plural: "Interprétations",
    cssVar: "var(--color-status-interpretation)",
    hint: "Signification attribuée aux observations ou résultats",
  },
  value: {
    letter: "V",
    label: "Valeur",
    plural: "Valeurs",
    cssVar: "var(--color-status-value)",
    hint: "Objectif normatif ou principe défendu",
  },
  choice: {
    letter: "C",
    label: "Choix",
    plural: "Choix",
    cssVar: "var(--color-status-choice)",
    hint: "Décision de conception ou de méthode",
  },
  proposal: {
    letter: "P",
    label: "Proposition",
    plural: "Propositions",
    cssVar: "var(--color-status-proposal)",
    hint: "Système, mécanisme ou règle proposé",
  },
  limit: {
    letter: "L",
    label: "Limite",
    plural: "Limites",
    cssVar: "var(--color-status-limit)",
    hint: "Incertitude, manque de données ou restriction connue",
  },
};

// Ordre d'affichage des groupes : le sens de la chaîne (INTRO §3).
export const STATUS_ORDER: readonly NodeType[] = [
  "source",
  "definition",
  "observation",
  "transformation",
  "measure",
  "hypothesis",
  "result",
  "interpretation",
  "value",
  "choice",
  "proposal",
  "limit",
];
