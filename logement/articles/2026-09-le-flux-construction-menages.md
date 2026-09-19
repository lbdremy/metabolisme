# Le flux s'est arrêté avant le stock

**Ce que la construction neuve couvrait de la formation des ménages, zone d'emploi par zone d'emploi — et ce qu'elle ne couvre plus depuis 2023.**

*Septembre 2026 — troisième article de l'étude « Efficacité du parc
immobilier français » du programme Métabolisme. Le premier établissait
l'état des preuves ; le deuxième concevait un opérateur de détente des
zones tendues, et sa revue contradictoire lui opposait une objection
que l'étude n'avait pas instruite : la proposition détend un stock —
194 488 logements — pendant que les ménages continuent de se former.
Cet article instruit le flux. Comme les précédents, chaque chiffre vient
d'une chaîne de preuves exécutable (dépôt
[metabolisme](https://github.com/lbdremy/metabolisme), tag
`efficacite-parc-v0.7`, document de preuve
`logement/evidence/efficacite-parc-immobilier.qmd`), le choix de son
sujet et de sa méthode est consigné dans le journal des décisions
(`evidence/decisions-2026-09-18.md`, DEC-21 à DEC-28), et une revue
contradictoire menée le jour même en a changé la source, la lecture et
la conclusion avant publication.*

---

## La question

Le recensement compte les ménages ; la base Sitadel du ministère compte
les logements dont le chantier est ouvert. Entre 2016 et 2022, la
France a formé 275 284 ménages par an (S-11). Combien a-t-il fallu
construire pour les loger, et où la construction a-t-elle manqué ? La
question paraît simple ; elle cache trois pièges que la revue a fait
apparaître, et qu'il faut poser avant les chiffres.

**Le premier piège est la source.** La série communale de Sitadel ne
compte que les déclarations d'ouverture de chantier qui remontent à
l'administration ; le service statistique du ministère écrit lui-même
qu'« environ 15 % des mises en chantier […] ne remontent jamais à
Sitadel » et publie une statistique nationale redressée par enquête
(S-58, S-57). L'écart entre les deux vaut 12 à 24 % selon l'année. La
première version de cet article utilisait la série brute ; elle
concluait que les zones tendues construisaient moins que leurs ménages.
Avec le facteur de sous-compte (H-21, 1,155 sur 2017-2022, contrôlé à
chaque reproduction), c'est l'inverse. Tous les chiffres qui suivent
sont en lecture « estimée » ; la lecture « déclarée » est publiée à côté
dans la chaîne.

**Le deuxième piège est la mesure elle-même.** Dans le recensement, un
ménage est une résidence principale occupée. Compter les ménages formés,
c'est compter les logements qui les logent : le « besoin de flux » à
structure constante est, à peu de chose près, la croissance observée du
parc. Le ratio construction / besoin dit donc combien il a fallu
commencer de logements pour produire la croissance que le recensement
enregistre — il ne dit pas si une formation de ménages plus forte a été
empêchée par le parc lui-même. La zone d'emploi de Paris construit 1,8
fois sa croissance et forme peu de ménages pour son parc : cause ou
conséquence, la mesure ne tranche pas (C-16, I-18).

**Le troisième piège est l'affectation.** Un logement commencé n'est
pas forcément une résidence principale : 12 % de la croissance du parc
2016-2022 est allée en résidences secondaires, 5 % en logements vacants.
Le besoin de flux dépend de cette affectation, et elle diffère d'une
zone à l'autre — 3 % à Montpellier, 73 % en Tarentaise. L'étude retient
la part observée dans chaque zone d'emploi, et publie les deux bornes.

## 1. 2016-2022 : la construction a produit la croissance du parc

Sur la fenêtre alignée sur les millésimes du recensement (chantiers
2017-2022), la France a commencé 398 460 logements par an contre un
besoin de flux de 350 689 : **ratio 1,14** (R-18). Les 97 zones
d'emploi tendues du premier article portent 54 % de la formation de
ménages pour 41 % du parc, et 52 % des chantiers : 206 540 commencés
par an contre 190 409 de besoin, **ratio 1,08** — 1,29 si l'on ne
compte aucune résidence secondaire dans le neuf. Trente-huit zones
tendues sont en déficit sur cette fenêtre, pour 10 134 logements par
an ; presque toutes sont littorales ou alpines — Est-littoral,
Narbonne, Tarentaise, Toulon, Bayonne, Digne — et le déficit y est une
question d'affectation : 13 % du neuf des zones tendues va en résidences
secondaires, jusqu'à 73 % en Tarentaise. Marseille fait exception, en
déficit sans résidences secondaires.

Deux faits corrigent des intuitions. La construction n'est pas plus
faible là où c'est cher : sur les 207 zones d'emploi qui forment au
moins 200 ménages par an, le ratio médian est **plus haut** dans les
zones tendues (1,11) qu'ailleurs (1,00), et il **croît** avec le coût du
logement (corrélation + 0,20). Et elle y est deux fois plus intense :
11,8 chantiers pour 1 000 logements existants contre 5,9 ailleurs. À la
maille des zones d'emploi, on n'a pas construit moins là où il fallait
construire.

Cette fenêtre est aussi la plus haute de la série. Décalée de deux ans
pour suivre les livraisons (2015-2020), le ratio national tombe à 1,11 ;
prolongée d'un an (2018-2023), à 1,06 ; sur 2019-2024, à **0,98**, et
les zones tendues passent en déficit.

## 2. Depuis 2023, le flux s'est effondré

Les années 2023 et 2024 sont closes dans la série en date réelle : un
chantier de 2023 déclaré tard est compté en 2023. Elles montrent une
chute d'un tiers. La France a commencé 263 113 logements par an en
2023-2024 (estimés ; 296 477 puis 259 595 dans la statistique publiée),
contre 398 460 sur 2017-2022. Dans les zones tendues, 132 193 par an
contre un besoin de flux de 190 409 : **− 58 216 par an, 77 zones sur
97 en déficit**. Les plus gros déficits ne sont plus littoraux : Toulouse
(− 5 862), Bordeaux (− 5 456), Nantes (− 3 928), Montpellier (− 3 889),
Marseille (− 3 627), puis Toulon, Bayonne, Cergy, Lille, Marne-la-Vallée.

Rien dans la chaîne ne dit si 2025 marque une reprise : la série
communale ne publie que les autorisations pour 2025, et la statistique
nationale (263 402) est au niveau de 2024. La formation de ménages,
elle, ne s'est pas arrêtée : les millésimes 2016-2022 la mesurent à
0,94 % par an.

## 3. Ce que cela fait à la proposition

Le deuxième article proposait un opérateur qui acquiert et rénove les
vacants durables des zones tendues, et construit sur friches là où le
gisement manque : 194 488 logements de détente, portés en dix ans à
raison de 19 400 par an. Rapporté au flux, ce stock vaut **1,3 an de
formation de ménages** des zones tendues.

Tant que le flux tenait — sur 2017-2022 — la détente par le stock
avait un sens : les 38 zones tendues en déficit ne portaient que 38 % du
besoin de détente, et leur déficit l'aurait consommé en six ans (médiane
par zone). Au rythme de 2023-2024, les 77 zones en déficit portent
**86 % du besoin de détente et le consomment en 2,9 ans** — le déficit
de flux mange en trois ans ce que l'opérateur mettrait dix ans à
produire, et l'opérateur, à son rythme, couvre un tiers du déficit
courant.

La conclusion ne renverse pas la proposition, elle la subordonne. La
détente du stock n'a de sens que si le flux revient au niveau de
2017-2022. Sinon, la contrainte dominante n'est plus le gisement
vacant, ni son prix, ni l'outil d'acquisition : c'est que l'on ne
construit plus, y compris là où l'on construisait le plus et où c'est
le plus cher. Le troisième étage de la proposition — construire sur
friches, où le foncier suffit — cesse d'être un arbitrage à la marge
pour devenir le cœur, et la question institutionnelle change : ce n'est
plus « qui porte le vacant ? », c'est « qui porte le chantier quand le
marché s'arrête ? ». L'étude ne répond pas ici ; elle établit que la
question est devenue première.

## 4. Ce que ces chiffres ne disent pas

- **Le sous-compte est national et uniforme** (H-21) alors que la
  non-remontée varie d'un département à l'autre : chaque solde par zone
  porte une incertitude de l'ordre de ± 10 % des chantiers (L-34).
- **Un chantier n'est pas un logement livré**, et Sitadel ne voit ni
  les démolitions ni les changements d'usage. L'écart entre chantiers
  et croissance du parc (66 318 par an) dépasse la mesure directe des
  sorties nettes de parc du ministère (27 000 par an, S-60) ; le reste
  est commencé non livré, annulé, ou lissage du recensement — jamais un
  chiffre de démolitions.
- **L'affectation du neuf aux résidences secondaires est une
  hypothèse**, bornée par « aucune » et « la structure de 2022 » ; le
  fichier détail du recensement permettrait de l'observer par zone
  d'emploi (année d'achèvement × catégorie), il n'est pas figé.
- **« Couvrir le flux » n'ajoute aucune vacance de fluidité** : le
  besoin de flux maintient la vacance de 2022, que le premier article
  juge insuffisante dans les zones tendues. Le stock et le flux sont
  deux besoins qui s'ajoutent, et la production de l'opérateur n'est pas
  nettée du flux.
- **Rien ici n'est causal**, et la maille des zones d'emploi masque
  l'infra-territorial : construire en périphérie couvre le ratio d'une
  zone sans détendre son centre.

## 5. Ce que la revue a changé

Trois relecteurs indépendants ont examiné le résultat le jour de sa
construction : 31 objections, 70 valeurs recalculées (exactes), cinq
sources ajoutées. La série a changé — la date réelle du producteur au
lieu de la date d'enregistrement, et le facteur de sous-compte. La
lecture a changé — les années 2023-2024, que la première version
écartait comme « incomplètes », sont closes et portent le résultat. Les
communes fusionnées avaient perdu 25 822 chantiers dans la jointure
géographique ; le fichier des mouvements de communes les a rendus. La
corrélation « nulle » entre construction et coût tenait aux 94 petites
zones aux ratios dégénérés ; au plancher de classement elle est
positive. Et le titre de la première version — « le flux n'est pas le
problème national » — est devenu son contraire. Les décisions
d'intégration et ce qui n'a pas été intégré sont dans le journal des
décisions (DEC-25 à DEC-28).

## 6. Ce qui vient

Le millésime 2025 des mises en chantier (série communale au printemps
2027) dira si le flux repart. Le fichier détail du recensement 2022
mesurerait l'affectation réelle du neuf par zone d'emploi. Et la
question que cet article ouvre — qui porte le chantier quand le marché
s'arrête — est celle du prochain : la production neuve elle-même,
sa structure (promotion, bailleurs sociaux, particuliers), son
financement et ce qui l'a arrêtée.

---

## Sources et reproduction

Sources nouvelles de cet article (figées et sommées dans
`logement/sources/sources.yaml`, 60 entrées au total) : SDES — série
communale Sitadel en date réelle (S-56), série nationale estimée (S-57),
note de présentation de la base open data 2021 (S-58), méthodologie
Sitadel (S-55), étude « Besoins en logements » 2025 (S-60), série
communale en date de prise en compte (S-54, trace) ; INSEE — recensement
2022 base communale, millésimes 2011/2016/2022 (S-11), code officiel
géographique 2026 et mouvements de communes (S-59). Hypothèse nouvelle :
H-21, facteur de sous-compte de la série communale.

Reproduction complète depuis le dépôt
[metabolisme](https://github.com/lbdremy/metabolisme), tag
`efficacite-parc-v0.7` :

```bash
cd logement
uv sync                     # environnement figé (uv.lock)
uv run logement validate    # registres + sha256 + graphe de preuves
uv run logement reproduce   # rebâtit les 16 artefacts data/processed/
./test.sh                   # 180 tests
```

Le document de preuve détaillé : `logement/evidence/efficacite-parc-immobilier.qmd`
(section R-18). Le compte rendu de la revue :
`logement/evidence/revue-contradictoire-2026-09-18-flux.md`.
