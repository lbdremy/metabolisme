# NEXT-STEPS — ce qui vient ensuite

Ce qui est déjà fait est consigné dans [`PREV-STEPS.md`](PREV-STEPS.md).

## État au sortir de la session 1 (2026-09-18)

Première mesure de la rente du programme, sur les comptes 2023 de trois
des quatre groupes concessionnaires, présentée à six taux, sur deux bases
et deux amortissements, avec témoin et avec la mesure du régulateur en
regard ; article écrit ; **rien n'a été relu par Rémy** ; pas de tag,
pas de déploiement, pas de revue contradictoire.

## Prochaines étapes (dans l'ordre)

1. **Lecture de Rémy** : `evidence/decisions-2026-09-18.md` (DEC-01 à
   07), puis l'article, puis `INTRO.md`. Points qui méritent son arbitrage :
   les prélèvements spécifiques comptés en destination (DEC-04) ; la
   variante centrale nette-comptable (DEC-06) ; le témoin VINCI (DEC-05) ;
   la proposition conditionnelle P-01 (DEC-07) ; le titre de l'article.
2. **Revue contradictoire** (rythme du dépôt : quatre relecteurs, rapports
   bruts et synthèse commis avant intégration) sur la mesure D-15
   appliquée : base d'actifs (IFRS vs comptes sociaux, L-07), traitement
   des prélèvements (C-03), extrapolation Sanef-SAPN (H-09), témoin (C-05),
   écart avec la méthode de l'ART (I-02), et le passage de « surprofit » à
   « rente de position » (I-01).
3. **Sanef-SAPN** : télécharger à la main
   `https://www.groupe.sanef.com/sites/default/files/2024-04/RCC-SANEF-31-12-2023-Signe.pdf`
   (page « Finances » du groupe ; le site rejette tout client non
   interactif), l'enregistrer (S-18), ajouter ses lignes à
   `data/transcribed/comptes-2023.csv`, retirer H-09 et L-04.
4. **Série temporelle** : les mêmes comptes 2006-2024 (rapports financiers
   annuels des groupes, synthèses ART depuis 2015) pour passer de la
   mesure d'une année (L-08) à la mesure sur la vie du contrat, et
   réconcilier numériquement M-01 et M-03 (I-02).
5. **Concessions récentes** (A65, A19, A28, A88, Millau, A150, A355, A79)
   comme témoin de la mise en concurrence (monopoles:H-02) : comptes des
   sociétés, TRI 5,9 % (O-02).
6. **Tag et déploiement** après relecture : `autoroutes-rente-v1.0`,
   `pnpm deploy:web` ; mettre à jour `monopoles/NEXT-STEPS.md` (l'étape 2
   y est faite) et `monopoles/INTRO.md` §14 (livrable 5).
7. **Contraintes** (gabarit, question 8) non instruites : classement
   Eurostat d'une reprise de la recette avec la dette des SCA ; droit des
   aides d'État ; contrats d'exploitation au forfait (précédents :
   DIR, concessions d'ouvrages d'art) ; coût de sortie de l'usager (Q3).

## Restes ouverts

- Les pages Légifrance (L. 3132-4 CCP, L. 425-1 CIBS, L. 122-4 et
  L. 122-9 du code de la voirie routière) ne sont pas figées : capture
  navigateur à faire (monopoles/CLAUDE.md, astuce headed) ; les
  définitions D-04 et D-06 citent des sources secondaires qui les
  reproduisent verbatim.
- Les six autres contrats de concession (Cofiroute, Escota, APRR, Area,
  Sanef, SAPN) et le décret RCEA sont publiés par le ministère ; seul ASF
  est figé (S-12).
- Les comptes sociaux des sept sociétés (Infogreffe / pappers, 403) —
  pour lever L-07.
- Le marché des autocars comme témoin externe : trouver une source qui
  publie les résultats d'exploitation des opérateurs (DEC-05).
- Dates de publication « au mois près » de S-08, S-09, S-10, S-16, S-17 :
  à préciser depuis les documents d'origine.
- Outillage : validateur de registres partagé (troisième copie de
  `models.py`, DEC-02) ; extraction à faire quand deux études sectorielles
  existeront (INTRO §20).

## Comment reprendre (2 minutes)

Lire dans l'ordre : `CLAUDE.md`, `INTRO.md`, `EVIDENCE.md`,
`evidence/decisions-2026-09-18.md`, l'article, puis ce fichier. Contrôle :
`uv run autoroutes validate && uv run autoroutes reproduce && ./check.sh
&& ./test.sh`, puis `cd ../site && pnpm content` (doit régénérer le post
à l'identique).
