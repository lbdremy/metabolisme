# Efficacité du parc immobilier français

Première recherche du projet **Métabolisme**, menée avec la méthode de
**chaîne de preuves exécutable** : sources identifiées et figées, définitions
explicites, hypothèses paramétrées, calculs codés et testés, résultats
reproductibles.

- **Cadrage de la recherche** : [`INTRO.md`](INTRO.md) — question, axiome
  normatif (une résidence principale occupée n'est jamais une inefficience),
  hypothèses directrices, dimensions d'analyse, livrables.
- **Index de la chaîne de preuves** : [`EVIDENCE.md`](EVIDENCE.md).
- **Conventions techniques** : [`CLAUDE.md`](CLAUDE.md).

## Reproduction

```bash
uv sync --locked            # environnement figé (uv.lock)
./test.sh                   # tests (pytest + hypothesis)
uv run logement validate    # contrôle des registres (sources, définitions, hypothèses)
uv run logement reproduce   # rejoue la chaîne stabilisée (encore vide à ce stade)
```
