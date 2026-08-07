# Revue contradictoire — R-01..R-10 (2026-08-07)

Compte rendu de la revue contradictoire exigée par la méthode (INTRO
étape 12 : chercher activement les objections avant publication), menée le
2026-08-07 sur l'état tagué en fin de session 2 (arc R-01..R-10, commit
`926a854`). Les corrections quantitatives sont commitées (code + artefacts
+ registres) ; ce document consigne la méthode, les objections et leur
disposition, et le tableau avant/après des chiffres-titres.

## Méthode

Quatre relecteurs indépendants (agents distincts, sans accès aux
conclusions des autres), chacun sur un angle imposé, plus une synthèse de
triage par l'orchestrateur :

1. **Sources alternatives** — existe-t-il des sources meilleures ou
   contradictoires que celles du registre ? (10 objections)
2. **Hypothèses et définitions** — chaque H-xx/D-xx/C-xx tient-il ?
   assiettes, centres, plages, circularités. (12 objections)
3. **Scénarios d'échec** — sous quelles conditions les conclusions
   s'inversent-elles ? cohérence inter-résultats. (10 objections)
4. **Statistique** — recalculs indépendants, significativité, biais de
   construit, mise en récit. (13 objections)

Matériau interne (non enregistré en S-xx — ce sont des productions de la
revue, pas des sources) : les cinq rapports bruts sont commités en annexe
dans `evidence/revue-contradictoire-2026-08-07/`
(`revue-sources-alternatives.md`, `revue-hypotheses-definitions.md`,
`revue-scenarios-echec.md`, `revue-statistique.md`, `revue-synthese.md`).
Les deux défauts de code allégués ont été vérifiés sur le code AVANT
correction et confirmés (`remob.py` : pas de `min(besoin, gisement)` ;
`tension.py` : pas d'écrêtage à zéro de la vacance disponible négative).
L'arithmétique publiée a été recalculée indépendamment : exacte partout
(1,65 · 48,3 · 3,9 · 11,5) — les objections portaient sur les modèles et
la mise en récit, pas sur les calculs.

Les sources produites par la revue sont enregistrées et figées :
**S-22** (Cour des comptes, mai 2025 — pivot), **S-23** (SDES Datalab,
déterminants de la vacance longue durée), **S-24** (Apur, logements
inoccupés à Paris), **S-25/S-26** (Cerema, bilan du fonds friches).

## Verdict global

- **Survivent tels quels** : R-01, R-04, R-06 (classements), la géographie
  de R-02/R-03, le contraste DOM de R-08, la direction de R-09
  (remobiliser < construire), la conclusion foncière de R-10.
- **Ne survivaient pas tels quels** : « le gisement suffit (couverture
  1,65, robuste) » (I-07) et « ~4 × moins cher (12,5 Md€) » (I-09).
- **Reformulation de la conclusion de l'arc (I-10)** : la contrainte
  institutionnelle n'est plus la *conséquence* de la suffisance — elle en
  est la **condition**. La suffisance en volume est marginale (couverture
  ~1 au central), conditionnelle au taux d'existence du gisement, et
  fausse au périmètre légal de la tension (0,69).

## Décisions actées par Rémy (avant intégration)

1. Intégration complète ; l'instruction de H-04 reste reportée.
2. Création de **H-12** `lovac_structural_existence_rate` (0,75 ;
   plage 0,6-0,9 ; S-22), propagée des **deux côtés** de C-06 (gisement
   effectif ET soustraction qui définit la vacance disponible). La
   mobilisabilité comportementale reste une limite qualitative (L-17),
   non paramétrée faute de source donnant une fraction.
3. Recentrage de **H-07** sur les emménagés récents : centre 35
   m²/personne (S-12, tranche 30-39 ans), plage [35 ; 51,2] — 51,2
   (l'ancien centre, parc en place) devient la borne haute « relocation
   au standard du parc ». Changement tracé (registre, L-11, R-06).
4. **C-06 conservé** sans recalibrage du test central ; la sensibilité
   d'assiette est publiée (seuil recalibré 4,31 % sur la disponible) et
   les ZE « tendues par structurelle record » sont marquées.

## Objections sérieuses et leur disposition

### Grappe A — suffisance du gisement (R-07/I-07)

| # | Objection (relecteurs) | Disposition |
|---|---|---|
| A1 | **Échelle infra-ZE** [3 relecteurs] : la couverture ZE suppose la mobilité du gisement dans la ZE ; Cour p. 16 : 118 330 vacants > 2 ans en communes TLV ; DHUP : 74 % du durable en marchés détendus ; Apur Paris | **Corrigée en code** : variante « communes TLV » publiée dans R-07 (couverture 0,69) + **L-16** créée |
| A2 | **Faux vacants LOVAC** [3] : ~25 % (Cour p. 21, Saint-Brieuc 74/270 ; Cerema +10-20 %) ; aucune L-xx ne couvrait la surestimation ; effet net à calculer (le besoin bouge aussi) | **Corrigée en code** : H-12 créée et propagée des deux côtés de C-06 ; grille H-08 × H-12 publiée (traverse 1) ; L-12 réécrite |
| A3 | **Mobilisabilité non paramétrée** [2] : la détente exige de remobiliser 94 % du gisement effectif ; constat ZLV ~3 % de sorties en 4 ans | **Intégrée en limite** (L-17) — décision : pas de paramètre, aucune source ne donne une fraction |
| A4 | **Circularité d'assiette C-06** [1, neuve] : seuil énoncé sur la vacance totale, appliqué à la disponible ; ZE DOM « tendues » par leur propre structurelle record | **Intégrée en sensibilité** : variante au seuil recalibré (28 ZE, couverture 1,19) + marquage des 31 ZE (37 % du gisement) ; test central conservé (décision), C-06/L-12 documentés |
| A5 | **Sens du biais de secrétisation faux** dans L-12 [1] : au national, réintégrer le masqué fait BAISSER la couverture | **Corrigée** : L-12 réécrite (correction majeure), borne publiée (1,06 → 1,05) |
| A6 | **Concentration du besoin** [1] : la majorité du besoin est dans les ZE non couvertes ; déficit incompressible même à 100 % | **Corrigée en code** : `besoin_couvert`/`besoin_non_couvert` publiés (68 % non couvert ; déficit 57 945) |
| A7 | **Stock vs flux** [2] : l'excédent du gisement < 1 an de formation de ménages des ZE tendues | **Intégrée en limite** (L-19) + reformulation I-10 |
| A8 | **Portée du mot « besoin »** [1] : besoin de fluidité ≠ flux du débat public ≠ file HLM | **Intégrée en limite** (L-21) — ordres de grandeur cités SANS entrer dans un calcul |
| A9 | Mineures : disponibles négatives non écrêtées (ZE corses) ; divergence étude/zonage publiée dans un seul sens ; bande grise du seuil | **Corrigées en code** : écrêtage publié (3 ZE, 412 logements) ; `n_tendues_non_majoritaires_tlv` (34, dont 14 < 1 % TLV) ; bande grise ± 1 pt (116 ZE dont 43 tendues) |

### Grappe B — coût (R-09/I-09)

| # | Objection | Disposition |
|---|---|---|
| B1 | **Incohérence interne R-07/R-09** (confirmée code) : ~58 000 logements facturés en rénovation là où R-07 établit zéro gisement local | **Corrigée en code** : règle MIXTE (C-07 corrigé) — rénovation = min(besoin, gisement effectif local), déficit au prix du neuf ; 15,8 Md€, ratio 2,1 ; rénovation seule gardée en trace |
| B2 | **Asymétrie du comparateur** [2] : S-18 inclut la charge foncière, la remobilisation exclut l'acquisition ; ratio ~4 (incitatif pur) à ~1 (acquisition-amélioration) | **Intégrée en limite** (L-14, C-07 notes) — variante chiffrée non calculée : pas de source figée du coût d'acquisition par ZE |
| B3 | **Rénovation énergétique ≠ remise en usage** [3] : R-08 détermine le sens du biais que L-14 disait « indéterminé » ; TVA mixte | **Corrigée** : L-14 requalifiée (biais vers le HAUT) + stress « réhabilitation lourde » ×2 publié (21,8 Md€, ratio 1,5 — la direction survit) |
| B4 | **Non-propagation de H-08** [2 + statistique] : plages publiées conditionnelles au besoin central | **Corrigée en code** : propagation publiée dans R-09 (5,5-37,5 Md€, ratios 2,3-1,9) et R-10 (ratios 28,6-5,1) |

### Grappe C — mise en récit et corrélations

| # | Objection | Disposition |
|---|---|---|
| C1 | **R-08 superlatif à périmètres mélangés** : à périmètre métropole, âge +0,56 ≈ coût −0,54 ≈ effort −0,51 ≈ emploi −0,47 (IC chevauchants) ; état mesuré sur le parc occupé/en transaction, jamais sur les vacants | **Corrigée** : superlatif ABANDONNÉ (R-08 amendé), Spearman par périmètre + IC de Fisher publiés partout ; L-13 complétée (direction DPE : couverture × vacance −0,14 → 0,40 = borne basse) ; I-08 au conditionnel ; S-23 conforte la piste |
| C2 | **R-06 centre H-07 mal choisi** : 51,2 = parc en place ; loyers 2025 ÷ revenus 2021 (direction tue) ; charges comprises | **Corrigée** : H-07 recentrée (décision) — médiane 27,4 % (27,4-40,1) ; directions des biais écrites dans L-09/L-11 (niveaux surestimés, classements insensibles) |
| C3 | **R-02 volume-titre sur source dégradée** (mill. 26 post-GMBI, 82 % de déclarants) ; Paris 32 091 vs Apur ~18 600 | **Corrigée en document** : volume-titre basculé sur le millésime pré-rupture (~1,15 M, aligné C-03) ; L-04 complétée ; contrôle Apur enregistré (S-24), écart à instruire |
| C4 | **L-07 périmée** (l'emploi localisé ZE existe jusqu'en 2023/2024) ; « ~85 % » calculé sur la seule masse visible | **Corrigée** : L-07 réécrite (re-exécution planifiée, NEXT-STEPS) ; borne de secrétisation publiée — part en ZE croissantes : 78-88 % (la lecture I-03 survit sur toute la borne) |
| C5 | **R-05 « sans lien » faux** (+0,15, IC excluant 0) + non-monotonie non discutée ; R-10 sans borne de densité constatée | **Corrigée** : R-05/I-05 reformulés (faible mais significative, signe opposé au contraste touristique ; RS × coût compatible avec zéro) ; densité constatée du fonds friches publiée dans R-10 (30,3 log/ha → ratio 2,2, S-25/S-26) |
| C6 | Mineures code : `min_count` incohérent entre modules (aucun effet constaté), IC jamais publiés | **Corrigées en code** : agrégation unifiée + IC de Fisher dans tous les artefacts (rho retouchés à la marge : R-04 −0,42 → −0,43, R-05 +0,17 → +0,15, corses de R-05 recalculés) |

### Objections écartées, avec raison

- **H-08 sans meilleure source** (sources-alt #10) : rien de contradictoire
  ni de validant publié — écartée ; la sensibilité, déjà publiée, est
  désormais propagée dans R-09/R-10 et croisée avec H-12.
- **Saint-Brieuc comme centre de H-12** : 74/270 (0,27) traité comme
  aberrant (campagne unique, biais de ciblage) — la plage H-12 s'arrête à
  0,6 ; documenté dans le registre.
- **Tri optimiste des logements dans R-09** (scénarios #8, partie
  sélection) : vérifiée sans objet — le coût est uniforme par ZE, aucun
  tri n'est fait.
- **Contrastes de médianes comme corroboration** (statistique #8) : c'est
  une re-description du même signal, pas une preuve indépendante — noté,
  aucun usage corroboratif dans les textes.

## Tableau avant/après des chiffres-titres

| Grandeur | Avant (2026-08-05) | Après (2026-08-07) |
|---|---|---|
| ZE tendues (C-06, H-08 = 6 %) | 142 | **97** (H-12 des deux côtés ; bande grise ± 1 pt : 116 ZE) |
| Besoin national de détente | 285 665 | **194 488** (écrêté ; 194 901 sans écrêtage) |
| Gisement des ZE tendues | 472 022 (brut) | **206 664** (effectif = brut × 0,75) |
| Couverture nationale | 1,65 « robuste sur H-08 » | **1,06** ; grille H-08 × H-12 : **0,82-1,85** (traverse 1) ; communes TLV : **0,69** ; borne secrétisation 1,05 |
| Couverture locale | 101/142 ZE | **56/97** ; 68 % du besoin en ZE non couvertes ; déficit incompressible 57 945 |
| Coût de la détente | 12,5 Md€ (10,6-15,3), rénovation partout | **15,8 Md€ MIXTE** (14,9-17,1), dont 9,8 de neuf ; rénovation seule 8,6 (trace) ; H-08 : 5,5-37,5 |
| Ratio neuf/détente | 3,9 (3,2-4,6) | **2,1** (1,9-2,2) ; stress réhabilitation ×2 : **1,5** ; rénovation seule : 3,8 (3,2-4,5) |
| Taux d'effort médian (R-06) | 40,1 % (27,4-55,6) | **27,4 %** (27,4-40,1) — H-07 recentrée, sensibilité orientée à la hausse |
| Paris (R-06) | 93,5 % | **63,9 %** (63,9-93,5) — classement invariant |
| Foncier en friche (R-10) | 22 328 ha, 3,29 M, 11,5 × | **14 383 ha, 2,12 M, 10,9 ×** (5,2-16,7 sur H-11 ; 5,1-28,6 sur H-08) ; plancher constaté 30,3 log/ha → **2,2 ×** |
| Vacance en ZE croissantes (R-03) | « ~85 % » | **78-88 %** (borne de secrétisation ; 84,9 % au visible) |
| RS × vacance (R-05) | « sans lien » (+0,17) | **+0,15 [0,04 ; 0,26]** — faible, significative, signe opposé au contraste touristique |
| Ancienneté × vacance (R-08) | « corrélat le plus fort de la chaîne » | **+0,56 [0,47 ; 0,63]**, du même ordre que coût (−0,54) et effort (−0,51) à périmètre égal ; > F+G seulement |
| Volume-titre R-02 | 1,18 M (mill. 26) | **~1,15 M (mill. 24, pré-rupture)** ; mill. 26 = source dégradée (L-04) |

## Ce qui reste ouvert

1. **H-04 (mobilités empêchées)** — reporté à la session suivante
   (décision), inchangé dans NEXT-STEPS.
2. **Emploi récent** — L-07 corrigée mais R-03 reste sur 1998-2018 : figer
   la source « estimations annuelles d'emploi localisées ZE 2023/2024 »
   (S-xx) et re-exécuter en variante à la prochaine session.
3. **Réconciliation communal/départemental LOVAC** — l'anomalie relevée
   par l'angle statistique (manquants ÷ communes masquées ≈ 11,2 > le
   plafond de 10 du masquage « < 11 ») n'est pas entièrement expliquée
   par la secrétisation : à instruire (test de réconciliation à écrire).
4. **Écart Paris LOVAC 26 (32 091) vs Apur 2022 (~18 600)** — enregistré
   (S-24, L-04), non expliqué : millésimes, périmètres et rupture GMBI à
   démêler.
5. **Fichiers LOVAC détaillés** (accès restreint) — condition de la
   sensibilité H-06 ET de la levée de L-18 (taille × époque des vacants).
6. **Mobilisabilité comportementale** — L-17 reste qualitative tant
   qu'aucune source ne donne une fraction mobilisable.
7. **Variante acquisition-amélioration** de R-09 — documentée en L-14,
   non chiffrée faute de source figée du coût d'acquisition par ZE.
