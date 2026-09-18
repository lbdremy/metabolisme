# Revue contradictoire — R-15..R-17, P-01 (2026-09-18)

Compte rendu de la revue contradictoire exigée par la méthode (INTRO
étape 12), menée le 2026-09-18 sur la proposition institutionnelle de
la session 7 (mécanismes M-A..M-E, résultats R-15..R-17, interprétations
I-15..I-17, proposition P-01, hypothèses H-14..H-18, sources S-39..S-46).
État examiné : commit `0498b4c` (arbre de travail de la session, avant
intégration). Les corrections sont commitées avec ce compte rendu ; les
décisions d'intégration sont dans `decisions-2026-09-18.md` (DEC-14..20)
— prises en autonomie, sans consultation de Rémy.

## Méthode

Quatre relecteurs indépendants (agents distincts, sans accès aux
conclusions des autres), mêmes angles qu'aux revues des 2026-08-07 et
2026-08-09 :

1. **Sources alternatives** — SA-1..SA-15 (15 objections, 8 fichiers
   figés recontrôlés sha256 et citations, 10 sources proposées)
2. **Hypothèses et définitions** — HD-1..HD-18 (18 objections)
3. **Scénarios d'échec** — SE-1..SE-15 (15 objections, 11 scénarios
   d'échec non nommés)
4. **Statistique** — ST-1..ST-13 (13 objections, ~130 valeurs
   recalculées depuis les sources figées par deux scripts indépendants
   du code de la chaîne, `verify-statistique*.py`)

Les quatre rapports bruts sont commités en annexe dans
`evidence/revue-contradictoire-2026-09-18/`. L'orchestrateur a
revérifié AVANT triage les allégations structurantes sur les fichiers
figés : la surface implicite de S-18 (169 200 € / 2 550 €/m² ≈ 66 m²,
p. 11 et p. 27), le tableau par logement de S-40 (p. 24 : 2 652 €), la
phrase de S-22 sur les 6 700 sorties « des 102 000 logements dont les
propriétaires ont été contactés » (p. 24), le produit DMTO 2025 du
pré-rapport OFGL 2026 (p. 47 : 11,9 Md€, champ p. 48), le barème de
remploi du dossier de DUP (p. 1), l'exonération de TFPB du bail à
réhabilitation (S-46, p. 1) et le Livret A à 3 % début 2025 (S-42).
Toutes confirmées.

L'arithmétique publiée a été recalculée indépendamment : **exacte
partout** (~130 valeurs, écart nul). Comme aux deux revues précédentes,
les objections portaient sur les unités, les modèles, les sources et la
mise en récit — pas sur l'exécution.

## Verdict global

- **Survivent** : la grille de comparaison (C-11), le journal des
  décisions, la structure des sensibilités, les MESURES de M-A (au sens
  d'un majorant), l'arithmétique de M-C, et un seul énoncé-titre : « le
  canal incitatif ne peut pas détendre » (I-15).
- **Ne survivaient pas** : trois chiffres-titres et deux énoncés
  porteurs de P-01. (1) « Le neuf s'équilibre au marché » (R-16, I-15,
  P-01) était une erreur d'unité — prix S-18 par logement de ~66 m²
  divisé par la surface des RP (~96 m²) ; le segment rénové avait le
  défaut symétrique (prix par logement vendu ~69 m² / 96 m²). (2) « Au-
  dessus du marché dans les 93 ZE » et la subvention « 2,38 Md€/an »
  dépendaient de la forme proportionnelle des charges (54,9 % d'un
  loyer trois fois plus haut que celui du secteur). (3) « Le repli rend
  l'offre de bail préférable » (I-16, P-01) est l'inverse de ce qu'un
  calcul de valeur actuelle établit. (4) M-D était calibré sur un
  millésime dépassé (2024, alors que 2025 = 11,9 Md€ était publié),
  avec un numérateur (péage fiscal total) qui ne correspondait pas à
  la part basculée, et citait des ZE hors périmètre. (5) P-01
  transcrivait « ≤ 2,4 Md€/an au pire cas » là où l'artefact publiait
  4,12 au coin défavorable.
- **Après intégration** (unités au m², charges fixes par logement,
  remploi, millésime 2025, numérateur départemental, plafonds M-A) :
  M-B s'équilibre PROCHE du marché (14,4 €/m² médian, 1,14 × ; sous le
  marché dans 18 ZE sur 93 et dans 92 à la moindre décote), le neuf en
  dessous du marché dans 61 ZE (11,5 €/m²), la subvention au loyer
  social tombe à 1,56 Md€/an (2,83 au coin défavorable), l'investis-
  sement monte à 61,8 Md€ (remploi + surface C-07 : majorant, L-27) ;
  M-D : 344 €/logement/an, 21 ans d'équivalence (29 en ZE tendues),
  régressive en valeur. La conclusion de la comparaison change de
  forme : l'opérateur qui acquiert produit du logement DISPONIBLE au
  prix du marché, pas du logement social — ce qui est exactement ce
  que le besoin de fluidité de R-07 demande, et pas ce que la version
  initiale de P-01 promettait.

## Objections structurantes et leur disposition

### Grappe A — unités, surfaces, forme fonctionnelle

| # | Objection | Disposition |
|---|---|---|
| A1 | **Surface du neuf** (SE-1, HD-1, ST-1 — majeures, convergentes) : 169 200 € / surface RP ~96 m² au lieu de 66 m² S-18 ; symétrique sur le rénové | **Recalculé** : tout au m² (DEC-15) ; « le neuf s'équilibre au marché » retiré de R-16/I-15/P-01/qmd ; neuf 11,51 €/m² (sous le marché dans 61/93 ZE), rénové 14,40 |
| A2 | **Charges proportionnelles** (HD-2 majeure, SA-13, ST-12) : 54,9 % d'un loyer 3 × plus haut ; S-40 publie 2 652 €/logement | **H-18 refondue** en €/logement (DEC-14), D-23 créée ; le titre « au-dessus du marché partout » tombe (18 ZE sous le marché) |
| A3 | **Remploi omis** (SA-4) : barème 20/15/10 % ≈ + 10 % | **H-20 créée**, S-50 figée (DEC-16) ; + 4 Md€ d'acquisition |
| A4 | **TFPB appliquée au bail** (SA-5, HD-13) ; BAR 30 ans en constante | M-C hors TFPB (2 093 €) ; **H-19 créée** [12 ; 40] |
| A5 | **Médianes simples lues comme « le logement médian »** (ST-5) | Pondérées publiées à côté (ventes, rénovables) ; convention dite (DEC-20) |

### Grappe B — préférence, outil, rythme (P-01)

| # | Objection | Disposition |
|---|---|---|
| B1 | **Le repli est une aubaine, pas une menace** (SE-2, HD-4 — majeures) : VA du bail 28-67 % de la vente | **I-16 inversée**, **C-15 créé**, P-01 réécrite : l'acquisition sécurise, le bail est offert (DEC-18) |
| B2 | **Outil d'utilité publique inexistant ; M-B sans horizon** (SE-3, HD-4) | C-15(1)/(4), L-29 : « sécuriserait, si… » ; rythme 5/10/20 ans publié (6,2 Md€/an sur 10 ans) |
| B3 | **« ≤ 2,4 Md€/an au pire cas » faux** (HD-7, ST-4) : 4,12 au coin défavorable | Corrigé partout ; coins publiés (0,17 / 2,83 après recalcul) |
| B4 | **Fluidité vs attribution** (SE-7) : le besoin R-07 est de la vacance disponible | Subvention au loyer de MARCHÉ publiée (0,31 Md€/an) ; I-15 et P-01 réécrites autour de « logement disponible au prix du marché » |
| B5 | **Stock vs flux** (SE-8, HD-15) : 1,39 an de formation de ménages, ~24 Md€/an | **L-32 créée** (avec SE-6 : succès qui accroît la subvention ; SE-4 : sortie latérale RS) ; nommé dans P-01 |

### Grappe C — la bascule DMTO (M-D)

| # | Objection | Disposition |
|---|---|---|
| C1 | **Millésime 2025 publié** (SA-1 majeure) : 11,9 Md€ | **S-47 figée**, central 2025, 2024 en sensibilité (DEC-17) |
| C2 | **Numérateur ≠ part basculée** (ST-2, HD-5) | Droit départemental seul ; résiduel 2,14 mois (au lieu de 1,02) |
| C3 | **ZE hors périmètre dans les quantiles** (ST-3, SA-11) | 19 ZE exclues (< 50 % du parc dans le périmètre), 6 partielles listées ; S-53 figée pour l'écart France entière |
| C4 | **Uniforme = régressive, capitalisation, ancrage** (SE-9, HD-8) | Charge en % du prix médian publiée (0,11-0,53 %) ; V-02/V-03/I-17 requalifiées ; **S-51 (CPO)** figée : réforme de l'assiette avant bascule |
| C5 | **Durée de détention invoquée sans nœud** (ST-13) | Retirée d'I-17 |

### Grappe D — sources, hypothèses, statuts

| # | Objection | Disposition |
|---|---|---|
| D1 | **H-14 : « 3 % du stock » n'est pas ce que dit S-22** (HD-3, SA-2, SE-10, HD-18) | H-14 réécrite en majorant par contacté, plafond par ZE au besoin (DEC-19) ; **S-52** (TVLH 2027) figée, **L-33** créée |
| D2 | **H-16 : bornes non sourcées, Livret A 3 % hors plage** (SA-3, SE-11, HD-17) | **S-48/S-49** figées ; plage [1,50 ; 3,60] |
| D3 | **Statuts** (HD-9) : R simulés, I contenant des C | « SIMULÉ » en tête de R-15..R-17 ; choix déplacés dans C-15 |
| D4 | **Références de pages, décompte S-39** (SA-8, SA-9) | Six pages corrigées ; « 94 + 3 = 96 » corrigé |
| D5 | **Hypothèses implicites** (HD-14, ST-12, ST-9) | L-30 complétée ; compteurs de ZE sans loyer publiés ; tests ajoutés (monotonies H-16/H-17/H-18/H-20, subventions ≥ 0, sommes, ZE sans référence) |

### Objections écartées, avec raison

Voir DEC-20 : médianes pondérées en central (ST-5), définition
juridique de l'opérateur (HD-10), part résidentielle des DMTO en H-xx
(HD-6), propagation H-08/H-12 dans R-16 (SE-14), communiqué Bercy
(SA-10), bilan du bail (SA-12 — introuvable), calcul supplémentaire sur
le statut d'occupation des mobiles (SE-13).

## Tableau avant/après

| Grandeur / énoncé | Avant (0498b4c) | Après (2026-09-18) |
|---|---|---|
| M-B investissement | 44,6 Md€ (28,8 acquisition) | 61,8 Md€ (46,1 acquisition avec remploi 10 %, surface C-07 — majorant L-27) |
| Coût unitaire rénové vs neuf | 248 k€ vs 169 k€ | 3 776 €/m² vs 2 550 €/m² (363 k€ à 96 m²) |
| Loyer d'équilibre rénové | 18,34 €/m², « au-dessus du marché dans les 93 ZE » (1,44 ×) | 14,40 €/m² (15,73 pondéré), 1,14 × ; sous le marché dans 18/93 ZE ; 2,2 × le social |
| Loyer d'équilibre neuf | 12,47 « ≈ le marché » | 11,51 — sous le marché dans 61/93 ZE |
| Subvention au loyer social | 2,38 Md€/an ; « ≤ 2,4 au pire cas » | 1,56 Md€/an (0,17-2,83 sur les coins), 8 159 €/logement/an ; au loyer de marché 0,31 |
| Annuité | 1,72 Md€/an, 140 €/RP | 2,38 Md€/an, 194 €/RP, 95 Md€ sur 40 ans, 12 256 €/logement porté |
| M-C loyer d'équilibre | 4,22 €/m² (avec TFPB, 30 ans constante) | 3,71 €/m² (hors TFPB, H-19) ; couverture bail seul 7-70 % publiée |
| M-A | 15 500 sorties, 8 % | 15 300 (plafond par ZE), 7,9 % — majorant déclaré |
| M-D charge | 286 €/logement/an (2024) | 344 (2025), 286 en sensibilité |
| M-D années équivalentes | 33 (44 tendues / 30 autres), toutes ZE | 21 (29 / 19), 277 ZE du périmètre ; 27 pondéré ventes |
| M-D péage résiduel | 1,02 mois | 2,14 mois (part communale, frais, CSI, émoluments) |
| P-01 enchaînement | offre → repli « rend l'offre préférable » | acquisition sécurise (outil à créer) ; bail offert (cession domine) ; arbitrage au m² ; M-D voie séparée conditionnée (CPO) |
| Sources / hypothèses / définitions | 46 / 13 / 22 | 53 / 15 / 23 |
| Nœuds du graphe | 141 | 144 (C-15, L-32, L-33) |
