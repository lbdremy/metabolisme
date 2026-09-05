# Synthèse de triage — revue contradictoire du cadrage (2026-09-04 / 05)

Synthèse de l'orchestrateur sur les quatre rapports de relecture
indépendants : sources alternatives (SA-1..SA-7, mandat réduit après une
première tentative interrompue par la limite de dépense), définitions et
hypothèses (HD-1..HD-12), scénarios d'échec (SE-1..SE-22), cohérence et
statuts épistémiques (CR-1..CR-17) — 58 objections. État examiné : commit
`59d021f` (cadrage, sept sources figées, quatorze définitions, huit
hypothèses, dix-neuf nœuds, article, document de preuve, post construit
non publié). Ce document trie ; les décisions d'intégration appartiennent
à Rémy et seront consignées dans le compte rendu final
(`../revue-contradictoire-2026-09-04.md`).

## Vérifications de l'orchestrateur

Avant triage, les allégations structurantes vérifiables ont été refaites
indépendamment (fichiers figés, graphe dérivé, pages externes rouvertes) :

| Allégation | Relecteur | Vérifiée |
|---|---|---|
| Index PDF OCDE faux : « Natural monopoly » p. 353, « Rent - OECD » p. 462 (registre : 346 / 452) | HD-8, SA-1 | **CONFIRMÉ** (`pdftotext -f 353 -l 353` / `-f 462 -l 462` trouvent les entrées ; 346 / 452 ne les trouvent pas — erreur de comptage des sauts de page en mode « layout ») |
| V-01 sans arête entrante dans `graph.json` | CR-2 | **CONFIRMÉ** — V-01, V-03, V-04, H-01, H-02, H-05, H-06, I-02 n'ont aucune arête entrante |
| Citation de D-04 coupée avant « or when their supply can be reduced over time through depreciation » | HD-3 | **CONFIRMÉ** (p. 462 : la quasi-rente OCDE inclut explicitement le capital amortissable) |
| Formule de D-13 simplifiée (« amortissement + BAR × CMPC ») alors que S-07 écrit « + IEC × coût de la dette » | HD-9 | **CONFIRMÉ** (index PDF 9, l. 968 du texte extrait) |
| Le build du site recopie les empreintes sans les vérifier ; l'article dit « empreintes vérifiées » | CR-9 | **CONFIRMÉ** (`study-to-graph.ts` : `checksum` copié, jamais recalculé) |
| Chiffres d'une note privée non enregistrée (31 %, 43 %, « moitié ») dans H-04 et H-07 | CR-3 | **CONFIRMÉ** (`hypotheses.yaml` l. 82, 144-145) |
| Q1 = « Non » sur les dix lignes de l'inventaire | SE-1, HD-4, CR-8 | **CONFIRMÉ** (tableau INTRO §8 et article) |
| Sénat, rapport n° 709 (2019-2020) : taux de rémunération du capital des concessions autoroutières passé « de 6,5 % à 5,9 % » (négociations DGITM / SCA, plan d'investissement 2017) | SE-7 | **CONFIRMÉ** (page rouverte le 2026-09-05, citation verbatim) |
| Réforme du régime hydroélectrique en 2026 (fin des concessions, droit réel de 70 ans) | SE-8 (« à vérifier ») | **CONFIRMÉ pour le texte** : rapport Sénat n° 498 (2025-2026) du 1er avril 2026 sur la proposition de loi — passage à un droit réel de 70 ans avec autorisation domaniale, résiliation des concessions > 4,5 MW, redevance progressive ; **promulgation non vérifiée** (page DAJ en 403) |
| TRI constatés 2019 des concessionnaires (ASF 4,9 / APRR 4,3 / SANEF −1,4 %) | SE-4 | page FIPECO ouverte par le relecteur (datée) ; non rouverte — retenu comme **plausible, à figer** par l'étude autoroutes |
| Loyers privés stables en part du revenu (tunnel de Friggit, IGEDD) | SE-3 | page IGEDD ouverte par le relecteur ; cohérent avec la littérature — **plausible, à figer** |
| Rapport ART, économie des concessions autoroutières, 3e éd., nov. 2024 (échéances 2031-2036, TRI projet ≈ 7 % [5,3 ; 8,8]) ; décision ARCEP n° 2025-2047 (CMPC 5,0 % nominal) ; Eaufrance / SISPEA 2022 (prix plus élevé en délégation, écart en réduction, attribué à la sélection) | SA-5, SA-6, SA-7 | ouverts et lus par le relecteur, datés — **à figer** (livrable de l'intégration) |

Aucune allégation vérifiée n'a été infirmée. Les relecteurs n'ont trouvé
aucune erreur dans les citations verbatim de D-01, D-02, D-06, D-10, D-11,
D-12, D-14 ni dans les empreintes ; les dix fichiers figés sont intègres
(SA, HD).

## Convergences entre relecteurs (les objections qui structurent)

Cinq blocs reviennent dans au moins deux rapports. Ce sont eux qui
appellent une décision.

### A. Q1 ne discrimine rien ; « monopole naturel » et « rente de position » sont deux choses (SE-1, HD-4, CR-8, CR-1)

Q1 répond « Non » dix fois sur dix : l'inventaire a été constitué de
secteurs choisis pour leur non-substituabilité, puis classés par Q2 et Q3.
D-05 agrège deux mécanismes différents — la sous-additivité des coûts
(D-01, un monopole naturel au sens de la source figée : construire un
second réseau est possible mais plus cher, la rente est bornée par le coût
de duplication) et la fixité positionnelle (D-03 : l'offre ne peut être
augmentée à aucun coût, la rente n'est pas bornée). Sous D-01 verbatim, le
logement (des millions d'offreurs, aucune économie d'échelle) et le
stationnement ne sont **pas** des monopoles naturels ; ce sont des rentes
foncières. Et l'identification est qualifiée de « constat » cinq fois alors
qu'elle repose sur un seuil non quantifié (« coût raisonnable ») et qu'elle
est enregistrée comme hypothèse H-01.

Disposition proposée : scinder D-05 en D-05a (non-duplicabilité, critère
opératoire : coût de duplication rapporté au coût du réseau, ou décision
motivée d'un régulateur) et D-05b (fixité positionnelle) ; donner à Q1 trois
réponses (substituable / non duplicable / fixe) ; ajouter à l'inventaire
des lignes témoins où Q1 répond « Oui » ou « Partiellement » (réseaux
mobiles, fibre en zone très dense, fret routier) ; reclasser logement et
stationnement sous « rente de position » et le dire dans l'objet de
l'étude ; remplacer « constat » par « hypothèse (H-01) » partout ;
requalifier « discriminante » dans le document de preuve. **Décision de
Rémy : périmètre et nom de l'objet (monopoles naturels seuls, ou monopoles
naturels et rentes de position).**

### B. Logement : C-03 n'est pas dérivé de la grille et la contredit ; H-07 est réfuté par les données de l'étude (SE-2, SE-10, HD-5, CR-4, CR-3, SE-21)

La règle Q2 dit « non partageable → accès nécessairement administré » ;
la ligne logement répond « non partageable » ; C-03 conclut « parc faiseur
de prix, propriété privée conservée ». Les deux ne peuvent être vrais :
soit Q2 n'est pas une règle générale (et il faut retirer « nécessairement
administré » pour toutes les lignes), soit C-03 est une décision extérieure
à la grille, fondée sur H-04 et sur une préférence (V-01, V-02), ce que ses
dépendances (`[V-02, I-01]`) masquent — et H-04 est justifiée par C-03
qu'elle fonde (circularité). H-07 (« 35 % [30 ; 40] du parc locatif ») est
contredit par les deux seules observations disponibles : la France (un
tiers à 43 % du locatif) est dans la plage sans être faiseur de prix, Vienne
(43 %, dénominateur différent) l'est ; la variable est l'ouverture du parc,
pas sa part, et Vienne rationne (files d'attente). Les chiffres qui portent
H-04 et H-07 viennent d'une note privée non enregistrée.

Disposition proposée : Q2 reformulée (« non partageable → la concurrence de
service ne discipline pas le prix d'accès », sans préjuger de l'allocation) ;
C-03 rattachée à V-01, V-02, H-04 et présentée comme choix fondé sur H-04,
non comme sortie de la grille ; H-07 redéfinie « part du parc locatif
ouvert à tout ménage sans condition de ressources, à loyer administré »,
sans valeur numérique tant qu'aucune estimation n'existe (le contrat du site
le permet) ; H-04 dotée d'une condition de réfutation ; chiffres de la note
privée retirés des hypothèses (ou la note enregistrée comme source, ce qui
suppose de rendre publiques ses sources — elles le sont déjà dans le dépôt
privé). **Décision de Rémy : garder le logement dans l'inventaire (sous
« rente de position », adossé à `logement/`) ou l'en retirer.**

### C. La définition mesurable de la rente n'est pas encore opératoire (HD-1, HD-2, SE-4, SE-5, SE-6, SE-7, CR-6, CR-15, SA-7)

C-02 laisse indéterminés : la **base d'actifs** sur laquelle le capital est
rémunéré (au prix d'acquisition, la rente est capitalisée et la mesure donne
zéro ; au coût historique net des subventions — ce que fait S-07 pour la
BAR, index PDF 18 — elle apparaît) ; le **« coût d'une fourniture
efficace »** (S-07 cite pourtant la notion légale : « coûts […] d'un
gestionnaire de réseau efficace », L. 341-2, index 14) ; les **postes**
(amortissement, impôt — H-06 est avant impôts, l'IS devient alors une
destination de la rente —, subventions, coûts externalisés à exclure
explicitement) ; et le **taux** : C-02 dit « une fois pour toutes » et H-06
« taux propre à chaque régulateur ». Sur les autoroutes, la rente change de
signe selon la base et selon la borne (4 / 8 %) — TRI constatés 2019 de
−1,4 à 4,9 %, taux reconnu par l'État 6,5 puis 5,9 % — : la première étude
sectorielle ne pourrait pas conclure. La borne 8 % n'a pas de source (le
TRI projet ART ≈ 7 % [5,3 ; 8,8] en donne une, SA-5) ; ARCEP fixe 5,0 %
nominal comme la CRE (SA-7), ce qui confirme la valeur centrale.

Disposition proposée : créer **D-15 « rente mesurable »** — base = coût
historique des actifs productifs net des subventions (modèle BAR, S-07),
coûts = exploitation + entretien + amortissement sur durée technique +
capital × taux, avant impôts, coûts externalisés exclus (renvoi au coût
collectif, question 6) ; H-06 devient le **taux de référence commun de
sensibilité** (deux bornes obligatoires, borne haute étayée par l'ART) et
chaque étude sectorielle enregistre son taux reconnu (ARCEP à figer, SA-7) ;
« fixée une fois pour toutes » remplacé par « forme fixée ici, paramètres
figés par secteur ». Pas de décision de fond : c'est une correction de
méthode, mais Rémy valide l'intégration.

### D. La position normative hésite entre dissiper la rente et la capter (SE-15, CR-2)

V-01 (« à l'usager sous forme de prix ») et V-04 (« prix couvrant le coût
complet ») dissipent la rente : le péage tombe au coût, il n'y a plus de
recette. Trois lignes de l'inventaire font l'inverse : capter la recette
(autoroutes « recette publique », stationnement « ne pas reconcéder ») ou
créer une rente (« tarifer la rareté » orbitale). Ce sont deux doctrines
— baisser le prix, ou substituer la collectivité au propriétaire comme
rentier — aux effets différents (demande, congestion, acceptabilité), et le
gabarit entérine l'ambiguïté (« gain pour l'usager **ou** la collectivité »).
Par ailleurs les « conclusions » par secteur sont des propositions qui
découlent de V-01, logées dans une interprétation (I-01) qui ne dépend
d'aucune valeur : V-01 est orpheline dans le graphe.

Disposition proposée : expliciter la **destination** de la rente comme
valeur ou choix distinct — prix au coût (rente dissipée), recette affectée
(rente captée, fonds dédié), budget général — et rattacher chaque ligne de
l'inventaire à l'une ; sortir la colonne « conclusion » de I-01 vers des
nœuds C ou P par secteur dépendant de V-01/V-04 ; traiter la tarification
de la rareté comme configuration à part. **Décision de Rémy : quelle
doctrine, ou les deux explicitement, secteur par secteur.**

### E. Les configurations comparées manquent la vraie alternative (SE-20, SE-6)

« Privé intégral » n'est proposé par personne pour l'eau, la chaleur ou le
rail : comme borne, il ne contraint rien. L'alternative réelle à la
collectivisation — **propriété privée sous régulation du prix** (base
d'actifs régulés type TURPE / ARCEP / Ofwat), régime effectif de la fibre,
du réseau électrique et des télécoms — est absente, alors que c'est
l'objection la plus évidente à V-01 (« pourquoi changer de propriétaire si
l'on peut réguler le prix ? »). Pour le logement, l'encadrement des loyers
(régulation du prix sans changement de propriété) manque de même. Le statu
quo autoroutier n'est pas un point fixe (échéances 2031-2036, retour à
l'État par défaut). Le porteur de risque et le classement en dette publique,
qui décident de la faisabilité des variantes de collectivisation, sont
relégués.

Disposition proposée : quatre configurations — statu quo / **privé régulé**
/ collectivisation (variantes, avec porteur de risque et classement
comptable) / privé intégral (borne facultative) ; pour le logement, ajouter
l'encadrement des loyers. Intégration proposée sans décision de fond.

## Les autres objections, par disposition

**Réécriture de H-01** (HD-6, SE-3, SE-5, CR-1) : le premier des quatre
effets est la mesure elle-même ; les trois autres ont des causes
concurrentes (coûts fixes, prix administré, rareté réglementaire, cycle du
crédit, divergence des revenus) ; contre-exemple dans les sources figées
(RTE : prix = coût efficace + rémunération, par la loi) ; sur le logement,
le loyer n'a pas décroché du revenu (signature en échec sur deux critères).
→ H-01 réécrite avec un périmètre (« non substituable **et à prix non
administré** ») et une condition de réfutation ; la signature devient un
faisceau d'indices (I) avec les contrôles à opposer ; retrait du premier
effet.

**Rente d'innovation ≠ quasi-rente** (HD-3) : la quasi-rente OCDE est le
rendement du capital fixe amortissable (marshallienne), et la taxonomie de
la source range les réseaux de ce côté. → D-04 réancrée comme notion
construite sans équivalence avec la quasi-rente ; citation restaurée en
entier ; caveat.

**Notions absentes que les sources figées fournissent** (HD-10, HD-11,
SE-16, SE-18) : exclusion (S-06), économies d'envergure, coûts
irrécupérables, barrières à l'entrée (S-01), base d'actifs régulés (S-07) ;
échelles de l'inventaire (« Partiellement », « Faible », « Totale ») non
définies ; captivité des réseaux de chaleur en partie réglementaire
(classement automatique) ; stationnement = monopole légal, offre hors voirie
substituable. → définitions ajoutées (exclusion, coûts irrécupérables,
barrières) ; échelles définies ; lignes chaleur et stationnement
reformulées.

**Inventaire secteur par secteur** (SE-8, SE-12, SE-13, SE-14, SE-17,
SE-19) : hydro — régime en réforme (proposition de loi 2026, droit réel de
70 ans : vérifié pour le texte, promulgation à confirmer) ; télécoms — le
cas témoin peut être un cas de rente privatisée sous régulation (fonds
d'infrastructure sur la fibre), et les prix bas viennent du mobile, modèle
inverse ; rail — l'open access réfute « concurrence marginale » (Paris-Lyon,
Espagne : à figer) ; électricité et hydro — la grille classe l'énergie ou
un site, pas le réseau ; eau — une régie peut transférer une rente au
budget ; orbite — infrastructure dupliquée, occupation non gratuite. → chaque
ligne reformulée en hypothèse de classement avec ses réserves ; L-04
élargie ; sources SA-5 (ART) figées pour les autoroutes.

**Sens des dépendances et statuts** (CR-7, HD-7, HD-12, CR-12, CR-16,
SE-21) : hypothèses justifiées par les choix qu'elles fondent (H-04 ← C-03,
H-05 ← C-04), limites en `justification`, notions construites reliées à des
sources comme si elles en étaient tirées, définition opératoire logée dans
C-02, valeur dans D-13, inventaire annoncé H et enregistré I. → dépendances
remises dans le bon sens ; D-15 pour la définition opératoire ; I-01 scindée
(classement H par secteur / configurations C).

**Importations de la note sans statut** (CR-10, CR-11, SE-21) : onze
énoncés au présent sans ancre (boucle locale, coût marginal de la fibre,
sortie des réseaux de chaleur, « risque faible, recette élevée », « ce qui
fonctionne » pour les télécoms, publication des comptes autoroutiers, etc.) ;
assertions factuelles dans L-01, L-02, L-05 ; section « Objections
examinées » : « formulées » pour « anticipées », réponse doctrinale
circulaire à l'objection 1, H-08 encode déjà la réponse à l'objection 3,
V-01 absente de l'objection 4, cinq objections de la note abandonnées sans
mention. → chaque énoncé ancré au conditionnel ou porté par une nouvelle
limite (L-09, propriétés physiques affirmées sans source) ; L-01/L-02/L-05
vidées de leur contenu assertif ; section renommée « Objections
anticipées » et complétée.

**H-03 / H-08** (SE-9, SA-6, CR-11) : la plage exclut zéro ; un écart de
prix régie / délégation n'est pas une rente (ressource, investissement
différé, sélection) ; Eaufrance / SISPEA 2022 confirme un écart en réduction
attribué à la sélection, littérature 2006 (écart brut 27 % avant contrôle).
→ H-08 recentrée, plage incluant zéro, sources SA-6 figées ; H-03 précisée
(écart de coût ≠ rente).

**H-05** (SE-11, HD-7) : justifiée par des nœuds qui ne la justifient pas ;
contre-exemple (Flamanville). → justification vidée, énoncé réduit à une
question ouverte, confiance faible.

**Sources et registre** (SA-1, SA-2, SA-3, SA-4, HD-8, HD-9, CR-13, CR-14,
CR-17) : index PDF corrigés (353 / 462) ; deux ISBN ; « © OCDE » et
« document public » ne sont pas des licences — redistribution des PDF non
démontrée ; OpenStax porte une clause anti-ingestion ; glossaire ART
« monopole naturel » (par le régime, non par le coût) ; « you » pour « We »,
formule D-13 complète, « quatre » notions pour cinq, comptes de nœuds, état
des livrables, absence de tag. → tout corrigé ; pour les PDF OCDE et CRE,
hébergement sous condition (URL d'origine + empreinte, fichier non servi si
la redistribution n'est pas établie) à trancher.

**Empreintes au build** (CR-9) : l'article promet une vérification que le
build ne fait pas. → soit le build recalcule les empreintes des fichiers
figés (petite extension de `study-to-graph` / `build-posts`), soit l'article
dit ce qui est vérifié et ce qui ne l'est pas. Recommandation : recalculer.

## Ce qui survit

L'isolation des valeurs (V) du reste, dans son principe ; les caveats des
définitions ; les citations verbatim vérifiées et les empreintes ; O-01 et
la valeur centrale de H-06 (confirmée par l'ARCEP) ; L-03 et L-06 ; le
gabarit sectoriel dans sa structure (à compléter d'une configuration) ; la
décision d'écarter les chiffres logement de la note ; la séparation des
trois niveaux, à condition de retirer « nécessairement administré » de Q2.

## Ce que la revue dit du cadrage dans son ensemble

Le cadrage a été écrit à partir d'un inventaire hérité de la note, puis
la grille a été construite pour le décrire : la grille n'a jamais été
confrontée à un cas où elle répond « non », la conclusion logement lui est
extérieure, et la mesure de la rente n'est pas encore définie au point
qu'une étude sectorielle puisse conclure. Rien de cela n'invalide le
programme ; cela invalide la publication en l'état. Les corrections sont
toutes faisables sans nouvelle acquisition, sauf le figement des sources
ART, ARCEP, SISPEA et Sénat identifiées par les relecteurs.
