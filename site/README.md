# Site Métabolisme

Le site public du programme **Métabolisme** : des articles d'étude et des notes
partageables, chacun accompagné de sa **chaîne de preuves explorable** — chaque
chiffre du texte renvoie à un nœud (source, définition, observation, calcul,
hypothèse, résultat, interprétation, limite), et le lecteur remonte de
dépendance en dépendance jusqu'aux fichiers sources figés.

> Architecture, doctrine et décisions techniques : [`CLAUDE.md`](./CLAUDE.md).
> La méthode de recherche elle-même : [`../INTRO.md`](../INTRO.md).

## Deux objets publiés

| Objet    | URL              | Contenu                                                                    | Chaîne de preuves                                                           |
| -------- | ---------------- | -------------------------------------------------------------------------- | --------------------------------------------------------------------------- |
| **Post** | `/posts/<slug>`  | Un article d'étude (`logement/articles/…`), long, sur une question ouverte | Dérivée des registres de l'étude (sources, définitions, hypothèses, claims) |
| **Note** | `/notes/<jeton>` | Un message court et sourcé, partagé par lien, jamais listé ni indexé       | Écrite à la main (`evidence.yaml`), souvent courte : un chiffre, sa page    |

Dans les deux cas, la page est coupée en deux tiers de texte et un tiers de
panneau : cliquer un chiffre souligné ouvre son nœud, ses dépendances, ses
limites, et toute la chaîne amont jusqu'aux sources — lisibles dans le site
(PDF, page HTML figée, CSV, code, sorties JSON), avec le lien d'origine.

## Démarrer

```bash
pnpm install
pnpm content        # dérive les posts des études + compile les notes
pnpm dev            # http://localhost:3000
```

Prérequis : Node ≥ 24, pnpm 10 (via corepack), Git LFS (les sources figées).

## Publier un post

1. Créer `content/posts/<slug>/post.yaml` (titre, date, étude, article, tag).
2. `pnpm content:posts` génère `post.json`, `article.md`, `graph.json`,
   `files.json` à côté — tous versionnés.

Le graphe vient des quatre registres de l'étude ; les fichiers sources restent
dans l'étude (Git LFS) et sont publiés au build. Au-delà de 25 Mio, un fichier
part en stockage objet : `pnpm --filter @metabolisme/tool-evidence upload-large`.

## Écrire une note

```bash
pnpm note:new ma-note              # crée content/notes/ma-note/
# écrire note.md (ancres [texte](ev:O-01)), evidence.yaml, déposer sources/
pnpm content:notes                 # valide et compile (refuse une ancre sans nœud,
                                   # une source sans fichier, un nœud orphelin…)
pnpm note:url ma-note              # l'adresse à partager
```

L'adresse d'une note est un jeton dérivé de son slug et d'un secret
(`NOTE_TOKEN_SECRET`, voir `.env.example`) : le dépôt, public, ne révèle pas
les adresses partagées. Une note reste accessible à qui a le lien.

## Commandes

```txt
pnpm dev / build / preview      application web
pnpm test · typecheck · lint · format
pnpm content                    posts + notes
pnpm deploy:web                 typecheck + tests, puis build et déploiement Cloudflare
```
