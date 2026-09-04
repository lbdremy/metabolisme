# NEXT-STEPS — ce qui vient ensuite

Ce qui est déjà fait est consigné dans [`PREV-STEPS.md`](PREV-STEPS.md).
Mis à jour à chaque fin de session de travail significative.

## État au sortir de la session 1 (2026-09-04)

L'étude est **ouverte et cadrée** : `INTRO.md` fixe la question, la grille
(quatre questions, trois niveaux), les valeurs assumées, les hypothèses
directrices, l'inventaire des dix secteurs comme hypothèses, le gabarit
d'étude sectorielle et la chaîne initiale. Les registres existent et sont
vides. Aucune source n'est figée, aucun article n'est écrit.

Décisions prises avec Rémy le 2026-09-04 :

- pas de projet Python tant que rien n'est calculé (registres + article) ;
- logement : parc faiseur de prix, propriété privée conservée, trois
  configurations comparées (existant / parc universel / privé intégral) ;
- l'article de cadrage ne contient que le cadrage (définitions, grille,
  légitimité, gabarit) ; la méthode de mise en œuvre juridique (§5 de la
  note d'origine) et les passages tactiques vont dans un article ultérieur ;
  les objections (§6) deviennent des limites et objections examinées.

## Prochaines étapes (dans l'ordre)

1. **Figer les définitions (livrable 1, INTRO §14).** Récupérer, sommer et
   enregistrer S-01..S-06 (glossaire OCDE ; Ricardo ch. 2 ; Légifrance :
   code de la commande publique L1121-1, CGCT L1411-1 / L1412-1 / L2221-1,
   CG3P L2111-1 / L3111-1 ; une délibération de régulateur fixant un coût du
   capital). Écrire D-01..D-14, verbatim pour les définitions officielles,
   et rattacher les quatre notions construites (D-03, D-05, D-07, D-08) à
   C-02. Vérifier l'accès libre à Demsetz 1968 avant de l'enregistrer.
   Piège : ne pas citer une définition trouvée par une IA comme une source
   (règle 21.1) ; chaque page est ouverte, datée, figée.
2. **Graphe du cadrage (livrable 2).** C-01..C-04, V-01..V-04, I-01..I-02,
   L-01..L-05 dans `evidence/claims.yaml` ; H-06 (rémunération normale du
   capital, à partir des délibérations figées), H-07 (seuil de part,
   30-40 %, confiance faible), H-08 (écart délégation / régie, 10-20 %, à
   sourcer ou à laisser en attente) dans `sources/hypotheses.yaml`.
3. **Article de cadrage (livrable 3).**
   `articles/2026-09-monopoles-naturels-grille.md` + document de preuve
   `evidence/monopoles-naturels.md` (INTRO §11, sans calcul). Registre de
   recherche ; chaque affirmation ancrée sur son nœud ; les objections de
   la note d'origine reformulées en §11.10.
4. **Publication (livrable 4).** `site/content/posts/…/post.yaml`, puis
   `pnpm content`. **Décision à prendre avant** : le contrat du graphe
   (`site/packages/evidence/src/graph.ts`, `HypothesisNodeSchema`) exige
   `central_value` / `plausible_range` / `unit` ; les hypothèses
   qualitatives H-01..H-05 et le classement de l'inventaire ne peuvent pas y
   entrer. Recommandation : étendre le contrat à une hypothèse qualitative
   (`statement`, champs numériques optionnels) dans `packages/evidence`,
   `study-to-graph` et le corps du panneau, avec tests ; alternative :
   convention `logement` (hors graphe). À soumettre à Rémy.
   Ajouter `monopoles/**` aux déclencheurs de `site-ci.yml` à ce moment.
5. **Première étude sectorielle (livrable 5).** Recommandation :
   `autoroutes/` (rente la plus documentée : rapports de l'ART, comptes des
   concessionnaires, échéances 2031-2036), sinon `eau/` (SISPEA en données
   ouvertes, test direct de H-03). Projet autonome au niveau racine, gabarit
   INTRO §9, projet `uv` dès le premier calcul.

## Restes ouverts

- Les chiffres de la note d'origine sur le logement (prix ×2,3 / ×2,6,
  3,5 % / 50 %, 58 %) restent non sourcés ; ne pas les réimporter sans
  acquisition (Notaires-Insee, Insee *Portrait social* 2021).
- La contradiction ICC / inflation de la note (§6.1 contre §7) est à
  trancher sur séries figées (ICC et IPC, Insee) si l'argument « le prix se
  décorrèle du coût » est repris pour le logement.
- Article ultérieur « mise en œuvre » : compression du rendement régulé,
  chaque brique tient seule, séquencement, oppositions — matière de §5 de
  la note d'origine, hors cadrage.

## Comment reprendre (2 minutes)

Lire dans l'ordre : `CLAUDE.md`, `INTRO.md` (§4 définitions, §5 grille,
§8 inventaire, §9 gabarit, §14 première phase), `EVIDENCE.md`, puis ce
fichier. Les registres sont vides : commencer par l'étape 1.
