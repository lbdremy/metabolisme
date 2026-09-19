# La rente des concessions autoroutières

Première étude sectorielle du programme **Métabolisme** « Monopoles
naturels, rentes de position et collectivisation des rentes »
(`../monopoles/`), menée avec la méthode de **chaîne de preuves
exécutable** (`../INTRO.md`). Elle applique aux sept concessions
autoroutières historiques privées la rente mesurable fixée par le cadrage
(surprofit sur base d'actifs au coût historique net des subventions, avant
impôts, à plusieurs taux, avec un témoin substituable) et compare le
résultat à la mesure du régulateur.

- **Cadrage sectoriel** : [`INTRO.md`](INTRO.md) — les neuf questions du
  gabarit (objet, acteurs, flux, mesure, attribution, coût collectif,
  quatre configurations, contraintes, limites) et la chaîne de preuves.
- **Article** :
  [`articles/2026-09-autoroutes-la-rente-en-fin-de-contrat.md`](articles/2026-09-autoroutes-la-rente-en-fin-de-contrat.md) ;
  document de preuve exécutable
  [`evidence/autoroutes-rente.qmd`](evidence/autoroutes-rente.qmd).
- **Index de la chaîne de preuves** : [`EVIDENCE.md`](EVIDENCE.md).
- **Décisions de la session autonome** :
  [`evidence/decisions-2026-09-18.md`](evidence/decisions-2026-09-18.md).
- **Reprise du travail** : [`NEXT-STEPS.md`](NEXT-STEPS.md) et
  [`PREV-STEPS.md`](PREV-STEPS.md).
- **Conventions techniques** : [`CLAUDE.md`](CLAUDE.md).

## Organisation

```
INTRO.md                 cadrage sectoriel (gabarit monopoles/INTRO §9)
EVIDENCE.md              index humain de la chaîne de preuves
sources/                 sources.yaml · definitions.yaml · hypotheses.yaml
data/raw/                fichiers sources figés (Git LFS, sha256 dans sources.yaml)
data/transcribed/        comptes transcrits à la main, page par page (T-01)
data/processed/          rente-d15.json, rebâti par `reproduce`
src/autoroutes/          models.py · cli.py · core/ (registry, rent, accounts) · shell/
tests/                   pytest + hypothesis sur le cœur pur + régression
evidence/                claims.yaml (graphe) · document de preuve · journal des décisions
articles/                l'article
```

## Vérification

```bash
uv sync                          # installe l'environnement
uv run autoroutes validate       # registres + empreintes sha256
uv run autoroutes reproduce      # rebâtit data/processed/rente-d15.json
./check.sh && ./test.sh          # gates statiques · tests
cd ../site && pnpm content       # dérive le post (graphe, fichiers, empreintes)
```
