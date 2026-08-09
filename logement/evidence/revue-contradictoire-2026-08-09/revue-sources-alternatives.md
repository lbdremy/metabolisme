# Revue contradictoire — angle SOURCES ALTERNATIVES (relecteur n°1)

- **Date** : 2026-08-09
- **Périmètre** : ajouts de la session 4 (2026-08-08) uniquement — S-27..S-32, D-16..D-18, H-13, C-09/C-10, O-25..O-35, T-12..T-15, R-11..R-14, I-11..I-14, L-22..L-25. Les objections déjà traitées par la revue du 2026-08-07 (R-01..R-10) ne sont pas re-soulevées.
- **État examiné** : commit `d563df4`, tag `efficacite-parc-v0.4`.
- **Méthode** : lecture des registres, du graphe, du qmd et du compte rendu de revue précédente ; vérification de vivacité des six URLs sources (toutes HTTP 200 le 2026-08-09) ; recherche active de sources meilleures ou contradictoires (INSEE, SDES, ANCOLS, DGFiP, OCDE/CAE, notaires) ; recoupement des chiffres-titres avec les publications tierces ; téléchargement et lecture de la table DMTO DGFiP de juin 2026 et du communiqué ANCOLS du 09/02/2026.

---

## Objections

### SA-1 — La « part démographique » du ralentissement est désormais publiée : 14 % (Insee Première n° 2073) — L-22/I-11 laissent ouverte une question que la littérature a tranchée

- **Cible** : L-22 (1), I-11, R-11 ; secondairement R-13/L-24.
- **Gravité** : sérieuse (correction qui RENFORCE le résultat, mais le texte actuel est en retard sur la littérature).
- **Énoncé** : L-22 dit « une partie de la chute nationale est démographique » et I-11 « la part démographique du ralentissement n'est pas séparée de la part “blocage” ». Or l'INSEE a publié le 30/09/2025 (donc AVANT la session 4) une décomposition explicite : sur la baisse de la mobilité résidentielle 2013→2023 (10,8 % → 10,5 % en 2018 → 8,8 %, EAR 2014-2024), « le vieillissement de la population et la part grandissante des plus âgés, moins mobiles, sont responsables de 14 % de la baisse globale de la mobilité sur dix ans » ; la baisse touche tous les types de ménages et tous les âges (hors fin de lycée) et se concentre sur les courtes distances (mobilité intra-communale −20,9 %) ; « les contraintes financières des ménages et le coût des logements constituent d'autres pistes ». L'objection de composition que L-22 anticipait est donc BORNÉE petite par une source externe indépendante — I-11 est plus solide que son propre énoncé ne le dit.
- **Preuve** : Insee Première n° 2073, « Moins de déménagements en dix ans, mais l'Ouest et le périurbain toujours attractifs », 30/09/2025, https://www.insee.fr/fr/statistiques/8648157 (consulté le 2026-08-09).
- **Effet si retenue** : I-11 peut abandonner le conditionnel sur la composition (en citant 14 % comme borne externe, sans refaire le calcul) ; la géographie de la chute (l'argument central de R-11) reste intacte. Bonus : la géographie IP2073 (Ouest et périurbain attractifs, cœurs urbains perdants) recoupe indépendamment les soldes de R-13 (Sables-d'Olonne, La Rochelle, Dinan positifs ; Paris négatif).
- **Disposition proposée** : enregistrer IP2073 comme S-xx (Licence Ouverte, fichier données des figures disponible), citer la décomposition dans L-22 et I-11, et ajouter le recoupement géographique dans R-13.

### SA-2 — Même chose côté parc social : l'ANCOLS a chiffré la part du vieillissement des attributaires à 9 % (communiqué du 09/02/2026)

- **Cible** : I-12, L-23, R-12.
- **Gravité** : sérieuse (même nature que SA-1 : le caveat « blocage vs stabilité choisie / composition » est partiellement instruit par une source publiée avant la session 4).
- **Énoncé** : communiqué ANCOLS du 09/02/2026 (PDF lu intégralement) : entre les cohortes d'attributaires 2015 et 2019, « la hausse de l'âge moyen des attributaires expliquerait donc 9 % de la baisse du taux de mobilité à quatre ans » ; sans vieillissement 2015-2022, le taux de rotation 2023 « serait ainsi passé de 8,1 % à 8,2 % » (3 800 libérations supplémentaires sur ~1 % du total). Autrement dit : l'explication démographique du gel social est marginale — ce qui conforte directement I-12 (« la sortie vers le privé est le déterminant dominant »), mais n'est ni enregistré ni cité.
- **Preuve** : ANCOLS, « Quelle est la part du vieillissement des attributaires dans la baisse de la mobilité au sein du parc social ? », communiqué du 09/02/2026, https://www.ancols.fr/assets/publication_file/2026/02/09/a2679302-7223-4616-a9d5-d98dc801c172-CP-Vieillissement-Rotation.pdf (consulté le 2026-08-09 ; attention, certificat TLS du site invalide — figer le PDF). Contexte : ANCOLS/Banque des Territoires, taux d'attribution sous 10 % en 2024, demande à 4,1 M (+4,8 %), https://www.banquedesterritoires.fr/le-taux-dattribution-des-logements-sociaux-passe-sous-les-10-en-2024 (consulté le 2026-08-09).
- **Effet si retenue** : I-12 gagne une borne externe sur son angle mort déclaré ; le « rotation 8,1 % en 2023 » ANCOLS recoupe en outre le 8,0 % RPLS 2023 de la chaîne (définitions voisines : libérations vs emménagements).
- **Disposition proposée** : enregistrer le communiqué (et l'étude complète qu'il annonce) comme S-xx ; citer dans I-12/L-23.

### SA-3 — L'« accélération » post-2022 (R-11, R-12) a une explication concurrente publiée : le choc de taux d'intérêt 2022-2024 — absent de L-22 et L-23

- **Cible** : I-11, I-12, O-29 (« le rythme récent est le plus raide de la série »), L-22 (3), L-23 ; indirectement l'énoncé de R-12.
- **Gravité** : sérieuse — c'est l'objection la plus lourde de cette passe. Aucun chiffre ne tombe, mais la mise en récit de l'accélération ne survit pas telle quelle.
- **Énoncé** : la chaîne lit l'accélération de la chute (R-11 : −0,92 pt sur 2017-2023 ; R-12 : −1,43 pt sur 2022-2025, « le rythme le plus raide ») comme l'intensification d'un verrouillage structurel. Or la période 2022-2024 est documentée par les notaires et la FNAIM comme un choc de cycle du crédit sans équivalent récent : transactions dans l'ancien ~1,2 M (2021) → ~875 k-935 k (2023) → ~780 k (fin 2024), « la hausse brutale des taux entre janvier 2022 et fin 2023 est largement responsable du retournement », avec amorce de reprise en 2025. Ce choc comprime mécaniquement les sorties du parc social vers l'accession (le canal dominant identifié par I-12) et la rotation générale — une composante CYCLIQUE, potentiellement réversible, que rien dans L-22 (qui ne cite que le COVID) ni L-23 ne mentionne. Le millésime RPLS 2025 (emménagements 2024) tombe exactement au creux du cycle ; la fenêtre « moins de 2 ans » du RP2023 (emménagements ~2021-2023) chevauche le début du choc.
- **Preuve** : bilans 2024 des Notaires de France et FNAIM relayés p. ex. par https://www.abcbourse.com/marches/immobilier-les-ventes-chutent-de-17-en-2024-les-prix-continuent-de-baisser et https://www.immomatin.com/evaluation/sites-evaluation/quel-bilan-du-marche-immobilier-2024-selon-les-notaires-de-france.html (consultés le 2026-08-09) ; IP2073 (SA-1) cite les « contraintes financières » parmi les pistes. À figer de préférence depuis la note de conjoncture immobilière des Notaires de France ou la Stat Info « crédits à l'habitat » de la Banque de France.
- **Effet si retenue** : la partie STRUCTURELLE du diagnostic (niveau miroir du marché, rho −0,80 ; concentration territoriale de la chute 2012→2023 qui commence AVANT le choc de taux : −0,25 pt dès 2012-2017 ; gradient de R-11) survit — elle ne dépend pas du cycle. Mais « la chute s'accélère » ne peut pas être titrée comme aggravation du verrouillage institutionnel sans le caveat du cycle ; et un rebond 2025-2026 de la mobilité ne réfuterait pas H-04 (il faut le dire d'avance, c'est exactement le rôle d'une limite).
- **Disposition proposée** : compléter L-22 et L-23 (composante cyclique taux d'intérêt, fenêtres de collecte au creux du cycle) ; reformuler la phrase d'accélération de I-11/I-12 pour séparer tendance longue (2013→2019/2012→2017, antérieure au choc) et fin de période ; enregistrer une source de conjoncture (notaires ou Banque de France).

### SA-4 — S-31 n'est plus la table DMTO en vigueur : deux éditions plus récentes existent (04/2026 et 06/2026) et la composition des départements a bougé

- **Cible** : S-31, H-13, L-25 (2), qmd R-14.
- **Gravité** : mineure sur les chiffres (le central 6,32 % et la plage [5,09 ; 6,32] tiennent), sérieuse sur la méthode (fraîcheur de source, déjà identifiée comme faiblesse dans NEXT-STEPS « veille de fraîcheur » — en voici un cas réel à 6 mois du figement).
- **Énoncé** : la DGFiP publie `dmto_2026-04.pdf` et `dmto_2026-06.pdf` (vérifiés HTTP 200 ; PDF de juin téléchargé et lu). Au 01/06/2026, la liste des départements restés à 4,50 % n'est plus celle de S-31 (05, 06, 07, 16, 26, 27, 48, 60, 71, 971) : l'**Eure (27) est passée à 5,00 %**, les **Hautes-Pyrénées (65) sont redescendues à 4,50 %**, et **Mayotte (976) figure à 4,50 %** (et non plus 3,80) ; l'Indre (36) reste seule à 3,80 %. La phrase de L-25 « une dizaine de départements sont à 5,81 % et l'Indre à 5,09 % » est donc datée — la composition bouge au fil des délibérations départementales. S'ajoute un décalage temporel dans R-14 : les prix sont ceux des ventes 2025, or la faculté 5,00 % ne s'applique qu'aux actes à partir du 01/04/2025 (et selon la date de délibération de chaque département) — une partie des ventes 2025 de l'assiette a réellement payé 5,81 %. Défendable si R-14 est lu comme « le péage d'un achat AUJOURD'HUI au prix médian observé », mais ce choix de lecture n'est écrit nulle part.
- **Preuve** : https://www.impots.gouv.fr/sites/default/files/media/1_metier/3_partenaire/notaires/dmto/dmto_2026-06.pdf (consulté le 2026-08-09 ; pages 1-3 : colonnes « taux voté » par département).
- **Effet si retenue** : aucun chiffre-titre ne bouge (H-13 central inchangé, borne basse 5,09 toujours fondée sur l'Indre) ; L-25 (2) doit être réécrite sans liste figée ou avec sa date ; la lecture temporelle de R-14 doit être explicitée.
- **Disposition proposée** : figer `dmto_2026-06.pdf` en S-xx (ou mettre à jour S-31 avec trace), dater toute énumération de départements, écrire dans C-10/L-25 que le péage est celui d'un acte au barème courant appliqué aux prix 2025 ; verser ce cas au dossier « commande `logement freshness` » de NEXT-STEPS.

### SA-5 — Le « plancher » de R-14 exclut la CSI, pourtant publiée et exactement calculable (0,10 % du prix)

- **Cible** : L-25 (1), T-15, O-35, H-13 (notes).
- **Gravité** : mineure.
- **Énoncé** : la contribution de sécurité immobilière est un taux fixe publié — 0,10 % du prix, minimum 15 €, stable depuis 2016 (art. 879-881 CGI) — aussi déterministe que les DMTO et les émoluments. L'exclure parce que « S-32 ne la chiffre pas » est un artefact du choix de source, pas une frontière de données : la page impots.gouv des frais d'acquisition la chiffre. À l'inverse, la chaîne ignore les abattements départementaux (ex. Calvados : abattement limité 46 000 €, table DMTO) et les réductions primo-accédants (ex. Savoie 4,00 %, art. 1594 F septies), qui jouent en sens inverse — cohérent avec « hors primo-accédants » mais à dire.
- **Preuve** : https://www.impots.gouv.fr/particulier/questions/jachete-un-bien-immobilier-quaurai-je-payer-comme-frais-au-notaire (consulté le 2026-08-09) ; table DMTO 06/2026 précitée (colonne abattements).
- **Effet si retenue** : +0,10 pt sur le péage (≈ 7,5-8,1 % au lieu de 7,4-8,0) — négligeable sur les mois de niveau de vie, mais le plancher devient plus serré et la part fiscale du péage (« ~83 % ») monte légèrement.
- **Disposition proposée** : soit intégrer la CSI au calcul (une ligne dans T-15, source à enregistrer), soit la citer chiffrée dans L-25 au lieu du seul « ni CSI ».

### SA-6 — Licence S-28 : CONFIRMÉE Licence Ouverte par les mentions légales du site SDES (le « à confirmer » peut être levé) ; RPLS 01/01/2026 non paru

- **Cible** : S-28 (champ `license`), NEXT-STEPS (item licences).
- **Gravité** : mineure (résolution favorable d'un point ouvert).
- **Énoncé** : la page de publication RPLS ne porte pas de licence, mais les mentions légales du site SDES disposent : « Les publications et données mises à disposition sur le site du service des données et études statistiques (SDES) sont consultables et téléchargeables gratuitement sous licence ouverte telle que décrite dans le décret n° 2017-638 » (décret d'homologation de la Licence Ouverte). Par ailleurs, aucun résultat RPLS au 01/01/2026 n'est publié à ce jour (seul existe le guide de collecte USH pour la campagne 2026) : S-28 est bien le dernier millésime disponible. Statut des autres licences : S-27/S-29 (INSEE) et S-30 (data.gouv) en Licence Ouverte déclarée — conforme ; S-32 (service-public) conforme ; S-31 (impots.gouv) reste « document public, citation » — acceptable pour des taux légaux (données non protégeables), à défaut de licence explicite.
- **Preuve** : https://www.statistiques.developpement-durable.gouv.fr/mentions-legales (consulté le 2026-08-09) ; https://www.union-habitat.org/centre-de-ressources/economie-financement/guide-rpls-au-1er-janvier-2026 (consulté le 2026-08-09).
- **Effet si retenue** : S-28 citable dans l'article sans réserve.
- **Disposition proposée** : mettre à jour `sources.yaml` (S-28 : Licence Ouverte via mentions légales SDES, URL et date de constat dans les notes) ; retirer l'item correspondant de NEXT-STEPS.

### SA-7 — Recoupements tiers : tous verts, mais le niveau de R-13 (9,87 %) doit être daté — la mesure publiée la plus récente (2023) est plus basse (8,8 %)

- **Cible** : R-13, L-24 (2), qmd R-13 ; validation de R-12/R-14.
- **Gravité** : mineure (les recoupements confirment ; seul le risque de lecture « actuelle » du 9,87 % appelle une retouche).
- **Énoncé et preuves** (tout consulté le 2026-08-09) :
  - **RPLS national** : la page SDES publie mobilité 9,3 % (2019) → 7,1 % (2025), vacance 2,1 % — identique aux 9,29/7,11/2,12 de la chaîne (https://www.statistiques.developpement-durable.gouv.fr/54-millions-de-logements-locatifs-sociaux-en-france-au-1er-janvier-2025).
  - **Rotation sociale ANCOLS** : 8,1 % en 2023 ≈ 8,0 % RPLS 2023 de O-32 (définitions voisines, SA-2).
  - **Frais d'acquisition** : « entre 7 et 8 % du prix dans l'ancien » (impots.gouv, notaires) ≙ les 7,4-8,0 % de R-14.
  - **Taux DMTO** : la décomposition 5,00 × 1,0237 + 1,20 = 6,32 % est confirmée par la table DGFiP et par les recoupements tiers (88 départements à 6,32 % environ).
  - **Mobilité des personnes** : la série IP2073 (10,8 % en 2013, 10,5 % en 2018, 8,8 % en 2023) encadre le 9,87 % de MIGCOM RP2022 — cohérent pour une moyenne de fenêtres 2020-2024 sur une série descendante (concepts voisins non identiques : MIGCOM inclut les arrivées de l'étranger, 0,44 pt). MAIS le chiffre publié le plus récent est 8,8 % (2023) : publier « 9,87 % de mobiles annuels » sans précision de fenêtre laisse croire à un niveau courant surestimé d'un point.
- **Effet si retenue** : confiance renforcée dans R-12/R-13/R-14 ; une phrase de datation à ajouter à R-13/L-24 (« moyenne des fenêtres annuelles 2020-2024 ; la série annuelle publiée est passée sous 9 % en 2023, IP2073 »).
- **Disposition proposée** : ajouter les recoupements au qmd (ils sont de la corroboration externe gratuite) et dater le niveau de R-13.

### SA-8 — Littérature coûts de transaction (OCDE, CAE, Fipeco) : rien de contradictoire avec I-14 — et une source chiffrée pour le « plusieurs points » d'agence de L-25

- **Cible** : I-14, L-25 (1).
- **Gravité** : mineure (renfort).
- **Énoncé** : la littérature publiée soutient I-14 plutôt qu'elle ne le contredit : l'OCDE chiffrait dès 2011 les coûts de transaction complets en France à ~14 % de la valeur du bien (contre ~5 % au Royaume-Uni/États-Unis, ~8 % en Allemagne — agence incluse) et recommande de réduire les DMTO « pour faciliter la mobilité des ménages » ; le CAE (Trannoy-Wasmer, 2013) proposait leur suppression ; Fipeco documente le mécanisme de perte sèche. Deux usages : (1) le « l'agence peut ajouter plusieurs points » de L-25 dispose d'un chiffrage sourcé (l'écart ~14 % vs ~7,5 % fiscal+émoluments) ; (2) I-14 peut adosser son lien péage→mobilité à une littérature comparative au lieu de la seule corrélation territoriale rho +0,81.
- **Preuve** : OCDE, « La fiscalité immobilière dans les pays de l'OCDE — points clés », https://www.oecd.org/fr/fiscalite/politiques-fiscales/brochure-la-fiscalite-immobiliere-dans-les-pays-de-l-ocde.pdf ; Fipeco, « La fiscalité du patrimoine immobilier », https://www.fipeco.fr/commentaire/La%20fiscalit%C3%A9%20du%20patrimoine%20immobilier (consultés le 2026-08-09).
- **Disposition proposée** : enregistrer une source OCDE (et/ou la note CAE 2013) et citer dans I-14/L-25 — utile aussi pour la future proposition P-xx (« ~83 % du péage est fiscal » gagne un comparatif international).

### SA-9 — Aucune source ouverte MEILLEURE que S-27/S-29/S-30 identifiée ; les frontières (Fidéli, EnL 2020, bases notariales, DV3F) sont réelles et à consigner

- **Cible** : S-27, S-29, S-30 ; L-24 ; NEXT-STEPS.
- **Gravité** : mineure (constat de complétude).
- **Énoncé** : au 2026-08-09 : RP2023/Melodi (S-27, publié le 08/08/2026) et MIGCOM RP2022 (S-29, idem) sont les derniers millésimes ouverts de leurs familles ; DVF 2025 année complète (S-30) est la dernière livraison (prochaine attendue ~octobre 2026) ; RPLS 2025 dernier paru (SA-6). Les mesures potentiellement supérieures sont toutes sous habilitation : Fidéli (suivi annuel exhaustif logements × occupants, la meilleure mesure de mobilité annuelle par statut — INSEE la décrit comme complément du recensement pour les territoires tendus), microdonnées EnL 2020, bases notariales BIEN/Perval, DV3F (acteurs publics). Une seule réserve : IP2073 montre qu'une exploitation EAR PLUS RÉCENTE (série annuelle jusqu'à 2023) existe côté INSEE — si les données des figures d'IP2073 sont téléchargeables (elles le sont normalement), elles donnent gratuitement la série annuelle de mobilité que MIGCOM seul ne donne pas (SA-1/SA-7).
- **Preuve** : https://www.insee.fr/fr/information/3897375 (Fidéli) ; https://www.insee.fr/fr/statistiques/8589767 (MIGCOM RP2022) ; https://files.data.gouv.fr/geo-dvf/latest/csv/2025/ (consultés le 2026-08-09).
- **Disposition proposée** : consigner ces frontières dans NEXT-STEPS (comme les frontières LOVAC détaillées) ; figer les données des figures d'IP2073 avec la publication (SA-1).

---

## Verdict

**Survit tel quel** :
- **R-11** (niveaux, deltas, gradients territoriaux) — aucune source contradictoire ; la décomposition INSEE (14 % démographique) désamorce la principale menace déclarée dans L-22.
- **R-12** (chiffres) — recoupé à l'identique par la page SDES (9,3 → 7,1 ; vacance 2,1) et, en ordre de grandeur, par l'ANCOLS (8,1 % en 2023).
- **R-13** (structure par statut, validation croisée +0,80, soldes) — cohérent avec IP2073 ; seule la présentation du niveau 9,87 % doit être datée (SA-7).
- **R-14** (taux 7,4-8,0 %, poids en mois, rho +0,81) — recoupé par les fourchettes publiées (7-8 % dans l'ancien) et par la littérature OCDE ; H-13 central et plage inchangés malgré la table de juin (SA-4).
- La licence de S-28 est confirmée (SA-6).

**Ne survit pas tel quel** :
- La mise en récit de l'**accélération** dans I-11/I-12 (« la chute s'accélère » lue comme aggravation du verrouillage) sans le caveat du **cycle du crédit 2022-2025** (SA-3) — la composante cyclique, documentée et potentiellement réversible, doit entrer dans L-22/L-23 avant tout titrage.
- Les énoncés « part démographique non séparée » de I-11 (SA-1) et l'angle mort équivalent de I-12 (SA-2) — la littérature les a tranchés (14 % et 9 %), en faveur de la chaîne : les maintenir en l'état serait ignorer des sources publiées avant la session.
- La liste figée des départements DMTO dans L-25 (2) et l'absence de datation de la table (SA-4).

**Sources candidates à enregistrer** :
1. Insee Première n° 2073 (30/09/2025), mobilité résidentielle 2013-2023, décomposition vieillissement 14 % — https://www.insee.fr/fr/statistiques/8648157
2. ANCOLS, communiqué + étude « Part du vieillissement des attributaires dans la baisse de la mobilité du parc social » (09/02/2026), 9 % / rotation 8,1→8,2 % — https://www.ancols.fr/assets/publication_file/2026/02/09/a2679302-7223-4616-a9d5-d98dc801c172-CP-Vieillissement-Rotation.pdf (certificat TLS du site invalide : figer le fichier)
3. DGFiP, table DMTO au 01/06/2026 — https://www.impots.gouv.fr/sites/default/files/media/1_metier/3_partenaire/notaires/dmto/dmto_2026-06.pdf (et l'édition 04/2026 pour la trace)
4. Une source de conjoncture pour le cycle 2022-2025 (note de conjoncture immobilière des Notaires de France ou Stat Info Banque de France « crédits à l'habitat ») — à figer en version datée
5. OCDE, « La fiscalité immobilière dans les pays de l'OCDE » (coûts de transaction ~14 % France, recommandation DMTO) — https://www.oecd.org/fr/fiscalite/politiques-fiscales/brochure-la-fiscalite-immobiliere-dans-les-pays-de-l-ocde.pdf ; éventuellement la note CAE n° 2 (Trannoy-Wasmer, 2013)
6. impots.gouv, « J'achète un bien immobilier : quels frais chez le notaire ? » (CSI 0,10 %, composition des frais) — https://www.impots.gouv.fr/particulier/questions/jachete-un-bien-immobilier-quaurai-je-payer-comme-frais-au-notaire
7. SDES, mentions légales (preuve de licence pour S-28) — https://www.statistiques.developpement-durable.gouv.fr/mentions-legales
8. ANCOLS, Panorama du logement social 2025 / attributions 2024 (contexte de file d'attente pour I-12) — https://www.ancols.fr/

Toutes les URLs ci-dessus ont été consultées le 2026-08-09. Les six URLs des sources S-27..S-32 du registre sont vivantes (HTTP 200) à cette date ; aucun millésime plus récent que ceux figés n'est disponible en accès ouvert, à l'exception de la table DMTO (SA-4).
