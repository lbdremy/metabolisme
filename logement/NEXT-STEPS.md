# NEXT-STEPS — ce qui vient ensuite

Ce qui est déjà fait est consigné dans [`PREV-STEPS.md`](PREV-STEPS.md).
Mis à jour à chaque fin de session de travail significative.

## Prochaines étapes (dans l'ordre)

1. ~~Croisement zones d'emploi (test de H-02)~~ — **fait** (R-03/I-03,
   session 1) : H-02 confirmée en intensité, réfutée en volume — ~85 % de la
   vacance structurelle est dans des ZE où l'emploi croît. Suite logique :
   descendre à l'infra-ZE (bassins de vie, D-08) et instruire H-03 (coût)
   et H-05 (blocages institutionnels), devenues les pistes dominantes.
2. **Sensibilité H-06 : BLOQUÉE au niveau source (vérifié 2026-08-03).**
   Les fichiers LOVAC détaillés (ancienneté fine) sont réservés aux
   collectivités à fiscalité propre, services de l'État et Anah (secret
   fiscal, Portail Données Foncières) — pas d'accès chercheur/particulier.
   L'analyse 1-3 ans promise par H-06 reste donc hors de portée ; la
   limite est actée dans la description de H-06. Alternatives possibles :
   demande de convention via un partenaire habilité, ou bornes indirectes
   depuis l'open data (vacance totale − structurelle).
3. ~~Définitions légales manquantes~~ — **fait** : D-12 habitat indigne
   (loi MOLLE 2009, art. 84) et D-13 passoire thermique (CCH L173-1-1,
   classes F-G) enregistrées depuis Légifrance (S-08), citations verbatim.
4. **H-03 (coût)** — exploration faite (notebook 04, S-09 loyers 2025 +
   S-10 Filosofi 2021) : indice de coût par ZE anticorrélé à la vacance
   (Spearman −0,42) — le coût marque la tension, il n'explique pas la
   vacance ; le cumul coût+vacance est ultramarin (La Réunion/Martinique,
   revenus faibles — d'abord mal identifié comme corse, corrigé en
   vérifiant les codes ZE). ~~Stabiliser R-04/I-04~~ — fait.
   Exploration 05 (recensement 2022, S-11) : l'axe « résidences
   secondaires » n'explique NI la vacance NI le coût à l'échelle ZE
   (ZE > 20 % RS : vacance 2,6 % vs 3,3 % ailleurs) — reste à stabiliser
   en R-05/I-05, et à descendre à l'échelle communale/AAV où l'effet peut
   exister (Porto-Vecchio : 57 % RS, 7,1 % de vacance). PUIS : un vrai
   taux d'effort territorial (D-09 : surfaces et composition des ménages).
5. Quand une nouvelle publication est prête : tag git + mise à jour du
   document de preuve (règle : l'article pointe une version précise).

## Comment reprendre (5 minutes)

```bash
cd logement
uv sync                     # env figé (uv.lock)
uv run logement validate    # registres + sha256 + graphe : doit être vert
uv run logement reproduce   # rebâtit les 2 artefacts data/processed/
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
- **Méthode** : aucun chiffre publié sans S-xx enregistré ; les constats
  d'un notebook se vérifient depuis les sorties avant d'être écrits (une
  erreur de ce type a déjà été interceptée en session 1 — indice parc vs
  ménages).
