# PREV-STEPS — ce qui est déjà fait

Journal des sessions de travail, la plus récente en premier. Les prochaines
étapes vivent dans [`NEXT-STEPS.md`](NEXT-STEPS.md).

## Session 1 — 2026-09-04 (ouverture, cadrage, sources, article)

Point de départ : la note de travail « La grille des deux questions —
collectiviser la rente là où le marché n'existe pas » (Rémy, septembre
2026), un texte doctrinal sur dix secteurs, non sourcé hors logement.

### Ouverture et cadrage (commit `df40c51`)

- **Lecture critique contre le dépôt.** Les chiffres logement de la note
  confrontés aux sources figées de l'étude `logement/` et de la note privée
  sur la fonction régulatrice du parc social : six divergences relevées
  (Vienne 60 % contre ~50 % ; « 80 % au plafond en zone tendue » contre
  17 % / 50 % à ≥ 98 % / 62 % en zone A dans le Panorama Ancols 2025
  p. 40 ; Paris 27,8 € contre 25,5 / 27,2 € OLAP ; « un tiers à 40 % »
  contre un tiers / 43 % ; prix ×2,3 / ×2,6, 3,5 %, 58 % sans source
  figée ; contradiction interne ICC / inflation). Tension interne relevée :
  « allocation administrée » (tableau) contre parc faiseur de prix avec
  privé conservé (proposition).
- **Décisions de Rémy** (AskUserQuestion) : étude `monopoles/` en
  registres + article, sans Python ; logement = parc faiseur de prix,
  privé conservé, trois configurations comparées ; article de cadrage
  limité au cadrage, mise en œuvre et tactique renvoyées à un article
  ultérieur.
- **Cadrage écrit** (`INTRO.md`) : question en cinq temps ; ce que
  l'approche matérialiste impose ; quatorze définitions à figer ; la grille
  passée de deux à quatre questions (captivité Q3 ajoutée, Q4 « qui
  exploite » isolé comme choix de gestion) plus l'entrée empirique Q5 ; la
  part normative isolée (V-01..V-04) ; H-01..H-05 directrices, H-06..H-08
  paramètres ; inventaire des dix secteurs comme hypothèses, ligne logement
  corrigée ; gabarit sectoriel en neuf questions ; ordre des études ;
  contraintes normatives ; risques ; chaîne initiale ; première phase.
- **Scaffold** : README, CLAUDE.md, EVIDENCE.md, registres vides, NEXT/PREV
  -STEPS, note d'origine archivée dans `exploration/` avec ses divergences
  en préambule ; LFS ; arborescence du `CLAUDE.md` racine.

### Sources, définitions, graphe, article

- **Sept sources figées** (`data/raw/`, sha256, LFS). Le glossaire OCDE de
  1993 n'est plus servi (HTTP 410) : remplacé par l'édition 2008 du
  glossaire statistique de l'OCDE, qui reprend ses entrées « Natural
  monopoly » (index PDF 346) et « Rent - OECD » (index 452), y compris la
  quasi-rente. Ricardo ch. II pris sur Wikisource (trad. Guillaumin 1847,
  révision 6570316). Légifrance est derrière un défi anti-robot (Cloudflare)
  qui bloque `curl` et le navigateur headless : captures du DOM rendu par
  un Chromium fenêtré (`agent-browser --headed`), une relance du navigateur
  par page (seule la première navigation passe le défi) — CCP L1121-1, CGCT
  L1411-1 / L1412-1 / L2221-1, CG3P L2111-1 / L3111-1, avec la date de
  version de chaque article ; limite L-08 (empreintes non reproductibles par
  script). OpenStax § 13.3 (CC BY-NC-SA) pour la rivalité, faute d'entrée
  OCDE (vérifié : pas de « public good », « switching cost », « franchise
  bidding » dans le glossaire). CRE délibération 2025-77 (TURPE 7 HTB) pour
  le CMPC reconnu : 5,0 % nominal avant impôts (4,6 % au TURPE 6). Demsetz
  1968 non enregistré (accès payant).
- **Quatorze définitions** (D-01..D-14) : verbatim pour les officielles
  (anglais pour OCDE et OpenStax, traduction de travail en limite L-07) ;
  cinq notions construites (rente de position, rente d'innovation,
  substituabilité, différenciabilité, captivité) rattachées à C-02 et à
  leur source d'ancrage. **Définition mesurable de la rente** fixée dans
  C-02 : prix payé moins coût d'une fourniture efficace, rémunération du
  capital au taux H-06 comprise.
- **Trois paramètres** : H-06 `normal_return_on_capital` 5,0 % [4 ; 8]
  (O-01, D-13) ; H-07 `price_maker_share_threshold` 35 % [30 ; 40],
  confiance faible (L-03) ; H-08 `water_delegation_cost_gap` 15 % [10 ; 20],
  confiance faible (L-06).
- **Graphe** (`evidence/claims.yaml`) : O-01, C-01..C-04, V-01..V-04,
  I-01..I-02, L-01..L-08. Validation indépendante avec les schémas
  pydantic de `logement` (mêmes formats) : 43 identifiants, références
  résolues, empreintes vérifiées, aucune erreur.
- **Article de cadrage** `articles/2026-09-monopoles-naturels-grille.md`
  (« Là où le marché n'existe pas ») : la question en cinq plans ; ce qu'est
  un monopole naturel (la définition dit qui doit produire, pas qui doit
  posséder) ; deux rentes ; la rente mesurable et H-06 ; la grille (Q1-Q5,
  trois niveaux) ; la part normative (V-01..V-04) ; l'inventaire comme
  hypothèses avec les trois lignes commentées (télécoms, logement, orbite) ;
  le gabarit et les trois configurations ; objections examinées en registre
  de recherche ; ce que ces pages ne disent pas ; reproduction. Aucun
  chiffre non figé (les chiffres logement de la note écartés et dits tels).
  Document de preuve `evidence/monopoles-naturels.md` (INTRO §11, sans
  calcul, avec les données écartées et pourquoi).
- **Site** : post déclaré (`site/content/posts/2026-09-monopoles-naturels-grille/post.yaml`,
  sans tag pour l'instant), `pnpm content` → 43 nœuds, 10 fichiers en
  assets ; tests, lint, format, types et build verts ; déclencheurs
  `monopoles/**` ajoutés à `site-ci.yml` ; note dans `site/CLAUDE.md`.
- Non fait, volontairement : tag et déploiement (relecture de Rémy
  d'abord) ; revue contradictoire ; extension du contrat du site aux
  hypothèses qualitatives (H-01..H-05 restent hors graphe).
