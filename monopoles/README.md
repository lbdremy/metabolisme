# Monopoles naturels, rentes de position et collectivisation des rentes

Deuxième recherche du projet **Métabolisme**, menée avec la méthode de
**chaîne de preuves exécutable** (`../INTRO.md`). Elle part d'une question :
dans quels secteurs le prix payé par l'usager rémunère-t-il une position
plutôt qu'une production, à qui cette rente revient-elle, de combien est-elle,
et sous quelles formes institutionnelles pourrait-elle revenir à la
collectivité ? Deux mécanismes sont distingués : le monopole naturel (un
réseau qu'il est inefficace de dupliquer) et la fixité positionnelle (une
ressource que rien n'augmente).

- **Cadrage de la recherche** : [`INTRO.md`](INTRO.md) — question, approche
  matérialiste, définitions, la grille (Q1 à trois réponses, quatre
  questions, trois niveaux), légitimité des rentes (valeurs assumées),
  hypothèses directrices, inventaire avec témoins, gabarit d'étude
  sectorielle, contraintes normatives, chaîne de preuves, première phase.
- **Article de cadrage** :
  [`articles/2026-09-reconnaitre-une-rente-de-position.md`](articles/2026-09-reconnaitre-une-rente-de-position.md)
  — « Reconnaître une rente de position », réécrit après la revue
  contradictoire ; document de preuve
  [`evidence/monopoles-naturels.md`](evidence/monopoles-naturels.md).
- **Revue contradictoire** (2026-09-04 / 05, 58 objections, intégration
  complète) : [`evidence/revue-contradictoire-2026-09-04.md`](evidence/revue-contradictoire-2026-09-04.md)
  et l'annexe `evidence/revue-contradictoire-2026-09-04/`.
- **Index de la chaîne de preuves** : [`EVIDENCE.md`](EVIDENCE.md).
- **Matériau d'origine** :
  [`exploration/2026-09-grille-deux-questions-note-de-travail.md`](exploration/2026-09-grille-deux-questions-note-de-travail.md)
  (régime exploratoire, rien n'y est établi).
- **Reprise du travail** : [`NEXT-STEPS.md`](NEXT-STEPS.md) (à faire) et
  [`PREV-STEPS.md`](PREV-STEPS.md) (journal).
- **Conventions techniques** : [`CLAUDE.md`](CLAUDE.md).

## Organisation

L'étude ne calcule rien à ce stade : pas de projet Python, seulement les
registres de la méthode et les documents. Chaque **étude sectorielle**
(autoroutes, eau, hydroélectricité…) sera un projet autonome au niveau
racine du dépôt, suivant le gabarit de `INTRO.md` §9, et référencera les
définitions communes établies ici (D-01 à D-21).

```
INTRO.md                 cadrage (question, grille, hypothèses, gabarit)
EVIDENCE.md              index humain de la chaîne de preuves
sources/                 sources.yaml · definitions.yaml · hypotheses.yaml
data/raw/                fichiers sources figés (Git LFS, sha256 dans sources.yaml)
evidence/                claims.yaml (graphe) · document de preuve · revue contradictoire
articles/                l'article de cadrage
exploration/             matériau exploratoire, jamais cité comme établi
```

## Vérification

Sans code, la chaîne est contrôlée au build du site : les registres sont
dérivés en graphe, chaque référence doit se résoudre et chaque empreinte
sha256 déclarée est recalculée.

```bash
cd ../site && pnpm content      # dérive les posts (dont celui-ci)
```
