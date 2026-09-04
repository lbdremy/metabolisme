*Août 2026 — premier article de l'étude « Efficacité du parc immobilier
français » du programme Métabolisme. Tout chiffre cité ici provient d'une
chaîne de preuves exécutable : un dépôt public où chaque source est figée et
sommée (sha256), chaque définition datée, chaque hypothèse nommée avec sa
plage de plausibilité, et chaque résultat recalculable par une commande.
Version de référence : tag `efficacite-parc-v0.5` du dépôt
[metabolisme](https://github.com/lbdremy/metabolisme), document de preuve
`logement/evidence/efficacite-parc-immobilier.qmd`. Les identifiants entre
parenthèses (S-xx, R-xx, I-xx, L-xx…) pointent vers ce dépôt.*

---

## La question

La France compte 38,4 millions de logements et environ 2,96 millions
d'entre eux sont vacants (7,7 % du parc en 2025 — France hors Mayotte,
S-01/S-02). Faut-il en conclure
qu'il suffirait de « remplir les logements vides » ? Ou au contraire qu'il
faut construire massivement ? La question posée par l'étude est plus
précise :

> Dans quelle mesure le parc immobilier français permet-il de loger
> correctement la population, dans les territoires où elle souhaite ou a
> besoin de vivre, à un coût soutenable et avec une mobilité suffisante ?

Une règle normative encadre tout le travail (V-01) : **une résidence
principale occupée n'est jamais une inefficience**. Ni sa surface, ni sa
« sous-occupation » statistique ne sont comptées comme capacité disponible.
Le champ légitime de l'analyse est la capacité qui ne sert à personne :
vacance durable, dégradation, blocage.

Deux revues contradictoires (quatre relecteurs indépendants chacune, 2026-08-07
et 2026-08-09) ont attaqué ces résultats — 44 objections pour la seconde,
arithmétique confirmée partout, mais plusieurs interprétations requalifiées.
Ce qui suit est l'état APRÈS revue : les énoncés qui ont tenu.

## 1. Le stock a suivi les ménages — le problème n'est pas le nombre brut

Depuis 1982, le parc de logements et le nombre de ménages croissent au même
rythme (indices 156,2 et 155,2 en 2022, base 100 en 1982), très au-dessus de
la population (121,9) : la construction a d'abord accompagné la
**décohabitation** — des ménages plus petits et plus nombreux (R-01, I-01).
Vers 2005-2006 le régime s'inverse : le parc croît désormais plus vite que
les ménages, et l'écart se loge dans la vacance, passée d'un minimum de
6,2 % en 2005 à 7,7 % en 2025.

Le « problème du logement » national n'est donc pas d'abord un déficit brut
de logements par rapport aux ménages. Les écarts sont ailleurs : dans la
disponibilité réelle, la localisation, l'accès économique et la mobilité.
C'est ce que le reste de la chaîne instruit.

## 2. La vacance durable existe — et elle est majoritairement là où l'emploi croît

Le parc privé compte environ **1,15 million de logements vacants depuis plus
de deux ans** (fichiers LOVAC, dernier millésime comparable, R-02) — environ
3,5 % du parc privé, un ordre de grandeur stable quel que soit le millésime
retenu. Deux corrections s'imposent d'emblée :

- ces fichiers **surestiment** la vacance réelle : la Cour des comptes
  (S-22) documente ~25 % de « faux vacants » ; l'étude propage donc un taux
  d'existence de 0,75 (plage 0,6-0,9, hypothèse H-12) dans tous les calculs ;
- la géographie a **deux régimes** (I-02) : en intensité, les taux élevés
  sont ruraux et ultramarins ; en volume, les grandes villes dominent.

Le résultat le plus contre-intuitif (R-03, I-03) : **78 à 88 % du volume de
vacance durable se trouve dans des zones d'emploi où l'emploi croît**. La
corrélation avec le déclin de l'emploi est réelle en intensité (taux médian
4,5 % dans les zones d'emploi déclinantes contre 2,9 % ailleurs) mais
l'essentiel de la capacité sortie d'usage coexiste avec la demande. Les
causes du blocage sont donc à chercher au niveau du bâti, de la propriété et
des successions — pas dans « la France qui se vide ».

De fait, en métropole, la vacance durable est un phénomène du **bâti ancien**
(corrélation +0,56 avec l'âge du parc, du même ordre que le coût et l'emploi,
R-08) ; l'écologie fine (SDES, S-23) montre ~45 % d'obsolescence et ~20 % de
successions. Et le coût n'explique pas la vacance : là où le logement est
cher, le parc est presque entièrement utilisé (R-04) — le coût marque la
tension, il ne crée pas la vacance (I-04). Les résidences secondaires non
plus, à cette échelle : les zones touristiques ont une vacance plus BASSE
(R-05, I-05).

Ce coût se mesure : se reloger aux loyers d'annonce 2025 coûterait au ménage
médian de la zone d'emploi médiane **~27 % de son revenu** (jusqu'à 40 % au
standard de surface du parc en place — plage de l'hypothèse H-07), et à
Paris 64 à 94 % : la relocation y est hors de portée du ménage médian local
à toutes les valeurs de l'hypothèse (R-06, I-06).

## 3. Le test central : le gisement couvre à peine le besoin, et pas au bon endroit

L'étude définit un besoin de **détente** : ramener chaque zone d'emploi
tendue à un taux de vacance disponible de fluidité (6 %, plage 5-7 %,
hypothèse H-08) — le niveau nécessaire pour que les déménagements soient
possibles. Résultat (R-07) :

- **97 zones d'emploi tendues** (15,26 millions de logements de parc) ;
- besoin national de détente : **194 488 logements** ;
- gisement structurel effectif local (LOVAC × 0,75) : **206 664** ;
- couverture : **1,06**.

Une couverture de 1,06 ressemble à un « ça passe ». La revue contradictoire
a imposé la lecture honnête (I-07) : **la suffisance est marginale et
conditionnelle**. La grille de sensibilité (H-08 × H-12) traverse 1 — de
0,82 à 1,85 selon les hypothèses ; au périmètre légal des communes en zone
tendue, la couverture tombe à 0,69 ; et surtout **le gisement n'est pas là
où est le besoin** : 68 % du besoin se trouve dans des zones d'emploi NON
couvertes par leur gisement local (déficit incompressible ~58 000
logements). La détente par la seule remobilisation des vacants n'est PAS
démontrée — c'est une contribution substantielle (~137 000 logements
rénovables), pas une solution.

## 4. Remobiliser coûte deux fois moins cher que construire — mais rien ne se déclenche tout seul

Détendre les 97 zones tendues par la règle mixte — rénover le gisement local
là où il existe, construire au prix du neuf là où il manque — coûterait
**~15,8 milliards d'euros** (14,9-17,1), contre ~32,9 milliards en
construction neuve équivalente : **ratio ~2,1** (R-09). Le ratio résiste aux
tests de stress : encore ≥ 1,5 en doublant le coût de réhabilitation. Mais
la revue a cadré l'argument (I-09) : il est solide en DIRECTION, plus étroit
en AMPLEUR qu'annoncé initialement, il s'agit d'un investissement total (pas
d'un coût public), et le canal incitatif censé le déclencher a un bilan
documenté faible — la taxe sur les logements vacants obtient ~3 % de sorties
de vacance en 4 ans en zone tendue (Cour des comptes, S-22).

Le foncier, lui, n'est pas la contrainte (R-10) : les seules friches « sans
projet » recensées dans les zones tendues porteraient, à densité de ville
dense, ~2,12 millions de logements — **10,9 fois le besoin** ; même au
plancher opérationnel constaté des opérations réelles du fonds friches
(30,3 logements/ha), c'est encore 2,2 fois le besoin.

D'où la conclusion de l'arc (I-10), qui est le premier titre de cette
étude : **le volume vacant ne suffit qu'à l'échelle agrégée et sous
conditions ; la contrainte institutionnelle n'est pas la conséquence de la
suffisance, elle en est la CONDITION.** Détendre suppose de lever les
verrous de propriété et de succession, de construire sur friches là où le
gisement manque, et de maintenir le flux de construction — la remobilisation
est un gain de stock unique, pas un flux.

## 5. Pendant ce temps, la mobilité résidentielle chute — partout

La seconde moitié de l'étude instruit l'hypothèse H-04 : le parc permet-il
les mobilités nécessaires ? Quatre mesures, issues de trois appareils
statistiques différents, disent la même chose : **ça se grippe**.

**La rotation du parc ralentit partout et la baisse s'accélère** (R-11). La
part des résidences principales occupées depuis moins de deux ans passe de
13,14 % (2012) à 11,97 % (2023) — ~364 000 emménagements récents
« manquants » dans le stock 2023, en ordre descriptif — et la baisse
s'accélère (−0,92 point sur 2017-2023 seul). 293 zones d'emploi sur 305
baissent. Le vieillissement de la population en explique une part réelle
mais **minoritaire** : ~45 % au shift-share démographique de l'étude (T-16),
14 % dans l'analyse INSEE sur la mobilité des personnes (S-33). Le signal
résiduel est l'ACCÉLÉRATION — que le vieillissement, graduel, ne produit
pas. La revue a par ailleurs fait tomber une interprétation séduisante : la
chute est plus forte dans les zones tendues en points (−1,54 vs −1,27), mais
ce contraste disparaît à niveau initial contrôlé — il est réel, mais ne
discrimine pas entre explications.

**Le parc social ne tourne plus, et son niveau est le miroir du marché**
(R-12). Le taux de mobilité du parc social passe de 9,29 % (2019) à 7,11 %
(2025), avec une accélération après 2022 (−1,43 point sur 2022-2025) ;
286 zones d'emploi sur 303 baissent. Le niveau, lui, reflète
l'accessibilité du marché local depuis au moins 2013 : corrélation de −0,80
avec le coût en 2025 (déjà −0,70 en 2013) — dans les zones tendues, la
mobilité médiane est de 6,74 % avec une vacance sociale de 1,63 % ; à Nice
ou Marseille, un logement social se libère environ tous les 20-25 ans. Et
en relatif comme à niveau initial contrôlé, la chute récente est **au moins
aussi forte dans les marchés chers** (−26,0 % vs −22,5 % ; partielle −0,50) :
là où le marché est le plus inaccessible, le parc social gèle encore plus.

**Les personnes bougent par le locatif privé** (R-13). 9,87 % des personnes
changent de logement chaque année ; les entrées de l'année représentent
19,51 % du locatif privé, contre 8,34 % du parc HLM et 5,73 % de la
propriété occupante. Le locatif privé est LE canal des mobilités : le
renchérir comprime la mobilité de tous. Les soldes migratoires parisiens
(−1,40 %/an) ont le profil du cycle de vie — seul le groupe 15-24 ans est
entrant net, les sorties nettes sont aux âges famille et retraite (O-36) ;
l'éviction par les prix reste une question ouverte, pas un résultat.

**Sortir par l'achat paie un péage lourd, et surtout fiscal** (R-14).
Acheter coûte 6,7 à 8,1 % du prix en frais de transaction (droits
d'enregistrement territorialisés, émoluments, contribution de sécurité
immobilière) : presque plat en taux, très inégal en poids — **6,15 mois de
niveau de vie médian** dans la zone d'emploi médiane (7,87 mois dans les
zones tendues contre 5,59 ailleurs ; jusqu'à ~11-13 mois à Paris, au Pays
basque, dans les DOM chers ; 5,81 mois au scénario primo-accédant).
Annualisé, ce péage vaut ~2,6 %/an du niveau de vie pour un ménage qui
reste 20 ans — mais ~10-13 %/an pour un ménage mobile tous les 5 ans : il
frappe d'abord la mobilité répétée. **83,2 % de ce péage est fiscal** —
c'est un paramètre institutionnel direct, pas une fatalité de marché.

## 6. Ce que ces chiffres ne disent pas

La méthode impose de publier les limites avec les résultats. Les
principales :

- **Descriptif, pas causal.** Aucun de ces résultats n'établit de lien
  causal (péage → gel, vacance → rotation). Les quatre mesures de mobilité
  partagent en outre le même étalon de croisement territorial (indice de
  coût et statut de tension, limite L-26) : leurs corrélations avec « le
  coût » ne sont pas quatre confirmations indépendantes.
- **Le choc du crédit n'est pas séparé.** Les fenêtres d'accélération
  (2021-2023, 2022-2025) recouvrent le choc des taux 2022-2024 (~1 % →
  > 4 %, Banque de France S-36). La part cyclique et la part structurelle
  des chutes récentes seront arbitrées par les millésimes 2026/2027.
- **Un vacant durable n'est pas un logement du besoin** : petits logements,
  bâti ancien, obsolescence (L-18) ; et la mobilisabilité COMPORTEMENTALE
  (successions, rétention) n'est pas paramétrée (L-17).
- **Les niveaux de coût sont des majorants** : loyers d'annonce 2025
  (charges comprises) rapportés à des revenus 2021 (L-09) ; le péage R-14
  est au contraire un plancher (ni frais d'agence ni débours, L-25).

## 7. Ce qui vient

Le diagnostic dessine la suite. Trois observations trancheraient
l'instruction de la mobilité : les discontinuités des droits de mutation aux
frontières départementales croisées avec les volumes de ventes (test de
causalité du péage), la rotation par âge et territoire (fichier détail du
recensement), et les millésimes 2026/2027 du parc social (rebond = cyclique,
persistance = structurel).

Et surtout : la proposition institutionnelle. L'étude établit que la détente
est possible en volume (à peine, sous conditions), qu'elle est environ deux
fois moins chère que le tout-neuf, que le foncier n'est pas la contrainte —
et que rien de tout cela ne se déclenche sans lever les verrous de
propriété, sans construire là où le gisement manque, et sans traiter un
péage de mobilité à 83 % fiscal. Concevoir ce mécanisme — inspectable,
sources ouvertes, hypothèses nommées — est l'objet du prochain article.

---

## Sources et reproduction

Principales sources (toutes publiques, figées et sommées dans
`logement/sources/sources.yaml` — 38 entrées) : INSEE (parc de logements
EAPL S-01/S-02, ménages S-03, recensements S-11/S-27/S-29, Filosofi S-10,
Insee Première n° 2073 S-33, estimations de population S-38) ; MTE/Cerema
(LOVAC S-05, Cartofriches S-20) ; ANIL/DHUP (carte des loyers 2025 S-09) ;
SDES (RPLS S-28, enquête Logement S-12, Datalab vacance S-23) ; DGFiP/Etalab
(DVF S-30, droits d'enregistrement S-31/S-35/S-37) ; Cour des comptes
(S-22) ; Banque de France (S-36) ; ANCOLS (S-34) ; Apur (S-24) ; Cerema
fonds friches (S-25/S-26) ; ADEME (DPE S-16) ; Enertech (S-17) ; Banque des
Territoires (S-18).

Reproduction complète depuis le dépôt
[metabolisme](https://github.com/lbdremy/metabolisme), tag
`efficacite-parc-v0.5` :

```bash
cd logement
uv sync                     # environnement figé (uv.lock)
uv run logement validate    # registres + sha256 + graphe de preuves
uv run logement reproduce   # rebâtit les 14 artefacts data/processed/
./test.sh                   # 153 tests
```

Le document de preuve détaillé (chiffres, code, sensibilités, limites,
comptes rendus des deux revues contradictoires) :
`logement/evidence/efficacite-parc-immobilier.qmd`.
