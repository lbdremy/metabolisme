# PREV-STEPS — ce qui est déjà fait

Journal des sessions de travail, la plus récente en premier. Les prochaines
étapes vivent dans [`NEXT-STEPS.md`](NEXT-STEPS.md).

## Session 2 — 2026-09-04 / 05 (revue contradictoire du cadrage et intégration complète)

Rémy a demandé, après lecture du cadrage : garder le titre et la section
d'objections (point 1), faire entrer les hypothèses qualitatives dans le
graphe (point 2), mener la revue contradictoire (point 3).

- **Contrat du site étendu aux hypothèses qualitatives** (commit
  `59d021f`) : `statement` sans triplet numérique dans
  `packages/evidence`, rejet d'un paramètre incomplet dans
  `study-to-graph`, corps du panneau sans jauge, tests ; H-01..H-05
  enregistrées ; post à 48 nœuds.
- **Revue contradictoire** (méthode `logement`) : quatre relecteurs
  indépendants — sources alternatives (mandat réduit après une
  interruption par la limite de dépense : SA-1..SA-7), définitions et
  hypothèses (HD-1..HD-12), scénarios d'échec (SE-1..SE-22), cohérence et
  statuts épistémiques (CR-1..CR-17) — 58 objections, 7 bloquantes.
  Vérifications de l'orchestrateur avant triage (index OCDE, V-01
  orpheline, coupe de D-04, formule D-13, empreintes non vérifiées,
  chiffres privés dans H-04/H-07, dix « non » à Q1, Sénat 6,5 → 5,9 %,
  proposition de loi hydro) : toutes confirmées. Synthèse de triage et
  rapports bruts commités en annexe AVANT intégration (commit `b173008`).
- **Décisions de Rémy** (AskUserQuestion, 2026-09-05) : monopoles naturels
  ET rentes de position (logement et stationnement reclassés) ; les deux
  destinations de la rente, explicites par secteur ; nouveau titre neutre ;
  intégration complète.
- **Intégration** : D-05 scindée (non-duplicabilité D-05, fixité D-16),
  Q1 à trois réponses, deux lignes témoins (mobiles, fibre en zone très
  dense), objet classé sur chaque ligne, Q2 sans « nécessairement
  administré » ; **D-15 rente mesurable** (base d'actifs au coût
  historique net des subventions, coût efficace L. 341-2, postes, avant
  impôts, témoin) et D-17..D-21 (exclusion, envergure, coûts
  irrécupérables, barrières, BAR) ; D-04 citation complète et statut de
  construction assumé ; D-13 sans valeur, formule complète ; index OCDE
  corrigés (353 / 462) ; H-01 réécrite (périmètre prix non administré,
  test D-15 avec témoin, réfutation), H-03 scindée, H-04 sur l'ouverture,
  H-05 question de recherche, H-06 « taux de référence » [4,0 ; 8,8]
  sourcé, H-07 qualitative sans valeur, H-08 écart brut [0 ; 27] ;
  H-09..H-20 hypothèses de classement ; V-01 principe, V-05 destination,
  V-06 continuité, V-03 réduite ; C-03 logement hors grille (4
  configurations), C-05 quatre configurations ; I-02 « cas à instruire »,
  I-03 attribution avec témoin ; L-09..L-12 ; dépendances remises dans le
  bon sens (`justification` S/O/I, `limitations`, `constructed_by`).
- **Neuf sources figées** : ART EGC 2024 (S-08, 13,8 Mo), ARCEP 2025-2047
  via sa publication au JORF sur Légifrance (S-09 ; le PDF de l'ARCEP est
  derrière un pare-feu qui rejette script, navigateur automatisé et service
  de lecture), Eaufrance (S-10), Persée / Carpentier et al. 2006 (S-11),
  Sénat n° 709 p. 130 (S-12), FIPECO (S-13, secondaire), IGEDD tunnel de
  Friggit (S-14), Sénat n° 498 PPL hydro (S-15), glossaire ART (S-16) ;
  neuf observations O-01..O-09. Licences reformulées ; PDF OCDE
  `redistributable: false`.
- **Site** : `build-posts` recalcule les empreintes sha256 et échoue sur
  un écart ; `study-to-graph` porte `constructed_by`, `redistributable`
  (fichier non servi) et `limitations` des hypothèses ; 12 tests ; post
  à 92 nœuds, 18 fichiers servis, aucun identifiant cité absent du
  graphe.
- **Documents** : INTRO.md réécrit ; article réécrit sous le titre
  « Reconnaître une rente de position »
  (`articles/2026-09-reconnaitre-une-rente-de-position.md`, l'ancien
  fichier retiré) ; document de preuve ; EVIDENCE, README, CLAUDE.md ;
  compte rendu `evidence/revue-contradictoire-2026-09-04.md` avec
  dispositions et tableau avant / après.
- Non fait, volontairement : tag et déploiement (relecture de Rémy de la
  version révisée) ; loi hydro promulguée et étude TRI d'origine (L-12).

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
- **Cadrage écrit** (`INTRO.md`), **scaffold** (README, CLAUDE.md,
  EVIDENCE.md, registres vides, NEXT/PREV-STEPS, note d'origine archivée
  dans `exploration/` avec ses divergences en préambule ; LFS ;
  arborescence du `CLAUDE.md` racine).

### Sources, définitions, graphe, article (commit `3efce86`)

- **Sept sources figées** (glossaire OCDE 2008 à la place du glossaire
  1993 plus servi ; Ricardo sur Wikisource ; six articles Légifrance
  capturés en DOM rendu par un Chromium fenêtré, une relance par page ;
  OpenStax ; CRE 2025-77). Demsetz 1968 non enregistré.
- **Quatorze définitions**, trois paramètres (H-06 5,0 % [4 ; 8], H-07
  35 % [30 ; 40], H-08 15 % [10 ; 20]), dix-neuf nœuds ; validation avec
  les schémas pydantic de `logement`.
- **Article** « Là où le marché n'existe pas » et document de preuve ;
  post déclaré et construit (43 nœuds), non tagué.
