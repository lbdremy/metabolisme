# NEXT-STEPS — ce qui vient ensuite

Ce qui est déjà fait est consigné dans [`PREV-STEPS.md`](PREV-STEPS.md).
Mis à jour à chaque fin de session de travail significative.

## Prochaines étapes (dans l'ordre)

L'état à la fin de la session 1 est tagué **`efficacite-parc-v0.1`**
(chaîne complète R-01..R-05, document de preuve auto-vérifié). Le détail de
ce qui est fait est dans `PREV-STEPS.md` ; les items ci-dessous sont ce qui
reste à ouvrir.

1. **Taux d'effort territorial réel (D-09).** L'indice de coût de R-04
   n'intègre ni surface ni composition des ménages. Il faut : une source
   de surfaces habitables (enquête Logement, ou nombre de pièces des RP
   dans S-11 comme proxy), une hypothèse de logement type paramétrée
   (H-07, plage plausible), les loyers S-09 et revenus S-10 déjà figés →
   R-06 (taux d'effort à la relocation par ZE), avec la variante
   nette/brute de D-09 explicitée.
2. **Instruire H-04 (mobilités empêchées).** Données candidates :
   demandes de logement social et délais (SNE / data.gouv), taux de
   rotation du parc, DVF pour les frais de transaction. C'est la dernière
   hypothèse directrice non instruite (H-01 ✓ R-02, H-02 ✓ R-03, H-03 ✓
   R-04, H-05 = piste dominante restante).
3. **Instruire H-05 (blocages institutionnels) au niveau propriété.**
   I-03/I-04 pointent vers l'état du bâti et les successions ; données
   candidates : parc privé potentiellement indigne (PPPI, si accessible),
   DPE par territoire (ADEME open data, D-13), indivisions/successions
   (piste : stats notariales ou fichiers fonciers agrégés).
4. **Frontières de données actées** (ne pas re-tenter sans nouveau
   levier) : fichiers LOVAC détaillés = habilitation collectivités/État/
   Anah (sensibilité H-06) ; éviction saisonnière infra-territoriale =
   non tranchable en open data secrétisé (notebook 06) — leviers
   possibles : convention avec un partenaire habilité, registre des
   meublés de tourisme, monographies communales.
5. **Chemin de publication** : revue contradictoire (méthode INTRO
   étape 12 — chercher activement les objections), premier article dans
   `articles/` pointant le tag, licence du millésime loyers 2025 à
   confirmer avant publication (L-09), puis tag suivant.

## Comment reprendre (5 minutes)

```bash
cd logement
uv sync                     # env figé (uv.lock)
uv run logement validate    # registres + sha256 + graphe : doit être vert
uv run logement reproduce   # rebâtit les 5 artefacts data/processed/
./check.sh && ./test.sh     # portes qualité
```

Lire dans l'ordre : `CLAUDE.md` (doctrine + décisions arrêtées),
`EVIDENCE.md` (index humain du graphe), puis `evidence/claims.yaml`.
Le rendu du document de preuve : `QUARTO_PYTHON=.venv/bin/python quarto
render evidence/efficacite-parc-immobilier.qmd` (Quarto 1.10.18 installé).

## Pièges connus (ne pas redécouvrir)

- **LOVAC** : niveaux de vacance *totale* non comparables au travers des
  ruptures 2023/2025 (L-04) — seule la série structurelle est robuste ;
  parc privé ≠ vacance INSEE (L-06) ; secrétisation « s » < 11 (L-05) ;
  cp1252, `;`, milliers en espaces insécables ; millésimes mélangés
  (`2026` vs `_26`) normalisés à 4 chiffres par `core/lovac.py`.
- **PLM** : Paris/Lyon/Marseille arrivent par arrondissement — toujours
  agréger (le secret se propage) via `lovac.aggregate_plm`.
- **INSEE** : colonnes années suffixées « (p) » = provisoires ; libellés
  avec espaces insécables ; concept « ménage » remplacé au 31/08/2025
  (D-05 → D-06) — documenter toute jonction de séries ; la table
  d'appartenance (feuille COM) ne contient PAS les arrondissements PLM
  (feuille ARM) — toujours ramener les codes LOVAC à la commune parente
  avant jointure ; certains xlsx INSEE cassent openpyxl → moteur calamine.
- **Classements publiés** : tri stable + clé de départage explicite (les
  taux arrondis créent des ex æquo dont l'ordre varie selon la plateforme —
  attrapé par la CI, corrigé dans `build_summary`).
- **pandas** : `groupby().sum()` transforme silencieusement les NaN
  (secret) en 0 — toujours passer par `lovac.aggregate_plm` ou
  `min_count` (attrapé au notebook 06).
- **Méthode** : aucun chiffre publié sans S-xx enregistré ; les constats
  d'un notebook se vérifient depuis les sorties avant d'être écrits (une
  erreur de ce type a déjà été interceptée en session 1 — indice parc vs
  ménages).
