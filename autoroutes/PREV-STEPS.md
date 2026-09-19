# PREV-STEPS — journal des sessions (la plus récente en premier)

## Session 1 — 2026-09-18 (ouverture, sources, première mesure, article) — AUTONOME

Consigne de Rémy : « reprend l'instruction du dossier sur la rente de
position en commençant par les autoroutes, arrête-toi après l'écriture de
l'article ». Session menée sans question intermédiaire ; les décisions
sont dans `evidence/decisions-2026-09-18.md` (DEC-01 à DEC-07). Rien n'a
été relu par Rémy ; pas de tag, pas de déploiement.

- **Ouverture** : projet `uv` (`pyproject.toml`, `check.sh`, `test.sh`,
  CI `.github/workflows/autoroutes-ci.yml`, filtre LFS, déclencheurs
  `site-ci.yml`) ; schémas pydantic étendus aux champs du cadrage
  (`statement`, `limitations`, `constructed_by`, `redistributable`) ; le
  cadrage `monopoles/` figé à son tag comme source S-01 (DEC-01).
- **Sources figées** (17, 20 fichiers, ≈ 70 Mo LFS) : ART (EGC3 2024,
  Focus rentabilité 2023, synthèse des comptes 2024, EGC1 2020), Sénat
  (commission d'enquête 2020 tome I — ce qui résout monopoles:L-12,
  l'« étude indépendante » étant l'expertise de Frédéric Fortin intégrée
  au rapport ; rapport Maurey 2024), IGF-CGEDD 2021, comptes 2023 des
  groupes ASF-Escota, Cofiroute, APRR-Area, VINCI 2023 (témoin), contrat
  ASF consolidé, Autorité de la concurrence 2014, DGITM 2020 et 2024,
  ASFA 2025. Sanef-SAPN non figé (pare-feu, trois méthodes, L-04).
  Inventaire des sources ouvertes établi par un agent (76 requêtes) puis
  vérifié et lu par l'orchestrateur.
- **Mesure** : transcription manuelle des comptes (T-01, 100 lignes avec
  source et page, rebouclage des bilans), cœur pur `core/rent.py`
  (forme D-15, forme TRI) et `core/accounts.py` (choix de base,
  d'amortissement, de prélèvements), stage `rente-d15`, 31 tests dont
  propriétés et régression. Résultat : sur les trois groupes (9,2 Md€ de
  recettes 2023), surprofit de 5,0 Md€ à 5,0 % et 4,2 Md€ à 8,8 % sur la
  base nette, 3,6 / 1,8 Md€ sur la base brute ; 6,1 / 5,1 Md€ extrapolés
  aux sept ; par la forme du régulateur, 2,6 Md€ à 5 %, 0,8 à 7 %, − 0,8 à
  8,8 % ; témoin VINCI Energies / Construction à 4-6 % du CA contre plus
  de 45 %.
- **Registres et graphe** : 9 définitions, 10 hypothèses, 58 nœuds ;
  `validate` vert ; site : post déclaré et dérivé.
- **Documents** : INTRO.md (gabarit §9), EVIDENCE.md, README, CLAUDE.md,
  document de preuve Quarto, article
  `articles/2026-09-autoroutes-la-rente-en-fin-de-contrat.md`.
- **Non fait, volontairement** (consigne) : revue contradictoire, tag,
  déploiement, notification avant l'article.
