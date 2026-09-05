# NEXT-STEPS — ce qui vient ensuite

Ce qui est déjà fait est consigné dans [`PREV-STEPS.md`](PREV-STEPS.md).
Mis à jour à chaque fin de session de travail significative.

## État au sortir de la session 2 (2026-09-05)

Le cadrage a été **revu contradictoirement et entièrement intégré** :
quatre relecteurs indépendants, 58 objections, décisions de Rémy
(périmètre « monopoles naturels et rentes de position », destination de la
rente explicite par secteur, nouveau titre, intégration complète), compte
rendu `evidence/revue-contradictoire-2026-09-04.md`. L'étude compte 16
sources figées, 21 définitions, 20 hypothèses, 92 nœuds ; l'article
« Reconnaître une rente de position » est réécrit ; le site recalcule les
empreintes au build, porte les hypothèses qualitatives, les notions
construites et les fichiers non redistribuables ; `pnpm content`, tests,
lint, types et build sont verts. **Le post n'est ni tagué ni déployé :
il attend la relecture de Rémy de la version révisée.**

## Prochaines étapes (dans l'ordre)

1. **Relecture de Rémy** de l'article révisé et du cadrage, puis tag
   `monopoles-cadrage-v1.0` (à reporter dans `post.yaml` → `version.tag`,
   dans l'en-tête de l'article et dans le document de preuve §11),
   `pnpm content`, commit, déploiement (`pnpm deploy:web`, depuis une
   machine qui a les deux dépôts).
2. **Deux restes de la revue à figer** (L-12) : la loi hydroélectricité
   promulguée (date, numéro, texte définitif — S-15 est le rapport de
   commission du 1er avril 2026) ; l'étude indépendante sur les TRI
   commandée par la commission d'enquête du Sénat (S-13 la rapporte).
   Et le PDF de l'ARCEP (S-09 est figé depuis le JORF ; la version ARCEP
   est derrière un pare-feu — à récupérer depuis un navigateur ordinaire
   si l'on veut les deux).
3. **Première étude sectorielle : `autoroutes/`** (C-04). Projet autonome
   au niveau racine, gabarit INTRO §9 : objet classé et témoin ; régime et
   échéances (S-08, S-12 ; figure 1.2 de S-08 à lire pour les dates par
   société) ; flux et base d'actifs reconstituée au coût historique net des
   subventions (comptes des concessionnaires, Cour des comptes) ; surprofit
   D-15 aux deux bornes de H-06 et au taux reconnu par l'ART ; attribution
   (I-03) ; quatre configurations (C-05) avec destination (V-05) ; ce qui
   se passe par défaut aux échéances 2031-2036. Projet `uv` dès le premier
   calcul ; ajouter le dossier aux déclencheurs de `site-ci.yml` et au
   filtre LFS.
4. **Étude « eau »** ensuite : rapports SISPEA (chiffres par mode de
   gestion), PDF intégral de S-11, correction de la sélection (H-03,
   H-08, L-06).
5. **Revue contradictoire** après la première étude sectorielle, sur la
   mesure D-15 appliquée (base d'actifs, témoin, bornes).
6. **Logement** : enregistrer les sources de la note privée sur le parc
   social avant tout usage chiffré (CR-3), et instruire L-03 (élasticité
   des loyers privés à la part du parc ouvert) — l'étude sectorielle
   s'adosse à `../logement/`.

## Restes ouverts

- Les chiffres de la note d'origine sur le logement (prix ×2,3 / ×2,6,
  3,5 % / 50 %, 58 %) restent non sourcés ; ne pas les réimporter sans
  acquisition (Notaires-Insee, Insee *Portrait social* 2021) ; la
  contradiction ICC / inflation de la note est à trancher sur séries figées.
- Demsetz 1968 clos (pas d'accès libre chez l'éditeur, vérifié le
  2026-09-05) ; D-09 ne porte que sa partie juridique.
- OpenStax (S-06) : remplacer par une source CC BY ou domaine public à la
  première révision (clause anti-ingestion, SA-3).
- Article ultérieur « mise en œuvre » : compression du rendement régulé,
  chaque brique tient seule, séquencement, oppositions — matière de §5 de
  la note d'origine, hors cadrage ; contraintes normatives sans nœud
  (INTRO §11).
- Outillage : un validateur de registres partagé entre études, qui
  connaisse les champs ajoutés ici (`statement`, `limitations` des
  hypothèses, `constructed_by`, `redistributable`) — à extraire quand une
  troisième étude en aura besoin (INTRO §20) ; en attendant, le build du
  site est le contrôle.

## Comment reprendre (2 minutes)

Lire dans l'ordre : `CLAUDE.md`, `INTRO.md` (§4 définitions, §5 grille,
§7 hypothèses, §8 inventaire, §9 gabarit, §13 chaîne), `EVIDENCE.md`,
l'article, le compte rendu de revue, puis ce fichier. Contrôle :
`cd ../site && pnpm content` (doit régénérer le post à l'identique : 92
nœuds, 18 fichiers).
