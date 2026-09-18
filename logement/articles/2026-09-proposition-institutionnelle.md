# Détendre le parc, au prix du marché

**Cinq mécanismes comparés sur les mêmes chiffres — et ce que la comparaison impose à la proposition.**

*Septembre 2026 — second article de l'étude « Efficacité du parc
immobilier français » du programme Métabolisme. Le premier article
([« Le parc immobilier français, au bord du compte »](2026-08-efficacite-parc-etat-des-preuves.md),
août 2026) établissait l'état des preuves ; celui-ci fait ce qu'il
annonçait : concevoir le mécanisme. Comme le précédent, tout chiffre
cité provient d'une chaîne de preuves exécutable — dépôt public, sources
figées et sommées, hypothèses nommées avec leur plage, résultats
recalculables par une commande. Version de référence : tag
`efficacite-parc-v0.6` du dépôt
[metabolisme](https://github.com/lbdremy/metabolisme), document de
preuve `logement/evidence/efficacite-parc-immobilier.qmd`. Les
identifiants entre parenthèses (S-xx, R-xx, H-xx, C-xx, L-xx…) pointent
vers ce dépôt. Deux pièces nouvelles s'y ajoutent : un **journal des
décisions** (`evidence/decisions-2026-09-18.md`) qui consigne, pour
chaque choix de conception, les options abandonnées et la raison du
choix ; et le compte rendu d'une **revue contradictoire** menée le
jour même sur la proposition, qui a corrigé trois erreurs de
construction avant qu'elle ne soit publiée.*

---

## Le point de départ

Le premier article laissait quatre contraintes chiffrées. Le gisement
de logements durablement vacants des zones tendues couvre à peine le
besoin de détente — 194 488 logements pour ramener 97 zones d'emploi à
une vacance de fluidité de 6 % — et il n'est pas là où est le besoin :
136 544 logements sont rénovables localement, 57 945 manquent (R-07,
R-09). Remobiliser coûte deux fois moins que construire — mais ce
ratio ne valait que pour les travaux (R-09, L-14). Le foncier n'est pas
la contrainte (R-10). Et rien ne se déclenche seul : le canal incitatif
existant a un bilan documenté faible, et 83 % du péage payé à chaque
achat est fiscal (R-14).

La question de conception qui en découle est simple à formuler :
**qui porte le bien ?** Tant que le logement vacant reste celui de son
propriétaire, tout mécanisme est une incitation, et la Cour des comptes
a mesuré ce que les incitations obtiennent. Dès qu'un opérateur le
porte, il faut l'acheter, le rénover, le financer, le louer — et
chaque terme a un prix que les sources permettent de calculer.

La méthode impose de ne pas défendre un mécanisme d'avance. Cinq
mécanismes ont donc été chiffrés **sur exactement la même géographie**
que le diagnostic — les 97 zones tendues, le besoin de 194 488, la
règle mixte rénovation/neuf — avant qu'aucun ne soit retenu (C-11) :

- **M-A** — le canal incitatif existant, tel quel ;
- **M-B** — un opérateur collectif qui *acquiert* les vacants durables,
  les rénove, et construit sur friches là où le gisement manque ;
- **M-C** — le même opérateur *sans* acquisition : le bail à
  réhabilitation, où le propriétaire confie son bien pour trente ans ;
- **M-D** — la bascule du péage fiscal de transaction vers une charge
  annuelle de détention ;
- **M-E** — la sécurisation de la mobilité locative, que les sources
  ouvertes ne permettent pas de chiffrer (L-31).

Les résultats de ces mécanismes sont des **simulations** : des calculs
sur hypothèses nommées, pas des observations. Ce qui suit est leur
état *après* revue contradictoire.

## 1. Le canal incitatif ne peut pas détendre

Le seul constat d'exécution disponible vient de la Cour des comptes
(S-22) : entre 2020 et 2024, parmi les propriétaires de logements
vacants *contactés* en zone tendue, 3 % ont remis leur bien en usage.
L'étude prend ce taux comme s'il s'appliquait à *tout* le gisement —
c'est-à-dire comme si tous les propriétaires étaient contactés, ce qui
en fait un majorant généreux du canal réel (H-14).

Même ainsi, le résultat est sans appel (R-15) : en dix ans, le canal
incitatif sortirait de vacance environ 15 300 logements dans les 97
zones tendues — **8 % du besoin**. À cinq ans, 4 % ; à vingt ans,
15 %. Au triple du taux constaté, 25 % en dix ans. La taxe sur les
logements vacants rapporte 271 millions d'euros par an ; elle est
remplacée en 2027 par une taxe unique dont personne n'a encore mesuré
l'effet (S-52, L-33).

C'est le seul énoncé de toute la comparaison qui ne dépend d'aucune
hypothèse nouvelle : quelle que soit la valeur qu'on donne au canal
incitatif dans sa plage plausible, la référence ne détend pas (I-15).

## 2. L'opérateur qui achète paie le prix du marché

Le second mécanisme sécurise le volume : un opérateur collectif
acquiert les 136 544 vacants durables rénovables des zones tendues, les
rénove, et construit les 57 945 logements manquants sur les friches
que le premier article a recensées. Chaque terme est sourcé (C-12,
C-13) : acquisition au prix médian au mètre carré des logements vendus
dans la zone d'emploi (DVF 2025, S-30) — c'est la *valeur vénale*, le
prix que fixe la loi en cas d'expropriation (S-45) — majoré de
l'indemnité de remploi de 10 % que la même loi prévoit (H-20, S-50) ;
rénovation aux coûts du premier article ; construction neuve au prix
de revient d'un logement social en 2023, 2 550 €/m² (S-18) ;
financement au circuit existant du logement social, prêt de la Banque
des Territoires au Livret A plus 0,60 %, soit 2,30 % sur quarante ans
(H-16, H-17, S-41, S-42) ; charges d'exploitation à ce que coûte
réellement un logement aux bailleurs sociaux, 2 652 € par an (H-18,
S-40).

Le premier résultat corrige une intuition du premier article (R-16).
Un vacant acquis et rénové dans une zone tendue coûte **3 776 € par
mètre carré** en médiane — *plus* qu'un logement social neuf à
2 550 €/m². « Remobiliser coûte deux fois moins que construire » était
vrai des travaux ; ce n'est plus vrai dès qu'il faut acheter le bien
au prix des marchés tendus. L'investissement total s'élève à
**61,8 milliards d'euros** (46,1 d'acquisition, 6,0 de rénovation, 9,8
de neuf), soit 6,2 milliards par an sur un programme de dix ans — un
majorant, puisque le calcul prend la surface des résidences principales
alors que le vacant durable est plutôt petit (L-27).

Le second résultat est le plus important. Le loyer qui équilibre cet
opérateur — annuité de l'emprunt plus charges, sans aucune subvention
— est de **14,4 € par mètre carré et par mois** en médiane des zones
tendues, contre 12,3 € de loyer de marché et 6,4 € de loyer du parc
social. Autrement dit, 1,14 fois le marché : au-dessus dans quatre
zones sur cinq, en dessous dans une sur cinq, et en dessous presque
partout à la moindre décote d'acquisition (à 0,75 fois la valeur
vénale : 11,8 €/m², sous le marché dans 68 zones sur 93). Le segment
neuf sur friches s'équilibre à 11,5 €/m², sous le marché dans deux
zones sur trois.

La conclusion n'est donc pas celle qu'on attend d'un « opérateur
public ». **L'opérateur produit du logement disponible au prix du
marché, pas du logement social.** Le ramener partout au loyer social
coûterait 1,56 milliard d'euros par an — 8 000 € par logement et par
an, pendant quarante ans ; entre 0,2 et 2,8 milliards selon les coins
de la plage des hypothèses. Le ramener au loyer de marché, 0,31
milliard.

Or c'est exactement ce que le besoin du premier article demandait.
Les 194 488 logements ne sont pas une file d'attente sociale : ce sont
des logements *disponibles*, la vacance de fluidité sans laquelle les
déménagements sont impossibles. Un logement au loyer social occupé
pendant vingt ans ne détend rien. Le mécanisme qui sécurise le volume
produit précisément la chose demandée — au prix du marché, sans
subvention d'exploitation — et laisse ouverte, comme un choix de
valeur et non comme un résultat, la question de savoir s'il faut
payer 1,6 milliard par an pour en faire du logement social (V-04).

## 3. L'opérateur qui n'achète pas est le moins cher — mais personne ne lui donne son bien

Le troisième mécanisme est un outil qui existe déjà dans le code de la
construction : le **bail à réhabilitation** (D-21, S-46). Le
propriétaire confie son logement vacant à un opérateur agréé, qui le
rénove à ses frais, le loue trente ans en moyenne, et le lui rend
rénové. L'opérateur ne paie ni le foncier ni le bâti — seulement les
travaux, exonéré de taxe foncière.

Le loyer d'équilibre tombe alors à **3,7 € par mètre carré**, sous le
loyer social dans toutes les zones (R-16). L'investissement se limite
aux 6 milliards de travaux, plus les 9,8 milliards de neuf pour le
déficit — 15,8 milliards, le chiffre du premier article.

Mais le volume dépend d'une inconnue que rien ne mesure : le
consentement du propriétaire. À 10 % d'adhésion, le bail seul couvre
7 % du besoin ; à 50 %, 35 % ; il faudrait 100 % pour les 70 % que le
gisement peut fournir. Et la revue contradictoire a établi la direction
de cette inconnue : à qui l'on garantit une acquisition à la valeur
vénale, la vente immédiate vaut davantage que trente ans de bail sans
loyer — la valeur actuelle du bail représente entre 28 et 67 % de
celle d'une vente selon le taux d'actualisation (I-16, C-15). Le bail
n'attire que les propriétaires qui veulent *garder* leur bien. La
première version de cette proposition affirmait l'inverse ; la revue
l'a renversée.

## 4. Le péage : une redistribution avant d'être un levier

Le quatrième mécanisme s'attaque au paramètre institutionnel que le
premier article avait isolé : 83 % du coût d'un achat est fiscal, et
l'essentiel en est le droit départemental de mutation. L'OCDE (S-44) et
le Conseil des prélèvements obligatoires (S-51) recommandent tous deux
de « moins taxer l'acquisition » et de compenser par la détention.

L'étude chiffre la bascule au plus simple (C-14) : le produit
départemental des droits de mutation en 2025 — 11,9 milliards d'euros
sur le périmètre de l'Observatoire des finances locales (S-47) —
réparti uniformément sur les 34,6 millions de logements du même
périmètre fait une **charge de 344 € par logement et par an**. En
face, le droit départemental sur le logement médian d'une zone
d'emploi vaut 7 250 € en médiane, soit 3,9 mois de niveau de vie
médian sur un péage total de 6,1 mois (R-17). Le péage résiduel —
part communale, frais d'assiette, contribution de sécurité
immobilière, émoluments — resterait à 2,1 mois.

En années de charge équivalente, le droit médian vaut **21 ans** — 29
ans dans les zones tendues, 19 ailleurs : la bascule favorise le
ménage qui transacte plus d'une fois par génération et pénalise celui
qui reste, d'autant plus dans les marchés chers (Paris 47 ans, Annecy
45 ; Montluçon ou Sarrebourg 9). Uniforme par logement, la charge est
régressive en valeur : 0,11 % du prix médian dans les zones les plus
chères, 0,53 % dans les moins chères.

Et l'effet sur la mobilité n'est pas établi. La seule expérience
naturelle française publiée (S-43 : la hausse de 0,7 point de 2014,
département par département) trouve une baisse de 6 % des
transactions sur trois mois et « aucune preuve d'un effet à moyen ou
long terme ». Une bascule de cinq points est hors du support de cette
estimation (L-28). La bascule se justifie donc par une valeur — ne pas
taxer le comportement rare dont le premier article déplorait la
raréfaction (V-03) — et par deux recommandations convergentes, pas par
une élasticité. Le CPO lui-même la conditionne à une réforme
préalable de l'assiette foncière (I-17).

## 5. La proposition

Assemblée après la comparaison, et réécrite après la revue (P-01,
C-15), la proposition tient en un **opérateur collectif de détente des
zones tendues** :

1. **Il acquiert** les logements vacants depuis plus de deux ans, à la
   valeur vénale plus remploi. C'est l'outil qui sécurise le volume —
   et il n'existe pas en droit : l'utilité publique d'une acquisition
   de logements vacants est à créer (D-22). Sans lui, la proposition
   se réduit au bail, c'est-à-dire à un canal incitatif amélioré d'un
   montant inconnu.
2. **Il offre**, avant d'acquérir, un bail à réhabilitation — sans
   compter dessus. Le prix de repli qui rendrait l'offre préférable à
   la vente est un paramètre de conception que l'étude ne chiffre pas.
3. **Il arbitre** au mètre carré, logement par logement, entre
   acquérir-rénover (3 776 €/m² en médiane) et construire sur friches
   (2 550 €/m²) : le foncier suffit (R-10), et le neuf s'équilibre
   souvent plus bas.

Il se finance par les prêts du logement social, portés par des loyers
proches du marché. Il produit du logement disponible ; en faire du
logement social est un choix de valeur qui coûte 1,6 milliard d'euros
par an au central. Ordres de grandeur : 61,8 milliards d'investissement
sur dix ans, 2,4 milliards d'annuité par an — contre 271 millions de
taxe sur les logements vacants et 11,9 milliards de droits de mutation
départementaux.

La bascule des droits de mutation vers la détention est une **voie
séparée**, conditionnée à la réforme de l'assiette foncière, régressive
si elle reste uniforme, assumée comme choix de valeur et non comme
levier démontré. Sur le locatif privé — le canal principal des
mobilités selon le premier article — l'étude ne peut poser que des
principes : portabilité des garanties, plafonnement des frais
d'entrée (L-31).

## 6. Ce que la revue a changé, et ce que la proposition ne démontre pas

Quatre relecteurs indépendants ont examiné la proposition le jour de
sa construction : 61 objections, 130 valeurs recalculées depuis les
sources (exactes), sept sources ajoutées. Trois erreurs de construction
ont été corrigées avant publication : le loyer du neuf divisait le prix
d'un logement de 66 m² par la surface des résidences principales
(96 m²) — « le neuf s'équilibre au marché » était un artefact ; les
charges d'exploitation étaient prises en proportion d'un loyer trois
fois plus haut que celui du secteur — « au-dessus du marché partout »
tombait avec elles ; la bascule des droits de mutation prenait un
millésime dépassé et le péage total au lieu de la part basculée. Et un
étage de la proposition a été inversé : le bail n'est pas préféré à la
vente. Les décisions d'intégration, et les sept objections écartées
avec leur raison, sont dans le journal des décisions.

Ce que la proposition ne démontre pas, la chaîne le dit (L-27..L-33) :

- **L'outil d'acquisition n'existe pas**, et le taux d'adhésion au bail
  n'a aucune source ; les propriétaires peuvent sortir de la cible
  avant le repli — relouer, vendre, transformer en meublé touristique
  dans les zones littorales et alpines où les loyers d'équilibre sont
  les plus hauts (L-29).
- **Les effets d'équilibre général sont ignorés** : un opérateur qui
  achète 136 000 logements paie la valeur vénale d'avant son entrée ;
  et la détente qu'il produit fait baisser les loyers de marché alors
  que son loyer d'équilibre ne bouge pas — la subvention croît avec le
  succès (L-32).
- **C'est un stock, pas un flux** : la formation de ménages des zones
  tendues rattrape les 194 488 logements en un an et demi, et
  représenterait au prix du neuf quelque 24 milliards par an —
  davantage que tout le programme (L-19, L-32).
- **Les totaux sont des majorants** (surface des résidences principales,
  pas de décote, pas de valeur résiduelle à quarante ans) et le modèle
  financier ignore vacance, impayés, inflation et portage (L-27, L-30).
- **La bascule fiscale** ne vaut pas pour Paris, Lyon, la Corse et les
  Antilles-Guyane, hors du périmètre de la source (L-28).

## 7. Ce qui vient

Trois inconnues de conception sont instruisables : le prix de repli qui
rendrait le bail préférable à la vente (précédents des foncières
solidaires et du portage foncier), la forme juridique de l'outil
d'acquisition, et la surface réelle des vacants durables, derrière une
habilitation. Les trois observations qui trancheraient la question de
la mobilité restent à faire : la réforme des droits de mutation de
2025, département par département, est l'expérience naturelle qu'il
faudra lire dans les ventes de 2026 ; le parc social au 1ᵉʳ janvier
2026 n'est pas encore publié ; la rotation par âge et territoire attend
le fichier détail du recensement.

---

## Sources et reproduction

Sources nouvelles de cet article (toutes publiques, figées et sommées
dans `logement/sources/sources.yaml` — 53 entrées au total) :
Observatoire des finances et de la gestion publique locales (produit
des droits de mutation 2024 et 2025, S-39/S-47) ; Banque des
Territoires (Perspectives 2025 sur les comptes des bailleurs sociaux
S-40, conditions des prêts PLUS/PLAI/PLS S-41/S-48/S-49, Livret A
S-42) ; INSEE — Économie et Statistique, Bérard & Trannoy 2018 (S-43) ;
OCDE, fiscalité immobilière 2022 (S-44) ; Conseil des prélèvements
obligatoires 2023 (S-51) ; DGCL (S-53) ; Service-Public (expropriation
S-45, taxe sur la vacance 2027 S-52) ; DREAL Occitanie (bail à
réhabilitation S-46) ; préfecture de l'Hérault (barème du remploi
S-50). Les sources du diagnostic (INSEE, LOVAC, ANIL, SDES, DGFiP,
Cour des comptes, Cerema…) sont celles du premier article.

Reproduction complète depuis le dépôt
[metabolisme](https://github.com/lbdremy/metabolisme), tag
`efficacite-parc-v0.6` :

```bash
cd logement
uv sync                     # environnement figé (uv.lock)
uv run logement validate    # registres + sha256 + graphe de preuves
uv run logement reproduce   # rebâtit les 15 artefacts data/processed/
./test.sh                   # 172 tests
```

Le document de preuve détaillé (chiffres, code, sensibilités, limites,
comptes rendus des trois revues contradictoires) :
`logement/evidence/efficacite-parc-immobilier.qmd`. Le journal des
décisions de conception : `logement/evidence/decisions-2026-09-18.md`.
