# Synthèse de triage — revue contradictoire R-11..R-14 (2026-08-09)

Synthèse de l'orchestrateur sur les quatre rapports de relecture indépendants
(mêmes angles que la revue du 2026-08-07 : sources alternatives SA-1..SA-9,
hypothèses/définitions HD-1..HD-14, scénarios d'échec SE-1..SE-12,
statistique ST-1..ST-9 — 44 objections). État examiné : commit `d563df4`,
tag `efficacite-parc-v0.4`. Ce document trie ; les décisions d'intégration
appartiennent à Rémy et seront consignées dans le compte rendu final.

## Vérifications de l'orchestrateur

Comme en session 3 (défauts de code vérifiés avant correction), les recalculs
**structurants** allégués par le relecteur n°3 ont été refaits indépendamment
par l'orchestrateur depuis les mêmes frames que les stages
(`verify_se_partials.py`, scratchpad) — tous CONFIRMÉS :

| Allégation | Alléguée | Vérifiée |
|---|---|---|
| SE-1 : rho(chute R-11, niveau 2012), métropole | −0,52 | **−0,515** (n = 287) |
| SE-1 : rho partiel(chute, coût \| niveau 2012) | −0,07 | **−0,067** |
| SE-1 : chute relative médiane tendues/autres | −12,2 / −10,7 % | **−12,0 / −10,5 %** |
| SE-4 : rho partiel(chute RPLS, coût \| niveau 2019) | −0,50 | **−0,493** |
| SE-4 : chute relative médiane tendues/autres | −26,0 / −22,4 % | **−26,0 / −22,5 %** |
| SE-5 : rho(mobilité sociale × coût) 2013/2019/2025 | −0,70/−0,68/−0,80 | **−0,691/−0,684/−0,795** |
| SE-6 : rho partiel(mob. sociale, rotation \| coût) | +0,21 | **+0,218** |

(Écarts ≤ 0,02, imputables au filtre parc ≥ 500 non appliqué dans la
vérification — sans effet sur aucune conclusion.)

## Arbitrage du conflit apparent ST ↔ SE-1 (R-11 « chute concentrée »)

Le relecteur statistique établit que l'écart de médianes tendues/autres
(−1,54 vs −1,27) est **significatif** (Mann-Whitney p = 0,003, permutation
p = 0,003, métropole p = 0,0006) et conclut « survit ». Le relecteur
scénarios établit que ce même écart **disparaît à niveau initial contrôlé**
(partiel ≈ 0) et conclut « ne survit pas ». Les deux sont vrais et ne se
contredisent pas : ils ne testent pas la même chose.

- **Le FAIT survit** : les ZE tendues/chères perdent significativement plus
  de points de rotation (et un peu plus en proportion : −12,0 vs −10,5 %).
- **L'ATTRIBUTION ne survit pas** : ce contraste est intégralement porté par
  le niveau initial (les tendues partent de 12,56 %, les autres de 11,79) —
  il est indiscernable d'une chute quasi proportionnelle commune, et
  l'argument d'I-11 « le sens opposé niveau/chute écarte l'explication
  structurelle » est logiquement inversé (c'est la signature *attendue*
  d'une chute proportionnelle).

Disposition retenue pour le triage : le constat descriptif reste dans
R-11 (avec les tests de ST publiés), le mot « signature d'une mobilité
empêchée » et l'argument niveau/chute sortent d'I-11 ; les trois vues
(points, relatif, partiel) sont publiées pour R-11 ET R-12 (SE-4) et les
interprétations ne portent que sur ce qui est invariant aux trois.

## Verdict global

- **L'arithmétique est exacte partout.** ~60 chiffres recalculés depuis le
  brut par le relecteur n°4 (et par sondage par le n°2) : zéro divergence ;
  deux coquilles de transcription (ST-6 : Porto-Vecchio 13,0 → 13,1 ;
  ST-7 : énumérations sélectives d'O-33). Les recoupements externes sont
  tous verts (SDES 9,3→7,1 identique ; ANCOLS 8,1 % ≈ RPLS 8,0 ;
  frais 7-8 % confirmés ; IP2073 encadre le 9,87 %).
- **Les conventions nouvelles tiennent** : C-09 renforcée (zéro NaN sur les
  colonnes utilisées — le secret ne mord que sur les loyers ; insensible à
  la pondération et au seuil), C-10 très robuste en métropole (médiane
  ±1,6 % sous toutes les variantes de bornes).
- **Ce qui ne survit pas, c'est l'étage interprétatif** : la session 4 a
  produit quatre bonnes mesures et sur-interprété leur convergence. Les
  quatre phrases-titres (« gel concentré dans les marchés verrouillés »,
  « chute uniforme + corrélation la plus forte de la chaîne », « validation
  croisée entre sources indépendantes », « le péage se superpose au gel »)
  demandent chacune une reformulation.

## Grappe A — indépendance des preuves et axes partagés

| # | Objections (relecteurs) | Constat | Disposition proposée |
|---|---|---|---|
| A1 | **« Sources indépendantes » R-11×R-13** — HD-1 (majeure), SE-7 | S-27 et S-29 = même appareil (RP/EAR, 3 enquêtes communes sur 4) ; le +0,80 est une cohérence interne, pas une validation externe ; la vraie validation inter-appareils est MIGCOM×RPLS (8,34 ≈ 8,0-8,5) | Reformuler R-13/I-13/qmd/EVIDENCE ; promouvoir MIGCOM×RPLS au premier rôle ; « quatre mesures issues de trois appareils » |
| A2 | **Étalon commun T-05/T-08 lu quatre fois** — HD-2, SE-10 | Les quatre croisements convergent contre le même indice de coût et le même drapeau tendue (centraux H-08/H-12 seuls) ; SE-1/SE-6/SE-9 montrent chacun un croisement qui se vide une fois l'axe contrôlé ; `fillna(False)` classe Mayotte « autres » (contraire à « unknown keeps ») | Limite transverse L-xx « axes partagés » portée par R-11..R-14 ; contrastes tendues/autres publiés aux bornes H-08 ; tension NaN exclue des médianes |
| A3 | **Superlatif « la plus forte de la chaîne »** — ST-1 | R-14 +0,8122 vs R-12 −0,8026 au même périmètre, IC massivement chevauchants — récidive du motif C1 de la revue précédente | Superlatif abandonné : « parmi les plus fortes (indistinguable de R-13/R-14) » |
| A4 | **Croisement −0,20 construit** — SE-6 (vérifié : partiel +0,218) | Le signe négatif est fabriqué par les deux gradients de coût opposés ; aucune association négative résiduelle | Présenter le « masquage » comme corollaire des deux gradients ; publier le partiel ; retirer le −0,20 des chiffres mis en avant |

## Grappe B — cadrage des chutes (niveau initial, démographie, cycle)

| # | Objections | Constat | Disposition proposée |
|---|---|---|---|
| B1 | **R-11 « gel concentré » = artefact du niveau initial** — SE-1 (majeure, vérifiée) vs ST (fait significatif) | Arbitré ci-dessus : le fait survit, l'attribution non | Publier les trois vues (pts/relatif/partiel) dans R-11 ; I-11 reformulée sans « signature » ; tests MW/permutation de ST publiés |
| B2 | **R-12 « chute uniforme » inversée par le même contrôle** — SE-4 (vérifiée : partiel −0,49) | L'uniformité en points masque une chute excédentaire dans les marchés chers — PLUS favorable à H-04 que le texte actuel ; réserve : le contrôle du niveau initial est lui-même attaquable (régression vers la moyenne) | Publier les trois vues aussi pour R-12 ; I-12(2) reformulée ; cadrage commun R-11/R-12 |
| B3 | **Part démographique chiffrable** — SE-2 (~35-40 % borne basse, shift-share S-29), SA-1 (INSEE IP2073 : 14 % de la baisse de mobilité), SA-2 (ANCOLS : 9 % côté social) | Trois bornes convergentes : la démographie explique une minorité de la chute, l'accélération récente ne peut pas être démographique | Enregistrer IP2073 + ANCOLS en S-xx ; citer les bornes externes dans L-22/L-23/I-11/I-12 ; option : publier le shift-share comme variante (demande de figer une pyramide des âges) |
| B4 | **Choc de taux 2022-2025 absent de la chaîne** — SA-3, SE-3 (convergence indépendante de deux relecteurs) | Les fenêtres d'« accélération » (RP2023 ~2021-2023 ; RPLS 2022-2025) coïncident avec le choc du crédit (transactions 1,2 M → ~780 k) ; composante cyclique potentiellement réversible, jamais mentionnée | Ajouter le cycle à L-22/L-23 ; séparer tendance longue (pré-2019/2017) et fin de période dans I-11/I-12 ; figer une source de conjoncture ; inscrire dans NEXT-STEPS l'observation qui tranche (RPLS 2026/2027) |
| B5 | **Le rho −0,80 est un gradient ancien** — SE-5 (vérifié : −0,69 dès 2013) | Le « miroir du marché » préexiste à la période — trait structurel du système HLM, pas un fait nouveau du gel ; le nouveau = creusement −0,68 → −0,80 | Publier les rho aux trois millésimes dans R-12 ; I-12(1) reformulée (« depuis au moins 2013 ») ; vieillissement des locataires HLM ajouté à L-23 |

## Grappe C — R-13 (migrations)

| # | Objections | Constat | Disposition proposée |
|---|---|---|---|
| C1 | **Soldes des cœurs chers sous-déterminés** — SE-8 | Déficit parisien ancien (−0,7 %/an dès 2012) ; profil des destinations = littoraux d'aménité ; solde×coût métropole compatible zéro ; « contre la géographie de l'emploi » sans croisement emploi (T-14 n'en a pas) | Retirer « contre la géographie de l'emploi » ; « partir n'est pas toujours choisi » en question ouverte ; option : décomposition AGEREVQ des soldes (calculable immédiatement depuis S-29) |
| C2 | **Datation du 9,87 %** — SA-7 | La série publiée la plus récente (2023) est 8,8 % — le niveau MIGCOM est une moyenne de fenêtres 2020-2024 sur une série descendante | Dater le niveau dans R-13/L-24 ; ajouter les recoupements IP2073 au qmd |
| C3 | **Rho faibles sans réserve de multiplicité** — ST-3 | 32 rho publiés ; solde×coût FR (−0,15) et delta×delta (+0,19) ne tiennent pas Bonferroni à 16 tests ; les conclusions principales (p ≪ 1e-6) survivent à toute correction | Marquer les rho faibles ; I-13 : hiérarchie de preuve (faits de flux d'abord, rho en appui) |
| C4 | **Labels et périmètres** — HD-10, HD-11, ST-7 | STOCD 21 = « non HLM » (pas exactement « privé ») ; « statut le moins mobile » = glissement contre L-24(1) ; énumérations sélectives d'O-33 | Reformulations ponctuelles ; « le statut dans lequel on entre le moins » ; listes complètes ou marquées « exemples » |

## Grappe D — R-14 (transaction) et H-13

| # | Objections | Constat | Disposition proposée |
|---|---|---|---|
| D1 | **Sensibilité H-13 annoncée, non publiée ; scénario « haut » = doublon du central** — HD-3 ; converge avec HD-5/HD-12 (le 5,81 manquant est AUSSI le scénario primo-accédant et le taux de droit commun) | T-15 promet trois scénarios, l'artefact n'en publie qu'un ; le vrai scénario informatif (5,81) n'existe pas | Publier %/mois aux scénarios {5,09 ; 5,81 ; 6,32}, nommer 5,81 « droit commun / primo-accédant » ; corriger le texte de H-13 (HD-12) ; reformuler « chaque achat paie 6,32 % » (HD-5) |
| D2 | **Territorialisation possible depuis S-31** — HD-4 ; SE-9c et SE-12 la demandent aussi (discontinuités) | Jointure département déterministe ; biais actuel dans le sens de la thèse (Nice/Menton à 4,50 % surestimées de ~6,5 % de péage) | Territorialiser les droits (option recommandée par le relecteur), ou publier l'écart borné par ZE concernée |
| D3 | **Le rho +0,81 est quasi mécanique ; annualisation absente** — SE-9 (rho(mois, prix) = 0,98 ; 2,6 %/an amorti sur 20 ans) ; ST note d'un autre côté qu'il n'y a PAS d'artefact de diviseur commun (+0,87 brut-à-brut) | L'apport propre de R-14 = niveau absolu en mois + part fiscale 83 % ; la « superposition » est la corrélation loyers-prix connue | Noter le caractère quasi mécanique dans R-14/L-25 ; publier l'annualisation paramétrée par une durée de détention (H-xx à plage) ; I-14 requalifiée |
| D4 | **Assiette C-10 : données écartées invisibles ; petites ZE DOM ; pas de seuil de classement** — HD-6 (33 % des logements vendus hors assiette), HD-7 (ZE 0101 : médiane ×12,7 par les bornes), ST-8 (332 ventes sans ZE) | Concept juste, publication incomplète ; incohérence de robustesse avec le seuil R-12 | Publier les comptages d'exclusion + bloc couverture + sensibilité des bornes ; seuil de ventes pour les classements ; caveat Guadeloupe |
| D5 | **Millésimes et fraîcheur** — ST-2 (prix 2025 / revenus 2021 — même motif que C2 de la revue précédente), SA-4 (table DMTO 06/2026 : Eure passée à 5,00, Hautes-Pyrénées redescendues, Mayotte 4,50 ; ventes début 2025 réellement à 5,81) | Niveaux de mois surestimés en énoncé « 2025 » ; liste de départements datée | L-25(6) sur le modèle L-09/L-11 ; dater la table et la lecture temporelle du péage ; figer dmto_2026-06.pdf ; verser au dossier `logement freshness` |
| D6 | **CSI exclue à tort du plancher** — SA-5 (0,10 % du prix, déterministe) | Artefact du choix de source, pas une frontière de données | Intégrer la CSI (une ligne dans T-15) ou la citer chiffrée dans L-25 |

## Grappe E — registre, code, qmd (mineures)

- **HD-8** : deltas C-09 = variation de taux + recomposition du parc
  (Issoire −13,18 → −11,84 à panel constant ; médianes insensibles −2,41) —
  caveat L-23, option variante panel équilibré.
- **HD-9 / ST-5** : le secret RPLS ne touche pas les colonnes utilisées
  (favorable — à écrire dans O-28/L-23) ; contrôle C-09 contre référence
  arrondie (dérive réelle +0,0102) ; commentaire « ≤ 0.011 » périmé.
- **HD-13** : O-26 embarque une lecture cohorte non établie (mécanique des
  classes quand le flux d'entrées chute) — redescendre en constat brut.
- **HD-14** : D-18 « cinq enquêtes 2020-2024 » — l'EAR 2021 a été annulée
  (à re-sourcer avant correction ; renforce A1).
- **ST-4** : IC de Fisher anti-conservateur pour Spearman aux \|rho\| élevés
  (Bonett-Wright : ±0,01 aux bornes) — adopter le facteur ou documenter.
- **ST-6** : O-35 « Porto-Vecchio 13,0 » → 13,1 (coquille).
- **ST-9** : fragilité latente `_weighted_rate` (aucun effet sur les données
  figées, vérifié) — garde min_count + test de propriété.
- **SE-11** : phrase de garde qmd (pas de causalité vacance→rotation ni
  péage→gel ; l'articulation avec la conclusion v0.3 n'est pas modifiée) ;
  intégrer I-11..I-14 au §8 après la passe.
- **SA-6** : licence S-28 CONFIRMÉE Licence Ouverte (mentions légales SDES)
  — lever le « à confirmer » de NEXT-STEPS.
- **SA-8/SA-9** : littérature OCDE/CAE favorable à I-14 (à enregistrer,
  utile pour P-xx) ; frontières Fidéli/EnL/notaires/DV3F à consigner.

## Objections écartées par le triage, avec raison

- **SE-9 « péage trop petit annualisé pour geler »** (comme réfutation) : le
  relecteur lui-même la neutralise — une taxe sur la transaction pénalise
  précisément le comportement rare dont H-04 s'inquiète, et la littérature
  (OCDE/CAE, SA-8) documente l'effet DMTO→mobilité. Retenu seulement comme
  demande de publication de l'annualisation (D3).
- **HD-4 « le central devrait être sous 6,32 »** (recalibrage du central) :
  le central 6,32 décrit le droit voté majoritaire au moment du figement ;
  la territorialisation (D2) répond mieux que déplacer le central — pas de
  recalibrage silencieux d'une hypothèse (INTRO §21).
- **ST « chute concentrée survit »** comme clôture de SE-1 : arbitré
  ci-dessus — les deux verdicts portent sur des énoncés différents (fait vs
  attribution) ; aucun des deux n'est écarté, ils sont réconciliés.

## Chiffres-titres : avant/après proposé (si l'intégration est complète)

| Grandeur | Avant (v0.4) | Après proposé |
|---|---|---|
| R-11 titre | « le gel se concentre dans les marchés verrouillés — signature d'une mobilité empêchée » | « la rotation baisse partout (−11 % relatif), un peu plus là où elle était haute ; le contraste tendues/autres (−1,54/−1,27, MW p = 0,003) est porté par le niveau initial (partiel ≈ 0) — compatible avec H-04, non discriminant » |
| R-11 « −1,17 pt / ~364 000 manquants » | publiés entiers | publiés avec la décote démographique externe (INSEE : 14 % de la baisse de mobilité ; shift-share interne ~35-40 % de la chute de rotation en borne basse) et le caveat cycle 2022-2025 |
| R-12 « chute UNIFORME » + « corrélation la plus forte de la chaîne » | tels quels | « chute générale ; à niveau 2019 contrôlé, excédentaire dans les marchés chers (partiel −0,49) » ; « parmi les plus fortes (≈ R-13/R-14) » ; rho par millésime publiés (−0,69 dès 2013) |
| R-13 « validation croisée entre sources indépendantes » | telle quelle | « cohérence interne du recensement (logements × personnes) ; validation inter-appareils : MIGCOM 8,34 % ≈ RPLS 8,0-8,5 % » |
| R-13 « les flux vident les cœurs chers … contre la géographie de l'emploi » | tel quel | soldes publiés comme faits, sous-détermination choisi/empêché en limite ; « contre l'emploi » retiré (pas de croisement emploi) |
| R-14 « le péage le plus lourd exactement là où le gel » (rho +0,81) | tel quel | « géographie du péage = géographie du prix (quasi mécanique) ; l'apport de R-14 : 6,1 mois (en niveau de vie 2021) et ~83 % fiscal » + scénarios H-13 {5,09 ; 5,81 ; 6,32} publiés |
| Bilan H-04 | « quatre mesures indépendantes qui se recoupent » | « quatre mesures issues de trois appareils, croisées contre un étalon partagé (T-05/T-08) ; recoupements réellement externes : MIGCOM×RPLS, et les bornes démographiques publiées (INSEE 14 %, ANCOLS 9 %) » |

## Ce que la revue laisse ouvert (candidats NEXT-STEPS)

1. **Décomposition AGEREVQ des soldes parisiens** (SE-8) — la seule
   observation qui tranche « choisi vs empêché » calculable immédiatement
   depuis S-29.
2. **Rotation par âge × ZE** (SE-1c) — fichier détail Logement du RP
   (ANEM × AGEMEN8) : ferait renaître ou réfuterait proprement I-11.
3. **Millésimes post-normalisation des taux** (SE-3) — RPLS 2026/2027 et
   prochain L_STAY : rebond → cyclique ; persistance → structurel.
4. **Territorialisation DMTO × discontinuités** (SE-12, D2) — vers un test
   de causalité du péage.
5. **Sources candidates** (SA) : IP2073, ANCOLS 02/2026, dmto_2026-06,
   conjoncture notaires/Banque de France, OCDE/CAE, page CSI, mentions
   légales SDES.
