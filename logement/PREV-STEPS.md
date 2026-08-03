# PREV-STEPS — ce qui est déjà fait

Journal des sessions de travail, la plus récente en premier. Les prochaines
étapes vivent dans [`NEXT-STEPS.md`](NEXT-STEPS.md).

## Session 1 — 2026-08-03 (fondation) — tag `efficacite-parc-v0.1`

Une **première boucle complète** de la chaîne de preuves exécutable :
sources figées → définitions verbatim → hypothèse nommée → exploration →
stabilisation testée → résultats reproductibles → document de preuve rendu.

| Élément | État en fin de session |
|---|---|
| Harnais | Projet uv autonome calqué sur le dépôt `learn` : core/shell, pydantic aux frontières, CLI clypi, `check.sh` (ruff · ty · skylos) + `test.sh` (pytest + hypothesis), CI GitHub (checkout LFS) |
| Sources (S-01..S-11) | 9 fichiers INSEE/ANIL + 4 fichiers LOVAC figés (Git LFS, sha256) + collections définitions INSEE et Légifrance |
| Définitions (D-01..D-13) | citées verbatim, datées, avec limites — liste du cadrage complète |
| Hypothèses | H-06 seuil de vacance structurelle (2 ans, plage 1-3) |
| Graphe (`evidence/claims.yaml`) | 39 nœuds — O-01..O-09, T-01..T-06, R-01..R-05, I-01..I-05, V-01, C-01..C-03, L-01..L-10 |
| Résultats reproductibles | R-01..R-05 (`data/processed/*.json`) — verrouillés par tests de régression ; document de preuve auto-vérifié couvrant les cinq |
| Notebooks d'exploration | 01 parc/ménages · 02 vacance territoriale · 03 vacance × emploi · 04 coût résidentiel · 05 résidences secondaires · 06 cumuls RS+vacance (frontière de données) |
| Document de preuve | `evidence/efficacite-parc-immobilier.qmd` + HTML rendu (auto-vérifié : artefacts publiés == recalcul) |
| Qualité | 30 tests verts ; CI verte après correction d'un vrai bug de reproductibilité (ordre des ex æquo dépendant de la plateforme, attrapé par le test de régression au premier run CI) |

- **R-05/I-05** — Les résidences secondaires n'expliquent ni la vacance ni
  le coût à l'échelle ZE (les ZE touristiques ont une vacance PLUS basse) ;
  cumul RS+vacance dans un sous-groupe corse/rural-touristique. La
  vérification a corrigé une erreur d'interprétation de R-04 (ZE
  ultramarines, pas corses).

- **Notebook 06 (frontière de données)** — dans les 12 ZE à cumul, la
  vacance est diffuse et la secrétisation rend la question de l'éviction
  saisonnière non tranchable en open data ; consignée comme frontière,
  sans R-xx (c'est la limite qui est le résultat).

### Décisions arrêtées (voir aussi `CLAUDE.md` et le graphe)

- **C-01** — vacance structurelle = convention LOVAC (> 2 ans), seuil
  paramétré H-06 (plage 1-3 ans).
- **C-02** — acquisition : national d'abord, puis LOVAC territorial.
- **C-03** — millésime de référence LOVAC pour les taux : 24 (dernier
  complet avant la rupture 2025).
- Git LFS pour tout `data/raw/` ; notebooks en Jupytext py:percent ;
  documents de preuve en Quarto.

### Corrections attrapées par la vérification (à relire avant de conclure vite)

1. Indice parc vs ménages (notebook 01) — première conclusion fausse,
   corrigée depuis les sorties.
2. Ordre des ex æquo dépendant de la plateforme (R-02) — attrapé par la CI.
3. ZE « corses » de R-04 qui étaient réunionnaises/martiniquaises —
   corrigé en vérifiant les codes, correction tracée dans le graphe.
4. NaN → 0 silencieux de pandas dans les agrégats communaux (notebook 06).

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
- **R-04/I-04** — Croisée avec le coût (loyers 2025 / Filosofi 2021) :
  anticorrélation nette (Spearman −0,42) — le coût marque la tension, il
  n'explique pas la vacance. Le cumul coût+vacance est ultramarin (La
  Réunion/Martinique, revenus faibles) — d'abord mal identifié comme
  corse, corrigé en vérifiant les codes ZE. L'exploration 05 (résidences
  secondaires, recensement 2022) écarte l'explication « saisonnière » à
  l'échelle ZE : les ZE à plus de 20 % de RS ont une vacance structurelle
  plus basse (2,6 % vs 3,3 %). La sensibilité H-06 est bloquée au niveau
  source ; D-12/D-13 complètent le registre des définitions.
