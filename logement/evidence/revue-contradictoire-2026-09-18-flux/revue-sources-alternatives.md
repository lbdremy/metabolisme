# Revue contradictoire R-18 (le flux) — relecteur « SOURCES ALTERNATIVES »

Date : 2026-09-18. Objet : C-16, O-41, T-18, R-18, I-18, L-34 ; sources S-54,
S-55 ; définition D-24 ; DEC-21..DEC-23 ; `core/flux.py`, `shell/build.py`
(`build_flux`, `_read_sitadel_annual`), `shell/acquire.py` (`run_sitadel`) ;
artefact `data/processed/flux-construction-menages-ze.json`.

## Méthode

1. Lecture des nœuds, des entrées de registre, du code et des décisions.
2. Recalcul des totaux nationaux de l'extrait figé S-54 (sha256 vérifié
   identique au registre : `ec50d34c…`) avec `uv run python`.
3. Interrogation du catalogue DiDo du SDES (producteur, API
   `data.statistiques.developpement-durable.gouv.fr/dido/api/v1`) pour
   les métadonnées du fichier source et de ses jeux frères ; téléchargement
   de trois séries alternatives du même producteur (communale annuelle en
   date réelle, nationale et départementale estimées en date réelle) ;
   recalcul de R-18 avec ces séries en injectant le tableau à la place de
   `_read_sitadel_annual` (aucun fichier du dépôt modifié).
4. Recoupement avec les chiffres publiés (INSEE « Logements mis en
   chantier », paru le 09/07/2026, source SDES Sitadel2) et avec la note
   méthodologique DR++ (SDES, 2025) et la « Présentation de la base
   nationale en open data des autorisations d'urbanisme » (SDES, 1er juin
   2021).
5. Vérification textuelle des citations de S-55 dans le HTML figé et sur la
   page en ligne ; vérification de la licence (mentions légales SDES,
   data.gouv).
6. Recherche des sources pour les ménages (INSEE, SDES), les disparitions
   de logements (SDES/Cerema, fichiers fonciers), l'affectation du neuf
   (fichier détail RP2022, liste des permis Sitadel).

URL vérifiées le 2026-09-18 :

- data.gouv, jeu `logements-autorises-et-commences-series-mensuelles-communales-en-date-de-prise-en-compte` (API `/api/1/datasets/…`) : licence `fr-lo`, `last_update` 2026-09-15, ressource CSV `ec384558-…` `last_modified` 2026-09-05, URL réelle de la ressource = DiDo datafile `577a8a66-4157-4787-b00a-031b61afea61`.
- DiDo datafile `577a8a66-…` (S-54) : millésime 2026-09, `last_modified` 2026-09-04, couverture 2013-01 → 2026-07.
- DiDo dataset `6513ee3a3b05e5cd969c270f` « Logements autorisés et commencés, nombre et surfaces, séries annuelles (données non estimées) » — datafile `9c90a880-4ba0-49b4-b99d-d7dd6c810dd0` « Données annuelles communales - Logements », « Données en date réelle à partir de 2011 », couverture 2013 → 2025, millésime 2026-09.
- DiDo dataset `6513eed03b05e5cd969c2710` « … séries mensuelles (données estimées) » — datafiles `175486a6-…` (national), `d264957b-…` (départemental), `f8883137-…` (régional), 2000-01 → 2026-07, millésime 2026-08.
- DiDo dataset `6513f0189d7d312c80ec5b5b` « Liste des permis de construire et autres autorisations d'urbanisme » — datafiles `8b35affb-…` (logements), `1a9a2f0c-…` (permis de démolir) ; pièces jointes : dictionnaires de variables, note de présentation (2021).
- https://www.statistiques.developpement-durable.gouv.fr/la-base-de-donnees-sitadel-methodologie (S-55, « Publié le 31/03/2026 », inchangée).
- https://www.statistiques.developpement-durable.gouv.fr/media/8697/download?inline (note DR++, SDES 2025).
- https://www.statistiques.developpement-durable.gouv.fr/media/8479/download?inline= (« Besoins en logements à horizon 2030, 2040 et 2050 », SDES, juin 2025, 83 p.).
- https://www.insee.fr/fr/statistiques/2015606 (« Logements mis en chantier », paru 09/07/2026).
- https://www.insee.fr/fr/statistiques/8647099 (fichier détail « Logements ordinaires en 2022 », paru 16/10/2025) + `varmod_LOGEMT_2022.csv`.
- https://www.insee.fr/fr/statistiques/8202874 (« Logements et résidences principales en 2021 », bases 2010/2015/2021).
- https://www.insee.fr/fr/statistiques/8640662 (Insee Focus 359, parc au 1er janvier 2025).
- https://www.observatoire-des-territoires.gouv.fr/nombre-de-logements-commences-constructions-neuves-par-pour-1-000-habitants.
- https://politiquedulogement.com/2025/12/mesurer-et-expliquer-les-disparitions-de-logements-en-france-une-approche-par-les-donnees-foncieres/ (Cerema, fichiers fonciers 2018-2024).
- https://www.statistiques.developpement-durable.gouv.fr/mentions-legales (licence du site SDES).

## Objections

### SA-1 (MAJEURE) — La série retenue sous-compte les mises en chantier d'environ 12 % par rapport à la statistique publiée du même producteur, et le sous-compte n'est ni une affaire de « date » ni compensé par la moyenne 2017-2022

**Énoncé.** O-41 présente « 377 769 en 2017, 361 803 en 2019, 345 203 en 2022 » comme « logements commencés en France (Sitadel) ». Le SDES publie, pour la même variable et le même champ (France hors Mayotte), 433 911 (2017), 385 384 (2019), 389 501 (2022) — séries « estimées en date réelle », reprises par l'INSEE (« 433,9 / 385,4 / 388,4 milliers », paru 09/07/2026, « SDES, Sitadel2, données brutes arrêtées à fin mai 2026 »). L'écart n'est pas un décalage de date : la série communale du producteur EN DATE RÉELLE (datafile `9c90a880-…`, années closes) donne 395 782 (2017), 341 882 (2019), 331 216 (2022) — elle reste 9 à 15 % sous la série estimée. La cause est documentée par le SDES : « On estime ainsi qu'environ 15 % des mises en chantier (malgré une relance courrier et plusieurs modalités de collecte) […] ne remontent jamais à Sitadel. Les statistiques publiées des logements commencés et annulés se fondent sur une enquête par sondage sur le champ non renseigné dans Sitadel, et diverses techniques d'estimation statistique » (Présentation de la base nationale en open data, SDES, 1er juin 2021, p. 7). La note DR++ (2025) : « chaque mois, seulement 80 à 85 % des autorisations et surtout 45 à 50 % des mises en chantier sont enregistrées dans Sitadel » ; l'enquête « anciens permis » « consolidait les informations à N-4 ». Le producteur avertit sur le fichier même de S-54 : « Données brutes en date de prise en compte administrative par l'application Sitadel, données à titre indicatif et non comparables aux données estimées en date réelle diffusées par ailleurs » (description DiDo du datafile `577a8a66-…`, absente de la note S-54).

**Preuve chiffrée** (LOG_COM « Tous Logements », sommes annuelles) :

| Année | S-54 extrait (DPC) | Communal date réelle (`9c90a880`) | National estimé date réelle (`175486a6`, hors Mayotte) | Écart S-54 / estimé |
|---|---|---|---|---|
| 2013 | 319 975 | 316 029 | 357 919 | − 10,6 % |
| 2017 | 377 769 | 395 782 | 433 911 | − 12,9 % |
| 2019 | 361 803 | 341 882 | 385 384 | − 6,1 % |
| 2022 | 345 203 | 331 216 | 389 501 | − 11,4 % |
| 2023 | 264 819 | 248 087 | 296 477 | − 10,7 % |
| 2024 | 234 808 | 212 868 | 259 595 | − 9,5 % |
| Moy. 2017-2022 | 349 169 | 350 918 | 398 852 | − 12,5 % |

Le rapport « estimé / communal date réelle » 2017-2022 vaut 1,138 en France et varie par département : médiane 1,196, p10 1,108, p90 1,314 (min 44 : 1,059 ; max 973 : 1,52 ; 75 : 1,164 ; 13 : 1,134 ; 34 : 1,137 ; 66 : 1,215 ; 64 : 1,173 ; 83 : 1,158 ; 06 : 1,163 ; 2B : 1,475). La non-remontée des DOC n'est donc pas uniforme dans l'espace : elle est plus forte hors des grandes agglomérations.

**Effet sur R-18** (recalcul complet de `build_flux` avec la série injectée ; artefact non modifié) :

| Variante | Commencés France | Ratio France | Ratio ZE tendues | Solde tendues | ZE tendues déficitaires | Déficit tendues | Années d'absorption (R-07) | Disparitions implicites |
|---|---|---|---|---|---|---|---|---|
| R-18 publié (S-54, DPC) | 347 340 | 1,04 | 0,97 | − 5 253 | 46 | 18 279 | 10,6 (37,5 hors RS) | 15 198 |
| Communal date réelle (années closes, PLM corrigé) | 343 696 | 1,02 | 0,96 | − 7 279 | 52 | 19 550 | 9,9 (34,7) | 11 554 |
| Communal date réelle × facteur départemental estimé | 397 387 | 1,18 | 1,10 | + 18 432 | 30 | 10 500 | 18,5 (152,9) | 65 245 |

Lecture : (i) la question « date de prise en compte vs date réelle » est bien sans effet sur la moyenne 2017-2022 — D-24 caveat 1 et L-34(1) sont VALIDÉS ; (ii) la question « déclarations jamais remontées » change le SIGNE du solde des ZE tendues (− 5 253 → + 18 432), le nombre de ZE tendues déficitaires (46 → 30) et double le temps d'absorption du stock (10,6 → 18,5 ans) ; la géographie des déficits, elle, tient (Montpellier − 1 224, Toulon − 1 119, Bayonne − 1 027, Perpignan − 974, Les Sables-d'Olonne, Narbonne, Nice, Pornic ; Marseille tombe à − 482) — l'énoncé « le déficit de flux est littoral et touristique » (I-18) survit, l'énoncé « ratio 0,97 des ZE tendues » et « l'essentiel du déficit des ZE tendues est la structure touristique » (R-18) ne survivent que sous une convention non déclarée (compter les seules DOC remontées). Recoupement externe : le SDES observe « le nombre de logements terminés sur cette période [2015-2020] est environ 1,5 fois supérieur à la progression du nombre de ménages » (Besoins en logements, juin 2025, encadré 1) ; R-18 donne commencés/ménages formés = 347 340/275 284 = 1,26 avec S-54 et 1,45 avec la série estimée — la série estimée est celle qui recoupe le producteur.

**Disposition proposée.** (a) Ne pas publier R-18 avec les seuls commencés « à titre indicatif » : enregistrer la série nationale et la série départementale estimées en date réelle (S-56, S-57) et publier R-18 en deux lectures — « déclaré » (S-54 ou mieux le communal en date réelle) et « estimé » (communal × facteur départemental estimé/déclaré 2017-2022, hypothèse H-xx explicite : non-remontée uniforme au sein du département) —, en faisant de la seconde la lecture centrale ou, à défaut, en encadrant tous les ratios par les deux. (b) Réécrire O-41 : les nombres actuels ne sont pas « les logements commencés en France » mais « les logements commencés déclarés dans Sitadel au 15/09/2026 », et citer en regard la série publiée (433 911 / 385 384 / 389 501). (c) Ajouter à D-24 et L-34 la cause documentée (≈ 15 % de DOC jamais remontées, enquête « anciens permis », estimation) avec la citation SDES 2021 — S-55 ne la contient pas. (d) Réviser I-18 : « le flux n'est pas le problème des zones tendues » devient plus vrai avec la série estimée (1,10), mais « Marseille et Montpellier font exception » et « ratio 0,97 » doivent être requalifiés.

### SA-2 (MAJEURE) — Une série communale « en date réelle », millésimée et publiée par le PRODUCTEUR existe ; DEC-22 l'a écartée sur un motif factuellement faux

**Énoncé.** DEC-22 abandonne l'option (c) « séries "en date réelle" millésimées diffusées par des portails tiers (Opendatasoft) » parce que « les miroirs ne sont pas le producteur, et leur date réelle n'est disponible qu'en millésimes fermés ». Or le SDES diffuse lui-même, dans le même catalogue DiDo que S-54, « Données annuelles communales - Logements » (dataset `6513ee3a3b05e5cd969c270f`, datafile `9c90a880-4ba0-49b4-b99d-d7dd6c810dd0`) : « Données portant sur les autorisations et les mises en chantier des logements neufs, selon le type de logement (individuel pur, groupé, collectif, en résidence), par commune. Données en date réelle à partir de 2011 », couverture 2013-2025, millésime 2026-09, 91,9 Mo (contre 1,27 Go pour le mensuel), colonnes ANNEE, COMM, TYPE_LGT, LOG_AUT, LOG_COM, SDP_AUT, SDP_COM — c'est-à-dire exactement l'extrait que `acquire-sitadel` reconstruit, mais à la date de l'événement, figeable tel quel dans le dépôt sans script de réduction ni fichier « NON figé ». L'Observatoire des territoires utilise cette famille de séries et rappelle la doctrine du SDES : les séries en date réelle « sont à privilégier aux séries en date de prise en compte pour les études locales, au niveau de la commune ou de l'EPCI ».

**Preuve.** Métadonnées DiDo citées ci-dessus ; téléchargement (sha256 `bddd6c4a…`, 463 366 lignes « Tous Logements », 36 737 codes dont 17 communes de Mayotte et les 20 arrondissements de Paris EN PLUS de 75056). Recalcul de R-18 : ratio France 1,02, tendues 0,96 — les résultats sont stables (cf. SA-1), ce qui prouve au passage que l'extrait S-54 est fidèle (les écarts annuels DPC/date réelle vont de − 5,8 % en 2019 à + 6,3 % en 2016 et se compensent sur 2017-2022 : 349 169 vs 350 918).

**Disposition proposée.** Substituer ce fichier à S-54 comme source du flux communal (S-54 reste utile pour 2026 en cours, pas pour R-18) ; corriger DEC-22 (le producteur publie bien une série communale en date réelle) ; la fenêtre 2013-2024 « longue » devient exploitable jusqu'en 2024 (2025 : LOG_COM entièrement vide dans ce millésime — à consigner). Attention au piège vérifié : le fichier contient 75056 ET 75101-75120 (sommes identiques : 16 053 sur 2017-2022) — `plm_parent` doublerait Paris (ratio 1,84 → 1,97, Lyon indûment en surplus) ; il faut exclure les arrondissements avant l'agrégation.

### SA-3 (SÉRIEUSE) — Les « disparitions implicites » (15 198/an) sont contredites par la mesure directe du SDES (27 000/an nettes, 50 000 démolitions) et l'écart s'explique par SA-1

**Énoncé.** R-18/L-34(2) présentent les disparitions comme un résidu non mesuré. Le SDES les mesure : « Sur cette période [2018-2023], il se crée, en moyenne sur une année, 27 000 logements à partir du parc non résidentiel. Dans le même temps, 14 000 logements sont transformés en locaux et 50 000 sont démolis. Les divisions accroissent le parc de 18 000 logements et les fusions le diminuent de 8 000 unités. Au total, le parc diminue sous l'effet des transformations en moyenne de 27 000 logements par an » ; « La part de logements subissant des transformations […] est en moyenne de 2 ‰ par an » ; « les démolitions (concernant 1 ‰ des logements) » (Besoins en logements, SDES, juin 2025, partie 6, source « Fichiers fonciers 2018-2023 (DGFiP-Cerema), calculs SDES »). Le Cerema (déc. 2025, fichiers fonciers 2018-2024) compte en brut « 99 000 logements fiscaux » disparaissant par an (démolitions ≈ 31 000, changements d'affectation 13 500, fusions 1 500, suppressions administratives 12 500, 23 % inclassables). Le résidu de R-18 (15 198) est inférieur à la mesure nette (27 000) parce que les commencés sont sous-comptés (SA-1) : avec la série estimée, le résidu passe à 65 245, cette fois au-dessus — l'écart restant (≈ 38 000) est le champ « commencé mais non livré / annulé après DOC » et le lissage censitaire, ce qui est exactement ce que L-34(2) doit dire.

**Disposition proposée.** Enregistrer la partie 6 de l'étude SDES (et l'article Cerema) comme source des sorties de parc ; remplacer « résidu, pas une mesure » par une confrontation résidu/mesure ; noter que la mesure est nationale (fichiers fonciers à la parcelle : une déclinaison ZE est possible via les fichiers fonciers Cerema, sous convention d'accès — hors open data).

### SA-4 (SÉRIEUSE) — L'affectation du neuf (RS / vacants / RP) est observable par ZE ; I-18 la traite comme « non observée »

**Énoncé.** L-34(3) : « dépend de qui achète le neuf (non observé) ». Deux sources l'observent. (1) Le fichier détail INSEE « Logements ordinaires en 2022 » (26 301 364 observations, 69 variables, Parquet 499 Mo, paru 16/10/2025) croise ACHL (année d'achèvement, une modalité PAR AN de 2006 à 2019 : C116 « En 2016 » … C119 « En 2019 », puis C2020-C2024 « (partiel) ») et CATL (1 résidences principales, 2 occasionnels, 3 résidences secondaires, 4 vacants) avec COMMUNE et IPONDL : on obtient par ZE les logements ACHEVÉS 2016-2019 (livraisons, pas mises en chantier) et leur statut en 2022 — le taux de RS du neuf récent, ZE par ZE, qui tranche entre les deux variantes de C-16. (2) La liste Sitadel des autorisations créant des logements (datafile `8b35affb-…`, depuis 2013 « en date réelle », 2017+ complet) porte RES_PRINCIP_OU_SECOND (« 1 = résidence principale, 2 = résidence secondaire, 3 = non rempli », « Seulement si occupation personnelle normalement » — donc les seuls maîtres d'ouvrage occupants, pas la promotion), NB_LGT_DEMOLIS (« Insuffisamment renseigné »), DATE_REELLE_DOC, DATE_REELLE_DAACT, et les indicateurs RES_TOURISME.

**Preuve.** `varmod_LOGEMT_2022.csv` (sha256 `22f92548…`) ; dictionnaire des variables PC logements (xls, dernière sauvegarde 12/06/2026, sha256 `b4002d23…`).

**Disposition proposée.** Un R-19 « affectation du neuf » à partir du fichier détail RP2022 (ACHL 2016-2019 × CATL × ZE) : il remplace l'encadrement « structure 2022 / hors RS » de C-16 par une mesure, et il donne les LIVRAISONS par ZE à comparer aux commencés (SA-1, SA-3). La liste des permis est un complément qualitatif (part de RS déclarée dans l'individuel pur en ZE littorales), pas une mesure.

### SA-5 (SÉRIEUSE) — La note S-54 omet l'avertissement du producteur et contient une erreur de champ ; la date de publication est celle de la page, pas du fichier

**Énoncé et preuve.** (a) La note ne cite pas la description DiDo du fichier : « données à titre indicatif et non comparables aux données estimées en date réelle diffusées par ailleurs » (cf. SA-1) — c'est la phrase qui aurait déclenché la recherche de SA-1/SA-2. (b) `geographic_scope` dit « arrondissements PLM séparés » : FAUX pour ce fichier — l'extrait ne contient aucun code 751xx/132xx/6938x (0 code) et contient 75056, 13055, 69123 ; le mappage `plm_parent` de `parse_sitadel_annual` est sans objet ici (mais indispensable pour le fichier de SA-2). (c) `publication_date: 2026-09-15` est le `last_update` de la page data.gouv (ressource HTML) ; la ressource CSV a `last_modified` 2026-09-05 et DiDo donne millésime 2026-09, `last_modified` 2026-09-04. (d) Champ : 36 708 codes, DOM (971-974) présents, Mayotte présente (17 communes, 550 commencés/an 2017-2022 — sans ZE dans S-06, donc hors R-18, alors que la série nationale publiée est « hors Mayotte » : à dire), Alsace-Moselle présente (1 634 communes) — exact. (e) Licence : data.gouv `fr-lo` (Licence Ouverte) — exact ; DiDo `legal_notice: SDES`.

**Disposition proposée.** Corriger (b) et (c), ajouter (a) et le champ Mayotte/hors-ZE ; garder la mention des 550 commencés/an de Mayotte dans `n_ze_sans_sitadel` ou la note.

### SA-6 (MINEURE) — S-55 : citations exactes, page inchangée, mais ce n'est pas la bonne page pour fonder D-24 et L-34, et la licence est à préciser

**Preuve.** Les cinq citations de S-55/D-24 sont textuellement présentes dans le HTML figé (sha256 `b4da7b9b…` vérifié ; apostrophes typographiques « ’ ») et sur la page en ligne (« Publié le 31/03/2026 ») : « transmises par les services instructeurs dans les six mois après le prononcé », « intervient généralement dans les dix-huit mois après l'ouverture de chantier », « Les séries estimées en date réelle visent à retracer dès le mois suivant… ». La page ne mentionne ni « date de prise en compte », ni la non-remontée définitive (≈ 15 %), ni l'enquête « anciens permis ». Licence : les mentions légales du site SDES disent « consultables et téléchargeables gratuitement sous licence ouverte telle que décrite dans le décret n°2017-638 ; sauf spécification contraire, elles peuvent être réutilisées à des fins commerciales […] que leurs sources et la date de leur dernière mise à jour soient mentionnées » — la formule actuelle « CRPA — Licence Ouverte 2.0 par défaut » est acceptable mais doit citer cette page.

**Disposition proposée.** Garder S-55 pour les délais ; adosser D-24 et L-34 à la note SDES 2021 (« Présentation de la base nationale en open data… », p. 6-7 : définition de la date de prise en compte, « environ 15 % des mises en chantier […] ne remontent jamais », « 74 % des autorisations […] reçues le premier mois, 84 % après deux mois, 93 % après 6 mois, 97 % au bout d'un an ») et à la note DR++ (2025).

### SA-7 (MINEURE) — Ménages : la source S-11 est la bonne, mais des millésimes intermédiaires et un comparateur officiel existent

**Énoncé.** L'INSEE publie les bases « chiffres clés logement » 2021 (millésimes 2010/2015/2021, géographie 2024) et 2020 (fichier détail 2020) : elles permettent une seconde fenêtre glissante 2015→2021 pour tester la sensibilité de la formation de ménages au lissage censitaire (L-34(4)) sans changer de source. Les projections de ménages par ZE ne sont pas publiées en fichier national (Omphale 2022 est déclinée par AAV dans les Insee Analyses régionales ; le SDES, « Projections du nombre de ménages à horizon 2030 et 2050 », déc. 2023, est national/régional). En revanche le SDES retient explicitement la MAILLE ZE pour les besoins en logements (« La maille retenue dans cette publication est celle des zones d'emploi définies par l'Insee » ; besoins liés aux ménages « évalués au niveau des zones d'emploi », juin 2025) et son modèle a la même structure que C-16 (ménages + RS + vacants + transformations du parc, « très proche de celle proposée par l'outil Otelo2 ») — C-16 devrait le citer comme comparateur, et signaler que le SDES ajoute la composante « renouvellement » (SA-3) que C-16 omet.

**Disposition proposée.** Citer le SDES 2025 dans C-16 ; ajouter une sensibilité 2015→2021 (bases 2021) à T-18 ; ne pas chercher d'Omphale par ZE en open data (inexistant).

## Chiffres recoupés

- Extrait S-54 : sha256 identique au registre ; 497 934 lignes, 36 708 codes ; totaux annuels recalculés IDENTIQUES à la note (2013 319 975 ; 2017 377 769 ; 2019 361 803 ; 2022 345 203 ; 2023 264 819 ; 2024 234 808 ; 2025 239 519 ; 2026 140 878). Moyenne 2017-2022 : 349 169 (France entière, Mayotte 550/an) — R-18 : 347 340 sur les communes jointes aux 305 ZE, cohérent.
- Série communale en date réelle du producteur (millésime 2026-09) : 2013 316 029 ; 2017 395 782 ; 2019 341 882 ; 2022 331 216 ; 2023 248 087 ; 2024 212 868 ; 2025 vide. Moyenne 2017-2022 : 350 918 (+ 0,5 % vs S-54). Écarts annuels S-54 / date réelle : 2014 + 5,0 %, 2016 + 6,3 %, 2019 − 5,8 %, 2021 + 5,8 %, 2022 − 4,2 %, 2024 − 10,3 %.
- Série nationale estimée en date réelle (SDES, hors Mayotte, millésime 2026-08) : 2016 369 432 ; 2017 433 911 ; 2018 400 477 ; 2019 385 384 ; 2020 369 647 ; 2021 414 193 ; 2022 389 501 ; 2023 296 477 ; 2024 259 595 ; 2025 263 402. Moyenne 2017-2022 : 398 852. INSEE (paru 09/07/2026, données arrêtées fin mai 2026) : 433,9 / 400,5 / 385,4 / 369,6 / 412,6 / 388,4 / 295,9 / 258,1 / 264,8 milliers — cohérent au millésime près.
- Rapport estimé / communal date réelle 2017-2022 : France 1,138 ; départements : médiane 1,196, p10 1,108, p90 1,314.
- SDES 2021 : « environ 15 % des mises en chantier […] ne remontent jamais à Sitadel » ; note DR++ 2025 : « 45 à 50 % des mises en chantier sont enregistrées » le mois même.
- SDES 2025 : logements terminés 2015-2020 ≈ 1,5 × ménages supplémentaires ; « + 234 000 ménages […] par an entre 2015 et 2020 » (métropole, RP). R-18 : 275 284 ménages/an 2016-2022 (France hors Mayotte, 305 ZE) — ordre de grandeur compatible (champ et fenêtre différents).
- Transformations du parc (SDES, fichiers fonciers 2018-2023, France hors Mayotte) : + 27 000 (local → logement), + 18 000 (divisions), − 8 000 (fusions), − 14 000 (logement → local), − 50 000 (démolitions) = − 27 000/an net. R-18 « disparitions implicites » : 15 198/an (S-54), 11 554 (date réelle), 65 245 (estimé).
- Recalculs R-18 (cf. tableau SA-1) : ratio France 1,04 / 1,02 / 1,18 ; ZE tendues 0,97 / 0,96 / 1,10 ; Paris 1,84 / 1,83 / 1,99 ; Montpellier − 1 994 / − 2 142 / − 1 224 ; Marseille − 1 450 / − 1 251 / − 482 ; MW p = 0,59 / 0,55 / 0,40 ; rho − 0,06 / − 0,07 / − 0,06.

## Sources à enregistrer

1. SDES, DiDo « Données annuelles communales - Logements » (séries annuelles, données non estimées, en date réelle), datafile `9c90a880-4ba0-49b4-b99d-d7dd6c810dd0`, millésime 2026-09 — https://data.statistiques.developpement-durable.gouv.fr/dido/api/v1/datafiles/9c90a880-4ba0-49b4-b99d-d7dd6c810dd0/csv — 91 895 467 octets, sha256 `bddd6c4a39965260583f832db15b6b8ec71fae33610186f2b92f0c8dc8c0bd82` (téléchargé 2026-09-18). Page catalogue : https://www.statistiques.developpement-durable.gouv.fr/catalogue?page=dataset&datasetId=6513ee3a3b05e5cd969c270f.
2. SDES, DiDo « Données mensuelles nationales - Logements » (données estimées en date réelle, hors Mayotte, brut et CVS-CJO, 2000-2026), datafile `175486a6-76a3-4c6c-a34b-aeb96758910b`, millésime 2026-08 — …/datafiles/175486a6-76a3-4c6c-a34b-aeb96758910b/csv — 199 038 octets, sha256 `7666ee0d581afb8c689c4b7bf3477ceabd7b18537ee61f5c5f5f100c71da17aa`.
3. SDES, DiDo « Données mensuelles départementales - Logements » (estimées en date réelle), datafile `d264957b-c6d2-4efa-bf5e-6a8da836550a`, millésime 2026-08 — 6 291 300 octets, sha256 `5c32cd64100a0ae3877fff54558ba3c686ad254563771a345939a91dd3715ca8`.
4. SDES, « Note de synthèse de la révision de la méthode d'estimation à date réelle (DR++) des logements autorisés et mis en chantier à l'aide du Machine Learning » (2025) — https://www.statistiques.developpement-durable.gouv.fr/media/8697/download?inline — 699 669 octets, sha256 `6823dac078a6b8bcbd5b489a3370f7011b25679f6554335791bcea265754f457`.
5. SDES, « Présentation de la base nationale en open data des autorisations d'urbanisme (extraite de Sitadel) », mise à jour le 1er juin 2021 — https://data.statistiques.developpement-durable.gouv.fr/dido/api/files/52ce326b-45b2-42ce-a2e7-4a60554ef559 — 179 545 octets, sha256 `b3d250b187c47de641d18ed741ccfe1238cb950606c0691000b1a25ed8bc1e3a`.
6. SDES, « Dictionnaire des variables des permis de construire des logements » (xls, 12/06/2026) — https://data.statistiques.developpement-durable.gouv.fr/dido/api/files/ab799b04-0b03-4f96-949c-eb23c478a8e8 — 64 000 octets, sha256 `b4002d2358d29db6b0f7bba47f83901d376363e94e6bfd4a620e5e78a6e69104` ; jeu « Liste des autorisations d'urbanisme créant des logements », datafile `8b35affb-55fc-4c1f-915b-7750f974446a` (non téléchargé) ; « Liste des permis de démolir », datafile `1a9a2f0c-56fe-4e69-84a7-fbbda2121f02` (non téléchargé).
7. SDES, « Besoins en logements à horizon 2030, 2040 et 2050 », collection Études, juin 2025, B. Boutchenik, G. Rateau, 83 p. — https://www.statistiques.developpement-durable.gouv.fr/media/8479/download?inline= — 6 180 689 octets, sha256 `7b2d22747a848eba38b966b61acc754d925a32d9e07609c33a47fce1586d240b`.
8. SDES, « Projections du nombre de ménages à horizon 2030 et 2050 : analyse des modes de cohabitation et de leurs évolutions », document de travail n° 64, décembre 2023 — https://www.statistiques.developpement-durable.gouv.fr/sites/default/files/2023-12/document_travail_64_projections_menages_decembre2023_0.pdf (non téléchargé).
9. INSEE, « Logements mis en chantier », paru le 09/07/2026 — https://www.insee.fr/fr/statistiques/2015606 (source SDES Sitadel2, données brutes arrêtées à fin mai 2026, France hors Mayotte).
10. INSEE, fichier détail « Logements ordinaires en 2022 », paru 16/10/2025 — https://www.insee.fr/fr/statistiques/8647099 ; dictionnaire https://www.insee.fr/fr/statistiques/fichier/8647099/varmod_LOGEMT_2022.csv — 5 029 272 octets, sha256 `22f925488a22aac99830a4302ecddfde48d52a04181d4b814f94249408428c86` (fichier national Parquet 499 Mo non téléchargé).
11. INSEE, « Logements et résidences principales en 2021 » (bases communales 2010/2015/2021) — https://www.insee.fr/fr/statistiques/8202874 ; fichier détail 2020 — https://www.insee.fr/fr/statistiques/7705908.
12. Cerema (via politiquedulogement.com, déc. 2025), « Mesurer et expliquer les disparitions de logements en France : une approche par les données foncières » — 99 000 logements fiscaux/an 2018-2024.
13. Observatoire des territoires, indicateur « Nombre de logements commencés (constructions neuves) par an pour 1 000 habitants » (Sit@del2 en date réelle, ZE 2020 disponible) — recoupement possible de R-18 par ZE.
14. SDES, mentions légales (licence ouverte, décret n° 2017-638) — https://www.statistiques.developpement-durable.gouv.fr/mentions-legales (pour S-55).

Fichiers téléchargés conservés dans le scratchpad de session (`/private/tmp/claude-501/-Volumes-Work-github-metabolisme/b4485b8b-294c-44f1-b226-62a47ec57d06/scratchpad/`), rien ajouté au dépôt.

## Verdict

L'extrait S-54 est fidèle à sa ressource et le choix « date de prise en compte » est sans effet sur la moyenne 2017-2022 (recalculé avec la série en date réelle du producteur : 1,04 → 1,02) ; mais la série retenue compte les seules DOC remontées et sous-estime les mises en chantier de ≈ 12 % par rapport à la statistique publiée du SDES (≈ 15 % de DOC jamais déclarées, estimées par enquête), écart non uniforme (p10-p90 départemental 1,11-1,31) qui renverse le signe du solde des ZE tendues (− 5 253 → + 18 432) et double le temps d'absorption du stock (10,6 → 18,5 ans), tout en laissant intacte la géographie littorale des déficits. R-18 ne peut être publié qu'en double lecture « déclaré / estimé » avec O-41 requalifié ; le producteur publie la série communale en date réelle que DEC-22 croyait absente, le SDES mesure les sorties de parc (− 27 000/an nets) et le fichier détail RP2022 (ACHL × CATL) observe l'affectation du neuf par ZE — trois sources à enregistrer avant l'article 3.
