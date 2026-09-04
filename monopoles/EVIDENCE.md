# EVIDENCE — index de la chaîne de preuves

Index humain des éléments de preuve de l'étude, par statut épistémique
(méthode Métabolisme, INTRO §4). Les registres machine font foi :
`sources/sources.yaml`, `sources/definitions.yaml`, `sources/hypotheses.yaml`,
puis `evidence/claims.yaml` pour le graphe de dépendances.

État au 2026-09-04 (cadrage) : 7 sources figées, 14 définitions,
5 hypothèses directrices et 3 paramètres, 19 nœuds de graphe ; aucun calcul. Document de preuve :
`evidence/monopoles-naturels.md` ; article :
`articles/2026-09-monopoles-naturels-grille.md`.

| Code | Statut | Registre / emplacement | État |
|------|--------|------------------------|------|
| S | Sources | `sources/sources.yaml` | S-01 glossaire OCDE 2008 · S-02 Ricardo ch. II (Wikisource, 1847) · S-03 Légifrance CCP L1121-1 · S-04 Légifrance CGCT L1411-1 / L1412-1 / L2221-1 · S-05 Légifrance CG3P L2111-1 / L3111-1 · S-06 OpenStax § 13.3 · S-07 CRE délib. 2025-77 (10 fichiers figés sha256/LFS dans `data/raw/`) |
| D | Définitions | `sources/definitions.yaml` | D-01 monopole naturel · D-02 rente économique · D-03 rente de position (construite) · D-04 rente d'innovation (construite) · D-05 substituabilité (construite) · D-06 rivalité · D-07 différenciabilité (construite) · D-08 captivité (construite) · D-09 concurrence pour / sur le marché · D-10 concession · D-11 régie · D-12 DSP · D-13 CMPC régulé · D-14 domaine public |
| H | Hypothèses | `sources/hypotheses.yaml` | H-01 décorrélation prix / coût · H-02 la mise en concurrence déplace la rente · H-03 étalon régie / délégation · H-04 seuil de bascule d'un parc régulé · H-05 coût système intégré (qualitatives, `statement`) · H-06 rémunération normale du capital 5,0 % [4 ; 8] · H-07 seuil de part faiseur de prix 35 % [30 ; 40] · H-08 écart délégation / régie 15 % [10 ; 20] |
| O | Observations | `evidence/claims.yaml` | O-01 CMPC de RTE 5,0 % (TURPE 7) / 4,6 % (TURPE 6) |
| C | Choix | `evidence/claims.yaml` | C-01 la grille · C-02 notions construites + définition mesurable de la rente · C-03 logement (parc faiseur de prix, privé conservé, trois configurations) · C-04 ordre des études |
| V | Valeurs | `evidence/claims.yaml` | V-01 la rente de position revient à l'usager · V-02 propriété d'usage non visée · V-03 rente d'innovation légitime · V-04 rente collectivisée visible |
| I | Interprétations | `evidence/claims.yaml` | I-01 classement provisoire des dix secteurs · I-02 télécoms, cas témoin |
| L | Limites | `evidence/claims.yaml` | L-01 brevets · L-02 plateformes · L-03 seuil de bascule · L-04 régimes actuels non sourcés · L-05 orbite et spectre · L-06 écart régie / délégation · L-07 traductions et notions construites · L-08 captures Légifrance |
| T/M/R/P | Transformations, mesures, résultats, propositions | — | relèvent des études sectorielles (gabarit INTRO §9) |

Sources enregistrées :

- **S-01** — OCDE, *Glossary of Statistical Terms*, 2008 (PDF, 605 p.) —
  entrées « Natural monopoly » (index 346) et « Rent - OECD » (index 452),
  reprises du glossaire Khemani & Shapiro 1993 (dont l'adresse d'origine ne
  répond plus).
- **S-02** — Ricardo, *Des principes de l'économie politique et de l'impôt*,
  ch. II « De la rente de la terre », trad. Constancio et Fonteyraud,
  Guillaumin 1847 (Wikisource, révision 6570316).
- **S-03** — Légifrance, code de la commande publique, art. L1121-1
  (version du 01/04/2019) — définition du contrat de concession.
- **S-04** — Légifrance, CGCT, art. L1411-1 (01/04/2019), L1412-1
  (03/05/2025), L2221-1 (24/02/1996) — DSP et régie.
- **S-05** — Légifrance, CG3P, art. L2111-1 et L3111-1 (01/07/2006) —
  domaine public, inaliénabilité.
- **S-06** — OpenStax, *Principles of Economics 3e*, § 13.3 « Public
  Goods » (2022, CC BY-NC-SA) — rivalité.
- **S-07** — CRE, délibération n° 2025-77 du 13 mars 2025 (TURPE 7 HTB) —
  CMPC reconnu 5,0 % nominal avant impôts.

Les pages Légifrance et OpenStax sont des captures de navigateur (DOM
rendu), pas des téléchargements par script : voir L-08 et l'en-tête de
`sources/sources.yaml`.

Matériau exploratoire (jamais cité comme établi) :

- `exploration/2026-09-grille-deux-questions-note-de-travail.md` — la note
  de travail d'origine, avec en préambule les divergences relevées contre
  les sources figées du dépôt.
