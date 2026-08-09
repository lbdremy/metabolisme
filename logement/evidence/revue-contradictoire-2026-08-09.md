# Revue contradictoire — R-11..R-14 (2026-08-09)

Compte rendu de la revue contradictoire exigée par la méthode (INTRO
étape 12), menée le 2026-08-09 sur les quatre résultats de la session 4
(R-11..R-14, instruction de H-04 « mobilités empêchées »), postérieurs à
la revue du 2026-08-07. État examiné : commit `d563df4`, tag
`efficacite-parc-v0.4`. Les corrections sont commitées (code + artefacts
+ registres, un commit par livrable) ; ce document consigne la méthode,
les objections et leur disposition, et le tableau avant/après.

## Méthode

Quatre relecteurs indépendants (agents distincts, sans accès aux
conclusions des autres), sur les mêmes angles qu'en 2026-08-07, plus une
synthèse de triage par l'orchestrateur :

1. **Sources alternatives** — SA-1..SA-9 (9 objections)
2. **Hypothèses et définitions** — HD-1..HD-14 (14 objections)
3. **Scénarios d'échec** — SE-1..SE-12 (12 objections)
4. **Statistique** — ST-1..ST-9 (9 objections) + ~60 recalculs depuis le brut

Les cinq rapports bruts (dont la synthèse de triage) sont commités en
annexe dans `evidence/revue-contradictoire-2026-08-09/`, avec le script
de vérification de l'orchestrateur (`verify-se-partials.py`) : les
recalculs structurants allégués (corrélations partielles SE-1/SE-4/SE-6,
gradient par millésime SE-5) ont été refaits indépendamment AVANT le
triage et confirmés à ± 0,02.

L'arithmétique publiée a été recalculée indépendamment depuis les
données brutes figées : **exacte partout** (~60 chiffres, zéro
divergence ; deux coquilles de transcription — Porto-Vecchio 13,0→13,1,
énumérations sélectives d'O-33). Comme en 2026-08-07, les objections
portaient sur les modèles et la mise en récit, pas sur les calculs.

## Verdict global

- **Survivent tels quels** : les quatre MESURES (niveaux, distributions,
  classements, conventions C-09/C-10 — toutes deux vérifiées robustes),
  la structure par statut de R-13 (19,51/8,34/5,73), le recoupement
  MIGCOM × RPLS, la part fiscale ~83 % et les niveaux absolus de R-14.
- **Ne survivait pas tel quel : l'étage interprétatif.** Les quatre
  phrases-titres — « gel concentré dans les marchés verrouillés »
  (I-11), « chute uniforme » + « corrélation la plus forte de la
  chaîne » (R-12/I-12), « validation croisée entre sources
  indépendantes » (R-13/I-13), « le péage se superpose au gel » (I-14)
  — ont chacune été requalifiées.
- **La conclusion d'arc v0.3 est inchangée** (couverture ~1
  conditionnelle, ratio ~2, contrainte institutionnelle = condition) ;
  une phrase de garde a été ajoutée au document de preuve (SE-11).

## Décisions actées par Rémy (avant intégration)

1. Intégration complète des 44 objections.
2. Les quatre calculs nouveaux : trois vues R-11/R-12, scénarios H-13 +
   territorialisation S-31 + CSI, décomposition AGEREVQ des soldes
   parisiens, shift-share démographique (pyramide S-38 figée).
3. Enregistrement des sources citées par les claims (S-33..S-38).

## Objections structurantes et leur disposition

### Grappe A — indépendance des preuves et axes partagés

| # | Objection | Disposition |
|---|---|---|
| A1 | **« Sources indépendantes » R-11×R-13** (HD-1 majeure, SE-7) : S-27 et S-29 = même appareil RP/EAR (3 enquêtes communes sur 4 — l'EAR 2021 a été reportée, D-18 corrigée) | **Requalifiée** : cohérence interne du recensement ; MIGCOM×RPLS promue validation inter-appareils (R-13/I-13, EVIDENCE, D-18) |
| A2 | **Étalon commun T-05/T-08 lu quatre fois** (HD-2, SE-10) ; `fillna(False)` classait Mayotte « autres » | **L-26 créée** (transverse, portée par R-11..R-14) ; contrastes publiés aux bornes H-08 dans les quatre artefacts ; tension inconnue exclue des médianes et comptée |
| A3 | **Superlatif « la plus forte de la chaîne »** (ST-1) : R-14 +0,81 ≈ R-12 −0,80, IC chevauchants — récidive du motif C1/2026-08-07 | **Abandonné** : « parmi les plus fortes, indistinguable de R-13/R-14 » |
| A4 | **Croisement −0,20 construit** (SE-6, vérifié : partiel +0,22) | Publié brut ET à coût contrôlé ; « masquage » requalifié en corollaire des gradients |

### Grappe B — cadrage des chutes (niveau initial, démographie, cycle)

| # | Objection | Disposition |
|---|---|---|
| B1 | **R-11 « gel concentré » = artefact du niveau initial** (SE-1 MAJEURE, vérifiée : partiel −0,07 ≈ 0) vs ST : écart de médianes significatif (MW p = 0,003) | **Arbitré** : le FAIT survit (publié avec ses tests MW), l'ATTRIBUTION tombe — trois vues publiées (points/relatif/partiel), I-11 requalifiée « compatible, non discriminant », l'argument « sens opposé niveau/chute » retiré (il était logiquement inversé) |
| B2 | **R-12 « chute uniforme » inversée par le même contrôle** (SE-4, vérifiée : partiel −0,49) | Trois vues publiées aussi pour R-12 : uniforme en points, EXCÉDENTAIRE dans les marchés chers en relatif/partiel — plus favorable à H-04 que le texte d'avant revue ; cadrage commun R-11/R-12 |
| B3 | **Part démographique chiffrable et bornée** (SE-2 ; SA-1 INSEE 14 % ; SA-2 ANCOLS 9 %) | **Shift-share T-16 publié** (−0,42 pt, −4,0 % relatif, ~45 % de la chute de rotation transposée — S-38 figée) ; bornes externes S-33/S-34 enregistrées et citées ; l'ACCÉLÉRATION, que le vieillissement ne produit pas, devient le signal résiduel |
| B4 | **Choc du crédit 2022-2025 absent de la chaîne** (SA-3, SE-3 — convergence de deux relecteurs indépendants) | S-36 figée (Stat Info BdF) ; caveat cyclique dans L-22/L-23 ; « la chute s'accélère » ne se titre plus comme aggravation du verrouillage ; arbitres inscrits dans NEXT-STEPS (RPLS 2026/2027, prochain L_STAY) |
| B5 | **Le rho −0,80 est un gradient ancien** (SE-5, vérifié : −0,69 dès 2013) | Rho publiés aux trois millésimes ; I-12 : « miroir du marché depuis au moins 2013 », le nouveau = creusement −0,68 → −0,80 |

### Grappe C — R-13 (migrations)

| # | Objection | Disposition |
|---|---|---|
| C1 | **Soldes des cœurs chers sous-déterminés** (SE-8) : déficit parisien ancien, destinations d'aménité, « contre la géographie de l'emploi » sans croisement emploi | **Décomposition AGEREVQ calculée** (O-36) : seul groupe positif 15-24, sorties nettes aux âges famille/retraite — profil de CYCLE DE VIE ; I-13(3) requalifiée (éviction = question ouverte) ; « contre la géographie de l'emploi » retiré |
| C2 | **Datation du 9,87 %** (SA-7) : la série publiée est à 8,8 % en 2023 | R-13/L-24 datent le niveau (moyenne de fenêtres 2020-2024, série descendante S-33) |
| C3 | **Multiplicité** (ST-3) : solde×coût −0,15 et +0,19 ne tiennent pas Bonferroni à 16 tests | Marqués « non robustes à la correction de multiplicité » (R-12/R-13, L-23/L-24) ; les conclusions principales (p ≪ 1e-6) survivent à toute correction |
| C4 | **Labels et périmètres** (HD-10/HD-11, ST-7) | STOCD 21 précisé dans L-24 ; « statut le moins mobile » reformulé en « entrées » ; énumérations d'O-33 complétées (La Tarentaise, Marie-Galante, Carhaix, Ghisonaccia, Draguignan) |

### Grappe D — R-14 (transaction) et H-13

| # | Objection | Disposition |
|---|---|---|
| D1 | **Sensibilité H-13 annoncée, non publiée ; scénario « haut » fantôme** (HD-3) ; le 5,81 manquant est AUSSI le scénario primo et le droit commun (HD-5/HD-12) | **Scénarios {5,09 ; 5,81 ; 6,32} publiés** (mois médians 5,22/5,81/6,22) ; H-13 réécrite (5,81 nommé) ; « chaque achat paie 6,32 % » corrigé |
| D2 | **Territorialisation possible depuis S-31** (HD-4) — biais dans le sens de la thèse (Nice/Menton) | **Territorialisé** : taux par département lus sur le PDF figé (11 départements à 4,50 % — le 65 manquait à la note S-31, corrigée), moyenne par ZE pondérée par les ventes |
| D3 | **Rho +0,81 quasi mécanique ; annualisation absente** (SE-9 : rho(mois, prix) = 0,98 ; ST écarte l'artefact de diviseur commun) | Publiés : rho mois×prix, annualisation 5/10/20 ans (2,6-10,2 %/an, 13,1 % tendues à 5 ans) ; I-14 requalifiée — l'apport de R-14 = niveau absolu + ~83 % fiscal, pas une confirmation du gel |
| D4 | **Assiette invisible ; petites ZE DOM ; pas de seuil** (HD-6/HD-7, ST-8) | Assiette publiée (127 555 mutations multi = 375 007 logements ~34 % ; 13 029 mixtes ; 6 320 hors bornes ; 332 sans ZE) ; ZE « bornes sensibles » nommées ; seuil de classement 100 ventes (symétrique du seuil R-12) |
| D5 | **Millésimes et fraîcheur** (ST-2 prix 2025/revenus 2021 ; SA-4 table DMTO 06/2026) | L-25(6) créée (même motif que C2/2026-08-07) ; S-35 figée en trace de fraîcheur ; lecture temporelle du péage écrite dans L-25(2) |
| D6 | **CSI exclue à tort** (SA-5) | **Intégrée** (0,10 %, min 15 €, S-37) — le plancher se resserre, la part fiscale passe à 83,2 % |

### Mineures intégrées (grappe E)

HD-8 (deltas C-09 = taux + recomposition — caveat L-23, médianes
vérifiées insensibles), HD-9 (le secret RPLS ne touche que les loyers —
constat favorable écrit dans O-28/L-23), HD-13 (O-26 redescendue en
constat), HD-14 (D-18 : quatre EAR, source ajoutée), ST-4 (IC
Bonett-Wright — tous les IC élargis de ≤ 0,01), ST-5 (contrôle C-09
non arrondi : dérives réelles ≤ 0,010), ST-6 (13,0 → 13,1), ST-9
(garde min_count + tests), SE-11 (phrase de garde du qmd), SA-6
(licence RPLS confirmée Licence Ouverte), SA-8/SA-9 (littérature OCDE
consignée pour P-xx ; frontières Fidéli/EnL/notaires dans NEXT-STEPS).

### Objections écartées, avec raison

- **« Le péage annualisé est trop petit pour geler »** (SE-9, comme
  réfutation d'I-14) : une taxe sur la transaction pénalise précisément
  le comportement rare dont H-04 s'inquiète, et la littérature
  (OCDE/CAE) documente l'effet DMTO→mobilité — retenue seulement comme
  demande de publication de l'annualisation (faite).
- **Recentrage du central H-13 sous 6,32** (HD-4, partie
  « sémantique ») : le central décrit le droit voté majoritaire ; la
  territorialisation répond mieux qu'un déplacement du central — pas de
  recalibrage silencieux d'une hypothèse.
- **Clôture de SE-1 par le test de significativité de ST** : les deux
  verdicts portent sur des énoncés différents (fait vs attribution) —
  réconciliés, aucun écarté.

## Tableau avant/après des chiffres et énoncés-titres

| Grandeur / énoncé | Avant (v0.4) | Après (2026-08-09) |
|---|---|---|
| R-11 titre | « le gel se concentre dans les marchés verrouillés — signature d'une mobilité empêchée » | « chute générale (−11 % relatif) ; contraste tendues/autres significatif (MW p = 0,003) mais porté par le niveau initial (partiel −0,07) — compatible avec H-04, non discriminant » |
| R-11 −1,17 pt / ~364 000 | publiés entiers | publiés avec la décote démographique (~45 % au shift-share T-16 ; INSEE 14 %, S-33) et le caveat du cycle (S-36) |
| R-12 « chute UNIFORME » | telle quelle | « uniforme en points (−2,40/−2,45), excédentaire dans les marchés chers en relatif (−26,0/−22,5 %) et à niveau contrôlé (partiel −0,50) » |
| R-12 « corrélation la plus forte de la chaîne » | telle quelle | « parmi les plus fortes, indistinguable de R-13/R-14 » ; gradient publié aux trois millésimes (−0,70/−0,68/−0,80) |
| R-12 croisement segments −0,20 | « troisième fait » | corollaire des gradients de coût (partiel +0,21) |
| R-13 « validation croisée entre sources indépendantes » | telle quelle | « cohérence interne du recensement ; validation inter-appareils : MIGCOM 8,34 % ≈ RPLS 8,0-8,5 % » |
| R-13 soldes parisiens | « contre la géographie de l'emploi — partir n'est pas toujours choisi » | profil par âge du cycle de vie (O-36 : seul groupe positif 15-24) ; éviction = question ouverte |
| R-14 péage | 7,4-8,0 % ; 6,14 mois ; tendues 7,76/5,53 ; « superposé au gel » (rho +0,81) | territorialisé + CSI : 6,7-8,1 % ; 6,15 mois (en niveau de vie 2021) ; tendues 7,87/5,59 ; rho +0,81 quasi mécanique (mois×prix 0,98) — apport propre : niveau absolu, 83,2 % fiscal, scénario primo 5,81 mois, annualisation 2,6-10,2 %/an |
| Bilan H-04 | « quatre mesures indépendantes qui se recoupent » | « quatre mesures issues de trois appareils, croisées contre un étalon partagé (L-26) ; recoupements externes réels : MIGCOM×RPLS, bornes démographiques S-33/S-34 » |
| IC de Fisher | 1/√(n−3) | Bonett-Wright (1+ρ²/2)/(n−3) — bornes élargies de ≤ 0,01, aucune conclusion ne bascule |

## Ce qui reste ouvert

1. **Rotation par âge × ZE** (SE-1c) — fichier détail Logement du RP
   (ANEM × AGEMEN8) : ferait renaître ou réfuterait proprement I-11.
2. **Millésimes post-normalisation des taux** (SE-3) — RPLS 2026/2027
   et prochain L_STAY : rebond → cyclique ; persistance → structurel.
3. **Discontinuités DMTO × volumes DVF** (SE-12/D2) — vers un test de
   causalité du péage (S-31 territorialisée le permet désormais).
4. **Frontières consignées** (SA-9) : Fidéli, EnL 2020, bases
   notariales, DV3F — toutes sous habilitation ; données des figures
   d'IP2073 figées avec S-33 pour la série annuelle de mobilité.
5. Les restes ouverts de la revue du 2026-08-07 (emploi récent,
   réconciliation LOVAC, point Paris/Apur) sont inchangés.
