# Revue contradictoire — angle COHÉRENCE ET STATUTS ÉPISTÉMIQUES (relecteur n°4)

- **Date** : 2026-09-04
- **Périmètre** : étude `monopoles/` (cadrage « Monopoles naturels et
  collectivisation des rentes ») — `INTRO.md`, `sources/*.yaml`,
  `evidence/claims.yaml`, `evidence/monopoles-naturels.md`,
  `articles/2026-09-monopoles-naturels-grille.md`, `EVIDENCE.md`,
  `README.md`, `CLAUDE.md`, `NEXT-STEPS.md`, `PREV-STEPS.md` ; graphe dérivé
  `site/content/posts/2026-09-monopoles-naturels-grille/graph.json` ; note
  d'origine `exploration/2026-09-grille-deux-questions-note-de-travail.md`
  (exploratoire, lue pour repérer les importations) ; article
  `logement/articles/2026-08-efficacite-parc-etat-des-preuves.md` comme
  référence de registre.
- **État examiné** : `main` à `59d021f` (« feat(site): Accept qualitative
  hypotheses and register the framing hypotheses »), arbre propre.
- **Méthode** : lecture intégrale de `INTRO.md` (racine, §1.3, §4, §10, §12,
  §15, §16, §21) puis de l'étude ; extraction mécanique des identifiants cités
  par l'article, le document de preuve et `INTRO.md` et confrontation aux 48
  nœuds de `graph.json` (ids, arêtes entrantes, nœuds jamais cités) ;
  confrontation de chaque citation entre guillemets de l'article au champ
  `definition` / `caveats` des D-xx puis aux fichiers figés de `data/raw/`
  (`pdftotext` sur S-01 et S-07, `grep` sur S-02, S-03, S-05, S-06) ; lecture
  de `site/tools/evidence/src/study-to-graph.ts` pour établir ce que le build
  du site contrôle réellement ; `git show --stat HEAD` pour dater les
  documents de suivi ; comparaison ligne à ligne article / note d'origine.
  Aucun fichier de l'étude ni du site n'a été modifié. Les numéros de ligne
  renvoient aux fichiers à `59d021f`.

---

## Objections

### CR-1 — Le constat central de l'article est l'hypothèse H-01

- **Cible** : article l. 31-33, 162-164, 257-258 ; `INTRO.md` §1 l. 62 et
  §3.3 l. 142-146 ; `hypotheses.yaml` H-01.
- **Gravité** : bloquante.
- **Énoncé** : la proposition « là où l'infrastructure n'est pas substituable,
  aucun mécanisme de marché ne discipline le prix » est enregistrée comme
  hypothèse (H-01, confiance moyenne, `affects: []`, aucune donnée) et
  présentée trois fois par l'article, et deux fois par le cadrage, comme un
  **constat** — la seule chose que l'étude prétend avoir établie.
- **Preuve** :
  - article l. 31-33 : « L'identification (la ressource est-elle
    substituable ?) et le destinataire (qui encaisse la recette d'usage ?)
    sont des constats. »
  - article l. 162-164 : « Si non, on est devant un monopole naturel : il
    n'existe aucun mécanisme de marché capable de discipliner le prix
    d'accès. » (aucune ancre ; D-01 est une propriété de coût qui, selon son
    propre caveat 3, « dit qu'une seule entreprise doit produire, pas qui doit
    la posséder ni qui doit encaisser » — elle ne dit rien du prix).
  - article l. 257-258 : « Que le marché ne puisse pas discipliner le prix
    d'un réseau non substituable est un constat. »
  - `INTRO.md` l. 143-145 : « Ce n'est vrai que de l'**identification** :
    qu'il n'existe aucun mécanisme de marché capable de discipliner ce prix
    est un constat. »
  - `hypotheses.yaml` H-01 : « Là où l'infrastructure n'est pas substituable,
    le prix payé par l'usager se décorrèle du coût de fourniture (hypothèse
    directrice H-01) », `confidence: medium`, « Testable secteur par
    secteur ».
  - Par ailleurs D-05 (caveat 2) reconnaît que « coût raisonnable » n'est pas
    quantifié et D-01 (caveat 4) que la délimitation du marché « est un choix
    de l'analyste » : l'identification elle-même repose sur un choix non
    quantifié, ce qui interdit de la qualifier de constat.
- **Effet si retenue** : violation de §1.3 (une hypothèse présentée comme
  établie), de §15 (« une proposition ne doit pas être présentée comme
  “prouvée” ») et de la règle 21.8. Le titre (CR-5) et la section « Ce que la
  grille ne dit pas » reposent sur ce « constat ».
- **Disposition proposée** : remplacer « constat » par « hypothèse (H-01) »
  aux cinq endroits ; réécrire l. 162-164 en « si non, l'étude fait
  l'hypothèse (H-01) que le prix se décorrèle du coût » ; dans le tableau des
  trois niveaux (article l. 245-246, INTRO l. 276-277), remplacer « constat »
  par « hypothèse de classement (I-01 / H-01) ». Ajouter au caveat de D-05
  que l'identification dépend d'un seuil non quantifié.

### CR-2 — La colonne « Hypothèse de conclusion » de l'inventaire fait passer des propositions et des valeurs pour des interprétations ; V-01 n'a aucune arête entrante

- **Cible** : `claims.yaml` I-01 (l. 125-141) et V-01 (l. 86-94) ; article
  l. 285-305 ; `INTRO.md` §8 l. 402-413 ; `graph.json`.
- **Gravité** : bloquante.
- **Énoncé** : les « conclusions » par secteur (« Régie », « Ne pas
  reconcéder », « Recette publique, exploitation et entretien délégués au
  forfait », « Tarifer la rareté », « prix administré couvrant le coût
  complet », « Exploitation publique ») sont des propositions (P) ou des
  choix (C) qui découlent de V-01 et V-04. Elles sont logées dans I-01, dont
  les dépendances sont `[C-01, D-05, D-06, D-07, D-08]` — aucune valeur. Dans
  le graphe, V-01 (« la rente de position doit revenir à l'usager ») n'est
  référencée par **aucun** nœud : la valeur centrale de l'étude est un
  orphelin, et le graphe répond « aucun » à la question de §10 « quelles
  propositions dépendent de cette valeur ? ».
- **Preuve** :
  - article l. 288 : « **Chaque ligne est une hypothèse**, à confirmer,
    nuancer ou réfuter par l'étude sectorielle correspondante » — puis
    l. 300 « Régie », l. 303 « Ne pas reconcéder : l'actif est déjà public »,
    l. 302 « Recette publique, exploitation et entretien délégués au
    forfait ». Une étude sectorielle ne peut ni confirmer ni réfuter
    « Régie » : ce n'est pas une hypothèse au sens de §4.
  - `claims.yaml` l. 140 : `depends_on: [C-01, D-05, D-06, D-07, D-08]` ;
    aucune mention de V-01, V-03, V-04 ; l. 138-139 « Chaque ligne est une
    hypothèse de classement ».
  - `graph.json` (calcul des arêtes entrantes) : `V-01 <- []`, `V-03 <- []`,
    `V-04 <- []` ; seule V-02 est référencée (par C-03).
  - `INTRO.md` §2.4 l. 96-99 et l. 109-112 : « Comparer plusieurs
    configurations, pas en défendre une » ; « La conclusion d'une étude
    sectorielle n'est pas “il faut collectiviser” ». La colonne de
    l'inventaire fait pourtant exactement cela, secteur par secteur, avant
    toute instruction.
  - `CLAUDE.md` l. 56-59 : « Never let a V read as an O. »
- **Effet si retenue** : c'est le mélange de plans que §1.3 et §17 (« le
  technicisme sans valeurs ») interdisent : un choix (« Régie ») présenté
  comme la sortie d'une grille de propriétés physiques. Le lecteur du graphe
  ne peut pas voir que les conclusions dépendent de V-01.
- **Disposition proposée** : scinder I-01 en (a) le classement Q1-Q3 par
  secteur (statut H ou I, cf. CR-17) et (b) une entrée de type C ou P par
  secteur (« configuration que l'étude propose d'instruire en premier »)
  avec `depends_on: [I-01, V-01, V-03, V-04]`. Dans l'article, renommer la
  colonne « Configuration à instruire (choix, V-01) » ou la retirer du
  tableau et la renvoyer à §« Comment une étude sectorielle répondra ».

### CR-3 — Des chiffres d'une note privée non enregistrée entrent dans le registre, alors que ceux de la note d'origine en sont exclus au même motif

- **Cible** : `hypotheses.yaml` H-04 (`statement`) et H-07
  (`description`) ; `INTRO.md` §12 l. 591-596 ; document de preuve §10
  l. 152-157.
- **Gravité** : sérieuse.
- **Énoncé** : H-04 et H-07 portent des données chiffrées (« loyers
  inférieurs de 31 % », « 43 % du parc, environ la moitié des habitants »)
  dont la source est « note privée “Le parc social, fonction régulatrice ou
  logique volumétrique ?” » — qui n'est ni un S-xx de cette étude, ni
  accessible au lecteur. Le même document de preuve écarte les chiffres de la
  note d'origine parce qu'ils sont « contredits par les sources déjà figées
  du dépôt ou sans source ».
- **Preuve** :
  - `hypotheses.yaml` H-04 : « Base empirique : le parc social français
    (loyers inférieurs de 31 %, taux d'effort proche du secteur libre) contre
    Vienne (parc universel, jamais privatisé, adossé à une cotisation) — note
    privée “Le parc social, fonction régulatrice ou logique
    volumétrique ?” ».
  - `hypotheses.yaml` H-07 : « cohérente avec le cas viennois (parc municipal
    et coopératif : 43 % du parc, environ la moitié des habitants — note
    “…”, dépôt privé) ».
  - `sources.yaml` : sept sources, aucune ne porte ces données.
  - document de preuve l. 152-157 : « Données écartées et pourquoi : les
    chiffres logement de la note d'origine (Vienne 60 %, …) — contredits par
    les sources déjà figées du dépôt ou sans source ».
  - Ambiguïté supplémentaire : « 43 % » apparaît dans le préambule de la
    note archivée (l. 21-22) comme part du parc social dans le parc locatif
    **français** (enquête Logement 2020) et dans H-07 comme part du parc
    **viennois**. Rien ne permet au lecteur de savoir s'il s'agit du même
    nombre.
- **Effet si retenue** : règles 21.1 et 21.2 (source originale enregistrée
  pour toute donnée retenue) ; §7 (« une URL seule n'est pas suffisante », a
  fortiori un document privé). Le traitement asymétrique des deux notes
  affaiblit la crédibilité de la section « données écartées ».
- **Disposition proposée** : soit enregistrer les sources primaires (SDES /
  Insee pour 31 %, Ville de Vienne pour 43 % et « environ la moitié ») comme
  S-08+ avec fichiers figés, soit retirer les chiffres des `statement` /
  `description` et ne garder que la relation qualitative, en le disant dans
  le document de preuve §10.

### CR-4 — H-07 est incohérent avec sa propre justification : la part du parc locatif ne discrimine pas la France de Vienne

- **Cible** : `hypotheses.yaml` H-04, H-07 ; `claims.yaml` L-03 ;
  `INTRO.md` §12 l. 591-596 ; article l. 329-333.
- **Gravité** : sérieuse.
- **Énoncé** : H-07 fixe un seuil de 30-40 % « du parc locatif » au-delà
  duquel un parc régulé devient faiseur de prix, « cohérent avec le cas
  viennois ». Mais le dépôt dit lui-même que le parc social français pèse « un
  tiers » à « 43 % » du parc locatif (préambule de la note archivée l. 21-22)
  — donc dans ou au-dessus de la plage — sans être faiseur de prix (H-04).
  L'étude explique cette différence par le **statut** (réservé / universel),
  pas par la taille ; `INTRO.md` §12 l'écrit explicitement. L'unité du
  paramètre ne mesure donc pas la variable que l'hypothèse dit décisive.
- **Preuve** :
  - `INTRO.md` l. 593-596 : « Vienne se distingue par le statut de son parc
    (universel, jamais privatisé, adossé à une cotisation) plus que par sa
    taille. C'est la base empirique de H-04. »
  - H-07 `unit: "% du parc locatif"`, `plausible_range: [30.0, 40.0]`,
    « cohérente avec le cas viennois ».
  - H-04 `statement` : « Un parc réservé (plafonds de ressources) loge moins
    cher sans réguler ; un parc universel et assez large devient faiseur de
    prix. »
  - note archivée, préambule l. 21-22 : « Ancols : un tiers ; enquête
    Logement 2020 (Insee) : 43 % par calcul ».
- **Effet si retenue** : le seul paramètre chiffré du volet logement est
  défini sur une variable que l'étude elle-même déclare non discriminante ;
  l'analyse de sensibilité prévue sur H-07 ne testerait rien.
- **Disposition proposée** : reformuler H-07 comme « part du parc locatif
  **ouvert sans plafond de ressources** » (ou « part des ménages éligibles »),
  ou le remplacer par deux paramètres (part + condition d'universalité), et
  dire dans L-03 que la France est un contre-exemple de la variable
  « taille » seule.

### CR-5 — Le titre affirme ce que les études sectorielles doivent tester

- **Cible** : article l. 1 ; `post.yaml` `title` ; note d'origine l. 38.
- **Gravité** : sérieuse.
- **Énoncé** : « Là où le marché n'existe pas » pose comme acquis que dans
  les secteurs visés le marché n'existe pas — c'est H-01 (CR-1) et le
  classement I-01, tous deux non instruits. Le titre est repris tel quel du
  sous-titre de la note d'origine (« Collectiviser la rente là où le marché
  n'existe pas »), texte doctrinal dont l'étude dit qu'il « relève du régime
  exploratoire ».
- **Preuve** : article l. 6-8 : « Cet article ne calcule rien » ; l. 436 :
  « Aucun secteur n'est instruit … aucune rente n'est mesurée » ; document de
  preuve l. 123-125 : « Ce qu'elles ne montrent pas : aucune rente, aucun
  destinataire, aucun montant ». `NEXT-STEPS.md` l. 34 signale déjà « le
  titre » comme point à trancher.
- **Effet si retenue** : §15 (« une proposition ne doit pas être présentée
  comme prouvée ») ; le registre du titre contredit celui de l'article. Par
  comparaison, l'article `logement` titre sur un état (« au bord du compte »)
  adossé à des R-xx.
- **Disposition proposée** : un titre au conditionnel ou interrogatif
  (« Là où le marché n'existerait pas » ; « Reconnaître les monopoles
  naturels ») ; le sous-titre actuel est tenu par le contenu et peut rester.

### CR-6 — « Tout tient dans le mot “normale” » : le terme « fourniture efficace » porte autant et n'a ni définition ni nœud

- **Cible** : article l. 131-136 ; `claims.yaml` C-02 l. 51-53 ; document
  de preuve §2 l. 46-50.
- **Gravité** : sérieuse.
- **Énoncé** : la définition mesurable de la rente (C-02) comporte deux
  termes non observables : la « rémunération normale du capital » (H-06) et
  le « coût d'une fourniture efficace ». L'article affirme que tout tient
  dans le premier ; or H-03 et H-08 (écart régie / délégation, biais de
  sélection L-06) montrent que la fixation du coût efficace est le problème
  empirique principal, et aucun D-xx ni H-xx ne dit comment il sera établi.
  Le document de preuve ne liste pas cette ambiguïté (§2 ne mentionne que
  « marché particulier » et « coût raisonnable »).
- **Preuve** : article l. 134-136 : « Tout tient dans le mot “normale”, qui
  est un paramètre nommé (H-06) » ; C-02 : « ce que paie l'usager moins le
  coût d'une fourniture efficace, rémunération du capital au taux H-06
  comprise » ; document de preuve l. 46-50.
- **Effet si retenue** : §16 « Les étapes implicites ont-elles été rendues
  visibles ? » — non ; le gabarit sectoriel (INTRO §9, question 4) hérite
  d'une définition dont la moitié est implicite.
- **Disposition proposée** : ajouter une définition construite « coût de
  fourniture efficace » (D-15, rattachée à C-02) énumérant les étalons admis
  (coût d'une régie comparable, coût reconnu par un régulateur, coût
  reconstruit) et une limite ; corriger la phrase de l'article.

### CR-7 — Sens des dépendances : hypothèses justifiées par les choix qu'elles fondent, limites servant de justification, notions construites présentées comme sourcées

- **Cible** : `hypotheses.yaml` H-03, H-04, H-05, H-07, H-08
  (`justification`) ; `definitions.yaml` D-03, D-04, D-05, D-07, D-08
  (`source`) ; `claims.yaml` L-01, L-02, C-02 ; `graph.json`.
- **Gravité** : sérieuse.
- **Énoncé** : plusieurs arêtes vont dans le mauvais sens ou manquent :
  1. H-04 est justifiée par C-03 et H-07 par C-03 — or C-03 (défendre le
     parc faiseur de prix) est la décision que H-04/H-07 sont censées
     fonder. Une hypothèse ne se justifie pas par le choix qu'elle motive.
  2. H-05 est justifiée par C-04 (ordre des études), alors que C-04 dit
     « électricité en dernier (H-05) » : c'est l'ordre qui dépend de
     l'hypothèse.
  3. H-03, H-04, H-07, H-08 listent des limites (L-06, L-03) dans
     `justification` ; dans `graph.json` cela devient `H-03 depends_on
     L-06`. Une limite restreint, elle ne justifie pas ; le schéma prévoit
     `limitations` pour cela (`INTRO.md` racine §10).
  4. Les cinq notions construites (D-03, D-04, D-05, D-07, D-08) ont pour
     seule dépendance une source (S-02, S-01, S-01, S-06, S-06). Dans le
     graphe, D-05 « substituabilité » dépend de l'OCDE exactement comme D-01
     ; le lien « construite par C-02 » n'existe qu'en prose. L-07 (« elles
     n'ont pas de source qui les définisse, seulement une source qui les
     ancre ») est attaché à C-02, pas aux D concernés.
  5. L-01 et L-02 n'ont aucune arête entrante (`L-01 <- []`, `L-02 <- []`) :
     elles ne limitent aucun nœud alors qu'elles portent sur D-03/D-04 et
     D-05 (ou sur V-03 et C-02).
- **Preuve** : `hypotheses.yaml` H-04 `justification: [C-03, L-03]` ; H-07
  `justification: [H-04, L-03, C-03]` ; H-05 `justification: [D-06, D-07,
  C-04]` ; H-03 `justification: [D-11, D-12, L-06]` ; H-08 `[H-03, L-06]` ;
  `graph.json` : `H-03 depends_on ['D-11','D-12','L-06']`, `D-05 depends_on
  ['S-01']`, `L-01 <- []`, `L-02 <- []` ; `claims.yaml` C-02 l. 54
  `depends_on: [D-01, D-02, D-06, S-01, S-02, S-06]` (C-02 dépend des
  sources, les D construites ne dépendent pas de C-02).
- **Effet si retenue** : le graphe ne peut pas répondre aux questions de §10
  (« quels résultats dépendent d'une hypothèse donnée ? », « une valeur
  est-elle présentée à tort comme un résultat ? ») ; la circularité C-03 ↔
  H-04 est précisément le risque « circularité » que `INTRO.md` §15
  l. 757-759 dit vouloir éviter.
- **Disposition proposée** : H-04 `justification: [D-03, D-08]` +
  `limitations: [L-03]`, C-03 `depends_on: [V-01, V-02, H-04, I-01]` ; H-05
  sans C-04 ; déplacer L-xx de `justification` vers `limitations` pour
  H-03/H-04/H-07/H-08 ; faire porter aux D construites une dépendance
  explicite sur C-02 (si le schéma `DefinitionRecord` ne le permet pas,
  étendre le schéma plutôt que laisser le graphe mentir) et attacher L-07 à
  chacune ; attacher L-01 à V-03/D-04 et L-02 à D-05/C-01.

### CR-8 — La grille n'a jamais dit « non » : Q1 = « Non » pour les dix secteurs, et l'inventaire précède la grille

- **Cible** : `claims.yaml` I-01 ; article l. 294-305 ; `INTRO.md` §8
  l. 402-413 ; document de preuve §8 l. 123-125.
- **Gravité** : sérieuse.
- **Énoncé** : le document de preuve conclut que « la grille est applicable
  et discriminante (elle ne classe pas tous les secteurs de la même
  façon) ». Sur le critère qui définit le monopole naturel (Q1), les dix
  lignes portent « Non » : la grille ne discrimine que sur Q2-Q3. Aucun
  secteur substituable n'a été passé à la grille pour montrer qu'elle sait
  exclure, alors que la note d'origine en nomme (l. 234 : « l'internet par
  satellite concurrence la fibre et la 4G. Le service est donc
  substituable »). L'inventaire est repris du tableau de la note (`INTRO.md`
  l. 395 : « reprend celui de la note de travail »), c'est-à-dire d'une
  liste constituée **avant** la grille, par des secteurs choisis pour y
  répondre « non ».
- **Preuve** : article l. 296-305, colonne « Q1 substituable ? » : Non ×10 ;
  document de preuve l. 124-125 ; article l. 42-43 : « un critère
  d'identification, applicable secteur par secteur et contestable ligne à
  ligne ».
- **Effet si retenue** : règle 21.12 (chercher les données contradictoires)
  et §13.4 (« un scénario dans lequel la proposition échoue ») : un critère
  qui n'a jamais produit de négatif n'est pas montré discriminant. La phrase
  du document de preuve est une surinterprétation.
- **Disposition proposée** : ajouter deux ou trois lignes témoins où Q1 =
  « Oui » (commerce de détail, transport routier de marchandises, service
  internet par satellite pris comme service) et une ligne ambiguë (gaz,
  ports) ; reformuler §8 du document de preuve : « discriminante sur Q2-Q3 ;
  non éprouvée sur Q1 ».

### CR-9 — L'article affirme que le build du site vérifie les empreintes ; il ne le fait pas, et la vérification faite n'est pas dans le dépôt

- **Cible** : article l. 456-461 ; document de preuve §11 l. 161-173 ;
  `README.md` l. 44-45 ; `site/tools/evidence/src/study-to-graph.ts`.
- **Gravité** : sérieuse.
- **Énoncé** : `study-to-graph.ts` recopie le champ `checksum` du registre
  dans le graphe (l. 134-156, 163-164) sans jamais recalculer un sha256 sur
  `data/raw/` (aucun `createHash` dans le chemin des études ; seul
  `build-notes.ts` en calcule pour les notes). La recomparaison des
  empreintes et la validation avec les schémas pydantic de `logement` ont
  été « exécutées le 2026-09-04 » hors de tout script committé.
- **Preuve** :
  - article l. 459-461 : « Leur cohérence — références résolues, empreintes
    vérifiées — est contrôlée au build du site (`site/tools/evidence`) ».
  - `study-to-graph.ts` l. 155 : `if (checksum !== undefined) file.checksum
    = checksum;` — copie, pas contrôle.
  - document de preuve l. 167-173 : « Vérification indépendante possible …
    exécuté le 2026-09-04 : 7 sources, 14 définitions, … aucune erreur » —
    aucun fichier de script, aucun `check.sh`, `CLAUDE.md` l. 24-25 : « no
    `check.sh`/`test.sh` ».
- **Effet si retenue** : règles 21.4 (calcul laissé dans une conversation),
  21.14 et 21.16 (opération manuelle non documentée) ; §16 « Le projet
  peut-il être reproduit dans un environnement neuf ? » — la vérification
  d'empreintes ne l'est pas ; l'article fait une promesse fausse au lecteur.
- **Disposition proposée** : corriger la phrase de l'article (« références
  résolues » seulement) ; committer le script de validation (même trente
  lignes réutilisant `logement/src/logement/models.py`, ou un `pnpm`
  `verify-checksums`) et le brancher dans `site-ci.yml` ; noter que L-08
  rend de toute façon la recomparaison non reproductible pour S-03..S-05.

### CR-10 — Énoncés de la note d'origine repris sans statut ni source

- **Cible** : article (lignes ci-dessous) ; `claims.yaml` L-01, L-02, L-05.
- **Gravité** : sérieuse.
- **Énoncé** : au-delà des chiffres (correctement écartés), l'article
  reprend, au présent de l'indicatif et sans ancre ou sous une ancre qui ne
  couvre pas l'énoncé, des affirmations factuelles ou évaluatives de la note.
  L-04 ne couvre que « la colonne “régime actuel” de l'inventaire », pas ces
  phrases.
- **Preuve** (article ← note) :
  - l. 74-76 « c'est le cas de la boucle locale de télécommunications, non
    duplicable, sur laquelle plusieurs opérateurs servent pourtant des
    clients différents » ← note l. 126 ; aucune ancre (I-02 n'apparaît que
    l. 309).
  - l. 115-116 « Un réseau d'eau, un sillon ferroviaire, une position urbaine
    ne le sont pas » ← note l. 62, verbatim ; c'est le classement I-01
    énoncé comme fait.
  - l. 179-181 « Un lien de fibre ne l'est presque pas, le coût marginal d'un
    utilisateur supplémentaire étant proche de zéro » ← note l. 85,
    verbatim ; aucune source sur le coût marginal.
  - l. 207-209 « les réseaux de chaleur, dont on ne sort qu'en refaisant
    l'installation de l'immeuble » ← note l. 174 ; aucune source.
  - l. 229-230 « Sur un monopole naturel à usager captif, le risque transféré
    est faible et la recette élevée » ← D-10 caveat 2, lui-même sans source :
    affirmé puis « à mesurer ».
  - l. 249-251 « La confusion entre le deuxième et le troisième niveau est ce
    qui permet de présenter un transfert de rente … comme une ouverture à la
    concurrence » ← note l. 95 (autoroutes), généralisé ; interprétation non
    enregistrée.
  - l. 311-315 « C'est exactement ce que le dégroupage puis la mutualisation
    de la fibre sous régulation ont organisé. … il montre que la grille
    décrit quelque chose qui fonctionne » ← note l. 128-130 ; le « reste à
    sourcer » qui suit ne retire pas « qui fonctionne » (jugement, hérité de
    « prouve que la grille n'est pas une théorie »).
  - l. 319-321 « Le sol y est non substituable par rareté positionnelle et la
    capacité totalement rivale » ← note l. 212 ; énoncé comme fait
    immédiatement après « chaque ligne est une hypothèse ».
  - l. 336-338 « on y observe la formation d'une rente en temps réel, par
    pure antériorité d'occupation » ← note l. 230, 243 ; « on observe » sans
    O-xx ; L-05 dit « sans source figée ».
  - l. 367-370 « les autoroutes … dont les concessionnaires publient leurs
    comptes et dont le régulateur publie ses analyses ; l'eau … dont
    l'observatoire national publie prix et mode de gestion service par
    service » ← note §3.5, §3.7 ; aucune source (ce sont des pistes de
    `INTRO.md` §10, « aucune n'est encore une source »).
  - l. 414-416 « le maintien d'opérateurs privés en concurrence *pour* le
    marché … conserve l'aiguillon sans céder la recette (Q4) » ← note
    l. 346 ; hypothèse non enregistrée, « Q4 » n'est pas un identifiant.
  - `claims.yaml` L-01 « Le brevet crée une rente juridiquement protégée et
    durable », L-02 « Les plateformes numériques fabriquent des monopoles par
    effets de réseau », L-05 « coordination internationale des fréquences par
    priorité au premier déclarant, responsabilité des États de lancement, pas
    d'exécution » ← note l. 64, 238, 251-255 : des assertions factuelles
    logées dans des nœuds de statut L (« incertitude, manque de données ou
    restriction connue », §4).
- **Effet si retenue** : règles 21.1, 21.7, 21.8 ; §2.1 « aucun résultat
  important ne doit être publié directement depuis ce régime » ;
  `INTRO.md` §14 l. 730 promet « chaque affirmation ancrée sur son nœud ».
- **Disposition proposée** : pour chaque énoncé, soit une ancre existante
  reformulée au conditionnel (« l'inventaire fait l'hypothèse que… »), soit
  une nouvelle L (« L-09 — propriétés physiques des secteurs affirmées sans
  source à l'ouverture »), soit suppression. Vider L-01/L-02/L-05 de leur
  contenu assertif (ne garder que la restriction de périmètre) ou en faire
  des I limitées.

### CR-11 — La section « Objections examinées » n'est pas loyale sur quatre points

- **Cible** : article l. 382-430 ; note d'origine §6 l. 307-377 ; document
  de preuve §10 l. 146-150.
- **Gravité** : sérieuse.
- **Énoncé et preuve** :
  1. **Origine des objections.** Article l. 384-385 : « Les objections
     ci-dessous ont été formulées contre la première version de ce
     raisonnement. » La note titre §6 « Objections **attendues** » : elles
     ont été anticipées par l'auteur, non reçues d'un contradicteur. Le
     registre suggère une revue externe qui n'a pas eu lieu (la présente
     revue est la première).
  2. **Objection 1 (concurrence entre logements).** La réponse l. 390-394
     (« c'est une concurrence *à l'intérieur* d'une rente, qui redistribue
     entre biens sans pouvoir faire descendre le prix sous la valeur de la
     position ») est reprise verbatim de la note l. 315 ; c'est une
     interprétation non enregistrée et circulaire (elle présuppose la
     « valeur de la position » que l'objection conteste). Seul le renvoi à
     H-01 est un traitement en registre de recherche — et H-01 parle
     d'« infrastructure », transposée au sol sans le dire.
  3. **Objection « la gestion publique est moins efficace ».** L'article
     (l. 411-414) dit la traiter « comme une hypothèse testable » mais ne dit
     pas que le registre a déjà encodé la réponse : H-08, valeur centrale
     15 %, mesure « ce que la délégation prélève au-delà du coût de la
     régie ». Le lecteur n'est pas informé que le paramètre central suppose
     la régie moins chère.
  4. **Objection « vous spoliez les propriétaires ».** Réponse l. 418-423
     limitée au propriétaire occupant (V-02). L'objection, telle qu'un
     bailleur ou un concessionnaire la formule, vise la rente lucrative — et
     la réponse honnête est « oui, c'est V-01 » ; V-01 n'est pas cité.
  5. **Objections abandonnées sans le dire.** « Cela coûte trop cher »
     (note l. 348-349 — dans le périmètre du gabarit, question 7 « coût de
     transition »), « la baisse des prix ruine les héritiers », « si la
     construction recule… », les deux objections d'attribution (§6.3) ne
     sont ni reprises ni mentionnées comme renvoyées ; `INTRO.md` l. 731-733
     annonce « celles de la note d'origine, §6, reformulées » et le document
     de preuve §10 n'en liste que cinq.
- **Effet si retenue** : §13.4 et règle 21.20 (la critique comme fonction du
  système) ; §11.10 (« quelles critiques ont été examinées ? ») — la liste
  publiée est incomplète et son origine mal décrite.
- **Disposition proposée** : « Objections anticipées » ; supprimer la
  réponse doctrinale de l'objection 1 et ne garder que le renvoi à H-01 (en
  notant la transposition infrastructure → sol) ; ajouter à l'objection 3 :
  « le paramètre de travail H-08 suppose l'inverse ; l'étude “eau” le
  testera aux deux bornes, y compris zéro » ; citer V-01 dans l'objection 4 ;
  lister dans le document de preuve les objections de la note non reprises
  et pourquoi (mise en œuvre → article ultérieur ; coût → gabarit q. 7).

### CR-12 — « Ces quatre énoncés sont la seule partie de l'étude que les données ne peuvent ni confirmer ni infirmer » est faux, et des contraintes normatives restent hors graphe

- **Cible** : article l. 279-281 ; `INTRO.md` §11 l. 539-572 ; document de
  preuve §9 l. 132-134.
- **Gravité** : mineure.
- **Énoncé** : les quatre choix (C-01 « choix de méthode », C-02 notions
  construites, C-03, C-04) et les cinq définitions construites ne sont pas
  non plus réfutables par « une source, un contrat ou un compte ». Par
  ailleurs `INTRO.md` §11 pose cinq « contraintes normatives » (continuité du
  service, règle publique, chaque mesure tient seule, transparence des fins,
  propriété d'usage) dont seules deux ont un V (V-02, V-04) ; le document de
  preuve les invoque comme « contraintes que tout système devra respecter »
  sans nœud.
- **Preuve** : article l. 279-281 ; document de preuve l. 132-135 : « Les
  contraintes … sont dans `../INTRO.md` §11 » ; `claims.yaml` : quatre V
  seulement.
- **Effet si retenue** : §1.3 (choix de conception distincts des valeurs et
  des faits) ; le lecteur croit que tout ce qui n'est pas V est empirique.
- **Disposition proposée** : « Ces quatre énoncés, et les choix de méthode
  marqués C-xx, sont ce que les données ne tranchent pas » ; enregistrer
  V-05 (continuité du service) et V-06 (chaque mesure tient seule) ou les
  renvoyer explicitement à l'article ultérieur.

### CR-13 — Citations entre guillemets : traductions de travail attribuées au glossaire, et trois écarts de lettre

- **Cible** : article l. 50-55, 85-88, 129-131, 140-142, 237.
- **Gravité** : mineure.
- **Énoncé** : les citations en anglais et les textes juridiques
  correspondent aux fichiers figés (vérifié : S-01 « A natural monopoly
  exists in a particular market… », « are thought to exist in some portions
  of industries… », « In modern economics, rent refers to… », « Quasi-rents
  exist when… » ; S-02 « cette portion du produit de la terre… » ; S-03 « à
  qui est transféré un risque… » ; S-05 « inaliénables et
  imprescriptibles » ; S-07 « La CRE définit le coût moyen pondéré du capital
  (CMPC)… », « est de 5,0 % nominal, avant impôts »). Mais :
  1. l. 50-55 : « Selon le glossaire de l'OCDE, un monopole naturel existe
     sur un marché « si une seule entreprise peut le servir … » » — le champ
     `definition` de D-01 est en anglais ; les guillemets enferment la
     « traduction de travail » du caveat 1 (L-07), présentée comme le
     glossaire. Idem l. 85-88 pour D-02.
  2. l. 85 : « le revenu **des facteurs** de production dont l'offre est
     fixe » ≠ caveat D-02 « le revenu **d'un facteur** de production dont
     l'offre est fixe ».
  3. l. 130-131 : « ce qui serait nécessaire pour **amener le fournisseur**
     à fournir le facteur » ne correspond ni au `definition` (« the amount
     required to induce the supplier to supply the factor ») ni au caveat
     (« pour l'amener à fournir le facteur »).
  4. l. 140 : « définit le coût moyen pondéré du capital sur la base… » omet
     « (CMPC) » sans crochets.
  5. l. 237 : « inaliénable et imprescriptible » (D-14) — au singulier, et
     tiré de L3111-1 (caveat) alors que le `definition` de D-14 est
     L2111-1.
- **Effet si retenue** : L-07 est vidée de son effet là où elle compte (le
  lecteur croit lire l'OCDE en français) ; règle 21.10 sur la fidélité au
  périmètre de la source.
- **Disposition proposée** : « selon le glossaire de l'OCDE (traduction de
  travail, L-07) » ; aligner les trois libellés sur les champs `caveats` ;
  citer D-14 en renvoyant explicitement à L3111-1.

### CR-14 — Décalages entre documents de l'étude (comptes, état des livrables, contrat du site)

- **Cible** : `NEXT-STEPS.md`, `PREV-STEPS.md`, `README.md`, `CLAUDE.md`,
  `INTRO.md` §4 / §7 / §14, `claims.yaml` C-02 / L-07,
  `definitions.yaml` (en-tête), article l. 9-14.
- **Gravité** : mineure (mais nombreux).
- **Énoncé et preuve** :
  1. **Quatre ou cinq notions construites ?** C-02 : « Quatre notions sont
     construites … — rente de position (D-03), rente d'innovation (D-04),
     substituabilité (D-05), différenciabilité (D-07) et captivité (D-08) »
     (cinq ids) ; L-07 : « Quatre notions (D-03, D-04, D-05, D-07, D-08) »
     (cinq) ; `INTRO.md` l. 192 et `definitions.yaml` en-tête l. 5-6 : quatre
     (sans D-04) ; article l. 439 et `PREV-STEPS.md` l. 61 : cinq.
  2. **Hypothèses qualitatives dans le graphe.** `graph.json` : 48 nœuds
     dont H-01..H-05 (commit HEAD). `NEXT-STEPS.md` l. 13 « 43 nœuds »,
     l. 35-36 « H-01..H-03 … ne sont pas dans le graphe », l. 37-47
     « décision à prendre … enregistrer H-01..H-05 » ; `PREV-STEPS.md`
     l. 72 « 43 identifiants », l. 90-91 « H-01..H-05 restent hors graphe » ;
     `INTRO.md` §14 l. 741-746 « le contrat du graphe … n'accepte que des
     hypothèses chiffrées » contre §7 l. 336-337 « forme ajoutée au contrat
     du site le 2026-09-04 » ; `CLAUDE.md` l. 46-47 « numeric parameters
     only (H-06+ …) » contre l. 69-71 du même fichier.
  3. `INTRO.md` §14 l. 707 : « Les sources S-01 à S-06 récupérées » — sept
     sources.
  4. `README.md` l. 38 : « articles/ l'article de cadrage (à venir) ».
  5. Article l. 11 : « chaque hypothèse est nommée avec sa plage » —
     H-01..H-05 n'en ont pas ; l. 12-13 : identifiants « (D-xx, C-xx, V-xx,
     H-xx, L-xx) » alors que O-01, S-xx et I-xx sont cités.
  6. L-08 est limitée aux « pages Légifrance (S-03, S-04, S-05) » ; S-06
     (`sources.yaml` l. 141-142 : « Page rendue par navigateur ») a la même
     non-reproductibilité, notée dans `EVIDENCE.md` l. 45-47 mais pas dans le
     nœud.
  7. Nœuds jamais cités par l'article : H-03, H-04, H-05 (H-03 n'y est que
     paraphrasée l. 371-373, H-04 jamais — alors que l. 329-333 discutent
     précisément H-04 via H-07) ; par le document de preuve : L-02, L-05.
  8. `INTRO.md` §12 cite R-14, I-09, I-10 : ce sont des nœuds de
     `logement/`, non résolubles dans ce graphe ; le préfixe est dit en
     prose mais rien ne le marque.
- **Effet si retenue** : règle 21.3 (modifications non tracées : la
  décision « statement » est prise mais les documents de reprise disent
  l'inverse) ; §16 « une modification future pourra-t-elle être comparée à
  cette version ? ».
- **Disposition proposée** : passer NEXT/PREV-STEPS, README, CLAUDE.md et
  INTRO §4/§14 à l'état HEAD ; fixer « cinq » partout ; citer H-04 à
  l. 329 ; étendre L-08 à S-06 ou créer L-09 ; préfixer `logement:R-14`.

### CR-15 — Plage de H-06, niveaux de confiance et phrase de sensibilité sans justification enregistrée

- **Cible** : `hypotheses.yaml` H-06 (`description`), H-01/H-02
  (`confidence`) ; article l. 145-148 ; document de preuve §7 ;
  `INTRO.md` §15 l. 767-769.
- **Gravité** : mineure.
- **Énoncé et preuve** :
  1. H-06 : borne haute 8,0 % justifiée par « ordre de grandeur d'un actif
     concédé exposé à un risque de trafic » — aucun S/O ; `justification:
     [O-01, D-13, C-02]` ne couvre que la valeur centrale (règles 21.1, 21.2 ;
     §9 « une justification »).
  2. H-01 et H-02 sont `confidence: medium` avec pour seule justification des
     définitions ; H-03..H-05 sont `low`. Aucun critère ne distingue les
     deux niveaux (§9, §16 « leur justification est-elle visible ? »).
  3. « deux points de plus ou de moins peuvent faire disparaître ou doubler
     une rente sur un actif capitalistique » (article l. 146-148, document
     de preuve l. 108-110, INTRO l. 768-769) : affirmation quantitative sans
     calcul ni nœud (§15 : « un calcul identifié »).
- **Disposition proposée** : sourcer 8 % (ART sur les concessions
  autoroutières, ou le noter L) ; expliciter la règle de confiance dans
  l'en-tête de `hypotheses.yaml` ; remplacer la phrase de sensibilité par un
  exemple chiffré minimal (BAR, CMPC 4 % / 6 %) ou la mettre au
  conditionnel.

### CR-16 — Statut de I-01 / I-02 : interprétations sans observation, là où le cadrage promettait des hypothèses

- **Cible** : `claims.yaml` I-01, I-02 ; `INTRO.md` §2.1 l. 76-78, §8
  l. 397.
- **Gravité** : mineure.
- **Énoncé** : §4 définit I comme « signification attribuée aux observations
  ou résultats » ; I-01 et I-02 ne dépendent d'aucun O ni R (I-02 ne dépend
  que de I-01). `INTRO.md` §2.1 annonçait « chaque application à un secteur
  est une hypothèse (H-xx) confirmée ou réfutée par l'étude sectorielle » et
  §8 « Chaque ligne est une hypothèse de classement » ; le registre les a
  filées en I. Le contrat `statement` (HEAD) permettrait désormais de tenir
  la promesse.
- **Preuve** : `claims.yaml` l. 138-139 « Chaque ligne est une hypothèse de
  classement … pas un résultat » sous `type: interpretation` ;
  `graph.json` I-02 `depends_on: ['I-01']`.
- **Disposition proposée** : soit H-09.. (une par secteur, `statement`,
  `confidence: low`, `limitations: [L-04]`), soit garder I-01 mais dire dans
  le document de preuve §8 qu'il s'agit d'une interprétation de la note, pas
  d'observations.

### CR-17 — Version : aucune attache Git de l'article ni du post

- **Cible** : `post.yaml` (`version`), article l. 9-14, document de preuve
  §11 l. 176-177.
- **Gravité** : mineure (état pré-publication, mais condition de §12 / règle
  21.17).
- **Énoncé** : `post.yaml` ne porte ni `tag` ni commit ; l'article ne cite
  aucune version (l'article `logement` l. 9-10 cite « tag
  `efficacite-parc-v0.5` ») ; le document de preuve dit « commit portant ce
  document » sans hash.
- **Preuve** : `post.yaml` `version: { repo_url, evidence_doc }` ;
  `git tag` : aucun tag `monopoles-*`.
- **Disposition proposée** : ne pas déployer avant le tag
  `monopoles-cadrage-v1.0` (prévu dans `NEXT-STEPS.md` l. 30-31) et son
  report dans l'article, `post.yaml` et le document de preuve.

---

## Ce qui survit

- **La séparation V / C / H est réellement tentée et, pour l'essentiel,
  réussie sur les valeurs** : V-01 à V-04 sont isolées, dites « ne se déduit
  d'aucune donnée » (V-01), et la section « Ce que la grille ne dit pas »
  fait ce que §1.3 demande. C'est nettement mieux que la note d'origine (« ce
  n'est pas une opinion politique, c'est un constat technique »), dont
  l'étude corrige explicitement la formule (`INTRO.md` §3.3) — même si elle
  garde le mot « constat » pour la moitié (CR-1).
- **C-02 et L-07** disent honnêtement que cinq notions sont construites et
  que les traductions sont de travail ; les caveats des D-xx sont de bonne
  qualité (D-01 caveat 3 : « elle dit qu'une seule entreprise doit produire,
  pas qui doit la posséder ni qui doit encaisser » ; D-10 caveat 2 sur
  risque / recette ; D-12 sur le renvoi à L1121-3 non figé).
- **Les citations vérifiables le sont** : OCDE, Ricardo, CCP L1121-1, CG3P
  L3111-1, CRE 2025-77 correspondent aux fichiers figés (CR-13 ne porte que
  sur des traductions et trois écarts de lettre).
- **O-01 est exemplaire** au sens de §15 : valeur, unité, période, périmètre,
  source, index PDF, et sa limite (propre à RTE) est dans D-13.
- **C-03** tranche une contradiction interne de la note et le dit ; **L-03**
  et **L-06** nomment les points faibles avant qu'un relecteur le fasse ;
  **H-02** est correctement présentée comme « l'hypothèse inverse » de
  l'objection, pas comme un théorème.
- **Les chiffres logement de la note sont écartés avec leurs motifs**
  (document de preuve §10, préambule de la note archivée) — c'est la règle
  21.9 appliquée.
- **Le document de preuve dit qu'il ne calcule rien** (§4, §6) au lieu de le
  masquer, et « Ce que ces pages ne disent pas » dans l'article est complet
  sur les limites enregistrées.
- **La structure du graphe** (48 nœuds, toutes les références résolues ;
  aucun id cité par l'article ou le document de preuve n'est absent de
  `graph.json`) et la décision d'accepter des hypothèses qualitatives
  (HEAD) sont saines ; les défauts relevés portent sur le sens des arêtes,
  pas sur leur résolution.

---

## Verdict

**Bloquantes (2)**

- CR-1 — H-01 (« aucun mécanisme de marché ne discipline le prix ») présentée
  cinq fois comme un « constat » (article l. 31-33, 162-164, 257-258 ;
  INTRO l. 62, 143-145).
- CR-2 — La colonne « Hypothèse de conclusion » de I-01 loge des
  propositions (« Régie », « Ne pas reconcéder ») sans dépendre d'aucune
  valeur ; V-01 n'a aucune arête entrante.

**Sérieuses (9)**

- CR-3 — Chiffres d'une note privée non enregistrée dans H-04 / H-07, alors
  que ceux de la note d'origine sont écartés pour absence de source.
- CR-4 — H-07 (« % du parc locatif ») ne discrimine pas la France de
  Vienne ; l'étude dit elle-même que c'est le statut, pas la taille.
- CR-5 — Le titre « Là où le marché n'existe pas » affirme la conclusion que
  les études sectorielles doivent tester.
- CR-6 — « Tout tient dans le mot “normale” » : « fourniture efficace »
  porte autant et n'a ni D ni H.
- CR-7 — Sens des dépendances : H-04/H-07 justifiées par C-03, H-05 par
  C-04, limites en `justification`, D construites reliées à des sources
  comme si elles en étaient tirées, L-01/L-02 sans attache.
- CR-8 — Q1 = « Non » sur les dix lignes ; la grille n'a jamais produit de
  négatif ; « discriminante » est une surinterprétation.
- CR-9 — L'article promet des « empreintes vérifiées » au build ; le build
  copie les empreintes ; la vérification faite n'est pas committée.
- CR-10 — Onze énoncés de la note repris au présent sans ancre couvrante ;
  L-01/L-02/L-05 portent des assertions factuelles.
- CR-11 — « Objections examinées » : « formulées » pour « attendues »,
  réponse doctrinale circulaire à l'objection 1, H-08 encode déjà la réponse
  à l'objection 3, V-01 absent de l'objection 4, cinq objections abandonnées
  sans mention.

**Mineures (6)**

- CR-12 — « Seule partie que les données ne peuvent ni confirmer ni
  infirmer » exclut à tort les C et D construites ; contraintes normatives
  de INTRO §11 hors graphe.
- CR-13 — Traductions de travail entre guillemets attribuées au glossaire ;
  trois écarts de lettre (D-02, D-02 caveat 3, D-13, D-14).
- CR-14 — Décalages entre documents : quatre / cinq notions, 43 / 48 nœuds,
  contrat du site « à décider » alors que décidé, S-01..S-06 pour sept,
  README « à venir », H-04 jamais citée par l'article.
- CR-15 — Borne 8 % de H-06 sans source ; confiance « medium » sans
  critère ; phrase de sensibilité chiffrée sans calcul.
- CR-16 — I-01 / I-02 sont des interprétations sans observation ; le
  cadrage promettait des H.
- CR-17 — Aucun tag ni commit rattaché à l'article ni au post.
