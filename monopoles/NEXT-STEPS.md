# NEXT-STEPS — ce qui vient ensuite

Ce qui est déjà fait est consigné dans [`PREV-STEPS.md`](PREV-STEPS.md).
Mis à jour à chaque fin de session de travail significative.

## État au sortir de la session 1 (2026-09-04)

L'étude est **cadrée, sourcée et rédigée** : `INTRO.md` (cadrage), sept
sources figées (`data/raw/`, sha256, LFS), quatorze définitions, trois
paramètres, dix-neuf nœuds de graphe, l'article de cadrage
`articles/2026-09-monopoles-naturels-grille.md`, le document de preuve
`evidence/monopoles-naturels.md`, et le post déclaré dans
`site/content/posts/2026-09-monopoles-naturels-grille/` (43 nœuds,
10 fichiers, `pnpm content` + tests + lint + types + build verts). Aucun
calcul. **Le post n'est pas encore déployé ni tagué : l'article attend la
relecture de Rémy.**

Décisions prises avec Rémy le 2026-09-04 :

- pas de projet Python tant que rien n'est calculé (registres + article) ;
- logement : parc faiseur de prix, propriété privée conservée, trois
  configurations comparées (existant / parc universel / privé intégral) ;
- l'article de cadrage ne contient que le cadrage ; la mise en œuvre
  juridique (§5 de la note d'origine) et les passages tactiques vont dans
  un article ultérieur ; les objections (§6) sont reprises en registre de
  recherche.

## Prochaines étapes (dans l'ordre)

1. **Relecture de l'article par Rémy**, puis tag `monopoles-cadrage-v1.0`
   (à reporter dans `post.yaml` → `version.tag`), `pnpm content`, commit,
   et déploiement (`pnpm deploy:web`, depuis une machine qui a les deux
   dépôts — les notes vivent dans `metabolisme-notes`). Points à trancher à
   la relecture : le titre ; la section « Objections examinées » (garder ou
   renvoyer au document de preuve) ; la présence des H-01..H-03 dans le
   texte alors qu'elles ne sont pas dans le graphe (voir 2).
2. **Hypothèses qualitatives dans le graphe (décision à prendre).** Le
   contrat du site (`site/packages/evidence/src/graph.ts`,
   `HypothesisNodeSchema` ; `tools/evidence/src/study-to-graph.ts`,
   `RegistryHypothesis`) exige `central_value` / `plausible_range` /
   `unit`. H-01..H-05 (directrices) restent donc hors graphe et l'article
   les cite en texte nu (H-01, H-02, H-03 dans « Objections examinées »).
   Recommandation : étendre le contrat à une hypothèse qualitative
   (`statement`, champs numériques optionnels), l'accepter dans
   `study-to-graph`, adapter le corps du panneau et les tests, puis
   enregistrer H-01..H-05 dans `sources/hypotheses.yaml`. Alternative :
   convention `logement` (hors graphe), déjà en place.
3. **Revue contradictoire du cadrage** (méthode `logement` : quatre
   relecteurs indépendants — sources alternatives · définitions et
   hypothèses · scénarios d'échec · cohérence du raisonnement — rapports
   bruts + synthèse committés AVANT intégration ; décisions via Rémy). À
   faire avant ou juste après la publication, comme pour l'article
   `logement`. Cibles évidentes : la définition mesurable de la rente
   (C-02) et son paramètre H-06 ; la construction de D-03/D-05/D-07/D-08 ;
   la ligne « logement » (C-03, H-07, L-03).
4. **Première étude sectorielle (livrable 5).** Recommandation :
   `autoroutes/` (rente la plus documentée : rapports de l'ART sur
   l'économie des concessions, comptes des sociétés concessionnaires,
   rapports de la Cour des comptes, échéances proches), sinon `eau/`
   (SISPEA en données ouvertes, test direct de H-03 / H-08). Projet
   autonome au niveau racine, gabarit INTRO §9 (neuf questions, trois
   configurations), projet `uv` dès le premier calcul, H-06 réutilisé aux
   deux bornes. Ajouter le dossier aux déclencheurs de `site-ci.yml` et au
   filtre LFS de `.gitattributes` à l'ouverture.
5. **Reproductibilité des sources Légifrance (L-08).** Évaluer la base
   LEGI (DILA, données ouvertes) ou l'API Légifrance (PISTE) pour remplacer
   les captures de navigateur par des téléchargements sommables par script ;
   le jour où c'est fait, re-figer S-03..S-05 et tracer le changement
   d'empreinte.

## Restes ouverts

- Les chiffres de la note d'origine sur le logement (prix ×2,3 / ×2,6,
  3,5 % / 50 %, 58 %) restent non sourcés ; ne pas les réimporter sans
  acquisition (Notaires-Insee, Insee *Portrait social* 2021).
- La contradiction ICC / inflation de la note (§6.1 contre §7) est à
  trancher sur séries figées (ICC et IPC, Insee) si l'argument « le prix se
  décorrèle du coût » (H-01) est repris pour le logement.
- Demsetz 1968 (« Why regulate utilities? ») n'est pas enregistré (accès
  payant) ; D-09 ne porte que sa partie juridique.
- Article ultérieur « mise en œuvre » : compression du rendement régulé,
  chaque brique tient seule, séquencement, oppositions — matière de §5 de
  la note d'origine, hors cadrage.
- Outillage (sans urgence) : un validateur de registres partagé entre
  études (les schémas de `logement/src/logement/models.py` ont servi tels
  quels pour valider `monopoles/` le 2026-09-04) — à extraire quand une
  troisième étude en aura besoin (INTRO §20).

## Comment reprendre (2 minutes)

Lire dans l'ordre : `CLAUDE.md`, `INTRO.md` (§4 définitions, §5 grille,
§8 inventaire, §9 gabarit, §13 chaîne, §14 première phase), `EVIDENCE.md`,
l'article, puis ce fichier. Contrôle : `cd ../site && pnpm content` (doit
régénérer le post à l'identique) ; vérification indépendante des registres
avec les schémas de `logement` (voir `evidence/monopoles-naturels.md` §11).
