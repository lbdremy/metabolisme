# Revue contradictoire — angle scénarios d'échec (10 objections)

## SÉRIEUSES
1. **R-07 échelle infra-ZE** : 37,4 % du gisement des 142 ZE tendues (176 561) est
   dans des communes NON tendues de ces ZE. Restreint aux communes TLV : couverture
   1,65 → 1,03 ; ZE couvertes 101 → 35. Preuve : tension.py:93-100 ; croisement
   LOVAC communal × zonage TLV × appartenance. L-12 ne couvre pas ce point.
   → sensibilité « gisement restreint TLV » + nouvelle L-xx.
2. **R-07 concentration du besoin** : les 41 ZE non couvertes portent 156 951 des
   285 665 (54,9 %) du besoin ; déficit incompressible 58 357 même à 100 % de
   remobilisation. Payload n'a pas besoin_couvert/besoin_non_couvert.
   → ajouter champs à tension.build_summary + corriger I-07/EVIDENCE.md.
3. **R-09 incohérent avec R-07** : remob.py:89 facture le besoin ENTIER en rénovation
   sans min(besoin, gisement local) — 58 357 logements facturés en rénovation là où
   R-07 dit qu'il n'y a pas de gisement. Coût mixte cohérent
   min(besoin,gisement)×réno + déficit×neuf = 19,8 Md€, ratio 3,9 → 2,4.
   → CORRECTION de document (pas seulement limite) : publier le scénario mixte ou
   restreindre 12,5 Md€ aux 101 ZE couvertes.
4. **Mobilisabilité absente** : la détente exige de remobiliser 60,5 % du gisement
   (central), 87,1 % au seuil 7 %. Aucune hypothèse de fraction mobilisable ; L-12
   l'admet en une phrase sans calcul. Bascule non écrite.
   → créer H-12 « fraction mobilisable » + table couverture H-08 × H-12 ; seuil de
   bascule 60,5 % dans R-07.
5. **Stock vs flux** (sérieuse comme lacune de cadrage) : besoin 285 665 = stock à
   date ; formation de ménages ~219 k/an sur le parc des ZE tendues (0,92 %/an,
   R-01) ; l'excédent 186 k < 1 an de flux. Jamais énoncé dans R-07..R-10.
   → nouvelle L-xx « gain unique, ne dispense pas du flux de construction » +
   reformuler I-10.

## MINEURES
6. **I-10 sur-agrège** : « volume + foncier + coût favorables » jamais vrais au même
   endroit (les 41 ZE sans gisement ont les friches mais au coût du neuf ≥ 9,9 Md€ ;
   31/41 couvertes par friches à densité centrale). → reformuler I-10.
7. **Artefacts corses** : 5 ZE à vacance disponible négative contribuent 15 906
   (5,6 %) du besoin ; pas de plancher à 0 (tension.py:106-109).
   → publier besoin avec/sans artefacts (269 759 vs 285 665).
8. **R-09 ignore l'état réel du gisement (R-08)** : coût moyen S-17 calibré
   opérations volontaires, surfaces parc occupé ; L-14 dit « sens indéterminé »
   alors que R-08 donne un indice directionnel haussier. Pas de tri optimiste
   (vérifié remob.py:88-89 — coût uniforme, objection sélection ne tient pas).
   → renforcer L-14 + variante coût haut +50 % (ratio resterait > 2).
9. **Effets de bord non nommés** : effet-prix voulu et ses perdants, incitations
   propriétaires (12,5 Md€ privés → subvention/contrainte), territoires détendus
   ignorés, attribution des logements remis en marché. Sérieuse si I-10 publié tel
   quel. → nouvelle L-xx, à instruire dans P-xx.
10. **Sensibilité jointe** : pire cas joint (7 % + coûts hauts + densité basse) ne
    casse PAS R-09 (ratio ~3,2) ni R-10 (ratio 4,1) — point FORT non publié — mais
    casse R-07 via mobilisabilité < 87 %. → publier le pire cas joint (section 7 qmd).

## Synthèse
La conclusion « contrainte institutionnelle, pas physique » survit en foncier (R-10
robuste) et en direction économique (ratio > 2 partout), mais : couverture ~1,0 au
proxy TLV, 55 % du besoin hors ZE couvertes, 12,5 → 19,8 Md€ (ratio 2,4), bascule
mobilisabilité 60,5 %/87 %. Corrigés, ces points DÉPLACENT la lecture : la contrainte
institutionnelle devient la CONDITION de la suffisance, pas sa conséquence.
