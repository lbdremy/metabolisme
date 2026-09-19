# Revue contradictoire de R-18 / I-18 — hypothèses, définitions et scénarios d'échec

**Objet.** Le résultat R-18 (article 3, « le flux ») et son interprétation I-18 :
par zone d'emploi, la construction neuve (Sitadel S-54, logements commencés
2017-2022) couvre-t-elle la formation de ménages (millésimes censitaires
2016 → 2022, S-11) ? Nœuds instruits : C-16, O-41, T-18, R-18, I-18, L-34 ;
contexte R-07/I-07, L-19, L-32, P-01, I-15 ; D-05, D-24 ; S-54, S-55 ; H-08 ;
`core/flux.py`, `build_flux` (`shell/build.py`) ; artefact
`data/processed/flux-construction-menages-ze.json` ; DEC-21..DEC-24 ; section
R-18 du document de preuve (`efficacite-parc-immobilier.qmd`).

**Méthode.** Étape 12 de la méthode (INTRO §14) et §13.4 : chercher une
définition alternative, un double comptage, une confusion stock/flux, une
hypothèse implicite, une causalité non démontrée, une donnée plus récente, un
ordre de grandeur incohérent, un scénario d'échec. Relecteur unique (DEC-24 :
hypothèses/définitions et scénarios d'échec fusionnés). Chaque objection porte
une gravité (haute / moyenne / basse), un énoncé, une preuve (nœud, ligne,
chiffre) et une disposition proposée. Tous les chiffres « recalculés » le sont
depuis les sources figées du dépôt, avec les fonctions de la chaîne
(`flux.flux_by_ze`, `tension.tension_by_ze` aux centraux H-08 = 6 %,
H-12 = 0,75) ; le script est dans le scratchpad de session (non commité —
règle §21.4 : les recalculs à conserver devront entrer dans un notebook de
vérification ou dans `core/flux.py`). Le cadre recalculé reproduit
l'artefact à l'unité près (347 340 / 335 470 / − 5 253 / + 20 423 /
15 198 / 10,6) : les objections ne portent pas sur l'exécution, elles
portent sur ce que la mesure mesure.

Rien dans ce rapport ne modifie un nœud ; les dispositions sont des
propositions pour l'intégration.

---

## A. Objections « hypothèses et définitions » (HD)

### HD-1 — Le « ratio de production » est une quasi-identité comptable ; il mesure la dérive de structure, pas la couverture d'un besoin

**Gravité : haute.** C'est l'objection qui conditionne la lecture de tout
R-18/I-18.

**Énoncé.** Dans le recensement, ménages = résidences principales (D-05,
caveat 2 ; vérifié : écart P22_MEN − P22_RP = 0 sur 30 888 593). Donc
« ménages formés » ≡ ΔRP, et le besoin C-16 = ΔRP / (1 − RS − vac) est
exactement ce que serait Δparc si la structure 2022 s'était maintenue. Le
ratio se décompose algébriquement :

    ratio = commencés / besoin = (commencés / Δparc) × (Δparc / besoin)

Le second facteur ne dépend que de la dérive de structure 2016 → 2022
(ΔRS, Δvac) ; le premier, du délai de livraison, des démolitions et des
écarts de champ (HD-5). Aucun des deux ne dit si les ménages qui auraient
voulu se former ont pu le faire : un ménage ne se forme que dans un logement
qui existe, donc là où la construction manque, la formation de ménages est
basse ET le ratio vaut ~1. La mesure est aveugle à la pénurie qu'elle
prétend détecter.

**Preuve.**
- Par ZE (≥ 200 ménages formés/an, n = 211) : Spearman(Δparc/besoin, Δ part
  RS+vac 2016→22) = 0,954 ; Spearman(ratio, Δ part RS+vac) = 0,677. Le
  ratio suit la dérive de structure.
- Les quantiles de Δparc/besoin sont serrés autour de 1 (p25 0,79, médiane
  0,92, p75 1,04) et ceux de commencés/Δparc aussi (0,90 / 1,02 / 1,14) :
  la médiane du ratio à 0,99 (artefact `ratio_production.toutes.median`)
  est une propriété de construction, pas une observation.
- Corollaire : « le ratio n'est pas corrélé au coût (rho − 0,06) » (R-18) et
  « à cette maille, la construction ne suit pas la cherté » — c'est le
  résultat attendu d'une quasi-identité, pas une découverte sur la
  construction. À l'inverse, Spearman(formation %/an, commencés pour 1 000
  logements) = 0,861 (0,735 en ZE tendues) : l'intensité de construction et
  la formation de ménages sont la même chose vue de deux côtés.
- Paris (I-18 : « construit 1,8 fois sa formation de ménages ») :
  1,84 = 1,28 (commencés/Δparc) × 1,44 (Δparc/besoin). Δparc 27 328/an =
  Δménages 16 514 + ΔRS 5 139 + Δvacants 5 674 : **40 % de la croissance du
  parc parisien 2016-2022 est allée en résidences secondaires et en
  vacants**, et la formation de ménages y est de 0,55 %/an contre 0,94 en
  France (et 0,28 %/an sur 2011-2016). Ce profil est exactement celui de la
  causalité inverse que L-34(6) évoque en une ligne : ce n'est pas « Paris
  couvre sa formation de ménages », c'est « à Paris, la formation de ménages
  est bornée et le neuf nourrit RS et vacance ».

**Disposition proposée.** Requalifier R-18 : la sortie première n'est pas
un « ratio de production » mais la **décomposition observée de la
croissance du parc** par ZE (Δménages, ΔRS, Δvacants, écart commencés −
Δparc), que le cadre calcule déjà en partie (P16_RSECOCC/P16_LOGVAC sont
dans S-11, pas encore dans `CENSUS_FLOW_COLS`). Renommer le ratio (« ratio
de structure » ou « commencés / croissance à structure constante ») et
retirer de I-18 tout énoncé qui le lit comme une couverture de besoin. Un
besoin de flux exogène demanderait une mesure de la demande indépendante du
parc : projections de ménages (INSEE Omphale), cohabitation contrainte
(jeunes adultes chez leurs parents, RP), demandes de logement social (SNE),
ou le signal-prix de R-16 — à instruire, ou à déclarer non instruit (§21.18).

### HD-2 — C-16 contient une hypothèse, pas une convention : la part du neuf affectée en RS, et elle renverse le signe des ZE tendues

**Gravité : haute.**

**Énoncé.** C-16 et DEC-24 affirment « aucune hypothèse nouvelle ». Or le
dénominateur (1 − RS − vac) suppose que chaque logement neuf est affecté
selon la structure 2022 de la ZE — à Briançon 3,3 logements par ménage
formé, à Challans 1,7 —, et la variante « hors RS » suppose l'inverse
(zéro RS). Entre les deux, le solde des ZE tendues passe de − 5 253 à
+ 20 423/an. Une grandeur qui renverse un signe publié est une hypothèse au
sens d'INTRO §9 (identifiant, valeur centrale, plage, confiance, résultats
affectés) ; la déclarer « convention de mesure » contrevient à §21.3 et
§21.8, et a servi de justification à DEC-24 (trois relecteurs au lieu de
quatre).

**Preuve — ce que l'observation dit de l'hypothèse.** L'affectation 2016-2022
est observable dans S-11 :
- Agrégat des 97 ZE tendues : Δparc 175 100/an = Δménages 150 057 +
  ΔRS 22 762 + Δvac 2 282. ΔRS/Δparc = 13,0 % ≈ part RS 2022 13,3 % :
  à l'agrégat, la composante RS de C-16 est **réalisée** (12,6 % des
  logements commencés en ZE tendues sont devenus des RS) ; la variante
  « hors RS » n'est donc pas « l'autre borne honnête » de ce qui s'est
  passé, c'est un contrefactuel de politique d'affectation.
- Mais dans les ZE les plus touristiques, la part RS se dilue : Perpignan
  ΔRS/Δparc 9 % (part 30 %), Bayonne 11 % (24 %), Toulon 8 % (19 %),
  Les Sables-d'Olonne 1,5 % (36 %), Fréjus < 0 (38 %). Le besoin C-16 y
  **surestime** : Perpignan besoin 4 621 pour un Δparc observé de 3 244.
- La composante vacance, elle, n'a pas tenu : en ZE tendues la vacance
  passe de 6,43 % à 6,08 % (Δvac/Δparc = 1,3 % contre 6,1 % supposé). Ce
  qui a « absorbé » le manque de flux, ce n'est pas la RS, c'est la
  vacance qui a baissé — l'inverse de la détente que P-01 vise.
- Variante « RS observée » (besoin = (ménages formés + max(ΔRS, 0)) /
  (1 − vac 2022)) : solde des ZE tendues − 4 133/an, 56 ZE déficitaires
  (13 212/an). Classement des déficits : Marseille − 1 699, Montpellier
  − 1 003, Est-littoral (Guyane) − 938, Bayonne − 721, Toulon − 714,
  Narbonne − 674, **Toulouse − 537, Bordeaux − 396**, Digne − 366,
  Perpignan − 320. Le « déficit littoral et touristique » de I-18 se
  contracte, le déficit métropolitain (Marseille, Montpellier, Toulouse,
  Bordeaux) apparaît.

**Disposition proposée.** Créer une hypothèse H-21 « part des logements
neufs affectée en résidence secondaire », plage [0 ; part RS 2022], valeur
centrale = ΔRS/Δparc observé 2016-2022 par ZE (borné à [0, part RS]),
confiance basse, `affects: [R-18]` ; publier les trois bornes (C-16
structure constante / RS observée / hors RS). Corriger C-16 et DEC-24.

### HD-3 — La vacance à « maintenir » est celle de 2022, que R-07 juge insuffisante ; le besoin de flux ne vise pas H-08, et le flux n'ajoute pas de vacants

**Gravité : moyenne** (effet arithmétique petit, effet de cohérence grand).

**Énoncé.** C-16 maintient la part de vacants 2022 (médiane 6,16 % en ZE
tendues au recensement, 4,89 % en vacance disponible R-07). Un flux qui
« couvre » au sens de C-16 laisse donc la ZE aussi tendue qu'en 2022 ; il ne
contribue pas à la détente. Le besoin de flux cohérent avec P-01 est celui
qui maintient la structure **après** la détente (vacance à H-08).

**Preuve.** Besoin des ZE tendues à vacance max(vac 2022, H-08) : 186 783
à 6 % (+ 1 340/an), 188 504 à 7 % (+ 3 061) — petit, parce que la vacance
censitaire y est déjà proche de 6 %. Mais l'observation tranche
davantage : Δvacants en ZE tendues = + 2 282/an sur 2016-2022 ; à ce rythme,
ajouter les 194 488 vacants disponibles de R-07 prendrait 85 ans. Et dans les
51 ZE tendues « excédentaires » de R-18, la part de vacants a **baissé**
(médiane − 0,20 pt) tandis que la part RS montait (+ 0,36 pt) : le surplus
de flux n'y a pas détendu, il a nourri la RS. L'énoncé de I-18 « le stock
[…] n'est pas rattrapé par le flux là où le flux est couvert » est donc
vrai, mais pour une raison qu'il ne donne pas : couvert au sens de C-16 ne
produit aucune détente.

**Disposition proposée.** Publier le besoin à H-08 (aux trois bornes) à
côté du besoin C-16 ; ajouter à L-34 que « couvrir le flux » (C-16)
n'entame pas le besoin de stock R-07 ; réécrire la phrase de I-18.

### HD-4 — Fenêtres : la fenêtre 2017-2022 est la plus haute des fenêtres de six ans disponibles, et elle n'est pas alignée sur la livraison

**Gravité : moyenne.**

**Énoncé.** Les millésimes 2016 (enquêtes 2014-2018) et 2022 (2020-2024) sont
centrés sur 2016 et 2022 ; le parc du millésime 2022 contient les logements
livrés jusqu'au centre de la fenêtre. Un logement commencé est livré 12 à
24 mois plus tard ; les commencés 2021-2022 ne sont donc pas dans le parc
2022. La fenêtre alignée sur la LIVRAISON est plutôt 2015-2020 (ou
2014-2019), pas 2017-2022. La date de prise en compte ajoute un décalage
dans le même sens (D-24 : remontée « dans les dix-huit mois »), qui pousse
aussi vers l'aval. DEC-23 aligne la fenêtre de construction sur les
millésimes comme si commencé = livré.

**Preuve** (totaux nationaux de l'extrait S-54, communes jointes) :
- Moyenne 2017-2022 : 349 169 ; 2016-2021 : 343 366 ; 2015-2020 : 334 853 ;
  2018-2023 : 330 344 ; 2013-2024 : 318 051. **2017-2022 est la fenêtre
  de six ans la plus haute de la série** (2017 = 377 769, + 21,7 % sur
  2016, année record d'autorisations 502 373).
- Ratio national selon la fenêtre : 1,04 (2017-22) ; 1,02 (2016-21) ; 1,00
  (2015-20) ; 0,98 (2018-23) ; 0,95 (2013-24). Le signe du solde national
  (+ 11 871) tient à la fenêtre ; celui des ZE tendues passe de − 5 253 à
  − 16 435 (2018-2023) et − 22 059 (2013-2024).
- Le résidu « disparitions implicites » (HD-5) tombe de 15 198 (2017-22) à
  2 711 (2015-20) et − 2 036 (2014-19) : le résidu est d'abord un artefact
  de fenêtre.
- La part des commencés 2022 réels enregistrés en 2023 n'est **pas
  mesurable** dans le dépôt : DEC-22 a figé un extrait annuel (« les mois
  ne sont plus dans le dépôt ») et la série « en date réelle » du SDES n'est
  pas figée. Direction du biais : au bord droit, une partie des commencés
  2022 est en 2023 (sous-estime 2017-22), au bord gauche une partie des
  2016 est en 2017 (surestime) ; sur six ans cela se compense à peu près —
  mais le décalage de livraison, lui, ne se compense pas.

**Disposition proposée.** Publier le ratio sur trois fenêtres (2015-2020 /
2017-2022 / 2018-2023) et retenir comme centrale une fenêtre décalée d'un
à deux ans vers l'amont ; figer la série nationale « en date réelle
estimée » du SDES (source à enregistrer) comme arbitre du décalage ;
compléter D-24 avec le délai commencé → livré (mesurable dans Sitadel par
les DAACT : non figé).

### HD-5 — « Disparitions implicites = 15 198/an » : un résidu qui change de signe avec la fenêtre et qui contient des erreurs de champ ; pas publiable comme chiffre

**Gravité : haute** (le chiffre est dans R-18 et O-41 ; L-34(2) dit
« résidu, pas mesure » mais le nombre est publié seul).

**Preuve.**
- Sensibilité à la fenêtre (HD-4) : 15 198 → 2 711 → − 2 036. Un chiffre
  dont le signe dépend d'un décalage de deux ans n'a pas de contenu.
- Distribution par ZE : **130 ZE sur 305 ont un résidu négatif** (le parc
  croît plus que les commencés) ; somme des négatifs − 16 337, des positifs
  + 31 535 ; quantiles de résidu/commencés : p10 − 0,28, médiane + 0,05,
  p90 + 0,35. Le 15 198 est la différence de deux masses de sens opposé.
- Les négatifs extrêmes sont des erreurs de champ, pas des « apparitions » :
  Guyane Est-littoral − 842/an (parc + 1 490 pour 649 commencés — habitat
  non déclaré), Savanes − 116, Corse (Propriano, Corte), Digne − 272,
  Narbonne − 519 : le recensement compte des logements que Sitadel ne voit
  pas (constructions sans DOC, changements d'usage, divisions). Les
  positifs extrêmes (L'Aigle, Vitry-le-François, Creusot-Montceau : parc en
  baisse malgré des commencés) mêlent démolitions réelles et fusions.
- Là où le résidu positif est plausible (Paris + 7 687/an, Rennes + 1 089,
  Marne-la-Vallée + 655), il n'est pas séparé entre délai de livraison,
  démolitions NPNRU et changements d'usage.

**Disposition proposée.** Retirer le chiffre de R-18 et d'O-41 ; publier à
la place la distribution par ZE sous le nom « écart de champ commencés −
croissance du parc », avec la sensibilité à la fenêtre, et L-34(2) réécrite
(« non signé, non interprétable sans les DAACT et les démolitions »).

### HD-6 — La jointure Sitadel → ZE perd 1 833 codes communaux (communes fusionnées) ; la note de S-54 est fausse et un cas cité par R-18 change de signe

**Gravité : moyenne** (0,4 % national, mais concentré sur des ZE nommées).

**Preuve.**
- La table d'appartenance (S-06, COG 2026) ne connaît pas 1 833 codes
  présents dans Sitadel (aucun n'est dans le recensement non plus) : codes
  d'avant fusion. Commencés non joints : 1 278/an sur 2017-2022, **4 414/an
  sur 2013-2016** (1,4 % — la fenêtre longue 2013-2024 est plus touchée),
  317/an sur 2023-2025.
- Concentration : 85166 Olonne-sur-Mer 126/an et 85060 Château-d'Olonne
  94/an (fusionnées dans Les Sables-d'Olonne 85194 au 01/01/2019, qui est
  bien dans la ZE 5214) ; 74011 Annecy-le-Vieux 101/an et 74268 Seynod
  46/an (Annecy, 2017) ; 93059 Pierrefitte-sur-Seine 160/an (Saint-Denis,
  2024 — et la série continue jusqu'en 2025) ; 69152, 49069, 69211.
- Les Sables-d'Olonne, exemple de R-18 et de I-18 : commencés 865 → 1 085 ;
  solde − 818 → − 598 ; **hors RS − 190 → + 30** (le signe change). Annecy
  + 150/an.
- S-54 affirme « codes INSEE au millésime de publication » : l'extrait
  prouve le contraire (Sitadel conserve le code de la commune à la date du
  permis).

**Disposition proposée.** Joindre via une table de passage COG (INSEE,
communes 2013-2026 → 2026) dans `acquire-sitadel` ou `flux_by_ze` ;
corriger S-54 ; refaire tourner ; recompter les ZE dont le signe change.

### HD-7 — Stock et flux se recouvrent : R-18 ne nette pas la production de P-01, et « 1,3 an de formation de ménages » compare un stock de vacants à un flux de ménages

**Gravité : moyenne.**

**Énoncé.** Un vacant remobilisé par P-01 loge un ménage formé (ou libère
un logement pour lui) : c'est un logement disponible de plus, comme un
logement commencé. Le besoin de flux d'une ZE tendue doit donc être netté
de la production de l'opérateur (~19 400 logements/an sur 10 ans, P-01), soit
~10 % du besoin de flux des ZE tendues (185 443) et 39 % du déficit de flux
2024 (SE-1). R-18 ne le fait pas, et I-18 sépare « stock » et « flux » comme
s'ils ne se touchaient pas — c'est le double comptage inverse : celui qui
ignore une contribution.

Inversement, « le besoin de détente vaut 1,3 an de formation de ménages »
(R-18, L-19, L-32) est un ratio rhétorique : un stock de vacants n'est
« mangé » par la formation de ménages que si le flux est déficitaire, et de
la seule différence flux − besoin, pas de la formation entière. Le calcul
correct est celui de SE-2 (années d'absorption par ZE).

**Disposition proposée.** Dans le module stock vs flux, publier le solde de
flux net de la production P-01 par ZE (19 400/an ventilés comme dans R-16)
; retirer « 1,3 an » ou le requalifier explicitement en ordre de grandeur.

### HD-8 — I-18 prend Paris pour contre-exemple métropolitain alors que la ZE Paris n'est pas tendue au sens de R-07 ; les métropoles tendues ont des ratios ≈ 1, c'est-à-dire rien

**Gravité : moyenne** (énoncé de I-18).

**Preuve.** ZE Paris (1109) : vacance disponible 6,25 % > H-08 → `tendue =
False` dans l'artefact (`plus_gros_surplus[0].tendue: false`) ; de même
Lyon (6,30), Strasbourg (6,34), Grenoble (6,61), Nice (8,33). I-18 oppose
« pas celle des grandes métropoles (Paris 1,8) » aux ZE littorales
déficitaires : la comparaison sort du périmètre tendu, et le 1,84 parisien
est un effet RS + vacance (HD-1). Les métropoles tendues : Bordeaux 1,02
(solde + 174), Nantes 1,03 (+ 221), Lille 1,05 (+ 264), Toulouse 0,98
(− 281 ; − 537 en RS observée), Rennes 1,21 (+ 1 175, dont
commencés/Δparc 1,19 = livraison/démolitions), Marseille 0,79, Montpellier
0,77. Des ratios à ± 5 % de 1 dans une quasi-identité ne disent rien ;
seuls Marseille et Montpellier (et Toulouse/Bordeaux hors structure
constante) portent un signal, et il est métropolitain.

**Disposition proposée.** Retirer Paris de l'argument (ou le présenter pour
ce qu'il est : L-12) ; reformuler « déficit littoral et touristique, pas
métropolitain » en « déficit dans une vingtaine de ZE littorales sous
structure constante, dans Marseille/Montpellier/Toulouse/Bordeaux sous RS
observée ».

### HD-9 — Le plancher de classement (200 ménages/an) ne s'applique ni aux quantiles ni au Spearman ratio × coût

**Gravité : basse.**

**Preuve.** `ratio_production.autres.max = 69,79` (Côte sous le vent,
0,46 ménage formé/an) ; Guéret 32,8, Épernay 10,7. Le Spearman ratio × coût
est calculé sur n = 279 ZE, donc sur 94 ZE sous le plancher où le ratio est
du bruit (`n_ze_sous_seuil_classement: 94`). Le rang amortit, mais la
moitié des « autres » sont dans ce cas. Disposition : appliquer le plancher
aux quantiles et au Spearman, ou publier les deux.

### HD-10 — Jonction de concept ménages 2016/2022 et « France hors Mayotte »

**Gravité : basse.**

D-05 est un concept abandonné le 31/08/2025 (D-06 « ménage-logement ») ;
C-16 devrait dire sur quel concept P16_MEN et P22_MEN de la base-cc 2022 sont
calculés (le caveat de D-05 exige de documenter toute jonction). L'égalité
ménages = RP est vérifiée aux deux millésimes dans le fichier, ce qui suffit
au calcul, mais pas à la trace. Par ailleurs O-41 dit « France hors
Mayotte, 305 ZE » : la Guyane et la Guadeloupe sont dedans et pèsent sur les
extrêmes (HD-5) ; à dire.

---

## B. Scénarios d'échec (SE)

### SE-1 — « Le flux n'est pas le problème national » est vrai de 2017-2022 et faux de 2023-2025 sur les données de la chaîne ; les années 2023-2024 sont closes, pas « en cours de remontée »

**Gravité : haute.**

**Énoncé.** O-41, S-54 et L-34(1) écartent 2023-2025 comme mêlant « la
chute réelle et les déclarations non encore remontées ». Or S-55 (D-24)
fixe la remontée des DOC « généralement dans les dix-huit mois » : un
chantier ouvert en décembre 2023 est enregistré au plus tard vers juin 2025,
et le fichier est du 15/09/2026. **2023 est close ; 2024 l'est presque
(remontées jusqu'à mi-2026) ; seules 2025-2026 sont ouvertes.** Les
264 819 (2023) et 234 808 (2024) sont donc des ordres de grandeur quasi
définitifs — et la chaîne les possède.

**Preuve.**
- National : ratio 0,79 (2023), 0,70 (2024), 0,71 (2025, ouverte) contre le
  besoin 335 470 ; hors RS 0,89 / 0,79 / 0,80. Fenêtre 2020-2025 : 0,86.
- ZE tendues : commencés 132 133 (2023), 119 885 (2024) contre un besoin de
  185 443 → solde − 53 310 puis − 65 558/an (− 27 634 / − 39 882 hors RS).
  La chute 2022 → 2024 est de − 30,6 % en ZE tendues (− 33,4 % ailleurs) :
  elle ne relocalise pas.
- Stock vs flux à ce rythme : le besoin de détente de 194 488 est
  consommé en **3,0 ans** (2024 ; 4,9 hors RS), 3,6 ans (2023), 5,0 ans
  (moyenne 2020-2025). Pour un flux tendanciel de 300 000 / 280 000 /
  265 000 commencés (51 % en ZE tendues, part stable 2013-2025) : 6,0 /
  4,6 / 3,9 ans.

**Scénario d'échec pour P-01.** L'opérateur livre ~19 400 logements
disponibles par an ; le déficit de flux des ZE tendues de 2024 est de
65 558/an (39 882 hors RS). P-01 couvre 30 à 49 % du déficit de flux
courant ; le stock qu'il détend sur dix ans est rattrapé en trois à cinq ans
par le seul manque de construction. I-18 conclut : « l'opérateur de P-01
n'a pas à porter le flux national » — c'est la conclusion inverse de celle
que les années disponibles donnent.

**Disposition proposée.** Publier dans R-18 la série annuelle 2013-2025 par
tension (elle est dans l'extrait), le solde des ZE tendues sur 2023-2024,
et les années d'absorption correspondantes ; corriger O-41/S-54/L-34(1)
(seules 2025-2026 sont ouvertes) ; réécrire I-18 : « le flux a couvert la
formation de ménages pendant le haut du cycle 2017-2022 ; il ne la couvre
plus depuis 2023 ». Figer la série « date réelle » du SDES comme
contrôle.

### SE-2 — « Absorbé en 10,6 ans » mélange les ZE ; par ZE, les tendues déficitaires portent la moitié du besoin de stock et l'absorbent en 5,5 ans

**Gravité : haute.**

**Preuve** (recalcul par ZE, cadre R-18 × cadre R-07 au central) :
- 46 ZE tendues déficitaires (C-16) : besoin de détente **99 798** (51,3 %
  des 194 488) pour un déficit de flux de 18 279/an → **5,5 ans**
  (médiane par ZE 5,8 ; p25 2,6 ; p75 12,8). Perpignan 1,6 an (besoin 2 331,
  déficit 1 484), Montpellier 2,6 (5 190 / 1 994), Bayonne 4,2 (6 201 /
  1 466), Marseille 4,3 (6 191 / 1 450), Toulon 7,2 (10 460 / 1 449),
  Narbonne 1,9, Sables-d'Olonne 2,5, Pornic 2,7.
- 21 de ces 46 ZE sont aussi « non couvertes » par leur gisement (R-07,
  couverture < 1), pour 69 843 de besoin : ce sont les ZE où P-01 ne peut ni
  remobiliser assez ni compter sur le flux (Bayonne 0,45, Toulon 0,50,
  Sables 0,16, Pornic 0,21, Fréjus 0,38, Challans 0,32, Agde 0,47).
- 51 ZE tendues excédentaires : besoin de détente 94 690 (48,7 %), surplus
  de flux 13 027/an → leur propre besoin serait comblé en 7,3 ans **si le
  surplus devenait vacance** — or il ne l'est pas devenu (HD-3 : part vac
  − 0,20 pt, RS + 0,36 pt).
- Hors RS : 23 ZE déficitaires, besoin 49 775, déficit 5 181/an → 9,6 ans
  (et non 37,5).
- La liste hors RS n'est pas « littorale » : Meaux, Creil, Dreux,
  Bourgoin-Jallieu, Ancenis, Chalon-sur-Saône, Cherbourg, Yvetot y
  figurent — petites ZE tendues sans RS, à déficit modeste mais réel.

**Disposition proposée.** Remplacer les deux nombres nationaux (10,6 / 37,5)
par la table par ZE (besoin R-07, déficit de flux aux trois bornes, années
d'absorption, couverture gisement) ; I-18 « il l'est en 10 ans dans les ZE
déficitaires » → « en 5 ans et demi ; en moins de 3 ans à Perpignan,
Montpellier, Narbonne, aux Sables-d'Olonne ».

### SE-3 — « La structure touristique absorbe une part de chaque logement construit » est un énoncé causal non établi ; ce qui est observé est une dilution de la RS et une baisse de la vacance

**Gravité : moyenne.**

**Preuve.** Dans les 46 ZE tendues déficitaires, la part RS a **baissé**
(médiane − 0,18 pt) et la part de vacants aussi (− 0,67 pt) ; dans les ZE
les plus touristiques la part de RS dans la croissance du parc est bien
inférieure à sa part dans le stock (HD-2). Le déficit « touristique » de
R-18 n'est pas une absorption observée, c'est l'écart entre une croissance
observée et une croissance à structure constante que le modèle exige. Qui
achète le neuf n'est pas observé (L-34(3) le dit) ; « absorbe » l'affirme
quand même. La formation de ménages n'est pas non plus corrélée à la part RS
en ZE tendues (Spearman 0,095) — le modèle ne peut donc pas être testé
contre l'idée inverse (la RS évince la formation de ménages).

**Disposition proposée.** Remplacer par un énoncé de définition : « à
structure constante, une ZE à 30 % de RS a besoin de 1,5 logement par
ménage formé » ; réserver « absorbe » à ce qui est mesuré (ΔRS/Δparc).

### SE-4 — Les tendances se croisent : la formation de ménages accélère (0,85 → 0,94 %/an) pendant que la croissance du parc ralentit (372 544 → 332 142/an)

**Gravité : moyenne.**

**Preuve** (S-11, trois millésimes) : France, formation 239 103/an
(2011-2016) → 275 284 (2016-2022) ; ZE tendues 1,21 → 1,32 %/an. Croissance
du parc 372 544 → 332 142/an (tendues 184 850 → 175 100). Le « flux
couvert » de 2016-2022 est une période où le parc a grandi MOINS qu'avant
pour PLUS de ménages : la couverture s'est faite par compression de la
structure (vacance − 0,35 pt en tendues). Prolongée avec SE-1 (commencés
− 30 %), c'est le scénario où P-01 est doublement débordé. Le scénario
inverse (ralentissement démographique de la formation de ménages,
projections INSEE) n'est pas instruit non plus ; il jouerait en faveur de
P-01. Aucun des deux n'est nommé.

### SE-5 — L'infra-ZE : le ratio par ZE ne dit rien des communes TLV où P-01 opère, et la donnée pour le savoir est dans le dépôt

**Gravité : moyenne.**

L-34(5) nomme la limite. Mais R-07 a montré que la couverture du gisement
tombe à 0,69 au périmètre des communes TLV ; la même question pour le flux
(les commencés sont-ils dans les communes TLV ou en périphérie ?) est
calculable avec les fichiers figés (Sitadel par commune × zonage TLV S-…)
sans nouvelle source. Ne pas la calculer, c'est laisser I-18 conclure sur
l'affectation « dans une trentaine de ZE littorales » sans savoir si le
neuf est dans les communes tendues de ces ZE. Disposition : ajouter la
ventilation TLV / hors TLV des commencés par ZE tendue.

### SE-6 — Le signe du solde des ZE tendues n'est pas robuste à H-08, et I-18 ne le porte pas

**Gravité : basse** (R-18 le publie, I-18 l'omet).

`sensibilite_h08` : − 5 387 (5 %, 54 ZE) / + 9 946 (7 %, 170 ZE). Le signe
change avec l'ensemble. I-18 énonce « pas d'abord celui des zones tendues »
sans cette réserve ; §15 exige la fourchette à côté de l'énoncé.

---

## C. Cohérence des décisions (DEC-21..DEC-24) avec les nœuds

- **DEC-21** (sujet) : cohérent avec L-19/L-32 et INTRO logement §15 q. 9.
  Rien à redire, sauf que l'article répond à « le flux rattrape-t-il le
  stock ? » avec une mesure qui ne peut pas le dire (HD-1).
- **DEC-22** (extrait annuel) : cohérent ; mais son prix est plus lourd que
  « la fenêtre est annuelle » : il rend HD-4 (part des remontées tardives)
  non mesurable. À écrire dans L-34 avec l'alternative (série date réelle).
- **DEC-23** (fenêtres, besoin, variante) : options et nœuds cohérents
  (C-16, L-34(3)). Deux faiblesses : (d) « un logement par ménage formé —
  sous-estime » est affirmé sans chiffre (à cette option le solde des ZE
  tendues est + 30 133, national + 71 231 : c'est la borne basse honnête,
  elle devrait être publiée avec les autres) ; le choix de 2017-2022 est
  justifié par l'alignement sur les millésimes, sans considérer le délai
  commencé → livré (HD-4). Le fait que la variante hors RS « renverse le
  signe » est la preuve que C-16 porte une hypothèse (HD-2).
- **DEC-24** (trois relecteurs) : la justification « sans hypothèse H-xx
  nouvelle » ne tient pas (HD-2). Le choix de fusionner les angles n'a pas
  nui ici, mais la règle « quatre pour les livrables à hypothèses » aurait
  dû s'appliquer.

---

## D. Scénarios d'échec non nommés dans R-18 / I-18 / L-34

1. **Rupture de tendance 2023+** (SE-1) : le seul scénario qui menace P-01
   frontalement, et il est dans les données figées.
2. **Formation de ménages bornée par le parc** (HD-1) : le besoin est
   sous-estimé exactement là où la pénurie est la plus forte ; aucune
   mesure exogène de la demande.
3. **Le surplus ne détend pas** (HD-3) : là où le flux dépasse la structure
   constante, il va en RS, pas en vacance disponible.
4. **Déficit métropolitain sous RS observée** (HD-2) : Marseille,
   Montpellier, Toulouse, Bordeaux — le contraire de la géographie de I-18.
5. **Dérive de la jointure COG** (HD-6) : elle grandit à chaque fusion
   (Saint-Denis 2024) et biaise la fenêtre longue dès aujourd'hui.
6. **Démolitions NPNRU dans les métropoles tendues** (HD-5) : un commencé
   qui remplace un démoli n'est pas un logement de plus ; non séparé.
7. **Recouvrement stock/flux** (HD-7) : la production de P-01 n'est pas
   nettée du besoin de flux ; l'équilibre général de L-32 ne l'est pas non
   plus.
8. **Ralentissement démographique** (SE-4) : scénario favorable à P-01,
   non instruit — un scénario d'échec de l'argument « le flux rattrape ».
9. **Millésime 2022 = fenêtre 2020-2024 avec l'enquête 2021 suspendue** :
   L-34(4) mentionne la fenêtre COVID, pas le fait que le millésime repose
   sur quatre collectes et non cinq (à vérifier auprès de S-11).
10. **Changement du droit d'affectation** (régulation des meublés
    touristiques, TVLH 2027 — L-33) : l'« affectation du flux » que I-18
    assigne à l'opérateur dépend d'un régime qui change ; non nommé.

---

## E. Verdict

**R-18** reproduit et s'exécute, mais ne survit pas tel quel : le « ratio de
production » est une quasi-identité qui mesure la dérive de structure et
non la couverture d'un besoin (HD-1) ; C-16 porte une hypothèse d'affectation
qui renverse le signe et doit devenir H-21 avec trois bornes (HD-2) ; les
« disparitions implicites », le 10,6 ans national et l'exclusion de 2023-2024
sont à retirer ou remplacer (HD-5, SE-2, SE-1) ; la jointure perd des
communes fusionnées (HD-6). Requalifié en **décomposition observée de la
croissance du parc par ZE, avec série 2013-2025 et table stock/flux par
ZE**, il devient un résultat utile.

**I-18** ne survit pas : « le flux n'est pas le problème national » est
contredit par 2023-2024 sur les données de la chaîne (déficit des ZE
tendues − 53 000 à − 66 000/an, stock de détente consommé en 3 à 5 ans) ;
« déficit littoral et touristique, pas métropolitain » dépend de l'hypothèse
d'affectation et se renverse partiellement sous RS observée ; « Paris 1,8 »
est hors périmètre tendu et signe une croissance de RS et de vacants, pas
une couverture ; « 10 ans » vaut 5,5 par ZE. À réécrire : le flux a suivi la
formation de ménages observée pendant le haut du cycle 2017-2022 en
comprimant la vacance ; il ne la suit plus depuis 2023 ; P-01 traite un
stock que le déficit de flux courant rattrape en quelques années, et
l'article 3 doit dire ce que l'opérateur fait de cela — ou déclarer que le
flux reste hors de sa portée (L-19/L-32), ce qui est au moins honnête.
