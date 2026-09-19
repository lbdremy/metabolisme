# Revue contradictoire 2026-09-18 — relecteur « statistique et arithmétique » (R-18, article 3)

Périmètre : R-18, I-18, L-34, O-41, C-16, T-18 (`evidence/claims.yaml`), la
section R-18 de `evidence/efficacite-parc-immobilier.qmd`, le bloc R-18 de
`EVIDENCE.md`, l'artefact `data/processed/flux-construction-menages-ze.json`
et `tests/test_flux.py`. Recalcul indépendant depuis les sources figées :
S-11 (`insee-rp-base-cc-logement-2022.zip`), S-54 (extrait annuel
Sitadel), S-06 (table d'appartenance 2026). Le script n'importe pas
`logement.core.flux` ; il emprunte au dépôt la table communes → ZE
(`ze.parse_commune_ze`, `lovac.plm_parent`), le drapeau de tension R-07
(`build._tension_flag_with_variants`), l'indice de coût (`build._cost_frame`)
et les noms de ZE (`build._ze_names`). Le besoin de détente 194 488 est lu
dans `tension-manque-absolu-ze.json` (`national.besoin_logements`).

## Commandes

```
cd logement
uv run python evidence/revue-contradictoire-2026-09-18-flux/verify-flux.py
```

(pandas 2, engine calamine ; pas de scipy dans l'environnement — le
Mann-Whitney est recalculé par comptage direct des paires puis par
permutation à 20 000 tirages, l'intervalle de Spearman par bootstrap à
3 000 tirages, en plus de la formule de Fisher/Bonett-Wright du dépôt.)

Résultat brut : **0 écart** entre l'artefact et le recalcul sur les blocs
`national`/`tendues`/`autres`, les parts, les quantiles, les trois
classements (32 entrées × 7 champs), la sensibilité H-08, le bloc
`stock_vs_flux` et les compteurs. Les objections qui suivent portent sur
ce que ces chiffres mesurent, sur ce qui tombe à la jointure, et sur la
transcription dans les textes.

## Objections

### ST-1 — MAJEURE (pour l'énoncé, pas pour la conclusion) : « le ratio n'est pas corrélé au coût » n'est pas établi — le signe dépend du plancher que l'étude applique elle-même ailleurs

**Énoncé.** R-18 publie ρ = − 0,06 [− 0,18 ; 0,06] (n = 279) entre le
ratio production (commencés / besoin) et l'indice de coût, et en tire « à
cette maille, la construction ne suit pas la cherté » ; I-18 reprend
« le ratio n'est pas corrélé au coût ». Or l'échantillon inclut 72 ZE
sous le plancher de classement de 200 ménages formés par an (C-16,
`seuil_classement_formation_an`), là où le dénominateur du ratio est
quasi nul et le ratio dégénéré (Côte-sous-le-Vent 69,8 avec 0,46 ménage
formé par an ; Guéret 32,8 ; Épernay 10,7 ; Nevers 9,9 ; Le
Centre-Atlantique 10,1). L'étude exclut ces ZE de ses classements mais
les garde dans sa corrélation.

**Preuve (recalcul).**

| plancher (ménages/an) | n | ρ Spearman | IC 95 % |
|---|---|---|---|
| 0 (publié) | 279 | − 0,059 | [− 0,18 ; + 0,06] (bootstrap [− 0,19 ; + 0,08]) |
| 100 | 241 | + 0,184 | [+ 0,06 ; + 0,30] |
| **200 (plancher C-16)** | **207** | **+ 0,227** | **[+ 0,09 ; + 0,35]** (bootstrap [+ 0,08 ; + 0,36]) |
| 300 | 181 | + 0,174 | [+ 0,03 ; + 0,31] |
| 500 | 131 | + 0,054 | [− 0,12 ; + 0,22] |
| 1 000 | 75 | + 0,115 | [− 0,12 ; + 0,33] |

Au plancher de l'étude, la corrélation est **positive et significative** :
les ZE chères construisent plutôt *plus* que leur besoin, pas moins. Le
mécanisme de confusion est visible : ρ(ratio × formation) = − 0,22 et
ρ(coût × formation) = + 0,55 — le ratio est mécaniquement haut là où la
formation est faible (petites ZE bon marché), ce qui fabrique le − 0,06.
Le solde pour 1 000 logements (une mesure non dégénérée) donne
ρ = − 0,10 [− 0,22 ; + 0,01] ; l'intensité (commencés pour 1 000
logements) donne ρ = + 0,68 [+ 0,61 ; + 0,75] et un Mann-Whitney
tendues/autres AUC 0,84, p ≈ 10⁻²¹ — cette partie de R-18 (« mais
l'intensité si ») est solide.

**Disposition.** Publier le Spearman au plancher de classement (cohérence
interne avec C-16) ou sur le solde pour 1 000 logements, avec la table
de sensibilité au plancher ; remplacer dans R-18 et I-18 « le ratio n'est
pas corrélé au coût » par « le signe de la corrélation ratio × coût
dépend du plancher (− 0,06 sur 279 ZE, + 0,23 sur les 207 ZE classables) :
aucune corrélation négative n'apparaît ». La conclusion de I-18 n'est pas
affectée (elle repose sur les totaux et sur la géographie des déficits,
pas sur cette corrélation).

### ST-2 — MOYENNE : les médianes 1,02 / 0,98 et le p = 0,59 excluent les 20 ZE à besoin nul, toutes d'un seul groupe

**Énoncé.** C-16 rend le ratio « indéfini » quand les ménages baissent
(besoin = 0). Ces 20 ZE sont toutes dans « autres » (0 en tendues), et
toutes construisent (de 231 à 250 logements/an pour Charleville-Mézières
ou Vitry-le-François Saint-Dizier) : leur production dépasse infiniment
leur besoin. Les retirer du test de rang n'est pas neutre — un test de
rang n'a pas besoin d'une valeur finie, seulement d'un rang, et ces ZE
occupent sans ambiguïté le rang maximal.

**Preuve (recalcul).** Sans elles (publié) : médiane tendues 1,016,
autres 0,978, U = 8 766 (n 97/188), AUC 0,481, p = 0,5934 (permutation
20 000 tirages : 0,5933 — la formule de `stats.mann_whitney_p` est
confirmée). Avec elles au rang maximal : médiane autres 1,017 ≈ tendues
1,016, AUC 0,434, **p = 0,065**, et le sens s'inverse (autres > tendues).
Médiane « autres » hors RS : 1,05 ; tendues hors RS : 1,16.

**Disposition.** Publier la variante « ZE à besoin nul au rang maximal »
à côté du p ; la phrase « les médianes ne distinguent pas tendues et
autres » reste vraie mais son p est fragile (0,59 → 0,07) et son sens
change. Reformuler C-16 : « publiées, jamais infinies » vaut pour le
ratio publié, pas pour le test de rang.

### ST-3 — MOYENNE : 943 codes Sitadel n'ont pas de ZE — 7 670 commencés (2017-2022) tombent à la jointure, et l'une des entrées nommées de R-18 change de signe

**Énoncé.** La jointure `annual.merge(commune_ze, how="inner")` est
silencieuse ; l'indicateur publié `n_ze_sans_sitadel = 0` dit que chaque
ZE a des commencés, pas que chaque commencé a trouvé sa ZE. Sitadel code
les communes au COG de l'événement, pas « au millésime de publication »
comme l'affirme la note S-54 : Olonne-sur-Mer (85166) et
Château-d'Olonne (85060), fusionnées le 1ᵉʳ janvier 2019, produisent des
commencés jusqu'en 2019 (216/343/199 et 144/172/246 en 2017-2019) ;
Annecy-le-Vieux (74011), Seynod (74268) et Meythet (74182), fusionnées
en 2017, jusqu'en 2017 (608, 275, 81) ; Pierrefitte-sur-Seine (93059,
absorbée par Saint-Denis en 2025) jusqu'en 2026 ; Orée-d'Anjou est
codée 49069 dans Sitadel et 49126 dans la table 2026 (recodage).

**Preuve (recalcul).** Sitadel brut 2017-2022 : 2 095 014 commencés
(349 169/an) = 347 340 (artefact) + 1 278/an perdus (943 codes, 0,37 %)
+ 550/an de Mayotte (ZE 0601, hors cadre censitaire, 3 301 commencés).
Perte concentrée sur 2017-2019 (2 817 / 1 887 / 1 536, puis 337-587) et
sur les départements 85 (1 734), 69 (1 132), 74 (1 044), 93 (963), 49
(551). Sur la fenêtre longue 2013-2024 la perte est de 25 961 commencés
(2 163/an, 0,69 % de 315 519). Effet sur les entrées nommées :

| ZE | commencés/an | solde | solde hors RS | ratio |
|---|---|---|---|---|
| Les Sables-d'Olonne (+ 85166 + 85060 : + 220/an) | 865 → 1 085 | − 818 → − 598 | **− 190 → + 30** | 0,51 → 0,64 |
| Annecy (+ 74011 + 74268 + 74182 : + 161/an) | 2 635 → 2 795 | + 33 → + 194 | + 421 → + 582 | 1,01 → 1,07 |
| Paris (+ 93059 : + 160/an) | 35 015 → 35 176 | + 16 014 → + 16 175 | + 17 122 → + 17 283 | 1,84 → 1,85 |

R-18 écrit « Les Sables-d'Olonne (36 %) de − 818 à − 190 » : après
rattachement de ses deux communes fusionnées, la ZE est à l'équilibre
hors RS (+ 30), ce qui renforce d'ailleurs la lecture I-18 (déficit =
structure touristique) mais rend le chiffre publié faux. Les autres
codes perdus (69152, 69211, 69159, 01091, 22123, 85021, 85224, 85107…)
ne sont pas identifiés ici ; la borne majorante « tous en ZE tendues »
déplacerait le solde des tendues de − 5 253 à − 3 974 (ratio 0,97 → 0,98)
— le bloc agrégé est robuste, les entrées ZE ne le sont pas toutes.

**Disposition.** Ajouter une table de passage COG (historique des
communes INSEE, millésimes 2013-2026) à l'acquisition Sitadel, ou à
défaut publier dans l'artefact `n_codes_sitadel_sans_ze`,
`commences_sans_ze_an` (fenêtre courte et longue) et rattacher à la
main les dix plus gros codes ; corriger l'entrée Les Sables-d'Olonne
dans R-18/EVIDENCE.md ; corriger la note S-54 (« codes au millésime de
publication » → « codes au COG de l'événement, communes fusionnées sous
leur ancien code jusqu'à l'année de fusion incluse »).

### ST-4 — MINEURE : huit communes du recensement à valeurs manquantes sont sommées comme zéro sans signalement (règle 9)

**Énoncé.** `groupby("ze").sum()` traite NaN comme 0 ; aucun compteur ne
le dit. Huit communes ont un NaN dans P16_MEN/P22_MEN : Sannerville
(14666, P16 NaN, P22 790), Les Hauts-Talican (60694, P16 NaN, P22 230),
L'Oie (85165) et Sainte-Florence (85212, P16 NaN, P22 fractionnaires
489,6 et 516,8 — valeurs estimées par l'INSEE), et quatre communes du
Cantal (15031, 15035, 15047, 15171, tout NaN).

**Preuve (recalcul).** Le biais brut serait + 132 ménages/an (ZE 2804
Caen, tendue), + 168 (5213 Les Herbiers-Montaigu), + 38 (0054 Beauvais).
Mais la commune-parente des défusions porte les ménages 2016 dans la
même ZE : Troarn 14712 passe de 2 241 (P16) à 1 463 (P22), Essarts-en-
Bocage 85084 de 3 447 à 2 729 — le biais au niveau ZE est nul pour Caen
et Les Herbiers ; il reste + 38 ménages/an pour Beauvais (commune
nouvelle 2019 sans rétropolation). Aucun chiffre publié n'est affecté.

**Disposition.** `sum(min_count=1)` ou un compteur `n_communes_na` par
ZE dans l'artefact, à l'image de `n_communes_masquees` en R-03.

### ST-5 — MINEURE : l'agrégation PLM du recensement tient à l'ordre du fichier, et le test entérine une sémantique fausse

**Énoncé.** `parse_census_vintages` mappe les arrondissements sur la
commune-parente puis `drop_duplicates(subset="code", keep="first")`. Le
fichier S-11 contient à la fois 75056 et 75101-75120 (idem Lyon,
Marseille). Le résultat est juste parce que la ligne 75056 précède
75101 dans le fichier (vérifié : parente avant ses arrondissements pour
les trois villes ; commune = Σ arrondissements sur les six colonnes) —
juste par construction du fichier, pas du code. `test_parse_census_
vintages_maps_plm_and_drops_duplicates` teste un fichier SANS ligne
parente et affirme que Paris = le premier arrondissement (P22_MEN = 130
au lieu de 260) : si un millésime futur omettait la ligne commune ou la
plaçait après, Paris compterait pour un vingtième sans qu'aucun test ne
le voie.

**Disposition.** Exiger la ligne parente (lever `FluxError` sinon) ou
sommer les arrondissements et asserter l'égalité avec la parente ;
corriger le test.

### ST-6 — MINEURE : transcriptions entre l'artefact et les textes

| Où | Publié | Recalculé | Correction |
|---|---|---|---|
| R-18, EVIDENCE.md, qmd (via artefact) | « 10,3 commencés pour 1 000 logements en ZE tendues » | médiane 10,247 ; l'artefact publie 10,25 (2 déc.) et le texte arrondit une seconde fois | 10,2 (le « deux fois plus » de I-18 tient : 10,25 / 5,08 = 2,02) |
| I-18, L-34 | « Paris construit 1,8 fois sa formation de ménages » ; « 1,84 avec une formation de ménages faible » | 1,84 = commencés / **besoin** (19 001) ; commencés / formation (16 514) = 2,12 | « 1,8 fois son besoin de flux, 2,1 fois sa formation de ménages » |
| I-18 | « la structure du parc (25-36 % de résidences secondaires) » | ZE tendues déficitaires : 1,8 % à 59,3 %, médiane 24,9 % ; les ZE nommées vont de 18,8 % (Toulon) à 40,7 % (Challans) | donner la plage réelle ou nommer les ZE |
| I-18 | « une trentaine de ZE littorales », « presque toutes littorales » | non chiffré dans l'artefact : 46 ZE tendues déficitaires ; 23 redeviennent ≥ 0 hors RS, 23 restent déficitaires, dont Meaux, Creil, Bourgoin-Jallieu, Dreux, Chalon-sur-Saône, Ancenis, Digne-les-Bains (non littorales) | publier le compte (23 ZE dont le signe tient à la structure RS) et retirer « presque toutes » |
| R-18 | « 54 % de la formation de ménages (150 057/an) » | part publiée 54,3 % = numérateur ET dénominateur écrêtés à 0 (276 110) ; 150 057 / 275 284 = 54,5 % | préciser la convention ou publier 54,5 |
| S-54 (notes) | « arrondissements PLM séparés » | l'extrait figé ne contient que 75056 / 13055 / 69123 (aucun code 751xx/132xx/6938x) | corriger la note |
| qmd | « 37 ans hors RS » | 37,54 | acceptable (arrondi à l'année) |

### ST-7 — INFORMATION : la sensibilité à la fenêtre Sitadel n'est pas publiée, et la fenêtre retenue est la plus favorable

**Preuve (recalcul, même besoin, mêmes ZE).**

| fenêtre commencés | national/an | ratio national | tendues/an | ratio tendues | solde tendues | déficit ZE tendues déficitaires | années d'absorption |
|---|---|---|---|---|---|---|---|
| 2017-2022 (publié) | 347 340 | 1,035 | 180 190 | 0,972 | − 5 253 | 18 279 | 10,6 |
| 2016-2021 | 341 112 | 1,017 | 179 312 | 0,967 | − 6 130 | 17 834 | 10,9 |
| 2017-2023 | 335 458 | 1,000 | 173 325 | 0,935 | − 12 118 | 22 034 | 8,8 |
| 2018-2023 | 328 927 | 0,980 | 169 008 | 0,911 | − 16 435 | 25 484 | 7,6 |

L'alignement sur les millésimes censitaires (C-16, D-24) est défendable
mais « le flux national est couvert » vaut 1,00-1,04 selon la fenêtre :
c'est une couverture marginale, comme R-07 l'était pour le stock. La
formation de ménages a accéléré (239 103/an en 2011-2016 → 275 284 en
2016-2022) et la construction a chuté depuis 2023 (O-41) : la
sensibilité mérite d'être publiée à côté de H-08. À noter aussi : le
besoin national à structure nationale (334 455) diffère de 0,3 % de la
somme des besoins par ZE (335 470) — effet de convexité négligeable ;
les autorisés 2017-2022 (458 572/an, 229 988 en tendues) ne sont pas
exploités.

### ST-8 — MINEURE : invariants non protégés par les tests

Tous les invariants ci-dessous **passent sur les données réelles**
(vérifié) ; l'objection porte sur leur absence dans `tests/test_flux.py`,
qui n'en garantirait aucun après un changement de code :

- ratio ≥ 0 et NaN si et seulement si besoin = 0 ; solde = commencés −
  besoin sur toutes les lignes (testé sur une seule) ;
- besoin hors RS ≤ besoin et solde hors RS ≥ solde partout ;
  logements par ménage formé ≥ 1 sur la sortie de `flux_by_ze` (la
  propriété Hypothesis actuelle teste l'identité arithmétique
  1/(1 − a − b) ≥ 1, pas le code) ; part RS + part vacants < 1 ;
- tendues + autres = national pour chaque agrégat (n, ménages, formation,
  besoin, commencés, croissance du parc, disparitions) ; parts ∈ [0, 100]
  et part(tendues) + part(autres) = 100 pour les quatre parts ;
- `n_ze_sous_seuil_classement`, `sensibilite_h08`, `n_ze_sans_sitadel`
  et les compteurs `n_ze_deficitaires` / `n_ze_menages_en_baisse` ne sont
  pas testés ;
- aucun test ne fait tomber une commune Sitadel hors table (ST-3) ni ne
  vérifie que la somme des commencés par ZE égale le total Sitadel moins
  les pertes déclarées ;
- l'ordre PLM (ST-5) n'est pas testé.

## Tableau : publié / recalculé / écart / verdict

| Chiffre-titre | Publié | Recalculé | Écart | Verdict |
|---|---|---|---|---|
| ZE | 305 | 305 (+ 0601 Mayotte hors cadre censitaire) | 0 | ✔ |
| ménages 2016 / 2022 | 29 236 888 / 30 888 593 | 29 236 888 / 30 888 593 | 0 | ✔ |
| formation de ménages /an | 275 284 | 275 284,2 | 0 | ✔ |
| commencés /an 2017-2022 | 347 340 | 347 340 (Sitadel brut 349 169 ; − 1 278 sans ZE, − 550 Mayotte) | 0 | ✔ (ST-3 sur les pertes) |
| commencés /an 2013-2024 | 315 519 | 315 519 (− 2 163/an sans ZE) | 0 | ✔ |
| besoin de flux / hors RS | 335 470 / 297 873 | 335 470 / 297 873 | 0 | ✔ |
| ratio national / hors RS | 1,04 / 1,17 | 1,035 / 1,166 | 0 | ✔ (1,00-1,04 selon la fenêtre, ST-7) |
| croissance du parc /an | 332 142 | 332 142 | 0 | ✔ |
| disparitions implicites /an | 15 198 | 15 198 | 0 | ✔ |
| ZE déficitaires (national) / ménages en baisse | 147 / 20 | 147 / 20 | 0 | ✔ |
| ZE sans Sitadel / sous plancher | 0 / 94 | 0 / 94 (dont 11 tendues) | 0 | ✔ mais `0` ne mesure pas les 943 codes sans ZE (ST-3) |
| ZE tendues | 97 | 97 (R-07 au central H-08 = 6 %, H-12 = 0,75) | 0 | ✔ |
| formation tendues /an | 150 057 | 150 057 | 0 | ✔ |
| besoin tendues / commencés | 185 443 / 180 190 | 185 443 / 180 190 | 0 | ✔ |
| ratio tendues / hors RS | 0,97 / 1,13 | 0,972 / 1,128 | 0 | ✔ (0,91-0,97 selon la fenêtre) |
| solde tendues | − 5 253 | − 5 253 | 0 | ✔ (− 3 974 si toutes les pertes ST-3 étaient tendues) |
| ZE tendues déficitaires / déficit | 46 / 18 279 | 46 / 18 279 | 0 | ✔ |
| hors RS : solde / déficit | + 20 423 / 5 181 | + 20 423 / 5 181 (23 ZE) | 0 | ✔ |
| autres : ratio | 1,11 | 1,114 | 0 | ✔ |
| parts tendues : formation / besoin / commencés / parc | 54,3 / 55,3 / 51,9 / 40,7 | 54,35 / 55,28 / 51,88 / 40,65 | 0 | ✔ (54,5 en net, ST-6) |
| médianes ratio tendues / autres | 1,02 / 0,98 | 1,016 / 0,978 | 0 | ✔ mais 1,017 « autres » avec les ZE à besoin nul (ST-2) |
| Mann-Whitney p | 0,59 | 0,5934 (paires), 0,5933 (permutation) | 0 | ✔ mais 0,065 avec les ZE à besoin nul (ST-2) |
| commencés pour 1 000 : tendues / autres | 10,25 / 5,08 (texte : 10,3 / 5,1) | 10,247 / 5,082 | texte : + 0,1 | ✗ texte → 10,2 (ST-6) |
| Spearman ratio × coût (France) | − 0,06 [− 0,18 ; 0,06], n 279 | − 0,059 [− 0,18 ; + 0,06], bootstrap [− 0,19 ; + 0,08] ; n = 305 − 20 − 8 + 2 | 0 | ✔ chiffre, ✗ énoncé : + 0,23 [0,09 ; 0,35] au plancher 200 (ST-1) |
| Spearman métropole | − 0,08 [− 0,20 ; 0,04], n 270 | − 0,083 [− 0,20 ; + 0,04], 270 | 0 | ✔ |
| besoin de détente R-07 | 194 488 | 194 488 | 0 | ✔ |
| années d'absorption / hors RS / formation | 10,6 / 37,5 / 1,3 | 10,64 / 37,54 / 1,296 | 0 | ✔ (8,8 / 7,6 ans selon la fenêtre, ST-7) |
| Montpellier | − 1 994 → − 762 (13,1 % RS) | − 1 993,8 → − 762,1 | 0 | ✔ |
| Perpignan | − 1 484 → + 9 (29,9 % RS) | − 1 483,9 → + 9,1 | 0 | ✔ |
| Bayonne | − 1 466 → − 319 (23,6 %) | − 1 466,5 → − 319,5 | 0 | ✔ |
| Marseille | − 1 450 → − 1 080 (5,0 %) | − 1 450,4 → − 1 080,2 | 0 | ✔ |
| Toulon | − 1 449 → − 427 | − 1 449,0 → − 427,0 | 0 | ✔ |
| Les Sables-d'Olonne | − 818 → − 190 (35,9 %) | − 818,1 → − 189,8 ; **− 598 → + 30** avec Olonne-sur-Mer et Château-d'Olonne | 0 artefact / + 220 réel | ✗ (ST-3) |
| Nice (non tendue) | − 1 062 | − 1 061,8 | 0 | ✔ |
| Paris | 35 015 / 19 001 = 1,84 | 35 015 / 19 000,6 = 1,843 (35 176 avec Pierrefitte) | 0 | ✔ (× formation = 2,12, ST-6) |
| Rennes / Marne-la-Vallée | 1,21 / 1,39 | 1,212 / 1,387 | 0 | ✔ |
| sensibilité H-08 : solde tendues 5 % / 7 % | − 5 387 (54 ZE) / + 9 946 (170 ZE) | − 5 387 / + 9 946 | 0 | ✔ |
| O-41 : commencés 2017 / 2019 / 2022 / 2023 / 2024 / 2025 | 377 769 / 361 803 / 345 203 / 264 819 / 234 808 / 239 519 | identiques | 0 | ✔ |
| PLM recensement | commune = Σ arrondissements | vérifié pour 75056, 13055, 69123 | 0 | ✔ (fragile, ST-5) |
| communes recensement absentes de Sitadel | — | 0 | — | ✔ |
| codes Sitadel absents de la table 2026 | non publié | 943 codes, 7 670 commencés 2017-2022 (0,37 %), 25 961 sur 2013-2024 | — | à publier (ST-3) |
| communes recensement à NA | non publié | 8 ; effet ZE + 38 ménages/an (Beauvais) | — | à publier (ST-4) |

## Verdict

1. **Arithmétique : irréprochable.** Chaque chiffre de R-18, I-18, du qmd et
   d'EVIDENCE.md se reproduit exactement depuis les sources figées par un
   calcul indépendant (0 écart sur ~70 valeurs), et les invariants (ratio
   ≥ 0, solde = commencés − besoin, hors RS ≤ avec RS, tendues + autres =
   national, parts sommant à 100) tiennent sur les données réelles.
2. **Statistique : deux énoncés à requalifier et une entrée à corriger.**
   « Le ratio n'est pas corrélé au coût » ne survit pas au plancher de
   classement de l'étude (ρ = + 0,23 [0,09 ; 0,35] sur les 207 ZE
   classables — ST-1) ; le p = 0,59 des médianes devient 0,07 dès qu'on
   cesse d'exclure les 20 ZE sur-productrices d'un seul groupe (ST-2) ;
   Les Sables-d'Olonne passe à + 30 hors RS quand on rattache ses deux
   communes fusionnées, que la jointure perd en silence avec 941 autres
   codes (ST-3).
3. **Conclusion I-18 : elle tient** (flux couvert au national à 1,00-1,04
   selon la fenêtre ; déficit des ZE tendues porté par la structure RS ;
   intensité deux fois plus forte en tendues, ρ = + 0,68 avec le coût),
   à condition de publier les sensibilités (plancher, ZE à besoin nul,
   fenêtre Sitadel), de compter les commencés perdus, et de corriger cinq
   transcriptions (10,2 ; Paris 2,1 × formation ; plage RS ;
   « trentaine » ; note S-54).
