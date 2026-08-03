# HANDOFF — reprendre l'étude logement

État au **2026-08-03** (session de fondation). Ce fichier dit où en est
l'étude et quoi faire ensuite ; il se met à jour à chaque fin de session de
travail significative.

## Où on en est

Une **première boucle complète** de la chaîne de preuves exécutable est
faite : sources figées → définitions verbatim → hypothèse nommée →
exploration → stabilisation testée → résultats reproductibles → document de
preuve rendu.

| Élément | État |
|---|---|
| Sources (S-01..S-05) | 3 fichiers INSEE + 4 fichiers LOVAC figés (Git LFS, sha256 vérifiés par `validate`) + collection définitions INSEE |
| Définitions (D-01..D-11) | citées verbatim, datées ; manquent : logement indigne, passoire thermique (légales, hors INSEE) |
| Hypothèses | H-01 seuil de vacance structurelle (2 ans, plage 1-3) |
| Graphe (`evidence/claims.yaml`) | 21 nœuds — O-01..O-04, T-01..T-03, R-01/R-02, I-01/I-02, V-01, C-01..C-03, L-01..L-06 |
| Résultats reproductibles | R-01 `data/processed/parc-menages.json`, R-02 `data/processed/vacance-structurelle.json` — verrouillés par tests de régression |
| Notebooks d'exploration | 01 parc/ménages, 02 vacance territoriale (py:percent, committés) |
| Document de preuve | `evidence/efficacite-parc-immobilier.qmd` + HTML rendu (auto-vérifié : artefacts publiés == recalcul) |
| Qualité | `./check.sh` + `./test.sh` (30 tests) verts ; CI `.github/workflows/logement-ci.yml` (checkout LFS) |

## Ce que disent les premiers résultats (résumé d'une phrase chacun)

- **R-01/I-01** — Sur 40 ans le parc suit les ménages (décohabitation), pas
  la population ; depuis ~2006 le parc croît plus vite et l'écart part en
  vacance (7,7 % en 2025, ~3,0 M).
- **R-02/I-02** — La vacance structurelle du parc privé est ~1,15 M de
  logements (3,5 % du parc privé), robuste aux ruptures LOVAC, avec un
  gradient territorial d'un ordre de grandeur : intensité rurale/DOM vs
  volume urbain — premier indice pour H-02.

## Prochaines étapes (dans l'ordre)

1. **Croisement zones d'emploi (test de H-02).** Acquérir le zonage
   ZE 2020 (INSEE, table d'appartenance communes → ZE) + un jeu
   emploi/tension par ZE ; agréger la vacance structurelle LOVAC par ZE et
   la confronter à la dynamique d'emploi. C'est l'étape qui transforme
   « premier indice » en résultat.
   Attention : codes commune LOVAC au COG 2026, zonage ZE sur un COG
   antérieur — prévoir la table de passage (et documenter T-xx).
2. **Fichiers LOVAC détaillés (sensibilité H-01).** L'open data ne publie
   que la coupure à 2 ans ; les fichiers détaillés (ancienneté fine, accès
   Cerema/datafoncier sur demande) permettent l'analyse 1-3 ans promise par
   H-01. Vérifier les conditions d'accès/licence avant tout engagement.
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
  (D-05 → D-06) — documenter toute jonction de séries.
- **Méthode** : aucun chiffre publié sans S-xx enregistré ; les constats
  d'un notebook se vérifient depuis les sorties avant d'être écrits (une
  erreur de ce type a déjà été interceptée en session 1 — indice parc vs
  ménages).
