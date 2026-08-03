# NEXT-STEPS — ce qui vient ensuite

Ce qui est déjà fait est consigné dans [`PREV-STEPS.md`](PREV-STEPS.md).
Mis à jour à chaque fin de session de travail significative.

## Prochaines étapes (dans l'ordre)

1. ~~Croisement zones d'emploi (test de H-02)~~ — **fait** (R-03/I-03,
   session 1) : H-02 confirmée en intensité, réfutée en volume — ~85 % de la
   vacance structurelle est dans des ZE où l'emploi croît. Suite logique :
   descendre à l'infra-ZE (bassins de vie, D-08) et instruire H-03 (coût)
   et H-05 (blocages institutionnels), devenues les pistes dominantes.
2. **Fichiers LOVAC détaillés (sensibilité H-06).** L'open data ne publie
   que la coupure à 2 ans ; les fichiers détaillés (ancienneté fine, accès
   Cerema/datafoncier sur demande) permettent l'analyse 1-3 ans promise par
   H-06. Vérifier les conditions d'accès/licence avant tout engagement.
3. **Définitions légales manquantes** : logement indigne (loi MOLLE 2009,
   art. 84) et passoire thermique (DPE F-G, loi Climat et résilience) —
   sourcer Légifrance, enregistrer D-12/D-13.
4. **H-03 (coût) — première brique** : loyers (observatoires locaux /
   carte des loyers MTE) et revenus (Filosofi) pour le taux d'effort
   territorial (D-09).
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
