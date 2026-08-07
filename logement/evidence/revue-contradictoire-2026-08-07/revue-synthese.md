# Revue contradictoire R-01..R-10 — synthèse de triage (2026-08-07)

4 relecteurs indépendants (sources alternatives · hypothèses/définitions ·
scénarios d'échec · statistique). Vérifications faites par l'orchestrateur :
remob.py:89 (pas de min(besoin, gisement)) et tension.py:106-109 (pas
d'écrêtage à 0) CONFIRMÉS dans le code.

## Verdict global
- L'arithmétique est EXACTE partout (recalculs indépendants : 1,65 / 48,3 /
  3,9 / 11,5 ; garde H-11 effective). Toutes les corrélations sont
  significatives (MW z 6,4-7,4 ; IC Fisher excluant 0).
- R-01..R-06 et R-08 (corrélations) survivent ; le Datalab SDES déc. 2023
  CONFIRME I-08 ; « le foncier n'est pas la contrainte » (I-10) survit à
  toutes les corrections (même à densité constatée 40-55 log/ha : ratio ~3-4).
- NE SURVIVENT PAS tels quels : « le gisement suffit (couverture 1,65) » et
  « ~4× moins cher (12,5 Md€) ». La revue ne « tient » donc pas sans
  intégration : corrections de document + sensibilités à calculer AVANT
  publication.
- Reformulation probable de la conclusion : la contrainte institutionnelle
  devient la CONDITION de la suffisance (échelle, mobilisabilité), pas sa
  conséquence — et la suffisance physique n'est démontrée qu'à l'échelle ZE,
  avant correction des faux vacants.

## Grappe A — suffisance du gisement (R-07/I-07) — 4 objections sérieuses convergentes
A1. Échelle infra-ZE [3 relecteurs] : 37,4 % du gisement des ZE tendues en
    communes non tendues ; couverture 1,03 au proxy TLV (même construction) ;
    ~0,41 au périmètre communal légal (Cour : 118 330 vacants > 2 ans en TLV,
    2022 ; DHUP : 74 % du durable en marchés détendus ; Apur Paris : 18 600).
A2. Faux vacants LOVAC [3] : ~25 % (Cour p. 21, Saint-Brieuc 74/270 ; Cerema
    +10-20 % vs INSEE ; biais déclaratif fiscal SPÉCIFIQUE zones tendues).
    ×0,75 → couverture 1,24 ; 0,86 (< 1) au seuil 7 %. Aucune L-xx ne couvre
    la surestimation. Effet net à CALCULER (structurelle surestimée ⇒ besoin
    majoré aussi).
A3. Mobilisabilité non paramétrée [2] : détente exige 60,5 % du gisement
    (central), 87,1 % (seuil 7 %) ; ZLV constaté : 3 % de sorties en zone
    tendue en 4 ans. → H-12 à créer.
A4. Circularité d'assiette C-06 [1, neuve] : seuil S-14/S-15 défini sur vacance
    TOTALE (le registre le dit : definitions.yaml:283-285), appliqué à la
    DISPONIBLE ; ZE DOM tendues-par-structurelle-record (couvertures 9,6-12,5),
    28/142 ZE apportent 16 % du gisement ainsi. Contredit I-02.
A5. Secrétisation : sens de L-12 FAUX au national (couverture DÉCROISSANTE en
    S : borne 1,65 → 1,50 ; jusqu'à 85 ZE basculables) [1].
A6. 55 % du besoin dans les 41 ZE non couvertes ; déficit incompressible
    58 357 même à 100 % de remobilisation [1].
A7. Stock vs flux : excédent 186 k < 1 an de formation de ménages des ZE
    tendues (~219 k/an) ; jamais énoncé [2].
A8. Portée du mot « besoin » : 285 665 = besoin de FLUIDITÉ (H-08), à mettre
    en regard de 2,7 M demandes HLM / flux 210-518 k/an [1].
Mineures : écrêtage corse (5 ZE, +15 906 de besoin, L-12 ne cite qu'Ajaccio) ;
divergence étude/zonage publiée dans un seul sens (67/142 non-TLV) ; bande
grise du seuil.

## Grappe B — coût (R-09/I-09) — sérieuses
B1. INCOHÉRENCE INTERNE (confirmée code) : 58 357 logements facturés en
    rénovation là où R-07 établit zéro gisement local. Coût mixte cohérent
    = 19,8 Md€, ratio 3,9 → 2,4. Seule vraie CORRECTION de document requise.
B2. Asymétrie du comparateur [2] : 169 200 € inclut la charge foncière
    (14-24 %) ; la remobilisation exclut l'acquisition. Ratio ~4 (incitatif
    pur) à ~1 (acquisition-amélioration, BdT 2 550 €/m²). Publier les deux.
B3. Rénovation énergétique ≠ remise en usage [3] : R-08 DÉTERMINE le sens du
    biais que L-14 dit « indéterminé » ; réhabilitation lourde marché
    1 000-2 000 €/m² ; TVA mixte. Variante ×2 : ~25 Md€, ratio ~2 (> 1 :
    la direction survit).
B4. Non-propagation de H-08 [2] : détente 5,4-24,7 Md€ sur la plage 5-7 % ;
    plages publiées conditionnelles au central. Idem R-10 (11,5 → 5,8 ×).

## Grappe C — mise en récit — sérieuses ciblées
C1. R-08 : superlatif à périmètres mélangés (métropole : âge +0,56, coût
    −0,53, emploi −0,47 — IC chevauchants) + état mesuré sur le parc
    OCCUPÉ/en transaction, jamais sur le vacant (saut non déclaré dans L-13).
C2. R-06 : centre H-07 = parc en place (emménagés récents ~35-40 m²/p →
    médiane ~31 %, Paris ~73-85 %) ; loyers 2025 ÷ revenus 2021 (direction
    tue) ; charges comprises. Classements invariants.
C3. R-02 : volume-titre (mill. 26) sur source dégradée post-GMBI (Cour :
    82 % déclarants, +6 % artefactuel) — basculer le titre en pré-rupture,
    aligner sur C-03 ; vérifier Paris 32 091 vs Apur 18 600.
C4. R-03 : L-07 PÉRIMÉE (emploi localisé ZE jusqu'en 2023 définitif/2024
    provisoire existe) ; « ~85 % » calculé sur 74 % de la masse → encadrer
    [62,5 ; 84,9] ; ANOMALIE masqués 11,2/commune > plafond 10 à instruire.
C5. R-05 : « sans lien » faux (+0,17, IC [0,06;0,28]) + non-monotonie non
    discutée. R-10 : borne « densité d'opération constatée » (fonds friches
    40-55 log/ha) à côté de H-11.
Mineures code : min_count incohérent (ze.py/cout.py sommes nues — aucun effet
aujourd'hui, 0/305 ZE tout-secret) + test de propriété à ajouter ; IC Fisher à
publier partout ; contrastes de médianes = même signal, pas corroboration.

## Sources à enregistrer (S-22+)
Cour des comptes mai 2025 (pivot — couvre A1/A2/B2/C3) ; SDES Datalab
déc. 2023 déterminants de la vacance ; Apur déc. 2023 ; INSEE emploi localisé
ZE 2022/2023 ; Cerema bilan fonds friches ; IGF-CGEDD 2016 ; FAP 2025 ;
(contexte : IP n°1979 ; étude charge foncière). Confirmés sans mieux :
Filosofi 2021 (2022 ANNULÉ), LOVAC 2026, carte loyers ANIL, frontière
successions.

## Plan d'intégration proposé (ordre)
1. Corrections de code/artefacts : écrêtage disponible négatif (ou marquage),
   coût mixte R-09 (min(besoin, gisement) + déficit × neuf), champs
   besoin_couvert/non_couvert, n_tendues_non_majoritaires_tlv, IC Fisher,
   min_count unifié + tests.
2. Nouvelles sensibilités : variante TLV infra-ZE (données figées), H-12
   mobilisabilité (0,75 ; 0,6-0,9) propagée R-07/R-09, propagation H-08 dans
   R-09/R-10, borne secrétisation, densité constatée dans R-10, pire cas joint.
3. Registres : S-22+ ; H-12 ; corrections L-04/L-07/L-09/L-11/L-12/L-13/L-14 +
   nouvelles L-xx (échelle, faux vacants, équivalence-unité, stock/flux,
   effets de bord) ; D-xx « besoin en flux ».
4. Reformulations : I-07, I-08 (conditionnel), I-09, I-10, R-02 titre,
   « sans lien » R-05 ; section revue contradictoire dans le qmd ; re-rendu.
Décisions de RECHERCHE à trancher par Rémy : centre H-07 (recentrer ou
intervalle d'abord) ; assiette C-06 (variante recalibrée) ; valeurs H-12.
