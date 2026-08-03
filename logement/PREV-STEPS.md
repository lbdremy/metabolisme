# PREV-STEPS — ce qui est déjà fait

Journal des sessions de travail, la plus récente en premier. Les prochaines
étapes vivent dans [`NEXT-STEPS.md`](NEXT-STEPS.md).

## Session 1 — 2026-08-03 (fondation)

Une **première boucle complète** de la chaîne de preuves exécutable :
sources figées → définitions verbatim → hypothèse nommée → exploration →
stabilisation testée → résultats reproductibles → document de preuve rendu.

| Élément | État en fin de session |
|---|---|
| Harnais | Projet uv autonome calqué sur le dépôt `learn` : core/shell, pydantic aux frontières, CLI clypi, `check.sh` (ruff · ty · skylos) + `test.sh` (pytest + hypothesis), CI GitHub (checkout LFS) |
| Sources (S-01..S-07) | 5 fichiers INSEE + 4 fichiers LOVAC figés (Git LFS, sha256 vérifiés par `validate`) + collection définitions INSEE |
| Définitions (D-01..D-11) | citées verbatim, datées, avec limites |
| Hypothèses | H-06 seuil de vacance structurelle (2 ans, plage 1-3) |
| Graphe (`evidence/claims.yaml`) | 28 nœuds — O-01..O-06, T-01..T-04, R-01..R-03, I-01..I-03, V-01, C-01..C-03, L-01..L-08 |
| Résultats reproductibles | R-01 parc-menages, R-02 vacance-structurelle, R-03 vacance-emploi-ze (`data/processed/*.json`) — verrouillés par tests de régression |
| Notebooks d'exploration | 01 parc/ménages, 02 vacance territoriale, 03 vacance × emploi (py:percent, committés) |
| Document de preuve | `evidence/efficacite-parc-immobilier.qmd` + HTML rendu (auto-vérifié : artefacts publiés == recalcul) |
| Qualité | 30 tests verts ; CI verte après correction d'un vrai bug de reproductibilité (ordre des ex æquo dépendant de la plateforme, attrapé par le test de régression au premier run CI) |

### Décisions arrêtées (voir aussi `CLAUDE.md` et le graphe)

- **C-01** — vacance structurelle = convention LOVAC (> 2 ans), seuil
  paramétré H-06 (plage 1-3 ans).
- **C-02** — acquisition : national d'abord, puis LOVAC territorial.
- **C-03** — millésime de référence LOVAC pour les taux : 24 (dernier
  complet avant la rupture 2025).
- Git LFS pour tout `data/raw/` ; notebooks en Jupytext py:percent ;
  documents de preuve en Quarto.

### Ce que disent les premiers résultats

- **R-01/I-01** — Sur 40 ans le parc suit les ménages (décohabitation),
  pas la population ; depuis ~2006 le parc croît plus vite et l'écart part
  en vacance (7,7 % en 2025, ~3,0 M).
- **R-02/I-02** — La vacance structurelle du parc privé est ~1,15 M de
  logements (3,5 % du parc privé), robuste aux ruptures LOVAC, avec un
  gradient territorial d'un ordre de grandeur : intensité rurale/DOM vs
  volume urbain — premier indice pour H-02.
- **R-03/I-03** — Croisée avec l'emploi par zone d'emploi (1998-2018) :
  H-02 confirmée en intensité (Spearman −0,36 ; taux médian 4,5 % dans les
  ZE déclinantes vs 2,9 %) mais réfutée en volume — ~85 % de la vacance
  structurelle est dans des ZE où l'emploi croît (Paris 69,8 k en tête).
  Les causes de blocage dominantes sont donc ailleurs → H-03/H-05.
