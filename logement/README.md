# Efficacité du parc immobilier français

Première recherche du projet **Métabolisme**, menée avec la méthode de
**chaîne de preuves exécutable** : sources identifiées et figées, définitions
explicites, hypothèses paramétrées, calculs codés et testés, résultats
reproductibles.

- **Cadrage de la recherche** : [`INTRO.md`](INTRO.md) — question, axiome
  normatif (une résidence principale occupée n'est jamais une inefficience),
  hypothèses directrices, dimensions d'analyse, livrables.
- **Index de la chaîne de preuves** : [`EVIDENCE.md`](EVIDENCE.md).
- **Articles** :
  [`articles/2026-08-efficacite-parc-etat-des-preuves.md`](articles/2026-08-efficacite-parc-etat-des-preuves.md)
  — « Le parc immobilier français, au bord du compte », l'état des preuves
  au tag `efficacite-parc-v0.5` ;
  [`articles/2026-09-proposition-institutionnelle.md`](articles/2026-09-proposition-institutionnelle.md)
  — « Détendre le parc, au prix du marché », la proposition institutionnelle
  au tag `efficacite-parc-v0.6` (cinq mécanismes comparés, revue
  contradictoire, journal des décisions
  [`evidence/decisions-2026-09-18.md`](evidence/decisions-2026-09-18.md)).
- **Conventions techniques** : [`CLAUDE.md`](CLAUDE.md).

## Reproduction

```bash
uv sync --locked            # environnement figé (uv.lock)
./test.sh                   # tests (pytest + hypothesis)
uv run logement validate    # contrôle des registres (sources, définitions, hypothèses)
uv run logement reproduce   # rejoue la chaîne stabilisée (15 stages)
```
