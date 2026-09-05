# Revue contradictoire — angle SCÉNARIOS D'ÉCHEC (relecteur n°3)

- **Date** : 2026-09-04
- **Périmètre** : étude `monopoles/` (cadrage « Monopoles naturels et
  collectivisation des rentes ») — `INTRO.md`, `sources/*.yaml`,
  `evidence/claims.yaml`, `evidence/monopoles-naturels.md`,
  `articles/2026-09-monopoles-naturels-grille.md`, comparés à la note
  d'origine `exploration/2026-09-grille-deux-questions-note-de-travail.md`.
  Contexte : `logement/` (INTRO, EVIDENCE) et la note privée « Le parc
  social, fonction régulatrice ou logique volumétrique ? ».
- **État examiné** : `main` @ `59d021f` (« feat(site): Accept qualitative
  hypotheses and register the framing hypotheses »).
- **Méthode** : relecture seule, sans accès aux autres relecteurs (méthode
  `../../INTRO.md`, étape 12 « scénarios d'échec »). Pour chaque ligne de
  l'inventaire, chaque hypothèse, chaque choix et chaque valeur, j'ai
  cherché le cas réel ou le résultat plausible qui le ferait tomber, puis
  vérifié que l'étude prévoit ce cas. Les faits extérieurs sont soit
  ouverts (page lue, URL et date de consultation donnés — toutes au
  2026-09-04), soit issus d'un résumé de moteur de recherche sans ouverture
  de la page (marqué « résumé de recherche, à vérifier »), soit marqués
  « à vérifier ». Aucun fichier de l'étude n'a été modifié ; aucun de ces
  faits extérieurs n'est une source au sens de la méthode (INTRO §21.1)
  tant qu'il n'est pas figé.

Convention de gravité : **bloquante** = le raisonnement publié ne tient pas
sans correction ; **sérieuse** = une conclusion ou un nœud doit être
requalifié ou complété avant qu'une étude sectorielle s'y adosse ;
**mineure** = correction de texte ou de registre.

---

## Objections

### SE-1 — La question Q1 ne discrimine jamais : dix secteurs, dix « Non »

- **Cible** : C-01, D-05, I-01, document de preuve §8 (« la grille est
  applicable et discriminante »).
- **Gravité** : bloquante.
- **Énoncé** : dans l'inventaire (INTRO §8, article), Q1 répond « Non » sur
  les dix lignes. Le pouvoir discriminant revendiqué au §8 du document de
  preuve ne vient que de Q2 ; Q1, qui est la question qui définit le
  monopole naturel, n'a jamais été confrontée à un cas où elle répond
  « Oui ». Or de tels cas existent au cœur même des secteurs de
  l'inventaire : (a) les réseaux mobiles, où quatre opérateurs ont chacun
  déployé leur propre réseau d'accès (observatoires de déploiement ARCEP
  par opérateur, Orange / SFR / Bouygues Telecom / Free Mobile) ; (b) la
  fibre en zones très denses, où « chaque opérateur peut déployer son
  propre réseau, immeuble par immeuble », la mutualisation ne commençant
  qu'au point de mutualisation en pied d'immeuble (décision ARCEP
  n° 2009-1106 ; 106 communes, ~5,5 M de logements). La grille a donc été
  appliquée à un échantillon pré-sélectionné de secteurs dont on savait la
  réponse, ce que la méthode interdit de présenter comme un test (INTRO
  §16, « les objections sérieuses ont-elles été examinées ? »).
  Aggravation par D-05 : l'extension de Q1 à la « rareté positionnelle »
  fait répondre « Non » pour tout bien localisé (un commerce en pied
  d'immeuble, une terre agricole, un restaurant avec vue), ce qui n'est
  plus un critère de monopole naturel mais un critère de rente foncière ;
  et D-01, verbatim, définit le monopole naturel par la sous-additivité des
  coûts d'*une seule entreprise* servant un marché — ce qui ne décrit ni le
  logement (des millions d'offreurs, aucune économie d'échelle) ni le
  stationnement.
- **Preuve** : article, tableau de l'inventaire (colonne Q1) ; D-01 et
  D-05 dans `sources/definitions.yaml` ; document de preuve §8. Fibre ZTD :
  résumé de recherche (guide ARCEP « fibre optique immeubles ZTD », mars
  2019, <https://www.arcep.fr/uploads/tx_gspublication/guide-fibre-optique-immeubles-ztd_mars2019.pdf> ;
  <https://www.ariase.com/box/actualite/arcep-renforcer-mutualisation-deploiement-ftth>),
  la page ARCEP dédiée étant derrière un défi anti-robot au 2026-09-04 —
  à vérifier sur la décision 2009-1106 elle-même. Mobiles :
  <https://www.arcep.fr/cartes-et-donnees/nos-cartes/deploiement-5g/observatoire-du-deploiement-5g-juin-2026.html>
  (résumé de recherche).
- **Effet si retenue** : le titre de l'étude (« monopoles naturels »)
  n'est pas tenable pour le logement et le stationnement, qui relèvent de
  la rente foncière (D-03) sans être des monopoles naturels (D-01) ; la
  phrase « la grille est discriminante » doit être retirée du document de
  preuve ; I-01 devient un classement de secteurs *déjà* identifiés, pas
  le produit d'un critère.
- **Disposition proposée** : (1) ajouter à l'inventaire au moins deux
  lignes témoins où Q1 = « Oui » (réseaux mobiles ; fibre ZTD, ou fret
  routier) et une où la réponse est « Partiellement » (autoroutes, cf.
  SE-15) pour montrer que le critère sépare ; (2) scinder D-05 en deux
  critères distincts (rareté physique = monopole naturel D-01 ; rareté
  positionnelle = rente foncière D-03), et reclasser logement et
  stationnement sous le second, hors du champ « monopole naturel » ;
  (3) reformuler §8 du document de preuve.

### SE-2 — Logement : C-03 n'est pas dérivé de la grille, il la contredit

- **Cible** : C-03, C-01 (règle Q2), I-01 ligne logement, article
  (« Le logement est l'application la plus radicale », réponse à
  l'objection « étatisme »).
- **Gravité** : bloquante.
- **Énoncé** : la règle Q2 est énoncée comme un constat général : « Réseau
  non partageable : un opérateur unique, et un accès à la capacité
  nécessairement administré » (INTRO §5, article). La ligne logement répond
  « Non partageable ». La conséquence de la grille est donc littéralement
  « allocation administrée » — ce que la note d'origine concluait et que
  C-03 abandonne au motif que « la grille dit que le marché ne discipline
  pas le prix, pas que l'allocation doit être administrée ». Les deux
  affirmations ne peuvent être vraies : soit la règle Q2 n'est pas
  générale, et il faut le dire pour toutes les lignes (elle est aussi
  appliquée à l'eau, aux autoroutes, au stationnement), soit C-03 est une
  décision prise hors de la grille, et `depends_on: [V-02, I-01]` masque
  qu'elle repose sur H-04 (non citée) et sur une préférence politique. Plus
  profondément, la grille est faite pour des *réseaux* (L-02 le reconnaît
  pour les plateformes) : « opérateurs de service », « capacité
  partageable », « exploitant du réseau » n'ont aucun sens pour un parc de
  logements. La configuration « parc universel faiseur de prix, propriété
  privée conservée » suppose en réalité des *milliers d'opérateurs*
  coexistant sur la « ressource » sol, c'est-à-dire un réseau partageable
  — l'inverse de la ligne I-01. Enfin la réponse à l'objection
  « étatisme » (« la grille conserve la concurrence partout où le réseau
  est partageable ») est vidée par C-03 : sur le logement, la grille dit
  « non partageable » et l'étude garde quand même le marché.
- **Preuve** : INTRO §5 Q2, §8.1 ; `claims.yaml` C-03 (`depends_on`) ;
  H-04 (`justification: [C-03, L-03]`) — circularité relevée en SE-21.
- **Effet si retenue** : la ligne logement sort de la grille « monopole
  naturel » ; C-03 doit être marqué comme choix indépendant fondé sur
  H-04, avec ses dépendances réelles ; la règle Q2 doit être reformulée en
  « non partageable → concurrence de service sans effet sur le prix
  d'accès », sans préjuger du mode d'allocation.
- **Disposition proposée** : reformuler Q2 (retirer « nécessairement
  administré ») ; `C-03.depends_on: [V-01, V-02, H-04]` et dire dans
  l'article que la configuration retenue vient de H-04, pas de la grille ;
  ou, mieux, adosser la ligne logement à `../logement/` et retirer le
  logement de l'inventaire des monopoles naturels (cf. SE-1).

### SE-3 — Signature H-01 sur le logement : le prix payé par l'usager n'a pas décroché

- **Cible** : H-01, article « Objections examinées » (première
  objection), INTRO §7 H-01, NEXT-STEPS (« reste ouvert ICC / inflation »).
- **Gravité** : bloquante pour l'argument logement de l'article ; sérieuse
  pour H-01 en général.
- **Énoncé** : la question de l'étude porte sur « le prix payé par
  l'usager ». Pour un locataire, c'est le loyer. Or l'IGEDD (Friggit)
  établit que « depuis le milieu des années 1970, l'indice des loyers
  observés par l'Insee à structure constante, rapporté au revenu
  disponible par ménage, est resté presque constant : il a évolué dans un
  “tunnel” horizontal de largeur 20 % » ; ce qui a décroché depuis 2000
  est le *prix d'actif*, que la même source attribue « au premier chef
  [au] très faible niveau des taux d'intérêt ». La note d'origine le dit
  elle-même (« ×1,3 à 1,4 pour l'inflation, les loyers et le revenu »).
  Conséquences : (a) le critère « le prix s'écarte durablement du coût »
  n'est pas rempli pour le prix d'usage ; (b) le critère « les marges ne
  s'érodent pas » est *inversé* : si les prix ont doublé et les loyers
  suivi le revenu, les rendements locatifs ont baissé ; (c) la
  « signature » peut être produite par autre chose qu'une rente de
  position : baisse des taux (capitalisation d'un flux stable), rareté
  *réglementaire* de la construction (PLU, zonage — ce que D-02 appelle
  « monopoly rent », restriction artificielle, et non D-03), écarts de
  productivité entre agglomérations (les « écarts entre territoires
  comparables » se creusent aussi par les salaires). Le test de H-01 tel
  qu'énoncé ne distingue aucune de ces causes ; l'étude ne prévoit pas ce
  cas.
- **Preuve** : IGEDD, « Tunnel de Friggit et courbe de Friggit »,
  <https://www.igedd.developpement-durable.gouv.fr/tunnel-de-friggit-et-courbe-de-friggit-qu-est-ce-a3578.html>
  (page ouverte le 2026-09-04 ; publiée 31/10/2022, mise à jour
  01/08/2025) ; note d'origine §3.9 (chiffres non figés, cités ici
  seulement pour la contradiction interne).
- **Effet si retenue** : le passage de l'article qui présente H-01 comme
  « le test qui tranche » l'objection « il y a bien une concurrence entre
  logements » est renversé : sur le prix d'usage, le marché locatif
  présente deux des quatre marques d'un marché concurrentiel. L'objection
  la plus sérieuse n'est pas tranchée, elle est plutôt confortée.
- **Disposition proposée** : distinguer dans H-01 prix d'usage et prix
  d'actif ; ajouter aux quatre critères une clause de causes alternatives
  (taux, réglementation, productivité) avec la méthode qui les écarte ;
  figer les séries Insee loyers / revenu et prix / revenu (IGEDD) avant de
  reprendre l'argument ; réécrire la première objection de l'article en
  « non tranchée ».

### SE-4 — La définition mesurable de la rente ne dit pas sur quelle base d'actifs elle rémunère le capital

- **Cible** : C-02, H-06, D-13, INTRO §4 (« la rente doit être
  mesurable »), §2.3 (comparabilité entre secteurs).
- **Gravité** : bloquante.
- **Énoncé** : « ce que paie l'usager moins le coût d'une fourniture
  efficace, rémunération du capital au taux H-06 comprise » laisse
  indéterminé le *capital* auquel s'applique H-06 : coût historique, coût
  historique amorti, base d'actifs régulés (la BAR de D-13), coût de
  remplacement, ou prix d'acquisition. Sur les autoroutes — première étude
  prévue — le choix change le signe : les acquéreurs de 2006 ont payé
  14,8 Md€ ; sur cette base, le TRI actionnaire d'ASF « a déjà atteint
  4,9 % en 2019 » (APRR 4,3 %, SANEF −1,4 %), c'est-à-dire *sous* la valeur
  centrale de H-06 : rente nulle ou négative au sens de C-02 ; sur la base
  du coût historique amorti par le contribuable, la rente est massive. La
  définition, telle que fixée « une fois pour toutes les études
  sectorielles », produira donc des mesures non comparables selon la base
  que chaque étude choisira — ce qui contredit la finalité §2.3. Le
  document de preuve §7 signale la sensibilité à H-06 mais pas cette
  indétermination, qui est d'un ordre de grandeur supérieur.
- **Preuve** : FIPECO, « Fallait-il concéder et privatiser les
  autoroutes ? » (fiche du 10/12/2020, ouverte le 2026-09-04 ;
  <https://www.fipeco.fr/fiche/Fallait-il-conc%C3%A9der-et-privatiser-les-autoroutes-%3F>) :
  TRI prévisionnels 2006 / constatés 2019 / attendus à terme — ASF 7,1 /
  4,9 / 10,9 % ; APRR 9,2 / 4,3 / 11,2 % ; SANEF 8,0 / −1,4 / 7,2 % (étude
  commandée par la commission d'enquête du Sénat). Prix de cession 2006 :
  14,8 Md€ (résumé de recherche, Sénat r19-709 ; à vérifier sur le
  rapport).
- **Effet si retenue** : toute mesure de rente est indéterminée tant que la
  base n'est pas fixée ; la première étude sectorielle ne pourra pas
  conclure.
- **Disposition proposée** : compléter C-02 par un choix explicite de
  base (recommandation : base d'actifs régulés à coût historique net de
  subventions, comme D-13, *et* base d'acquisition en sensibilité), et
  dire que la « rente » mesurée sur base d'acquisition est celle payée
  d'avance à l'État en 2006 — un destinataire différent (question 5 du
  gabarit).

### SE-5 — C-02 mesure un profit économique, pas une rente de position, et sans groupe témoin

- **Cible** : C-02, D-03, D-04, H-01, INTRO §1 (« pour chaque secteur qui
  le remplit »).
- **Gravité** : sérieuse.
- **Énoncé** : « prix moins coût efficace, capital rémunéré à H-06 » est
  la définition du profit économique (surprofit). Elle ne distingue pas la
  rente de position (D-03) de la rente d'innovation (D-04) ni de la rente
  de monopole réglementaire (D-02) : une entreprise concurrentielle en
  avance technique montrera une « rente » positive ; un service d'eau en
  régie, dont le coût observé *est* le coût de référence, montrera zéro par
  construction (cf. SE-6). La distinction D-03 / D-04 n'est donc opérée
  que par Q1, en amont, et la mesure ne peut pas la tester. Et comme la
  rente n'est mesurée que « pour chaque secteur qui remplit [le
  critère] », H-01 (« là où l'infrastructure n'est pas substituable, le
  prix se décorrèle ») n'a aucun groupe de contrôle : sans mesurer la même
  chose sur un secteur substituable, rien ne peut réfuter H-01.
- **Preuve** : C-02, H-01 (`statement`), INTRO §1 et §4 (texte).
- **Effet si retenue** : H-01 est non réfutable en l'état ; la mesure doit
  être renommée (« surprofit mesuré ») et l'attribution à une position
  devenir une interprétation (I) séparée.
- **Disposition proposée** : exiger dans le gabarit (§9, question 4) un
  secteur ou segment témoin substituable mesuré de la même façon ;
  renommer la sortie de C-02 « surprofit » et réserver « rente de
  position » à l'interprétation qui l'attribue à Q1.

### SE-6 — Scénarios où la mesure donne zéro sur un monopole évident, ou positif sur un secteur concurrentiel

- **Cible** : C-02, H-06, D-10 (caveat « risque faible, recette élevée »),
  article Q4, gabarit §9 questions 3-4.
- **Gravité** : sérieuse.
- **Énoncé**, cinq scénarios concrets :
  1. *Coût efficace inobservable.* En régie, coût observé = coût
     « efficace » faute de référence : rente nulle par construction, même
     si le service perd 18,8 % de l'eau mise en distribution (rendement
     moyen national 81,2 % en 2023, SISPEA) — l'inefficacité est absorbée
     dans le coût. Symétriquement, un concessionnaire qui sous-investit
     affiche un surprofit qui est en réalité un coût différé.
  2. *Subventions croisées.* Le TURPE est identique sur tout le
     territoire : la même mesure donne une rente positive en zone dense et
     négative en zone rurale ; un agrégat national masque un transfert,
     pas une rente.
  3. *Actifs financés par le contribuable.* Réseaux de chaleur
     subventionnés (Fonds chaleur), barrages construits sur fonds publics :
     base nette de subvention → rente ; base brute → pas de rente. Retour à
     SE-4.
  4. *Risque de trafic réel.* L'article et le caveat de D-10 posent en
     règle : « sur un monopole naturel à usager captif, le risque
     transféré est faible et la recette élevée ». Contre-exemples : A65
     Langon-Pau, trafic ~40 % sous le contrat (poids lourds −66 %),
     déficit d'exploitation > 35 M€ en 2011 et 2012 ; viaduc de Millau,
     400 M€ financés sans subvention sur une concession de 75 ans. Une
     mesure ex post ignore la prime de risque ex ante ; une rente négative
     sur A65 ne signifie pas que la position n'est pas monopolistique.
  5. *Qualité de service.* La mesure prix − coût ne voit pas une baisse de
     qualité (fréquence d'entretien, délais de raccordement) : un
     concessionnaire peut convertir de la qualité en surprofit sans que la
     rente mesurée bouge de nature.
  L'étude ne prévoit aucun de ces cas (le §7 du document de preuve ne
  parle que de H-06).
- **Preuve** : SISPEA rapport 2023 (résumé de recherche,
  <https://www.ofb.gouv.fr/actualites/publication-du-13eme-rapport-national-de-lobservatoire-des-services-publics-deau-et>,
  à vérifier sur le PDF) ; A65 (résumé de recherche,
  <https://www.aquitaineonline.com/actualites-en-aquitaine/sud-ouest/a65-autoroute-langon-pau-bilan-financier-2012.html>,
  à vérifier sur les comptes d'A'liénor) ; Millau (résumé de recherche,
  <https://www.lapresse.ca/debats/200901/09/01-693375-millau-un-ppp-reussi.php>,
  à vérifier sur le contrat CEVM) ; TURPE : S-07 déjà figée.
- **Effet si retenue** : la phrase générale « risque faible, recette
  élevée » doit passer du statut d'énoncé au statut d'hypothèse (elle est
  importée de la note sans marquage) ; le gabarit doit imposer une
  décomposition surprofit = rente + prime de risque + inefficacité + coût
  différé, ou avouer qu'il ne la fait pas.
- **Disposition proposée** : marquer « risque faible / recette élevée »
  H-xx ; ajouter au gabarit (question 4) les quatre corrections ci-dessus
  comme sous-questions obligatoires, avec le mode de traitement du
  « zéro par construction » des régies.

### SE-7 — Aux deux bornes de H-06, la rente change de signe

- **Cible** : H-06, document de preuve §7, INTRO §15.
- **Gravité** : sérieuse.
- **Énoncé** : le document de preuve prévient que « deux points de taux
  peuvent faire disparaître ou doubler une rente ». C'est plus grave : sur
  les TRI constatés en 2019 (ASF 4,9 %, APRR 4,3 %, SANEF −1,4 %), la
  borne basse 4 % donne une rente positive pour ASF et APRR, la valeur
  centrale 5 % la rend nulle, la borne haute 8 % la rend négative pour les
  trois. Et l'État lui-même a reconnu des taux de 6,5 % puis 5,9 % dans le
  plan d'investissement autoroutier — au-dessus de la valeur centrale. Le
  choix de la borne contient donc toute la conclusion de la première étude,
  ce qui est exactement le risque de circularité de l'INTRO §15 déplacé
  d'un cran (non plus « définir la rente comme ce qu'on veut
  collectiviser », mais « choisir le taux qui la fait apparaître »).
- **Preuve** : FIPECO (ouvert, cf. SE-4) ; Sénat, rapport r19-709-1, page
  ouverte le 2026-09-04
  (<https://www.senat.fr/rap/r19-709-1/r19-709-130.html>) : « diminution
  du taux de rémunération du capital investi, qui est passé de 6,5 % à
  5,9 % ».
- **Effet si retenue** : « présenter la mesure aux deux bornes » ne suffit
  pas quand les bornes encadrent zéro ; il faut une règle de décision
  (quel taux pour quel type d'actif) fixée *avant* la mesure.
- **Disposition proposée** : ajouter à H-06 une table par classe de
  risque (réseau régulé sans risque de volume ; concession avec risque de
  trafic ; actif de production exposé au prix de marché), chacune figée
  sur une décision de régulateur (CRE, ART, ARCEP), et interdire de
  conclure sur un secteur dont la rente change de signe dans sa plage.

### SE-8 — H-02 est réfutable par des dispositifs existants, et le régime actuel de l'hydroélectricité est déjà périmé

- **Cible** : H-02, I-01 ligne hydroélectricité (« concessions non
  renouvelées, exploitation publique »), colonne « régime actuel », C-04
  (ordre : hydro en 3e), L-04.
- **Gravité** : sérieuse.
- **Énoncé** : (a) H-02 (« un appel d'offres capture au mieux une fraction
  de la rente à l'attribution ; les hausses ultérieures reviennent au
  concessionnaire ») est contredite par les mécanismes qui capturent en
  continu : la redevance proportionnelle de l'article L523-2 du code de
  l'énergie, due pour toute concession hydroélectrique nouvelle ou
  renouvelée, assise sur les recettes *valorisées au prix de marché* —
  donc indexée sur les hausses ultérieures ; les enchères à valeur
  actualisée des recettes (LPVR, Engel-Fischer-Galetovic, Chili — à
  vérifier), qui rendent la durée endogène et bornent la rente. Un
  résultat où la redevance capte l'essentiel de la hausse réfuterait H-02 ;
  l'étude ne dit pas ce qui la réfuterait. (b) Selon economie.gouv.fr, une
  loi « visant à relancer les investissements dans le secteur de
  l'hydroélectricité » promulguée le 29 juin 2026 substitue un régime
  d'autorisation aux concessions de plus de 4,5 MW, met fin à tous les
  contrats de concession avec indemnisation, et impose à EDF pendant vingt
  ans des enchères de capacité virtuelle sous contrôle de la CRE (accord
  de principe avec la Commission, août 2025). Si c'est exact, la ligne
  hydro de l'inventaire (« concessions d'État, contentieux européen »,
  « concessions non renouvelées ») décrit un régime disparu, et le test
  de H-02 prévu sur l'hydro (INTRO §7) n'a plus d'objet : la rente y
  sera désormais partagée par enchères de capacité, un mécanisme que la
  grille ne classe nulle part.
- **Preuve** : L523-2 (résumé de recherche,
  <https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000027720267/2014-08-24>,
  à vérifier en version en vigueur) ; loi de 2026 (résumé de recherche,
  <https://www.economie.gouv.fr/daj/la-loi-visant-relancer-les-investissements-dans-le-secteur-de-lhydroelectricite-pour-contribuer-la-transition-energetique-ete-promulguee-le-29>
  et <https://www.senat.fr/rap/l25-498/l25-498_mono.html> — **à vérifier
  impérativement** : date, numéro, contenu).
- **Effet si retenue** : L-04 (« régimes actuels non sourcés ») est
  insuffisant : au moins une ligne est fausse à la date de publication,
  pas seulement non sourcée ; C-04 doit reconsidérer la place de l'hydro.
- **Disposition proposée** : figer le texte de la loi avant publication ;
  réécrire la ligne hydro ; ajouter à H-02 la condition de réfutation
  (part de la hausse captée par la redevance ≥ x %) ; ajouter les enchères
  de capacité aux variantes de configuration (§2.4).

### SE-9 — H-03 / H-08 : la plage exclut zéro, et un écart de coût n'est pas une rente

- **Cible** : H-03, H-08, L-06, I-01 ligne eau (« Régie »).
- **Gravité** : sérieuse.
- **Énoncé** : la littérature disponible (Chong, Huet, Saussier, Steiner,
  2006, ~5 000 collectivités, régression à changement de régime) trouve
  des prix significativement plus élevés en délégation *conditionnellement
  au choix* — mais un écart de prix mesure la somme de la marge du
  délégataire, des différences de ressource et de traitement, des
  investissements réalisés et de la fiscalité, pas « ce que la délégation
  prélève ». Deux scénarios d'échec : (a) écart nul après contrôle (taille,
  ressource, densité, investissement) — la plage de H-08 (10-20 %) ne
  contient pas zéro, donc ce résultat n'est pas prévu ; (b) écart
  positif mais entièrement expliqué par le renouvellement des réseaux
  (les régies qui « coûtent moins » renouvelant moins) : l'« étalon
  d'efficacité » mesure alors un coût différé. L-06 ne nomme que le biais
  de sélection, pas ces deux cas.
- **Preuve** : Chong et al., *Review of Industrial Organization* 29(1),
  2006 (résumé de recherche,
  <https://link.springer.com/article/10.1007/s11151-006-9106-8>, à
  vérifier sur le texte) ; rendement des réseaux, cf. SE-6.
- **Effet si retenue** : H-08 doit avoir une plage contenant zéro, ou être
  déclassée en « ordre de grandeur de la note, non retenu ».
- **Disposition proposée** : `plausible_range: [0, 20]`, confiance faible ;
  reformuler H-03 : « l'écart de coût *à niveau d'investissement et de
  qualité contrôlé* » ; prévoir dans l'étude « eau » la décomposition de
  l'écart.

### SE-10 — H-04 / H-07 : un parc rationné n'est pas faiseur de prix, quelle que soit sa part

- **Cible** : H-04, H-07, L-03, C-03, article (paragraphe logement).
- **Gravité** : sérieuse.
- **Énoncé** : un parc loué sous le prix de marché est rationné : il ne
  discipline le loyer privé que s'il est une option *effectivement
  disponible* pour le locataire privé marginal. Vienne, le cas invoqué
  pour H-07, est rationnée : « the city does not publish an official
  waiting time », délai courant « roughly one and a half to two years »,
  « around 14,000 council and subsidised flats per year » attribués, et
  (résumé de recherche) 21 000 à 25 000 ménages en liste en 2023. Un
  article de recherche sur Vienne (non ouvert, 403) rapporte que les
  suppléments de localisation du privé sont passés de 4 €/m² (2010) à
  12,21 €/m² (2019) — ce qui, s'il est confirmé, montre un marché privé
  viennois en forte hausse malgré 43 % de parc régulé. Berlin
  (Mietendeckel, 2020-2021) montre le mécanisme inverse : −52 % d'annonces
  dans le segment régulé et hausse plus rapide des loyers non régulés
  (DIW). Le seuil H-07 n'est donc pas la variable qui compte : c'est la
  condition d'accès marginal (absence de file, prix d'entrée proche du
  marché). Résultat qui réfuterait H-04 : loyers privés viennois évoluant
  comme ceux des autres villes autrichiennes à parc régulé moindre ; L-03
  ne prévoit que « pas d'estimation », pas « effet inverse possible ».
- **Preuve** : wohnwahn.at, « Council housing in Vienna: the Wohn-Ticket »
  (ouvert le 2026-09-04, <https://wohnwahn.at/en/municipal-housing-vienna/>) ;
  Vienne loyers privés : Tandfonline 10.1080/12265934.2022.2110144
  (résumé de recherche, page 403 — à vérifier) ; DIW « Forward to the
  Past » (résumé de recherche,
  <https://www.diw.de/documents/publikationen/73/diw_01.c.808950.de/dp1928.pdf>,
  à vérifier) ; note privée `parc-social-fonction-regulatrice` (43 % du
  parc, ~50 % des habitants).
- **Effet si retenue** : H-07 (part du parc) doit être doublée d'un
  paramètre d'accès (délai d'attente ou taux de rotation ouvert) ; la
  base empirique de H-04 (« Vienne ») est à ce stade un contre-exemple
  possible autant qu'un appui.
- **Disposition proposée** : ajouter H-09 « condition d'accès marginal »
  ; figer une série de loyers privés viennois (Statistik Austria, déjà
  dans les sources de la note privée) et comparer à Graz / Linz avant de
  réutiliser Vienne.

### SE-11 — H-05 n'est justifiée par rien de ce que le registre cite, et un opérateur intégré a déjà échoué à optimiser

- **Cible** : H-05 (`justification: [D-06, D-07, C-04]`), INTRO §7.
- **Gravité** : sérieuse.
- **Énoncé** : D-06 (rivalité) et D-07 (différenciabilité) ne disent rien
  sur l'organisation optimale du coût système ; C-04 est l'ordre des
  études, il ne justifie pas une hypothèse — il en dépend. La
  justification est vide. Réfutation plausible : l'opérateur intégré
  historique a produit l'EPR de Flamanville (3,3 Md€ prévus en 2006,
  19,1 Md€ selon la Cour des comptes en juillet 2020) ; un « coût
  système » mal optimisé par un opérateur intégré est donc un cas
  documenté. H-05 confond l'existence d'un coût système (réel) et la
  forme d'organisation qui le minimise (question ouverte). Aucun résultat
  n'est désigné comme la réfutant.
- **Preuve** : Cour des comptes, *La filière EPR*, juillet 2020 (résumé
  de recherche,
  <https://www.goodplanet.info/2020/07/20/la-cour-des-comptes-epingle-lepr/>,
  à vérifier sur le rapport).
- **Effet si retenue** : H-05 doit être requalifiée en question de
  recherche (pas en hypothèse « confiance faible ») ou justifiée par une
  source.
- **Disposition proposée** : `justification: []` avec un caveat « énoncé
  de la note d'origine, non fondé », ou retirer H-05 du registre jusqu'à
  l'étude électricité.

### SE-12 — Le « cas témoin » télécom peut se retourner en cas de rente privatisée sous régulation

- **Cible** : I-02, I-01 ligne fibre, article (« Les télécommunications
  sont le cas témoin »).
- **Gravité** : sérieuse.
- **Énoncé** : trois faits fragilisent I-02. (a) La boucle locale fibre
  *est* dupliquée là où c'est rentable (ZTD, cf. SE-1) : le « non
  substituable » n'est vrai qu'en zone moins dense. (b) La réussite de
  prix française est attribuable à la concurrence *par les
  infrastructures* mobiles (quatre réseaux) plus qu'au partage : la
  Commission européenne (2023) classe la France parmi les plus
  compétitives en *mobile* (avec la Roumanie et le Danemark), pas parmi
  les moins chères en *fixe* (Lituanie, Danemark, Roumanie). Le meilleur
  résultat de prix français vient donc du modèle inverse de la grille
  (Q1 = « Oui »). (c) Les réseaux fibre sont détenus par des fonds
  d'infrastructure précisément parce qu'ils rendent un flux régulé :
  49,99 % de SFR FTTH (XpFibre) cédés à Allianz, AXA IM et OMERS pour
  1,8 Md€ (2018), valorisation ~8 Md€ dette comprise en 2025-2026 lors de
  la vente relancée. Si la rente mesurée selon C-02 y est positive, le
  « cas où la grille ne propose rien » devient un cas où elle devrait
  proposer quelque chose. I-02 dit « à sourcer » ; il ne dit pas qu'il
  peut être contredit.
- **Preuve** : CE, « Mobile and fixed broadband prices in Europe 2023 »
  (résumé de recherche,
  <https://digital-strategy.ec.europa.eu/en/library/mobile-and-fixed-broadband-price-europe-2023-insights-european-broadband-market>,
  à vérifier) ; XpFibre (résumé de recherche,
  <https://fr.wikipedia.org/wiki/XpFibre>, à vérifier sur les communiqués
  Altice) ; ZTD cf. SE-1.
- **Effet si retenue** : I-02 doit être reformulée en « cas à instruire »
  et non « cas témoin » ; la mention « cas où la doctrine a déjà
  fonctionné » (INTRO §8) retirée jusqu'à mesure.
- **Disposition proposée** : ajouter à I-02 les deux conditions qui la
  renverseraient (surprofit positif chez les détenteurs de réseaux ;
  prix fixe non compétitif en comparaison européenne) et le rôle des
  quatre réseaux mobiles.

### SE-13 — Rail : l'open access réfute « concurrence marginale »

- **Cible** : I-01 ligne rail, INTRO §8, note §3.2 (importée sans
  marquage : « la concurrence entre opérateurs reste possible à la marge »).
- **Gravité** : sérieuse.
- **Énoncé** : la rivalité des sillons n'empêche pas une concurrence
  effective sur les axes où la capacité n'est pas saturée. France : sur
  Paris-Lyon, depuis l'entrée de Trenitalia (2021), prix moyen en baisse de
  plus de 10 % entre 2019 et 2024 alors qu'il montait de 10 % au niveau
  national, trafic +20 % (ART, bilan 2024). Espagne : la CNMC (juillet
  2026) rapporte que la grande vitesse a « doublé les voyageurs et réduit
  les prix de plus de 40 % » depuis la libéralisation, avec Iryo et Ouigo à
  près de 50 % de part sur Madrid-Valence et Madrid-Barcelone fin 2023. La
  ligne « partiellement partageable, concurrence marginale » est donc
  contredite sur les axes qui comptent ; le classement dépend de la
  saturation de l'axe, variable que la grille n'a pas.
- **Preuve** : ART (résumé de recherche,
  <https://www.lechotouristique.com/article/hausse-de-loffre-baisse-des-prix-lart-dresse-un-bilan-positif-de-louverture-a-la-concurrence>,
  à vérifier sur le bilan ART) ; CNMC (résumé de recherche,
  <https://www.cnmc.es/prensa/inf-anual-ferro-25-20260717>, à vérifier).
- **Effet si retenue** : la ligne rail passe à « partageable là où la
  capacité n'est pas saturée ; concurrence effective sur le prix » ; la
  rente à mesurer y est celle du gestionnaire d'infrastructure (péages),
  pas celle des opérateurs.
- **Disposition proposée** : ajouter à Q2a un degré (« rivale à
  saturation ») et une colonne « capacité disponible » dans l'inventaire.

### SE-14 — Électricité et hydroélectricité : la grille change d'objet sans le dire

- **Cible** : I-01 lignes électricité et hydroélectricité, D-06 (caveat
  « unité de capacité du réseau »), D-07.
- **Gravité** : sérieuse.
- **Énoncé** : pour l'électricité, Q2a répond « rivale, avec contrainte
  temporelle » en parlant de l'*énergie* (« elle n'existe qu'au moment où
  elle est consommée »), alors que D-06 est explicitement appliquée à une
  unité de capacité du *réseau* — or un fil de transport n'est rival qu'en
  congestion, exactement comme l'autoroute classée « faiblement rivale ».
  Le classement électricité ≠ autoroutes tient à ce déplacement d'objet.
  Pour l'hydro, l'objet n'est pas un réseau mais un site de production
  vendant sur un marché de gros concurrentiel ; « partageable entre
  opérateurs de service » n'y a aucun sens, et la rente y est ricardienne
  (producteur inframarginal), ce que Q2 ne capte pas et que seule C-02
  peut mesurer. Enfin la concurrence de fourniture existe (fournisseurs
  alternatifs) : D-07 la déclare « purement comptable », ce qui est un
  jugement sur la différenciation contractuelle (garanties d'origine,
  tarification dynamique, services d'effacement), pas une propriété
  physique.
- **Preuve** : texte de l'inventaire et des définitions ; contre-exemple
  interne (autoroutes « faiblement rivales, sauf congestion »).
- **Effet si retenue** : deux lignes sur dix appliquent la grille à un
  autre objet que le réseau ; la comparabilité entre lignes (finalité
  §2.3) est rompue.
- **Disposition proposée** : ajouter une colonne « objet classé »
  (réseau / site / ressource) ; classer séparément réseau de transport et
  production ; reformuler D-07 pour dire que la différenciation
  contractuelle est possible mais ne porte pas sur le bien physique.

### SE-15 — La position normative oscille entre dissiper la rente et la capter : V-01 contre I-01

- **Cible** : V-01, V-04, I-01 (autoroutes « recette publique » ;
  stationnement « ne pas reconcéder » ; orbite « tarifer la rareté,
  affecter le produit au nettoyage »), article Q4 et « Les trois niveaux ».
- **Gravité** : bloquante (cohérence de la partie normative).
- **Énoncé** : V-01 dit que la rente doit revenir « à l'usager sous forme
  de prix » ; V-04 que le prix administré couvre « le coût complet ». Si
  ces deux valeurs sont appliquées, le péage tombe au coût et il n'y a
  plus de recette à collectiviser : la « rente » est dissipée, pas
  captée. Or trois lignes de l'inventaire proposent l'inverse : capter la
  recette (autoroutes « recette publique » ; stationnement, où la note
  précise que « l'argument ne porte pas sur le prix mais sur le
  destinataire de la recette ») ou créer une rente délibérément
  (« tarifer la rareté » orbitale et affecter le produit). Ce sont deux
  doctrines distinctes — la première baisse le prix pour l'usager, la
  seconde substitue l'État au propriétaire comme rentier (position
  georgiste) — dont les gains pour l'usager, les effets sur la demande
  (congestion) et l'acceptabilité diffèrent du tout au tout. L'étude ne
  choisit pas et le gabarit (question 7, « gain annuel pour l'usager ou
  la collectivité ») entérine l'ambiguïté avec un « ou ». La tarification
  de la congestion, mentionnée pour les autoroutes (« faiblement rivales,
  sauf congestion »), est même contradictoire avec V-01 : elle fait payer
  la rareté à l'usager.
- **Preuve** : `claims.yaml` V-01, V-04 ; INTRO §8 tableau ; note §3.8
  (« Point de vigilance rhétorique »).
- **Effet si retenue** : V-01 doit être scindée (V-01a « prix au coût »
  vs V-01b « recette publique ») et chaque ligne de l'inventaire rattachée
  à l'une ; sinon chaque étude sectorielle choisira, et les tableaux ne
  seront pas comparables.
- **Disposition proposée** : ajouter une valeur explicite sur la
  destination (prix / budget / fonds affecté) et une variante de
  configuration par destination ; traiter la tarification de la rareté
  comme configuration à part, avec son propre destinataire.

### SE-16 — Stationnement : monopole légal, pas naturel ; l'offre hors voirie est substituable

- **Cible** : I-01 ligne stationnement, D-01, D-05, D-14 (caveat sur
  la non-reconduction).
- **Gravité** : sérieuse.
- **Énoncé** : D-01, verbatim, exclut du monopole naturel ce qui naît
  « from the activities of governments ». La position de la commune sur
  le stationnement de voirie est un monopole *légal* (police du domaine
  public), pas une sous-additivité de coûts ; et l'offre hors voirie
  (parcs privés sur sol privé, garages, report modal) est un substitut.
  La ligne « sol non substituable, capacité totalement rivale » décrit
  n'importe quelle activité localisée (cf. SE-1). La conclusion « ne pas
  reconcéder » est peut-être bonne, mais elle ne découle pas de la grille :
  elle découle de D-14 (l'actif est public) et de H-02.
- **Preuve** : D-01, D-14 (`sources/definitions.yaml`).
- **Effet si retenue** : le stationnement sort du champ « monopole
  naturel » ; il reste dans l'inventaire comme « rente sur domaine public
  concédé » (autre catégorie).
- **Disposition proposée** : créer dans l'inventaire une catégorie
  « domaine public concédé » (stationnement, une partie des autoroutes)
  distincte des monopoles naturels au sens D-01.

### SE-17 — Eau : une régie peut prélever une rente par transferts, et la captivité n'est pas totale

- **Cible** : I-01 ligne eau (« Régie », captivité « Totale »), V-04.
- **Gravité** : mineure.
- **Énoncé** : la conclusion « Régie » suppose rente nulle en régie.
  Or le budget annexe d'un SPIC peut reverser un excédent au budget
  général sous conditions, recevoir des subventions d'équilibre par
  dérogation (L2224-2 CGCT, trois exceptions), et le service verse à la
  commune une redevance d'occupation du domaine public : une régie peut
  donc fixer un prix au-dessus du coût et transférer la différence — V-04
  le prévoit en principe, mais l'inventaire ne le dit pas. Captivité
  « totale » : faux pour les gros consommateurs (forages propres) et pour
  l'usage non potable.
- **Preuve** : L2224-2 (résumé de recherche,
  <https://questions.assemblee-nationale.fr/q17/17-827QE.htm>, à vérifier
  sur Légifrance) ; jurisprudence sur le reversement d'excédent : à
  vérifier (CE, Commune de Bandol, 1999, cité de mémoire — **non
  vérifié**).
- **Effet si retenue** : « Régie » n'est pas une conclusion mais une
  configuration parmi d'autres ; la mesure de rente doit inclure les
  transferts budgétaires en sortie.
- **Disposition proposée** : ajouter « transferts au budget général » aux
  flux de la question 3 du gabarit.

### SE-18 — Réseaux de chaleur : la captivité est en partie réglementaire, pas physique

- **Cible** : I-01 ligne chaleur, D-08, article Q3 (« dont on ne sort
  qu'en refaisant l'installation de l'immeuble » — importé de la note
  sans marquage).
- **Gravité** : sérieuse.
- **Énoncé** : (a) la sortie d'un réseau de chaleur pour un immeuble à
  distribution hydraulique consiste à remplacer la sous-station par une
  chaufferie (gaz, PAC) sans refaire la distribution intérieure ; le
  coût est celui d'un générateur, pas de « l'installation complète » — à
  vérifier sur un guide technique (AMORCE, ADEME), mais l'affirmation de
  l'article est énoncée sans source. (b) Le classement automatique des
  réseaux (décret n° 2022-666, loi climat et résilience) impose le
  raccordement aux bâtiments neufs ou renouvelant une installation
  > 30 kW dans le périmètre de développement prioritaire : la captivité
  y est *créée par le droit*, ce qui relève de la rente de monopole
  (restriction artificielle, D-02) et non de la rente de position (D-03).
  La grille attribue à la physique ce que fait la réglementation — et
  c'est la collectivité elle-même qui fabrique ici la captivité qu'elle
  invoque pour justifier la maîtrise publique.
- **Preuve** : décret 2022-666 (résumé de recherche,
  <https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000045667347>, à
  vérifier) ; France Chaleur Urbaine, « obligations de raccordement »
  (résumé de recherche,
  <https://france-chaleur-urbaine.beta.gouv.fr/ressources/obligations-raccordement>).
- **Effet si retenue** : D-08 doit distinguer captivité physique et
  captivité réglementaire ; la phrase de l'article doit être marquée
  hypothèse ou sourcée.
- **Disposition proposée** : deux sous-critères dans D-08 ; reformuler la
  ligne chaleur.

### SE-19 — Orbite et spectre : l'infrastructure est dupliquée et l'occupation n'est pas gratuite

- **Cible** : I-01 ligne orbite / spectre (Q1 « Non », régime actuel
  « occupation gratuite »), L-05.
- **Gravité** : mineure (aucune étude prévue), mais la ligne est fausse
  telle quelle.
- **Énoncé** : les constellations — l'infrastructure — sont dupliquées
  (Starlink, OneWeb, Kuiper, constellation chinoise) : Q1 devrait répondre
  « Oui » pour l'infrastructure et « Non » pour la *ressource* (bande de
  fréquences, coquille orbitale), incohérence de délimitation avec les
  autres lignes (cf. SE-14). Le régime « occupation gratuite » est faux
  au niveau national : l'ARCEP a autorisé Starlink (bandes 10,95-12,70 et
  14-14,5 GHz) avec une redevance de fréquences calculée selon le décret
  n° 2007-1532, et les enchères 5G (2020) tarifent déjà la rareté du
  spectre terrestre. La « rente en formation » existe, mais au niveau des
  dépôts UIT, pas de l'usage national.
- **Preuve** : ARCEP, décision 2022-1102 et consultation avril 2022
  (résumé de recherche,
  <https://www.arcep.fr/uploads/tx_gspublication/consultation-autorisation-frequences-Starlink-avril2022.pdf>,
  à vérifier).
- **Effet si retenue** : corriger la ligne et L-05.
- **Disposition proposée** : « Q1 : infrastructure Oui / ressource Non ;
  régime : dépôts UIT sans prix, licences nationales avec redevance ».

### SE-20 — Les configurations comparées : une borne épouvantail, une alternative réelle absente, un statu quo mobile

- **Cible** : INTRO §2.4, §9 question 7, article « Comment une étude
  sectorielle répondra », C-03 (trois configurations logement).
- **Gravité** : sérieuse.
- **Énoncé** : (a) « privé intégral : cession de l'infrastructure et prix
  libre » n'est proposé par personne pour l'eau, la chaleur, le rail ou
  l'électricité ; comme borne il ne contraint rien et donne l'apparence
  d'un spectre équilibré. (b) L'alternative réelle à la collectivisation —
  la *propriété privée sous régulation du prix* (base d'actifs régulés,
  type TURPE, régulation ARCEP de l'accès fibre, modèle Ofwat) — n'est pas
  dans la liste, alors que c'est le régime effectif de trois lignes de
  l'inventaire (fibre, réseau électrique, télécom) et l'objection la plus
  évidente à V-01 (« pourquoi changer de propriétaire si l'on peut réguler
  le prix ? »). (c) Le statu quo autoroutier n'est pas un point fixe : les
  contrats s'éteignent entre 2031 et 2036 et l'actif revient à l'État par
  défaut ; « collectiviser » y est le scénario de référence, et la vraie
  question est ce qui suit. (d) Les variantes de collectivisation (régie,
  entreprise publique, concession à recette publique avec exploitation au
  forfait) ne se distinguent que par le porteur de risque et le classement
  en dette publique — critère relégué en question 8 alors qu'il décide de
  la faisabilité (la note d'origine §7 le disait : « un parc exclusivement
  pauvre est un parc dont la dette compte »). Pour le logement, la même
  faille : le « privé intégral » (parc social cédé) est un épouvantail,
  et l'encadrement des loyers — la régulation du prix sans changement de
  propriété, en vigueur à Paris et Lyon — est absent des trois
  configurations.
- **Preuve** : INTRO §2.4, §8.1, §9 ; ART, échéances 2031-2036 (résumé
  de recherche,
  <https://www.autorite-transports.fr/actualites/lautorite-de-regulation-des-transports-art-a-publie-ce-samedi-30-novembre-2024-son-3eme-rapport-sur-leconomie-generale-des-concessions-autoroutieres/>).
- **Effet si retenue** : le gabarit impose quatre configurations et non
  trois ; le « privé intégral » est remplacé ou complété par « privé
  régulé » ; la question 8 (dette, porteur de risque) remonte dans la
  question 7.
- **Disposition proposée** : §2.4 : « statu quo / privé régulé /
  collectivisation (variantes, avec porteur de risque et classement
  comptable) / privé intégral (borne, facultative) » ; pour le logement,
  ajouter « encadrement des loyers ».

### SE-21 — Contradictions internes entre INTRO, article, registres et document de preuve

- **Cible** : C-02, L-07, article (« Ce que ces pages ne disent pas »),
  `definitions.yaml` (en-tête), INTRO §4, H-04, H-07, H-05, INTRO §6.1,
  document de preuve §8, NEXT-STEPS.
- **Gravité** : sérieuse pour (b) et (e) ; mineure pour le reste.
- **Énoncé** :
  - (a) Nombre de notions construites : l'en-tête de `definitions.yaml`
    et INTRO §4 disent quatre (D-03, D-05, D-07, D-08) ; C-02 dit
    « Quatre notions » puis en liste cinq ; L-07 dit « Quatre notions »
    et en liste cinq ; l'article dit « Cinq notions ». D-04 est ou n'est
    pas construite selon le fichier.
  - (b) Circularité de justification : H-04 est justifiée par C-03 ;
    H-07 par H-04 et C-03 ; C-03 est limitée par L-03, qui porte sur
    H-04/H-07. La décision (C-03) justifie l'hypothèse (H-04) qui la
    fonde. Une décision ne justifie pas une hypothèse (INTRO §9 :
    « justification visible »).
  - (c) H-05 justifiée par C-04 (cf. SE-11).
  - (d) INTRO §6.1 : la rente de position « ne finance rien » ; I-01
    orbite : « affecter le produit au nettoyage » ; note §6.2 : la rente
    finance l'acquisition d'actifs. Cf. SE-15.
  - (e) L'article importe de la note, sans statut, des énoncés généraux :
    « Sur un monopole naturel à usager captif, le risque transféré est
    faible et la recette élevée » (contredit, SE-6) ; « le coût marginal
    d'un utilisateur supplémentaire [sur la fibre] étant proche de zéro »
    (non sourcé) ; « dont on ne sort qu'en refaisant l'installation de
    l'immeuble » (SE-18) ; « la confusion entre le deuxième et le
    troisième niveau est ce qui permet de présenter un transfert de rente
    […] comme une ouverture à la concurrence » (thèse de la note §2 sur
    les autoroutes, présentée comme évidence).
  - (f) Document de preuve §8 : « la grille est applicable et
    discriminante » — contredit par dix « Non » (SE-1).
  - (g) `NEXT-STEPS.md` point 2 présente l'entrée des H-01..H-05 dans
    le graphe comme « décision à prendre » ; le commit examiné (59d021f)
    l'a faite ; le document de preuve §11 dit « 19 nœuds » alors que
    `EVIDENCE.md` compte 5 hypothèses directrices + 3 paramètres en plus.
    Cohérent mais à mettre à jour.
  - (h) `hypotheses.yaml`, H-04 : « loyers inférieurs de 31 % » et
    « Vienne : 43 % du parc, environ la moitié des habitants » sont des
    chiffres tirés d'une note *privée* non figée dans `monopoles/`
    (« dépôt privé ») ; ils entrent dans un registre public sans source
    S-xx de l'étude — c'est un réimport de chiffres par un autre chemin
    que celui que L-04 interdit.
- **Preuve** : lecture croisée des fichiers cités, HEAD 59d021f.
- **Effet si retenue** : (a) et (g) : texte ; (b) et (c) : réécrire les
  `justification` ; (e) : marquer H ou sourcer ; (h) : figer les sources
  de la note privée dans `monopoles/sources/` ou retirer les chiffres du
  registre.
- **Disposition proposée** : passe de cohérence sur les cinq fichiers ;
  règle : une `justification` ne cite jamais un C-xx.

### SE-22 — Ce qui renverserait chaque conclusion (synthèse demandée)

- **Cible** : C-01..C-04, I-01, I-02, V-01..V-04.
- **Gravité** : — (récapitulatif ; les gravités sont celles des
  objections référencées).
- **Énoncé** :

| Nœud | Observation qui le renverserait | Prévu par l'étude ? |
|---|---|---|
| C-01 (grille) | Un secteur où Q1 = « Oui » produit la signature H-01 (ex. : mobile en zone rurale), ou un secteur Q1 = « Non » où le prix suit le coût (fibre régulée) : Q1 ne prédit pas la rente | Non (SE-1, SE-5) |
| C-02 (rente mesurable) | Deux bases d'actifs légitimes donnant des signes opposés sur le même secteur (autoroutes 2006) ; un secteur concurrentiel affichant un surprofit | Non (SE-4, SE-5) |
| C-03 (logement) | Un parc régulé large mais rationné n'infléchissant pas les loyers privés (Vienne, à mesurer) ; un encadrement des loyers obtenant le même effet sans parc | Partiellement (L-03), pas le second cas (SE-10, SE-20) |
| C-04 (ordre) | Régime hydro modifié par la loi (SE-8) ; comptes des SCA insuffisants pour isoler une concession (INTRO §15) | Non pour le premier |
| I-01 (inventaire) | Toute ligne : voir SE-1, SE-13, SE-14, SE-16, SE-18, SE-19 ; globalement, une ligne où la grille classe un objet qui n'est pas un réseau | Non (chaque ligne est dite « hypothèse » sans condition de réfutation) |
| I-02 (télécom) | Surprofit positif chez les détenteurs de réseaux fibre ; prix fixe non compétitif ; prix bas expliqués par la concurrence d'infrastructures mobiles | Non (SE-12) |
| V-01 (rente → prix) | Non réfutable par des données (valeur) ; mais rendue inopérante si l'étude choisit « recette publique » (SE-15) | Contradiction interne |
| V-02 (propriété d'usage) | Une configuration logement qui touche le propriétaire occupant par la baisse de valeur de son bien (la note §6.2 le reconnaît : primo-accédants endettés) — V-02 protège l'occupation, pas la valeur | Non : l'article dit « ce que devient la valeur des actifs […] est un poste du tableau », sans dire que V-02 ne couvre pas ce cas |
| V-03 (rente d'innovation légitime) | Le brevet (L-01) : rente d'innovation non substituable pendant vingt ans — V-03 dit « tant que la ressource reste substituable », ce qui exclut le brevet de la légitimité sans le dire | Partiellement (L-01) |
| V-04 (rente visible) | Une régie qui transfère au budget général sans compte séparé (SE-17) ; V-04 n'a pas de critère de visibilité mesurable | Non |

- **Preuve** : objections ci-dessus.
- **Effet si retenue** : chaque nœud C/I devrait porter dans `claims.yaml`
  une clause « ce qui le renverserait », comme la question 9 du gabarit
  l'exige des études sectorielles.
- **Disposition proposée** : ajouter un champ `falsified_by` (texte) aux
  nœuds C et I du cadrage, ou une section dédiée dans le document de
  preuve §10.

---

## Ce qui survit

- **La séparation des cinq plans** (identification / destinataire /
  mesure / coût / conception) et la séparation constat / valeur (INTRO
  §3.3, article « Ce que la grille ne dit pas ») sont solides et
  correctement marquées ; V-01 est bien isolée comme valeur. Les
  objections ci-dessus portent sur le contenu des plans, pas sur leur
  séparation.
- **Q2 (rivalité × différenciabilité) et Q4 (concurrence pour / sur le
  marché, exploitation au forfait sans transfert de recette)** sont les
  deux apports discriminants de la grille ; ils survivent aux
  contre-exemples à condition d'ajouter à Q2a un degré (saturation, SE-13)
  et de ne pas énoncer « nécessairement administré » (SE-2).
- **Q5 (où va la recette)** comme point d'entrée empirique est la bonne
  méthode ; c'est ce qui manque le plus à la note d'origine et ce qui
  rend les études sectorielles instruisables.
- **Le refus des chiffres non sourcés de la note** (préambule de la copie
  archivée, INTRO §12, document de preuve §10) est exemplaire — à
  l'exception des réimports relevés en SE-21(e) et (h).
- **L-03, L-04, L-06** anticipent correctement trois attaques ; L-01,
  L-02 nomment honnêtement les zones grises. Le problème n'est pas
  l'absence de limites mais leur portée : elles disent « non sourcé »,
  rarement « peut être faux dans l'autre sens ».
- **H-02 comme hypothèse et non théorème** est la bonne posture ; elle
  survit si on lui donne sa condition de réfutation (SE-8).
- **La ligne eau et la ligne chaleur** restent les cas les plus proches
  d'un monopole naturel au sens strict de D-01 ; les objections SE-17 et
  SE-18 les précisent sans les renverser.
- **L'ordre des études (C-04)** — autoroutes puis eau — est justifié par
  la disponibilité des données et survit, sous réserve de la place de
  l'hydro (SE-8) et d'avoir fixé la base d'actifs avant d'ouvrir
  `autoroutes/` (SE-4).

---

## Verdict

**Bloquantes (5)**

- SE-1 — Q1 répond « Non » dix fois sur dix ; la grille n'a jamais été
  confrontée à un « Oui » ; D-05 étendue à la rareté positionnelle attrape
  tout bien localisé et contredit D-01.
- SE-2 — C-03 (logement) n'est pas dérivé de la grille et contredit la
  règle Q2 « non partageable → accès administré » ; la grille n'a pas de
  sens pour un objet qui n'est pas un réseau.
- SE-3 — Pour le logement, le prix payé par l'usager (loyer) n'a pas
  décroché du revenu (IGEDD) ; la signature H-01 échoue sur deux critères
  et peut être produite par les taux, la réglementation, la productivité.
- SE-4 — C-02 ne fixe pas la base d'actifs à laquelle s'applique H-06 ;
  sur les autoroutes la rente change de signe selon la base (TRI
  constatés 2019 : 4,9 / 4,3 / −1,4 %).
- SE-15 — V-01/V-04 (rente dissipée dans le prix) contredisent trois
  lignes de l'inventaire (rente captée comme recette publique ou créée
  par tarification de la rareté) ; deux doctrines non départagées.

**Sérieuses (13)**

- SE-5 — C-02 mesure un surprofit, pas une rente de position ; H-01 sans
  groupe témoin est non réfutable.
- SE-6 — Cinq scénarios (coût efficace inobservable, subventions
  croisées, actifs subventionnés, risque de trafic réel — A65, Millau —,
  qualité) donnent zéro sur un monopole ou positif ailleurs ; « risque
  faible, recette élevée » est un énoncé général non marqué.
- SE-7 — Aux bornes 4 / 8 %, la rente autoroutière change de signe ;
  l'État a reconnu 6,5 puis 5,9 %.
- SE-8 — H-02 réfutable par la redevance L523-2 et les enchères LPVR ;
  la ligne hydro décrit un régime que la loi de juin 2026 (à vérifier) a
  supprimé.
- SE-9 — H-08 exclut zéro ; un écart de prix régie / DSP n'est pas une
  rente (coût différé, ressource, investissement).
- SE-10 — Un parc rationné (Vienne : 1,5-2 ans d'attente) n'est pas
  faiseur de prix ; H-07 n'est pas la bonne variable ; Berlin montre
  l'effet inverse possible.
- SE-11 — H-05 est justifiée par des nœuds qui ne la justifient pas ;
  Flamanville contredit l'optimisation par l'opérateur intégré.
- SE-12 — Le cas témoin télécom peut être un cas de rente privatisée
  (fonds d'infrastructure sur la fibre) ; les prix bas français viennent
  du mobile, modèle inverse de la grille.
- SE-13 — L'open access ferroviaire (Paris-Lyon −10 %, Espagne −40 %)
  réfute « concurrence marginale ».
- SE-14 — Électricité et hydro : la grille classe l'énergie ou un site,
  pas le réseau ; comparabilité rompue.
- SE-16 — Stationnement : monopole légal exclu par D-01 ; offre hors
  voirie substituable.
- SE-18 — Chaleur : captivité en partie réglementaire (classement
  automatique) ; « refaire l'installation » non sourcé.
- SE-20 — Configurations : « privé intégral » épouvantail, « privé
  régulé » et « encadrement des loyers » absents, statu quo autoroutier
  mobile, porteur de risque relégué.
- SE-21(b)(e) — Justifications circulaires (H-04 ← C-03 ← L-03) ; énoncés
  généraux importés de la note sans statut.

**Mineures (4)**

- SE-17 — Eau : une régie peut transférer une rente au budget général ;
  captivité non totale.
- SE-19 — Orbite : constellations dupliquées ; redevances de fréquences
  existantes (ARCEP / Starlink).
- SE-21(a)(c)(d)(f)(g) — Quatre / cinq notions construites ; H-05 ← C-04 ;
  « ne finance rien » vs « affecter le produit » ; « discriminante » ;
  NEXT-STEPS à mettre à jour.
- SE-21(h) — Chiffres de la note privée (31 %, 43 %) dans un registre
  public sans source figée dans l'étude.

SE-22 (tableau des renversements) est un récapitulatif sans gravité
propre ; sa disposition (`falsified_by` sur les nœuds C et I) est
recommandée.
