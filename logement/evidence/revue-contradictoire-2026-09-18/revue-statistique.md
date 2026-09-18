# Revue contradictoire — relecteur « STATISTIQUE ET ARITHMÉTIQUE » (session 7, 2026-09-18)

Objet : la proposition institutionnelle — mécanismes M-A..M-D, résultats
R-15..R-17, interprétations I-15..I-17, proposition P-01 ; artefact
`data/processed/scenarios-institutionnels-ze.json` ; code
`src/logement/core/institution.py` + `build_institution` ; tests
`tests/test_institution.py` ; nœuds « Session 7 » de `evidence/claims.yaml` ;
H-14..H-18 ; S-39..S-46 ; `evidence/decisions-2026-09-18.md` ;
section « R-15 à R-17 » du qmd ; `EVIDENCE.md`.

## Méthode

Recalcul **indépendant** de chaque chiffre publié depuis les fichiers figés
(`data/raw/`), sans appeler `core/institution.py` : les entrées amont déjà
revues (tension R-07, cadre de détente R-09, médianes DVF R-14, loyer mix
R-06, niveau de vie S-10) sont relues avec leurs parseurs ; toute
l'arithmétique de la session 7 (annuité, loyers d'équilibre, sommes,
subvention, grilles, charge de détention, péage, années équivalentes,
sensibilités) est refaite en pandas/numpy nu, puis comparée à l'artefact
et aux textes. Les citations des sources S-39/S-40/S-41/S-42/S-46 ont été
vérifiées dans les fichiers figés (`pdftotext -layout`, `grep` sur les
HTML).

Commandes exécutées (depuis `logement/`) :

```bash
uv run python evidence/revue-contradictoire-2026-09-18/verify-statistique.py
#   → sections 0-7 : annuité, ZE nommées, totaux, charge, péage, grilles,
#     sensibilités, cohérences (DVF ≈ 90 s)
uv run python evidence/revue-contradictoire-2026-09-18/verify-statistique-complements.py
#   → ZE de M-D hors périmètre OFGL ; base de surface des loyers (ST-1)
pdftotext -layout data/raw/ofgl-rapport-2025-fiches-departements.pdf - | grep -n "9,9 Md€\|périmètre constant"
pdftotext -layout data/raw/banque-territoires-perspectives-2025-logement-social.pdf - | grep -n "54,9\|43,8"
pdftotext -layout data/raw/dreal-occitanie-fiche-3-1-bail-rehabilitation-2025.pdf - | grep -n "moyenne 30"
grep -o "Livret A + 60 pb\|de 5 à 40 ans" data/raw/banque-territoires-pret-plus-2026.html
grep -o "1,7 % à compter du 1er août 2026" data/raw/banque-territoires-livret-a-2026-08.html
```

Vérifications de sources : S-39 p. 4 « un montant total de 9,9 Md€ » et
champ « périmètre constant entre 2018 et 2024, donc hors Rhône, Martinique,
Guyane, Corse et Paris » (p. 5, graphiques 6) — confirmés ; S-40 p. 15
« 54,9 € … charges d'exploitation et 43,8 € … annuités » — confirmé ;
S-46 « entre 12 et 99 ans, en moyenne 30 ans » — confirmé ; S-41 « Livret
A + 60 pb », « Bâti : de 5 à 40 ans » — confirmé ; S-42 « 1,7 % à compter
du 1er août 2026 » — confirmé.

**Résultat d'ensemble du recalcul** : les ≈ 130 valeurs comparées de
l'artefact (facteurs d'annuité, 12 loyers de ZE nommées, 15 agrégats M-B,
20 quantiles, 18 cases de la grille M-A, 12 cases de la grille M-C, 70
valeurs de sensibilité, 10 valeurs M-D, charge et parc) sont reproduites
**à l'unité / au centime près**. Une seule divergence de valeur (ratio
équilibre/social 2,81 vs 2,85, ST-8) tient à un dénominateur différent,
pas à une erreur de calcul. Les objections qui suivent portent donc sur
la **construction** de trois chiffres-titres (base de surface, numérateur
du péage, périmètre), sur des **transcriptions** (P-01) et sur le
**statut** des médianes — pas sur l'exécution du code.

---

## Objections

### ST-1 — MAJEURE — Le loyer d'équilibre en €/m² divise le prix d'UN logement par la surface d'un AUTRE

**Énoncé.** Dans `operator_frame`, le coût unitaire du segment rénové est
`prix_median` (prix du logement **médian vendu** dans la ZE, DVF) + coût
de rénovation C-07 ; le loyer d'équilibre est ensuite ramené au m² en
divisant par la surface **moyenne des résidences principales** de la ZE
(mix C-07 : 114,3 / 65,5 m² selon la part maison). Or le logement médian
vendu n'a pas cette surface : `prix_median / prix_m2_median` (les deux
colonnes sont dans le même frame `prices_by_ze`) donne la surface
implicite des biens vendus.

**Preuve (recalcul).**

| ZE | prix médian | prix/m² médian | surface implicite | surface C-07 | loyer publié | loyer à surface implicite |
|---|---|---|---|---|---|---|
| Annecy | 311 317 € | 4 872 €/m² | 64 m² | 84,7 m² | 29,32 | 38,86 |
| Bayonne | 293 513 € | 4 850 €/m² | 61 m² | 88,1 m² | 26,97 | 39,27 |
| Digne-les-Bains | 104 755 € | 2 224 €/m² | 47 m² | 97,0 m² | 11,19 | 23,05 |

Sur les 96 ZE : ratio surface implicite / surface C-07 médian **0,71**
(min 0,41, max 0,86) ; médiane des surfaces C-07 96,6 m², des surfaces
implicites 69,1 m². Conséquences au central :

| grandeur | publié (surface C-07) | surface implicite DVF | tout-par-m² (prix/m² + coût/m²) |
|---|---|---|---|
| loyer rénové médian | 18,34 €/m² | 26,27 | 24,74 |
| ratio rénové / marché médian | 1,44 | 2,07 | 1,95 |
| loyer NEUF médian (169 200 € S-18) | 12,47 €/m² | 17,42 | 18,38 à 65,5 m² ; 17,20 à 70 m² |
| ZE où le neuf ≤ marché | 44 / 93 | 6 / 93 | 4 / 93 (65,5 m²) |
| subvention d'équilibre au social | 2,38 Md€/an | 2,83 | — |

La surface intervient deux fois : au numérateur (dans `cu`, cohérent avec
C-07) et au dénominateur ; mais le **prix d'acquisition** et le **prix de
revient du neuf** sont des prix par logement dont la surface n'est ni celle
de C-07 ni connue (S-18 ne publie pas de surface ; la fiche ne cite que
« 169 200 € par logement »). Le mélange sous-estime tous les loyers
d'équilibre d'environ 30 % et, surtout, fabrique l'égalité « neuf 12,47 ≈
marché 12,29 » qui porte R-16 (« le segment NEUF s'équilibre à 12,47 €/m²
≈ le marché »), I-15 (« le segment neuf sur friches s'équilibre au loyer
de marché sans subvention d'investissement ») et l'étage 3 de P-01. À
toute surface plausible d'un logement social neuf (65-70 m²), le neuf
s'équilibre **au-dessus** du marché médian dans ~90 % des ZE.

Le sens général de R-16 (« au-dessus du marché partout, 2,8 × le social »)
est **renforcé**, pas renversé ; mais le chiffre 18,34, le ratio 1,44 et
la conclusion sur le neuf sont des artefacts de construction.

**Disposition proposée.** (a) Segment rénové : calculer tout par m² —
`loyer = (prix_m2_median × H-15 + coût_rénovation_m2) × facteur / (1 − H-18) / 12`,
sans surface (le frame DVF fournit déjà `prix_m2_median`) ; la subvention
par logement exige alors une surface **du vacant durable**, à poser en
hypothèse H-xx (plage : surface implicite DVF ↔ surface C-07 ; L-18 dit
que les vacants sont plus petits que la médiane vendue). (b) Segment
neuf : une surface de logement social neuf sourcée (RPLS S-28 publie
peut-être la surface moyenne ; sinon H-xx explicite avec plage 60-75 m²)
et une sensibilité publiée. (c) Requalifier R-16/I-15/P-01 : « le neuf
s'équilibre au marché » devient conditionnel à la surface retenue, et
la comparaison pertinente V-04 est au loyer social, où le neuf exige
0,41 Md€/an au central (déjà dans l'artefact, `dont_neuf_mdeur_an`).
(d) Ajouter la limite L-xx « base de surface » à L-30.

### ST-2 — SÉRIEUSE — Les « années équivalentes » et le « péage résiduel » de M-D contredisent L-28 (2)

**Énoncé.** L-28 (2) : « seule la part départementale est basculée (la taxe
communale 1,20 % et les frais d'assiette restent) ». Mais
`toll_shift_scenario` divise le péage fiscal **total** (droits territorialisés
= départemental × 1,0237 + communal 1,20 % ; + CSI) par une charge qui ne
remplace que le produit **départemental** (9,9 Md€), et définit le
« résiduel » comme les émoluments seuls — comme si tout le péage fiscal
disparaissait. Deux lectures sont possibles, l'artefact prend le
numérateur de l'une et le dénominateur de l'autre.

**Preuve (recalcul, 296 ZE).** Part départementale dans le péage fiscal :
médiane 0,779.

| grandeur | publié (péage total / charge départementale) | cohérent avec L-28 (2) : droits départementaux / charge |
|---|---|---|
| années équivalentes, médiane | 32,9 (p25 26,2 ; p75 41,7 ; max 72,6) | **25,6** (20,4 ; 32,5 ; max 56,5) |
| ZE tendues | 44,3 | **34,5** |
| autres | 29,7 | **23,1** |
| péage résiduel après bascule, mois de niveau de vie | 1,02 (émoluments seuls) | **2,17** (communal + frais d'assiette + CSI + émoluments) |

Les chiffres-titres de R-17 (« 33 ans, 44 en zones tendues », « 5,15 →
1,02 mois »), repris dans I-17, P-01, EVIDENCE.md et la lecture du qmd,
sont surestimés de ~30 % (années) et le résiduel sous-estimé de ×2.

**Disposition.** Choisir : soit la bascule porte sur la seule part
départementale (alors numérateur = `prix × (taux − 1,20)/1,0237 / 100`,
résiduel = péage total − droits départementaux + émoluments : 25,6 ans /
34,5 / 23,1 ; 2,17 mois), soit elle porte sur tout le péage fiscal (alors
la charge doit remplacer aussi la taxe communale et les frais d'assiette,
qu'aucune source figée ne chiffre — L-28 à étendre). Corriger C-14, R-17,
I-17, P-01, EVIDENCE.md, qmd en conséquence.

### ST-3 — SÉRIEUSE — 22 des 296 ZE de M-D sont hors du périmètre de la charge, dont les deux exemples-titres

**Énoncé.** La charge de 286 € est calibrée « hors 75, 69, 2A, 2B, 972,
973 » (C-14, DEC-11) et L-28 (1) dit qu'elle « ne vaut pas pour ces
territoires ». Pourtant le frame M-D garde les 296 ZE, calcule leurs
années équivalentes avec cette charge, les inclut dans les quantiles et
en fait ses exemples.

**Preuve (recalcul sur le recensement S-11 × appartenance ZE2020).**
16 ZE **entièrement** hors périmètre : Ajaccio, Bastia, Calvi, Corte,
Ghisonaccia, **Porto-Vecchio**, Propriano (Corse) ; les six ZE de
Martinique ; Est-littoral, Ouest-Guyanais, Savanes (Guyane). 6 ZE
**partiellement** : Paris (39 % du parc en 75 — mais la quasi-totalité
des ventes DVF de la ZE), Lyon (92 %), Tarare (87 %), Villefranche-sur-
Saône (64 %), Saint-Étienne (3 %), Vienne-Annonay (3 %). Le maximum
publié (Porto-Vecchio 72,6 ans) et le deuxième exemple de R-17 (Paris
72,2) sont tous deux hors périmètre. Corte (11,77 €/m²) est aussi le
« ratio/marché minimal » de M-B — hors sujet pour ST-3 mais même
géographie. Note : la vérification demandée sur « 69 » est positive —
les 266 communes 69xxx du recensement couvrent le Rhône ET la métropole
de Lyon (Lyon 69123 et Villeurbanne 69266 présents), conformément au
champ OFGL qui neutralise la création de la métropole (p. 1 et p. 5 de
la fiche).

**Disposition.** Ajouter un drapeau `hors_perimetre` par ZE (entier /
partiel avec la part du parc), publier les quantiles sur les 274 ZE du
périmètre (ou les deux), remplacer les exemples par des ZE du périmètre
(Annecy 69,8 ; Le Genevois Français 67,2 ; La Teste-de-Buch 66,1) et
retirer Paris/Porto-Vecchio de la phrase de R-17.

### ST-4 — SÉRIEUSE — P-01 transcrit le central de la subvention comme « pire cas », et « ≈ 0 » là où l'artefact dit 0,41 Md€/an

**Énoncé et preuve.** P-01 : « subvention d'équilibre au loyer social
≤ 2,4 Md€/an au pire cas tout-acquisition (R-16), ≈ 0 si le bail domine
et le neuf prend le déficit ». Or 2,38 est la valeur **centrale**
(H-15..H-18 aux centraux). Sur la plage plausible, l'artefact publie :
coin défavorable **4,12 Md€/an**, durée 30 ans seule 3,17, charges 0,60
seules 2,86, taux 2,81 seul 2,72. « ≤ 2,4 au pire cas » est donc faux
d'un facteur 1,7. Et si « le neuf prend le déficit » avec attribution au
loyer social (V-04, dans la même phrase de P-01), le segment neuf exige
`dont_neuf_mdeur_an` = **0,41 Md€/an** au central (12,47 > 6,43 partout) —
et davantage sous ST-1 ; « ≈ 0 » n'est vrai que pour le segment bail
(M-C : 4,22 < social dans les 94 ZE).

**Disposition.** « 2,4 Md€/an au central du tout-acquisition, jusqu'à
4,1 sur la plage H-15..H-18 ; ≈ 0,4 Md€/an si le bail domine (le neuf
au loyer social) ». Même correction dans EVIDENCE.md (« ≤ 2,4 Md€/an au
pire cas »).

### ST-5 — SÉRIEUSE — Des médianes de ZE (une ZE = un poids) sont lues comme des médianes de logements

**Énoncé.** Tous les quantiles publiés (`_quantiles`) sont des médianes
**simples** sur les ZE. R-17 écrit « le péage fiscal … sur le logement
médian vaut 9 419 € en médiane » ; R-16 « loyer d'équilibre du segment
rénové 18,34 €/m²/mois en médiane » ; I-17 « point d'équivalence (33 ans,
44 en zones tendues) ». Un lecteur y lit la situation du logement ou du
ménage médian, alors que Guéret et Paris pèsent chacun 1.

**Preuve (recalcul).**

| grandeur | médiane simple (publiée) | médiane pondérée | pondération |
|---|---|---|---|
| M-D péage fiscal | 9 419 € | **12 067 €** | ventes DVF de la ZE |
| M-D années équivalentes | 32,9 | **39,8** / **42,1** | parc de logements / ventes |
| M-B loyer rénové | 18,34 €/m² | **20,16** (moyenne pondérée 19,89) | rénovables |
| M-B ratio rénové / marché | 1,44 | 1,43 | rénovables |
| M-C loyer travaux | 4,22 | 4,05 | rénovables |

Les grandeurs de niveau (péage, années) sont sous-estimées de 25-30 % en
médiane simple parce que les ZE chères sont les plus peuplées ; les
ratios sont robustes. C'est la convention de R-14 (`mediane_mois` par
ZE), donc cohérent dans la chaîne — mais R-14 le disait explicitement
(« n_ze », « distribution ») alors que R-17 dit « le logement médian ».

**Disposition.** Écrire la convention dans R-16/R-17 (« médiane des ZE,
une ZE = un poids ») et publier en regard la médiane pondérée (ventes
pour M-D, rénovables pour M-B) — un ajout de quatre lignes dans
`_quantiles`. Pour I-17, préférer la pondérée (le « point d'équivalence »
concerne des ménages, pas des ZE).

### ST-6 — MINEURE — Millésimes mêlés dans M-D : produit 2024 à 4,50 %, péage 2025 à 5,00 %

**Énoncé et preuve.** La charge (286 €) divise un produit **2024** perçu
au taux départemental 4,50 % (S-39 : « taux plafond … 4,5 % avant de
passer à 5 % en 2025 ») ; le péage par ZE applique les taux **2025**
(5,00 % dans la grande majorité des départements — 13 exceptions à 4,50 ou 3,80 %, S-31) à des prix 2025. Au taux 2025, le
même produit vaudrait ≈ 9,9 × 5/4,5 = 11,0 Md€ et la charge **318 €**
(+11 %). Cumulé avec ST-2 (numérateur départemental), la médiane des
années équivalentes descend vers **~23 ans**. L-28 (1) mentionne le
« point bas du cycle » mais pas le changement de taux.

**Disposition.** Le dire dans L-28 avec le sens de l'écart, ou calibrer
la charge au taux 2025 (choix C-14 amendé) — sans nouvelle source, c'est
une hypothèse, à déclarer comme telle.

### ST-7 — MINEURE — L-27 affirme « jamais des totaux » ; Colmar sort bien des totaux de M-B

**Preuve.** La ZE tendue sans prix DVF est **4405 Colmar** (Haut-Rhin,
Livre foncier — hors champ DVF avec 57/67/68 et 976 ; les 10 ZE absentes
de M-D sont toutes en Alsace-Moselle) : rénovables 191, déficit 0.
`operator_frame` joint `prix_median` en `inner` : 136 544 − 191 = 136 353
(M-B) ; les 191 logements (≈ 0,05 Md€ au coût unitaire médian, 0,1 %
des 44,6) sont absents de l'investissement, de l'annuité et de la
subvention de M-B, présents dans M-C (97 ZE, 136 544) et R-09. L'écart
96/97 et 93/94 s'explique ainsi (les 3 ZE sans loyer de marché sont
Est Grande Terre, Est-littoral, Ouest-Guyanais — elles ont un loyer
social, cf. ST-9). Rien d'autre à signaler : 136 353 + 57 945 ≠ 194 488
est donc attendu, mais aucun texte ne le dit.

**Disposition.** Réécrire L-27 (« … sortent des comparaisons de loyers
ET des totaux de M-B, pour 191 logements ») ; publier
`n_ze_hors_dvf` / `renovables_hors_dvf` dans le payload (règle
INTRO §21-9 : flagué, pas silencieux).

### ST-8 — MINEURE — « 2,81 × le social » est calculé sur 96 ZE, « 1,44 » et « dans les 93 ZE » sur 93

**Preuve.** `ratio_equilibre_renove_sur_social` est quantilé sur le frame
entier (96 ZE, dont les 3 ZE d'outre-mer sans loyer de marché) : 2,81 ;
sur les 93 ZE « avec les deux loyers » de la même phrase de R-16 : **2,85**.
**Disposition.** Même dénominateur dans la phrase (2,85 sur 93, ou dire
« sur 96 »).

### ST-9 — MINEURE — Le cas limite `fillna(0)` de la subvention est vide aujourd'hui, mais silencieux et non testé

**Preuve.** Comptage : **0** ZE de M-B sans loyer social (les 306 ZE ont
un loyer RPLS) ; les 3 ZE sans loyers sont sans loyer de **marché**. La
sous-estimation actuelle est donc de **0 €**. Mais `subvention_eur_an =
fillna(0)` traiterait une ZE à rénovables > 0 sans loyer social comme
« subvention nulle » sans trace dans le payload ni test. Même chose en
M-D : **8 ZE** sans niveau de vie (mois = NaN, exclues des quantiles sans
compteur, alors que R-14 publie `n_ze_avec_niveau_vie`).
**Disposition.** Publier `n_ze_subvention_inconnue` et
`n_ze_sans_niveau_vie` ; test unitaire : une ZE sans loyer social avec
rénovables > 0 → compteur = 1 et subvention nationale marquée partielle.

### ST-10 — MINEURE — Couverture des tests : bonne sur l'annuité, lacunaire sur les invariants des scénarios

Couvert (utile) : bornes et monotonie du facteur d'annuité (propriété,
200 exemples), rejets (durée ≤ 0, taux < 0, charges ≥ 1), pondération
RPLS NA-safe, linéarité/plafond M-A (le plafond `min(1, …)` n'est
atteint par aucun cas : 2,5 % × 20 = 50 %), prix des deux segments,
monotonie en H-15 (propriété), sommes = total, ordre des coins, grille
de consentement croissante et = 1 à 100 %, rupture M-D. Le test de
régression `test_committed_institution_artifact_matches_rebuild`
protège l'artefact entier.

Manquant (INTRO §6.7) : (i) loyer d'équilibre décroissant en H-17 et
croissant en H-16/H-18 (propriété, même patron que le test H-15) ;
(ii) `subvention ≥ 0` et `= 0` quand équilibre ≤ social (propriété) ;
(iii) `dont_acquisition + dont_renovation + dont_neuf` et
`dont_renove + dont_neuf` (subvention) ≈ totaux arrondis ; (iv) le cas
ST-9 ; (v) M-D : années équivalentes croissantes dans le prix, et
`n_ze_tendues + autres = n_ze` ; (vi) M-C : `couverture ≤ 1` et
`≥ déficit/besoin` à consentement 0 (le neuf seul) ; (vii) un cas M-A où
le plafond 100 % mord (ex. 2,5 % × 50 ans) ; (viii) `equilibrium_rent`
n'est testé qu'à la borne 1,0, pas à 0 (loyer = annuité).

### ST-11 — MINEURE — « couverture 0,37 à 10 % de consentement » : 81 % de ce 0,37 est le neuf, pas le bail

**Preuve.** Couverture = (136 544 × 10 % + 57 945) / 194 488 = 0,37 ;
le déficit au neuf seul fait 57 945 / 194 488 = 0,30 ; le bail à 10 %
apporte 0,07. R-16 écrit honnêtement « (le neuf compris) », mais I-16
(« le bail … couverture bornée par l'inconnue comportementale ») et
P-01 se lisent comme si la grille mesurait le bail. **Disposition.**
Publier `couverture_bail_seul` (0,07 / 0,18 / 0,35 / 0,70) à côté.

### ST-12 — MINEURE — Loyer d'équilibre = annuité / (1 − 0,549) ≠ structure S-40 (annuités = 43,8 %)

**Preuve.** S-40 p. 15 : pour 100 € de loyers nets, charges 54,9,
annuités 43,8, autofinancement 1,5 (+ autres produits 2,4, risques
− 2,2). Diviser par 0,451 au lieu de 0,438 sous-estime le loyer de
3,0 % (médiane 18,88 au lieu de 18,34). Sens défavorable à l'opérateur,
à ajouter à L-30 (qui ne liste que des majorants).

### ST-13 — MINEURE — I-17 compare 33 ans à « la durée de détention médiane du ménage mobile » sans chiffre ni nœud

Aucun R-xx / S-xx de la chaîne ne donne cette durée ; la phrase porte un
ordre de grandeur implicite (INTRO §15 : « une affirmation quantitative
importante ne peut être publiée que si elle possède une source ou un
calcul identifié »). Sourcer (mobilité résidentielle R-11/R-12 : durée
d'occupation ?) ou retirer.

---

## Tableau des chiffres-titres

Convention : « recalculé » = mon calcul indépendant à la même
construction ; la colonne « verdict » distingue la reproduction (exacte)
de la validité de la construction (renvoi ST-n).

| Chiffre (où) | Publié | Recalculé | Écart | Verdict |
|---|---|---|---|---|
| Facteur d'annuité 2,30 %/40 ans (R-16) | 0,03851 | 0,038512 | 0 | exact |
| Facteur d'annuité 2,30 %/30 ans (M-C) | 0,04651 | 0,046514 | 0 | exact |
| Annecy loyer rénové (R-16 liste) | 29,32 €/m² | 29,32 | 0 | exact ; 38,86 à surface cohérente (ST-1) |
| Bayonne loyer rénové | 26,97 | 26,97 | 0 | exact ; 39,27 (ST-1) |
| Digne-les-Bains loyer rénové | 11,19 | 11,19 | 0 | exact ; 23,05 (ST-1) |
| Investissement M-B (R-16) | 44,6 = 28,8 + 6,0 + 9,8 Md€ | 44,608 = 28,831 + 5,973 + 9,804 | 0 | exact ; hors Colmar (ST-7) |
| Coût unitaire médian rénové | 248 038 € | 248 038 | 0 | exact |
| Annuité M-B | 1,72 Md€/an | 1,72 | 0 | exact |
| Annuité / RP des ZE tendues | 140 € (12 302 355 RP) | 140 (12 302 355) | 0 | exact |
| Loyer rénové médian (R-16) | 18,34 (11,19-29,32) | 18,34 (11,19-29,32) | 0 | exact ; 26,27 à surface cohérente (ST-1) ; 20,16 pondéré (ST-5) |
| Loyer neuf médian | 12,47 ≈ marché 12,29 | 12,47 | 0 | exact ; 17,4-18,4 à surface cohérente : **au-dessus du marché** (ST-1) |
| Loyer de marché / social médians (O-40) | 12,29 / 6,43 | 12,29 / 6,43 | 0 | exact |
| Ratio rénové/marché, /social | 1,44 ; 2,81 | 1,44 ; 2,85 (93 ZE) / 2,81 (96) | 0 / +0,04 | exact ; dénominateurs mêlés (ST-8) |
| ZE rénové ≤ marché | 0 / 93 | 0 / 93 (min ratio 1,004 Corte) | 0 | exact |
| Subvention d'équilibre | 2,38 = 1,97 + 0,41 Md€/an | 2,38 = 1,97 + 0,41 | 0 | exact ; 2,83 (ST-1) ; « pire cas » = 4,12 (ST-4) |
| Sensibilité H-15 0,5 | 30,2 Md€ ; 10,88 ; 77 ZE | 30,2 ; 10,88 ; 77 | 0 | exact |
| H-16 1,50 / H-17 50 / H-18 0,40 | 15,92 / 16,13 / 13,79 | 15,92 / 16,13 / 13,79 | 0 | exact |
| Coins favorable / défavorable | 6,07 (0,07 Md€) / 26,73 (4,12) | 6,07 (0,07) / 26,73 (4,12) | 0 | exact |
| M-C loyer travaux médian | 4,22 (3,46-4,58), 94/94 sous social | 4,22 (3,46-4,58), 94/94 | 0 | exact |
| M-C grille 10 / 50 / 100 % | 0,37 / 0,65 / 1,0 | 0,37 / 0,65 / 1,00 | 0 | exact ; bail seul 0,07 / 0,35 / 0,70 (ST-11) |
| M-C travaux + neuf | 6,0 + 9,8 = 15,8 Md€ | 5,973 + 9,804 = 15,8 | 0 | exact |
| M-A gisement / besoin | 206 664 / 194 488 | 206 664 / 194 488 | 0 | exact |
| M-A 15 500 sorties = 7,5 % ; couverture 0,08 | 15 500 ; 0,08 | 15 499,8 ; 0,0797 | 0 | exact |
| M-A 4 % / 16 % / 27 % / 3 % (R-15) | 0,04 / 0,159 / 0,266 / 0,027 | idem | 0 | exact |
| Parc du périmètre (C-14) | 34 565 110 | 34 565 110 (37 527 880 − 2 962 770) | 0 | exact ; codes exclus vérifiés, 69 = Rhône + métropole |
| Charge de détention | 286 €/log/an | 286,42 | 0 | exact ; 318 au taux 2025 (ST-6) |
| Péage fiscal médian (R-17) | 9 419 € (4 140-20 780) | 9 419 (4 140-20 780) | 0 | exact ; 12 067 pondéré ventes (ST-5) |
| Péage en mois / résiduel | 5,15 / 1,02 | 5,15 / 1,02 | 0 | exact ; résiduel cohérent avec L-28 = 2,17 (ST-2) |
| Années équivalentes | 33 (26-42) ; 44 tendues ; 30 autres | 32,9 (26,2-41,7) ; 44,3 ; 29,7 | 0 | exact ; **25,6 / 34,5 / 23,1** au numérateur départemental (ST-2) ; ~23 avec ST-6 |
| Exemples R-17 | Porto-Vecchio 72,6 ; Paris 72,2 ; Annecy 69,8 ; Montluçon 14,5 ; Sarrebourg 14,6 | idem | 0 | exact ; Porto-Vecchio et Paris hors périmètre (ST-3) |
| n_ze : 97 / 96 / 93 / 94 / 296 / 96 | — | 97 tendues ; 96 avec DVF (− Colmar) ; 93 = 96 − 3 DOM sans marché ; 94 = 97 − 3 ; 296 = 306 − 10 Alsace-Moselle ; 96 tendues dans M-D | 0 | cohérent, à expliciter (ST-7) |
| P-01 « ≤ 2,4 Md€/an au pire cas » / « ≈ 0 » | 2,4 / ≈ 0 | central 2,38 ; pire cas plage 4,12 ; neuf au social 0,41 | — | **transcription erronée** (ST-4) |

---

## Verdict global

1. **Exécution** : l'artefact est reproduit chiffre pour chiffre depuis
   les sources figées (130 valeurs, écart nul) ; le code fait ce que
   T-17 décrit, les sommes bouclent, les sensibilités sont monotones.
2. **Construction** : trois chiffres-titres ne survivent pas à un contrôle
   d'unités et de périmètre — le loyer d'équilibre au m² mêle deux
   surfaces (ST-1 : le neuf ne s'équilibre pas au marché, ~17-18 €/m²),
   les années équivalentes divisent un péage total par une charge
   départementale (ST-2 : 26 ans, pas 33 ; 34, pas 44 en zones tendues ;
   résiduel 2,2 mois, pas 1,0), et 22 ZE hors périmètre dont les deux
   exemples-titres (ST-3).
3. **Publication** : R-16/R-17/I-15/I-17/P-01 et EVIDENCE.md doivent
   être recalculés ou requalifiés sur ces trois points, et P-01 corrigé
   pour son « pire cas » (4,1 Md€/an, pas 2,4) et son « ≈ 0 » (0,4) ; le
   reste (ST-5..ST-13) est de la précision d'énoncé et de la couverture
   de tests, sans effet sur les conclusions qualitatives — qui, pour
   R-16, sortent renforcées (l'acquisition est encore plus chère que
   publié).
