# Revue contradictoire — angle statistique (13 objections)

Vérif arithmétique : 1,65 / 48,3 / 3,9 / 11,5 exacts ; garde H-11 effective.
Aucune erreur de calcul. Les objections portent sur la lecture.

## SÉRIEUSES
1. **R-08 superlatif à périmètres mélangés** : 0,56 est métropole seule ; R-03/R-04
   publiés France entière. À périmètre métropole harmonisé : âge +0,559
   [0,474;0,634], coût −0,527 [−0,605;−0,437], emploi −0,467 [−0,553;−0,371] —
   IC chevauchants, « corrélat le plus fort » non testable (seul vs F+G : z=3,5
   significatif). → publier Spearman métropole/DOM pour R-03/R-04/R-06,
   reformuler R-08/I-08 (« du même ordre que coût et emploi à périmètre égal »).
2. **L-12 sens du biais de secrétisation FAUX au national** : couverture =
   S/(S−186 357) est DÉCROISSANTE en S quand gisement > besoin → réintégrer le
   masqué donne borne 1,65 → 1,50 (surestimation, pas sous-estimation) ; jusqu'à
   85 ZE pourraient basculer tendues à la borne haute du masqué — partition
   142/101/41 instable. → corriger L-12, sensibilité secrétisation dans R-07,
   test de monotonie.
3. **I-08 saut écologique non déclaré** : ancienneté calculée sur les RÉSIDENCES
   PRINCIPALES (P22_RP_ACH*), F+G sur les diagnostiqués (parc en transaction) —
   l'état du parc VACANT n'est mesuré nulle part ; « remobiliser a un coût »
   attribue l'état de l'occupé au vacant. → compléter L-13, I-08 au conditionnel,
   piste fichiers fonciers.
13. **R-09/R-10 ne propagent pas l'incertitude amont** : plages publiées
    (10,6-15,3 ; 5,5-17,6) conditionnelles au besoin central H-08 — la plus
    grosse incertitude de la chaîne n'est pas propagée (converge hyp/déf #4).
    → croiser variantes ou déclarer conditionnalité dans L-14/L-15.

## MINEURES
4. **R-03 « ~85 % » sur 74 % de la masse** : 26,2 % de structurelle hors calcul,
   masqué plus rural-déclinant (25,7 % vs 17,8 % du parc) ; réallocation
   proportionnelle 84,2 % (robuste), borne extrême 62,5 %. ANOMALIE : manquants/
   communes masquées = 11,2 > plafond 10 du masquage < 11 — écart pas entièrement
   expliqué par la secrétisation, à instruire. → encadrer [62,5;84,9] + test de
   réconciliation.
5. **R-05 « sans lien » faux** : +0,17, n=297 → IC [0,06;0,28], p≈0,003 ;
   incohérence avec le contraste touristique négatif (non-monotonie non
   discutée). → reformuler + convention de lecture des rho.
6. **L-13 sens du biais DPE non dit** : intensité de diagnostic × vacance
   rho ≈ −0,14 → 0,40 plutôt borne basse (conservateur) mais niveaux (Ussel
   37,3 %) = parc en transaction seulement. → phrase de direction + publier rho.
7. **R-06 loyers 2025 ÷ revenus 2021** : ~+10-15 % de croissance nominale non
   corrigée → niveaux surestimés (médiane vraisemblable ~35-37 %, Paris ~82-85 %) ;
   direction jamais énoncée dans L-09/L-11. → direction + variante indexée.
8. **Aucun IC/test publié** : tout vérifié significatif (MW z 6,4-7,4) — objection
   écartable sur le fond ; ajouter IC Fisher (fonction pure) ; contrastes de
   médianes = re-description du même signal, pas corroboration.
10. **min_count incohérent** : ze.py/cout.py sommes nues (NA→0) vs tension/effort
    min_count=1 ; aucune ZE tout-secret aujourd'hui (0/305) — invariant porté par
    les données, pas le code. → unifier + test de propriété.
9/11/12 : construit disponible bruité au seuil (bande grise à publier) ; partition
déclin 2018 (seuil dur non paramétré) ; I-04 mécanisme individuel conditionnel —
écartables/mineures, tracées.

## Bilan
Chiffres exacts, corrélations toutes significatives ; c'est la MISE EN RÉCIT
(superlatifs, absence d'IC, directions de biais tues, plages non propagées) qui
prête le flanc.
