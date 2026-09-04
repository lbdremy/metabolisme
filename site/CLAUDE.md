# CLAUDE.md — site/ (le site Métabolisme)

Workspace pnpm autonome dans le dépôt `metabolisme` (à côté des études, qui
sont des projets `uv`). Il reprend **à l'identique le cadre du dépôt
`livretlogementlfi`** (`/Volumes/Work/github/livretlogementlfi/CLAUDE.md`,
lecture recommandée) : même stack, même doctrine MVVM steme, mêmes
frontières. Ce fichier ne décrit que ce qui est propre au site.

## Mission

Publier les productions du programme avec leur **chaîne de preuves
explorable** (méthode : `../INTRO.md`, statuts §4, graphe §10) :

1. **Posts** — les articles d'étude (`../logement/articles/*.md`), avec le
   graphe complet dérivé des registres de l'étude ;
2. **Notes** — des messages courts et sourcés, partagés par une URL non
   devinable, avec une chaîne souvent minuscule (un chiffre → sa page).

La page de lecture : deux tiers de texte, un tiers de panneau ; chaque chiffre
ancré ouvre son nœud, et le lecteur « dépile » jusqu'aux sources figées.

## Organisation

```txt
apps/web/                  TanStack Start + Cloudflare Workers (cf. livret)
  src/web/routes/          / · /posts/$slug · /notes/$token · /methode
  src/web/modules/
    evidence/              le panneau : modèle externe (trail, fichier ouvert),
                           hook ViewModel, corps par statut, visionneuse
    reading/               Markdown → React (react-markdown) + ancres ev:
    posts/ notes/          en-têtes et liste
  src/contracts/           ré-exporte @metabolisme/evidence
  src/content-assets/      fetch du graphe/markdown/fichiers (navigateur)
  src/web-rpc/             index figé au build (métadonnées + markdown)
  vite-plugins/content-assets.ts   content/ → module virtuel + assets
packages/web-core/         primitives steme (copie du livret)
packages/evidence/         CONTRAT du graphe (zod), index pur, ancres, jeton
tools/evidence/            build-posts · build-notes · upload-large
content/
  posts/<slug>/            post.yaml (main) → post.json, article.md, graph.json, files.json
  pages/methode.md         copie de ../INTRO.md
../../metabolisme-notes/   DÉPÔT PRIVÉ des notes (METABOLISME_NOTES_DIR)
  <slug>/                  note.yaml, note.md, evidence.yaml, sources/ (main, LFS)
                           → note.json, graph.json, files.json
```

## Contrat central : le graphe de preuves

`packages/evidence/src/graph.ts` — un seul format pour posts et notes. Nœuds
typés par statut (`source`, `definition`, `observation`, `transformation`,
`measure`, `hypothesis`, `result`, `interpretation`, `value`, `choice`,
`proposal`, `limit`), identifiants `X-nn`, relations `depends_on` /
`limitations`, et pour chaque statut ce qu'il faut pour vérifier : fichiers
figés (chemin logique, empreinte, hébergement), localisateurs (fichier, page,
citation), plage plausible, code et sortie. Le graphe d'un post est DÉRIVÉ
(pure fonction `studyToGraph`, testée) ; celui d'une note est ÉCRIT puis
validé (`noteToGraph` : références résolues, ancres connues, fichiers
présents, pas d'orphelin).

Ancres dans le texte : lien `[passage](ev:R-07)` ou identifiant nu `(R-07)`
(plugin remark, seulement s'il existe dans le graphe). Le nœud ouvert est un
état d'URL (`?n=R-07`).

## Décisions propres au site

- **Le contenu lourd ne passe jamais par le serveur.** Article et markdown
  de note entrent dans l'index (rendu serveur, quelques dizaines de Ko) ;
  graphe et fichiers sont des assets. Les fichiers sources ne sont pas copiés
  dans `content/` : `files.json` pointe vers le dépôt (`logement/data/raw/…`,
  LFS) et le plugin les émet au build. Au-delà de 25 Mio → stockage objet
  (`upload-large`), servi par le Worker sous la même URL.
- **Notes secrètes, dépôt public.** Le CONTENU des notes vit dans le dépôt
  privé `metabolisme-notes` (lu au build, jamais copié ici ; absent → site
  sans note). L'URL porte `HMAC(NOTE_TOKEN_SECRET, slug)` calculé au build.
  Pas de secret → jetons de développement, prévisibles (avertissement au
  build de production). `robots: noindex`, jamais listées. Le déploiement
  se fait depuis une machine qui a les deux dépôts.
- **Charte dérivée du logo** (douze disques en spirale) : une couleur par
  statut, dans l'ordre de la chaîne ; papier et encre pour le reste ; serif
  pour le texte lu, sans pour le panneau. Jetons dans `src/styles.css`,
  mapping dans `modules/evidence/model/status.ts`.
- **Pas de lefthook ici** (le dépôt Git est à la racine, avec les études) :
  `pnpm format && pnpm lint` avant de committer ; la CI
  (`../.github/workflows/site-ci.yml`) rejoue format, lint, types, tests,
  contenu (doit être à jour) et build.

## Commandes

```txt
pnpm dev · build · preview · test · typecheck · lint · format
pnpm content            posts (depuis les études) + notes
pnpm note:new <slug>    dossier de note
pnpm note:url <slug>    adresse partageable (NOTE_TOKEN_SECRET requis)
pnpm --filter @metabolisme/tool-evidence upload-large [--dry-run]
pnpm deploy:web
```

## Conventions

Code, identifiants, commits en anglais ; interface, contenus, documentation
en français. Commits conventionnels. `content/**` est hors format/lint. Les
sources figées des notes sont en Git LFS dans `metabolisme-notes`.
