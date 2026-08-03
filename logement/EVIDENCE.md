# EVIDENCE — index de la chaîne de preuves

Index humain des éléments de preuve de l'étude, par statut épistémique
(méthode Métabolisme, INTRO §4). Les registres machine font foi :
`sources/sources.yaml`, `sources/definitions.yaml`, `sources/hypotheses.yaml`,
puis `evidence/claims.yaml` pour le graphe de dépendances.

| Code | Statut | Registre / emplacement | État |
|------|--------|------------------------|------|
| S | Sources | `sources/sources.yaml` | 5 sources (INSEE + LOVAC ; 7 fichiers figés sha256/LFS + la collection des définitions) |
| D | Définitions | `sources/definitions.yaml` | 11 définitions citées verbatim, datées, avec limites |
| H | Hypothèses | `sources/hypotheses.yaml` | H-06 seuil de vacance structurelle (2 ans, plage 1-3) |
| O/T/R | Observations, transformations, résultats | `evidence/claims.yaml` | O-01..O-04, T-01..T-03, R-01/R-02 (sorties dans `data/processed/`) |
| I/V/C/L | Interprétations, valeurs, choix, limites | `evidence/claims.yaml` | I-01/I-02, V-01, C-01..C-03, L-01..L-06 |
| M/P | Mesures, propositions | — | à venir |

Sources enregistrées :

- **S-01** — INSEE, Parc de logements au 1ᵉʳ janvier 2025 (Insee Focus n° 359,
  données des figures — EAPL, séries nationales 1982-2025).
- **S-02** — INSEE, Répartition du parc selon la catégorie de logement et le
  type d'habitat (chiffres détaillés EAPL, 1982-2025).
- **S-03** — INSEE, Ménages en séries longues (SL_MEN1, recensement,
  millésimes 1962-2022).
- **S-04** — INSEE, Définitions (métadonnées statistiques, collection en
  ligne — chaque définition citée verbatim et datée dans le registre).
- **S-05** — Ministère de la Transition écologique (DGALN/Cerema), LOVAC open
  data — logements vacants du parc privé par territoire et durée, millésimes
  2020-2026 (4 fichiers figés ; ruptures méthodologiques 2023 et 2025
  documentées ; parc privé uniquement, secrétisation < 11).

Définitions enregistrées : D-01 logement · D-02 résidence principale ·
D-03 logement vacant · D-04 résidence secondaire · D-05 ménage (recensement,
concept remplacé le 31/08/2025) · D-06 ménage-logement · D-07 zone d'emploi ·
D-08 bassin de vie · D-09 taux d'effort · D-10 vacance structurelle (LOVAC,
> 2 ans) · D-11 vacance frictionnelle (LOVAC, ≤ 2 ans). Restent à sourcer :
logement indigne, passoire thermique (définitions légales, hors INSEE).

Hypothèses : **H-06** — seuil de vacance structurelle, valeur centrale 2 ans
(convention C-01), plage plausible 1-3 ans (sensibilité complète possible
seulement avec les fichiers LOVAC détaillés).

Valeur normative déjà posée par le cadrage (`INTRO.md` §3) :

- **V-01** — Une résidence principale occupée est pleinement utilisée ; elle ne
  peut jamais être comptée comme capacité disponible ni comme inefficience.

Choix de conception arrêtés (2026-08-03) — désormais dans le graphe
(`evidence/claims.yaml`) : **C-01** (convention de vacance structurelle > 2 ans,
seuil paramétré 1-3 ans), **C-02** (national d'abord, puis LOVAC).

Résultats stabilisés (2026-08-03) :

- **R-02** — Vacance structurelle du parc privé (sortie reproductible
  `data/processed/vacance-structurelle.json`) : ~1,18 M de logements
  (millésime 26), taux national 3,5 % (millésime 24, choix C-03), gradient
  départemental d'un ordre de grandeur (DOM et diagonale des faibles
  densités vs zones tendues). Lecture : **I-02** — deux régimes distincts,
  intensité rurale/ultramarine vs volume urbain, premier indice cohérent
  avec H-02. Limites L-04 (ruptures 2023/2025), L-05 (secrétisation),
  L-06 (parc privé ≠ INSEE).

- **R-01** — Comparaison parc / ménages / population 1982-2025 (sortie
  reproductible `data/processed/parc-menages.json`, rebâtie par
  `uv run logement reproduce`, verrouillée par le test de régression
  `tests/test_reproduce.py`). Lecture : **I-01** — le parc suit les ménages
  (décohabitation), régime inversé vers 2005-2006, la remontée de la capacité
  hors résidence principale depuis 2006 est de la vacance. Limites L-01..L-03
  (national seulement, 2023-2025 provisoires, écart conceptuel ménage/RP).
