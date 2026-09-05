# Revue contradictoire — cadrage de l'étude (2026-09-04 / 05)

Compte rendu de la revue contradictoire exigée par la méthode (INTRO
étape 12), menée les 4 et 5 septembre 2026 sur le cadrage de l'étude
« Monopoles naturels et collectivisation des rentes » — INTRO.md, seize
définitions, huit hypothèses, dix-neuf nœuds, l'article « Là où le marché
n'existe pas » et son document de preuve — à l'état du commit `59d021f`.
Les corrections sont commitées ; ce document consigne la méthode, les
objections et leur disposition, et le tableau avant / après.

## Méthode

Quatre relecteurs indépendants (agents distincts, sans accès aux
conclusions des autres), sur quatre angles, plus une synthèse de triage
par l'orchestrateur :

1. **Sources alternatives** — SA-1..SA-7 (7 objections ; mandat réduit
   après une première tentative interrompue par la limite de dépense)
2. **Définitions et hypothèses** — HD-1..HD-12 (12 objections)
3. **Scénarios d'échec** — SE-1..SE-22 (22 objections)
4. **Cohérence et statuts épistémiques** — CR-1..CR-17 (17 objections)

Les cinq rapports bruts (dont la synthèse de triage) sont commités en
annexe dans `revue-contradictoire-2026-09-04/` (commit `b173008`, AVANT
toute intégration). L'orchestrateur a re-vérifié les allégations
structurantes avant le triage (index PDF de l'OCDE, arête entrante de
V-01 dans le graphe, coupe de la citation de D-04, formule de D-13,
absence de vérification des empreintes au build, chiffres de la note
privée dans H-04 / H-07, dix « non » à Q1, taux 6,5 → 5,9 % au Sénat,
proposition de loi hydroélectricité) : **toutes confirmées, aucune
infirmée** (tableau dans la synthèse). Trois allégations externes ont été
retenues comme plausibles et figées ensuite (TRI FIPECO, tunnel de
Friggit, rapport ART, décision ARCEP, Eaufrance, Carpentier et al.).

## Verdict global

- **Survivent** : l'isolation des valeurs (V) et des choix (C), dans son
  principe ; les citations verbatim et les empreintes (toutes vérifiées) ;
  les caveats des définitions ; O-01 et la valeur centrale du taux de
  référence (confirmée par un second régulateur) ; L-03 et L-06 ; la
  séparation des trois niveaux ; la distinction concurrence pour / sur le
  marché ; la décision d'écarter les chiffres logement de la note.
- **Ne survivaient pas** : la question Q1, qui répondait « non » à tout ;
  l'agrégation du monopole naturel et de la fixité positionnelle ; la
  ligne logement, extérieure à la grille et contraire à sa règle Q2 ; la
  définition mesurable de la rente, sans base d'actifs ni postes ; la
  position normative, qui dissipait et captait à la fois ; le titre, qui
  affirmait la conclusion ; onze énoncés de la note repris sans statut ;
  le sens de plusieurs dépendances ; les index de pages OCDE ; la promesse
  d'empreintes vérifiées au build.

## Décisions actées par Rémy (2026-09-05, avant intégration)

1. **Périmètre** : monopoles naturels ET rentes de position — D-05
   scindée, Q1 à trois réponses, lignes témoins, logement et
   stationnement reclassés « rente de position », logement adossé à
   `logement/`.
2. **Destination de la rente** : les deux doctrines, explicites, choisies
   par secteur (prix au coût / recette affectée), V-05.
3. **Titre** : nouveau titre neutre — « Reconnaître une rente de
   position ».
4. **Intégration complète** des 58 objections.

## Objections structurantes et leur disposition

### A. Q1 ne discriminait rien ; monopole naturel ≠ rente de position (SE-1, HD-4, CR-8, CR-1)

Confirmé. Disposition : D-05 devient « non-duplicabilité » avec un critère
opératoire (sous-additivité D-01 + coûts irrécupérables D-19) ; D-16
« fixité positionnelle » créée ; Q1 a trois réponses (substituable / non
duplicable / fixe) plus « partiellement » ; deux lignes témoins ajoutées
(réseaux mobiles H-10, fibre en zone très dense H-11) ; hydroélectricité,
stationnement et logement reclassés « fixe » ; « constat » remplacé par
« hypothèse (H-01) » partout ; « discriminante » retiré du document de
preuve ; l'objet classé est dit sur chaque ligne (colonne ajoutée).

### B. Logement : C-03 extérieur à la grille, H-07 réfuté (SE-2, SE-10, HD-5, CR-4, CR-3, SE-21)

Confirmé. Disposition : Q2 reformulée (« la concurrence de service ne
discipline pas le prix d'accès », sans « nécessairement administré ») ;
C-03 rattachée à V-01, V-02, H-04, H-19 et présentée comme choix fondé sur
H-04 ; H-07 redéfinie « part du parc locatif OUVERT à loyer administré »,
sans valeur numérique ; H-04 réécrite (ouverture, pas part ; condition de
réfutation) ; chiffres de la note privée retirés des hypothèses (à
enregistrer avant usage) ; quatre configurations pour le logement, dont
l'encadrement des loyers.

### C. La définition mesurable de la rente (HD-1, HD-2, SE-4, SE-5, SE-6, SE-7, CR-6, CR-15, SA-7)

Confirmé. Disposition : D-15 « rente mesurable — surprofit sur base
d'actifs » créée (base = coût historique net des subventions, modèle BAR
D-21 ; coût efficace au sens de L. 341-2 ; postes ; avant impôts ; coûts
externalisés exclus ; témoin) ; H-06 renommée `reference_return_on_capital`,
plage [4,0 ; 8,8] sourcée (CRE, ARCEP, ART), taux sectoriel à enregistrer
en plus ; « une fois pour toutes » remplacé par « forme fixée, paramètres
par secteur » ; I-03 créée (l'attribution à une position est une
interprétation avec témoin) ; L-11 (cas d'échec : régie sans témoin,
secteur régulé, subventions croisées, qualité, prime de risque).

### D. Dissiper ou capter (SE-15, CR-2)

Confirmé (V-01 orpheline dans le graphe). Disposition : V-01 réécrite en
principe (« ne revient pas au propriétaire privé au titre de la
position ») ; V-05 créée (deux destinations admises et dites par secteur ;
tarification de la rareté à part) ; la colonne « conclusion » de
l'inventaire sortie de I-01 vers C-05 (configurations à instruire,
dépendant de V-01, V-04, V-05) ; V-01, V-03, V-04 désormais référencées.

### E. Configurations comparées (SE-20, SE-6)

Confirmé. Disposition : C-05 — quatre configurations (statu quo / privé
régulé / collectivisation avec porteur de risque et classement en dette /
privé intégral facultatif) ; destination dite ; statu quo autoroutier
décrit comme mobile (retour à l'État par défaut).

## Les autres objections, par disposition

| Objection | Disposition |
|---|---|
| HD-6, SE-3, SE-5, CR-1 (H-01 n'est pas un test) | H-01 réécrite : périmètre « non duplicable ET prix non administré », test par D-15 aux deux bornes avec témoin, condition de réfutation ; signature → faisceau d'indices I-03 ; O-08 (IGEDD) figé : sur le logement l'hypothèse porte sur le prix des actifs, pas sur le loyer |
| HD-3 (quasi-rente ≠ rente d'innovation) | D-04 : citation complète, assumée comme notion construite sans source qui la définisse ; D-03 distingue les deux cas et dit que la source range les réseaux du côté de la quasi-rente |
| HD-10, HD-11, SE-16, SE-18 (notions absentes, échelles, monopole légal, captivité réglementaire) | D-17 exclusion, D-18 économies d'envergure, D-19 coûts irrécupérables, D-20 barrières à l'entrée, D-21 base d'actifs régulés ; D-08 : deux sous-critères et échelle ; D-14 et H-18 : catégorie « domaine public concédé » ; H-16 : captivité en partie réglementaire, « refaire l'installation » déclassé en énoncé à vérifier |
| SE-8, SE-12, SE-13, SE-14, SE-17, SE-19 (inventaire secteur par secteur) | H-14 : régime hydro en réforme (O-09, S-15 figé ; L-12 promulgation) ; I-02 : télécoms « cas à instruire » avec trois conditions de renversement ; H-12 : rail partageable là où la capacité n'est pas saturée ; H-13 : électricité classée sur le réseau, production séparée ; H-15 : transferts budgétaires comptés, captivité non totale ; H-20 : ressource fixe / constellations substituables, licences payantes |
| CR-7, HD-7, HD-12, CR-12, CR-16, SE-21 (dépendances, statuts) | `justification` limité à S / O / I, limites dans `limitations` (champ ajouté aux hypothèses) ; H-04 et H-05 sans justification circulaire ; `constructed_by` porté dans le graphe pour les huit notions construites ; L-07 attaché à chacune ; L-01 → V-03, L-02 → C-01 ; D-13 sans valeur (→ O-01) ; inventaire enregistré en H-09..H-20 ; V-03 réduite à sa part normative ; V-06 continuité du service ; « seule partie que les données ne tranchent pas » corrigé (valeurs et choix de méthode) |
| CR-10, CR-11, SE-21(e) (importations sans statut, objections) | Énoncés de la note portés par H-09..H-20 comme « à sourcer » et par L-09 ; L-01, L-02, L-05 vidées de leur contenu assertif ; section renommée « Objections anticipées », origine dite, réponse doctrinale de l'objection 1 retirée, H-08 incluant zéro dit à l'objection 3, V-01 cité à l'objection 4, objections non reprises listées avec leur renvoi |
| SE-9, SA-6, CR-11 (H-03 / H-08) | H-03 scindée hypothèse / méthode (sélection, ressource, investissement, fiscalité, qualité) ; H-08 « écart brut » 10 % [0 ; 27] sur O-04 (Eaufrance, S-10) et O-05 (Carpentier et al., S-11) ; L-06 élargie |
| SE-11, HD-7 (H-05) | H-05 requalifiée en question de recherche, justification vide, condition de réfutation, D-18 pour le coût système |
| SA-1, HD-8 (index OCDE) | 353 / 462 (et 47, 163, 525 pour les nouvelles entrées) dans S-01, D-01, D-02, D-04, D-18..D-20 ; deux ISBN |
| SA-2, SA-3, SA-4 (licences, OpenStax, sources FR) | Licences reformulées (courte citation ; CRPA pour CRE, ART, ARCEP, Sénat, Eaufrance) ; `redistributable: false` pour le PDF OCDE (non servi par le site, L-10) ; clause anti-ingestion OpenStax dite ; glossaire ART figé (S-16) en caveat de D-01 ; Demsetz clos (pas d'accès libre, vérifié) |
| SA-5 (L-04 autoroutes) | Rapport ART 2024 figé (S-08, 13,8 Mo), O-03 ; H-17 devient la ligne la mieux sourcée ; L-04 restreinte aux autres lignes |
| SA-7 (H-06 second régulateur) | Décision ARCEP figée via sa publication au JORF (S-09 ; le PDF de l'ARCEP est derrière un pare-feu), O-02 |
| SE-4, SE-7 (TRI autoroutes, base d'actifs) | O-06 (Sénat n° 709, S-12) et O-07 (FIPECO, S-13, source secondaire L-12) figés ; sensibilité à la base documentée dans le document de preuve §7 |
| CR-9 (empreintes) | Le build du site recalcule désormais le sha256 de chaque fichier figé déclaré et échoue sur un écart (`build-posts`) ; l'article dit ce qui est vérifié |
| CR-5 (titre) | « Reconnaître une rente de position » ; sous-titre « Monopoles naturels, ressources fixes, et ce que collectiviser une rente veut dire » |
| CR-13, HD-9 (citations) | « traduction de travail » dit dans l'article ; « We » pour « you » (D-07) ; formule complète de D-13 (IEC × coût de la dette, page 18) ; contexte « economies of scope » dans D-01 ; `last_updated` de D-06..D-08, D-17 = date de la page ; « cinq » → huit notions construites, comptées partout |
| CR-14, SE-21(a)(g) (décalages entre documents) | INTRO, EVIDENCE, README, CLAUDE.md, NEXT / PREV-STEPS, document de preuve alignés sur l'état HEAD ; identifiants `logement:` préfixés ; L-08 étendue à S-06 et S-09 |
| CR-15 (H-06, confiances) | Borne haute sourcée (O-03) ; règle de confiance écrite dans l'en-tête du registre ; phrase de sensibilité remplacée par les observations O-03, O-06, O-07 |
| CR-17 (version) | Tag `monopoles-cadrage-v1.0` à poser après relecture, à reporter dans `post.yaml`, l'article et le document de preuve |
| SE-22 (ce qui renverserait chaque nœud) | Clause « ce qui le renverserait » dans le titre de chaque C et I ; question 9 du gabarit |

## Avant / après

| | Avant (`59d021f`) | Après |
|---|---|---|
| Objet de l'étude | monopoles naturels | monopoles naturels ET rentes de position (fixité) |
| Q1 | « substituable ? » — « Non » ×10 | substituable / non duplicable / fixe (+ partiellement) — 2 témoins, 3 « fixe » |
| Q2 | non partageable → « accès nécessairement administré » | non partageable → la concurrence de service ne discipline pas le prix d'accès |
| Objet classé | implicite (énergie pour l'électricité) | dit sur chaque ligne (réseau / site / ressource) |
| Définitions | 14 (5 construites) | 21 (8 construites, `constructed_by` dans le graphe) |
| Rente mesurable | « prix − coût efficace, capital normal » (C-02) | D-15 : base d'actifs au coût historique net des subventions, coût efficace L. 341-2, postes, avant impôts, témoin |
| Taux du capital | H-06 « normal » 5,0 [4 ; 8], borne haute sans source | H-06 « de référence » 5,0 [4,0 ; 8,8] (CRE, ARCEP, ART) + taux sectoriel à enregistrer |
| H-07 | 35 % [30 ; 40] du parc locatif | part du parc OUVERT, qualitative, sans valeur |
| H-08 | 15 % [10 ; 20] « ce que la délégation prélève » | écart BRUT 10 % [0 ; 27], sourcé (O-04, O-05) |
| Hypothèses | 8 | 20 (dont 12 de classement, avec condition de réfutation) |
| Sources | 7 | 16 (dont ART, ARCEP via JORF, Eaufrance, Sénat ×2, IGEDD) |
| Observations | 1 | 9 |
| Valeurs | 4 (V-01 orpheline) | 6 (V-05 destination, V-06 continuité ; toutes référencées) |
| Configurations | 3 | 4 (privé régulé ajouté), destination dite |
| Logement | sortie de la grille, « allocation administrée » puis C-03 | rente de position hors grille ; C-03 fondé sur H-04, V-01, V-02 ; 4 configurations |
| Titre | « Là où le marché n'existe pas » | « Reconnaître une rente de position » |
| Empreintes | recopiées | recalculées au build, échec sur écart |
| Nœuds du post | 48 | 92 ; 18 fichiers servis, le PDF OCDE conservé sans être servi |

## Ce que la revue n'a pas tranché

- L-03 (élasticité des loyers privés à la part du parc ouvert) n'a pas été
  instruite ; c'est le premier travail de sourçage de l'étude sectorielle
  « logement ».
- La promulgation de la loi hydroélectricité (O-09) et l'étude d'origine
  des TRI (O-07) restent à figer (L-12).
- Une nouvelle revue contradictoire est due après la première étude
  sectorielle, sur la mesure D-15 appliquée.
