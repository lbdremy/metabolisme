# EVIDENCE — index de la chaîne de preuves

Index humain des éléments de preuve de l'étude, par statut épistémique
(méthode Métabolisme, INTRO §4). Les registres machine font foi :
`sources/sources.yaml`, `sources/definitions.yaml`, `sources/hypotheses.yaml`,
puis `evidence/claims.yaml` pour le graphe de dépendances.

| Code | Statut | Registre / emplacement | État |
|------|--------|------------------------|------|
| S | Sources | `sources/sources.yaml` | 4 sources INSEE (3 fichiers figés sha256 + la collection des définitions) |
| D | Définitions | `sources/definitions.yaml` | 9 définitions INSEE citées verbatim, datées, avec limites |
| H | Hypothèses | `sources/hypotheses.yaml` | vide |
| O/T/M/R | Observations, transformations, mesures, résultats | `src/logement/` + `evidence/claims.yaml` | aucune chaîne stabilisée |
| I/V/C/P/L | Interprétations, valeurs, choix, propositions, limites | documents de preuve (`evidence/*.qmd`) | à venir |

Sources enregistrées :

- **S-01** — INSEE, Parc de logements au 1ᵉʳ janvier 2025 (Insee Focus n° 359,
  données des figures — EAPL, séries nationales 1982-2025).
- **S-02** — INSEE, Répartition du parc selon la catégorie de logement et le
  type d'habitat (chiffres détaillés EAPL, 1982-2025).
- **S-03** — INSEE, Ménages en séries longues (SL_MEN1, recensement,
  millésimes 1962-2022).
- **S-04** — INSEE, Définitions (métadonnées statistiques, collection en
  ligne — chaque définition citée verbatim et datée dans le registre).

Définitions enregistrées : D-01 logement · D-02 résidence principale ·
D-03 logement vacant · D-04 résidence secondaire · D-05 ménage (recensement,
concept remplacé le 31/08/2025) · D-06 ménage-logement · D-07 zone d'emploi ·
D-08 bassin de vie · D-09 taux d'effort. Restent à sourcer : vacance
frictionnelle/durable, logement indigne, passoire thermique (définitions
légales, hors INSEE).

Valeur normative déjà posée par le cadrage (`INTRO.md` §3) :

- **V-01** — Une résidence principale occupée est pleinement utilisée ; elle ne
  peut jamais être comptée comme capacité disponible ni comme inefficience.

Choix de conception arrêtés (2026-08-03) :

- **C-01** — La distinction vacance frictionnelle / vacance durable adopte la
  convention administrative « vacance structurelle = plus de 2 ans » (LOVAC /
  Zéro Logement Vacant), à enregistrer comme D-10 lors de l'acquisition de
  LOVAC ; le seuil sera paramétré comme hypothèse (plage plausible 1 à 3 ans)
  pour rendre visible la sensibilité des résultats.
- **C-02** — Ordre d'acquisition : séries nationales d'abord (S-01..S-03),
  puis LOVAC pour l'analyse territoriale.

Aucun résultat n'a encore été produit : ce fichier s'enrichit à mesure que des
éléments passent du régime exploratoire au régime stabilisé.
