# EVIDENCE — index de la chaîne de preuves

Index humain des éléments de preuve de l'étude, par statut épistémique
(méthode Métabolisme, INTRO §4). Les registres machine font foi :
`sources/sources.yaml`, `sources/definitions.yaml`, `sources/hypotheses.yaml`,
puis `evidence/claims.yaml` pour le graphe de dépendances.

| Code | Statut | Registre / emplacement | État |
|------|--------|------------------------|------|
| S | Sources | `sources/sources.yaml` | 32 sources (INSEE, LOVAC, ANIL, SDES, MTE, DGFiP, DILA, DREAL, ADEME, Cerema, Enertech, Banque des Territoires, Légifrance, Cour des comptes, Apur ; 36 fichiers figés sha256/LFS + 2 collections vivantes) |
| D | Définitions | `sources/definitions.yaml` | 18 définitions citées verbatim, datées, avec limites |
| H | Hypothèses | `sources/hypotheses.yaml` | H-06 seuil de vacance structurelle · H-07 surface de relocation (RECENTRÉE 2026-08-07 : emménagés récents) · H-08 seuil de fluidité · H-09/H-10 coûts de rénovation performante · H-11 densité de référence haussmannienne (dérivée S-11×S-21, contrôlée par la chaîne) · H-12 taux d'existence du gisement LOVAC (créée 2026-08-07, revue contradictoire) · H-13 taux de droits de mutation (créée 2026-08-08, S-31) |
| O/T/R | Observations, transformations, résultats | `evidence/claims.yaml` | O-01..O-36, T-01..T-16, R-01..R-14 (sorties dans `data/processed/`) |
| I/V/C/L | Interprétations, valeurs, choix, limites | `evidence/claims.yaml` | I-01..I-14, V-01, C-01..C-10, L-01..L-26 (L-16..L-21 et corrections L-04/L-07/L-09/L-11..L-15 : revue du 2026-08-07 ; L-26 et requalifications I-11..I-14, L-22..L-25 : revue du 2026-08-09, comptes rendus `evidence/revue-contradictoire-*.md`) |
| M/P | Mesures, propositions | — | à venir |

Sources enregistrées :

- **S-01** — INSEE, Parc de logements au 1ᵉʳ janvier 2025 (Insee Focus n° 359,
  données des figures — EAPL, séries nationales 1982-2025).
- **S-02** — INSEE, Répartition du parc selon la catégorie de logement et le
  type d'habitat (chiffres détaillés EAPL, 1982-2025).
- **S-03** — INSEE, Ménages en séries longues (SL_MEN1, recensement,
  millésimes 1962-2022).
- **S-04** — INSEE, Définitions (métadonnées statistiques, collection en
  ligne — chaque définition citée verbatim et datée dans le registre).
- **S-06** — INSEE, table d'appartenance géographique des communes 2026
  (communes → ZE 2020, même COG que LOVAC).
- **S-07** — INSEE, emploi par zone d'emploi 1998-2018 (dernier millésime
  publié à la maille ZE).
- **S-05** — Ministère de la Transition écologique (DGALN/Cerema), LOVAC open
  data — logements vacants du parc privé par territoire et durée, millésimes
  2020-2026 (4 fichiers figés ; ruptures méthodologiques 2023 et 2025
  documentées ; parc privé uniquement, secrétisation < 11).
- **S-08** — Légifrance (DILA), textes consolidés (collection en ligne —
  définitions légales D-12/D-13).
- **S-09** — ANIL/DHUP, carte des loyers 2025 — loyers d'annonce prédits
  par commune, fichiers appartement ET maison (licence du millésime à
  confirmer avant publication, L-09).
- **S-10** — INSEE, Filosofi 2021 — niveau de vie médian (€/UC/an),
  personnes et unités de consommation par territoire (dont ZE 2020).
- **S-11** — INSEE, recensement 2022 — chiffres clés logement par commune
  (catégories, maisons/appartements, millésimes 2011/2016/2022).
- **S-12** — SDES, enquête nationale Logement 2020 (Datalab essentiel
  n° 296) — surfaces habitables moyennes, dont 51,2 m²/personne (source de
  H-07 ; premiers résultats provisoires, champ métropole).
- **S-13** — MTE (Observatoire habitat), zonage TLV par commune (décret
  n° 2025-1267 du 22/12/2025 + millésimes 2013/2023 ; base de D-14).
- **S-14** — DREAL Pays de la Loire (2020), Lutter contre la vacance des
  logements — bande de vacance optimale 6-7 % (source de H-08/D-15).
- **S-15** — Observatoire de l'habitat CUA d'Alençon (2025), La vacance —
  borne basse du seuil de fluidité (« en-deçà de 5 %, le marché cesse
  d'être fluide »).
- **S-16** — ADEME, DPE logements existants depuis 07/2021 — extrait
  agrégé commune × étiquette (14,8 M de DPE couverts, acquisition
  scriptée `logement acquire-dpe` ; biais d'échantillon documenté).
- **S-17** — Enertech pour l'ADEME (2016), Analyse des coûts de la
  rénovation énergétique — coûts €HT/m² d'une rénovation performante
  (base de H-09/H-10).
- **S-18** — Banque des Territoires (Éclairages n°33, 2024), prix de
  revient des logements sociaux — 169 200 €/logement neuf en 2023
  (comparateur de R-09).
- **S-19** — INSEE (BDM 011779962), indice IPEA résidentiel — facteur
  d'actualisation 2016→2023 des coûts de travaux (×1,267).
- **S-20** — Cerema, Cartofriches (export 15/06/2026) — 36 241 friches
  inventoriées (inventaire PARTIEL : les totaux sont des planchers).
- **S-21** — INSEE, base du comparateur de territoires — superficies des
  arrondissements municipaux (dénominateur de H-11).
- **S-22** — Cour des comptes (mai 2025), La lutte contre les logements
  vacants dans le parc privé — source pivot de la revue contradictoire :
  ~25 % de faux vacants LOVAC (base de H-12), 118 330 vacants > 2 ans en
  communes TLV (2022), DHUP 74 % du durable en marchés détendus,
  campagne GMBI 2023 chaotique (L-04), bilan des instruments incitatifs
  « non démontré » (ZLV ~3 % de sorties en zone tendue en 4 ans).
- **S-23** — SDES Datalab (déc. 2023), déterminants de la vacance longue
  durée — écologie de la vacance logement par logement : ×2,8 si < 35 m²,
  ×3,3 si avant 1900, ~45 % obsolescence, ~20 % successions (fonde L-18,
  conforte I-08).
- **S-24** — Apur (déc. 2023), logements inoccupés à Paris — contrôle
  externe du volume parisien : ~18 600 vacants > 2 ans du parc privé
  (1,3 %) contre 32 091 au millésime LOVAC 26 (écart à instruire, L-04).
- **S-25** — Cerema (23/11/2023), coût des friches (lauréats du fonds
  friches, échantillon déficitaire) — remise en état moyenne 780 k€
  HT/ha, projets résidentiels 2,5 × plus chers, 80 % pollués, lauréats
  majoritairement en zone détendue (L-14/L-15).
- **S-26** — Cerema (déc. 2023), article de bilan du fonds friches —
  1 382 projets, 3 375 ha recyclés, ~6,7 M m² de logements attendus :
  dénominateur de la densité constatée ~1 985 m² SP/ha (O-24, plancher
  opérationnel de R-10).
- **S-27** — INSEE, RP « Logement en 2023 » (jeu Melodi
  DS_RP_LOGEMENT_PRINC, Parquet figé) — résidences principales par
  ancienneté d'emménagement (L_STAY, 6 classes) à la maille ZE2020,
  millésimes 2012/2017/2023 comparables par construction (concepts
  européens 2023, COG 2026 — base de R-11).
- **S-28** — SDES, RPLS au 01/01/2025 — parc locatif social par commune
  (16 863), séries annuelles 2013-2025 du taux de mobilité (D-17), de
  la vacance et des loyers ; parc 5,4 M de logements ; Licence Ouverte
  (mentions légales du site SDES, constat 2026-08-09) — base de R-12.
- **S-29** — INSEE, fichier détail MIGCOM RP2022 (Parquet 17,36 M obs.
  + dictionnaire varmod figés) — résidence actuelle × résidence un an
  auparavant, statut d'occupation, pondération IPONDI — base de R-13.
- **S-30** — DGFiP/Etalab, DVF géolocalisées 2025 (année complète,
  3,7 M de lignes) — prix de vente des logements ; hors Alsace-Moselle
  et Mayotte — base de R-14 (assiette C-10).
- **S-31** — DGFiP (impots.gouv, espace notaires), taux des droits
  d'enregistrement par département au 01/02/2026 — base de H-13.
- **S-32** — Service-Public/DILA, fiche F17701 — barème des émoluments
  proportionnels du notaire (contrôlé par test sur l'exemple chiffré de
  la fiche).
- **S-33** — INSEE, Insee Première n° 2073 (30/09/2025) + données des
  figures — mobilité résidentielle 2013-2023 (10,8 → 8,8 %) ; le
  vieillissement explique 14 % de la baisse — borne externe de L-22
  (revue du 2026-08-09).
- **S-34** — ANCOLS, communiqué du 09/02/2026 — le vieillissement des
  attributaires explique 9 % de la baisse de la mobilité du parc
  social — borne externe de L-23 (revue du 2026-08-09).
- **S-35** — DGFiP, table DMTO au 01/06/2026 — trace de fraîcheur de
  S-31 (l'Eure passée à 5,00 %, les Hautes-Pyrénées à 4,50 %) ; les
  énumérations de départements se datent.
- **S-36** — Banque de France, Stat Info « Crédits aux particuliers »
  mai 2026 — le choc du crédit 2022-2024 (taux ~1 % → > 4 %) qui
  fonde le caveat cyclique de L-22/L-23.
- **S-37** — DGFiP (impots.gouv), frais d'acquisition — la contribution
  de sécurité immobilière (0,10 %, min 15 €) intégrée au péage R-14.
- **S-38** — INSEE, estimations de population par département, sexe et
  âge quinquennal 1975-2026 — structures 2012/2023 du shift-share
  démographique T-16.

Définitions enregistrées : D-01 logement · D-02 résidence principale ·
D-03 logement vacant · D-04 résidence secondaire · D-05 ménage (recensement,
concept remplacé le 31/08/2025) · D-06 ménage-logement · D-07 zone d'emploi ·
D-08 bassin de vie · D-09 taux d'effort · D-10 vacance structurelle (LOVAC,
> 2 ans) · D-11 vacance frictionnelle (LOVAC, ≤ 2 ans) · D-12 habitat
indigne (loi MOLLE 2009, Légifrance) · D-13 passoire thermique (CCH
L173-1-1, classes F-G) · D-14 zone tendue (art. 232 CGI, zonage TLV) ·
D-15 vacance de fluidité · D-16 ancienneté d'emménagement (RP —
rotation du parc, pas mobilité des personnes) · D-17 taux de mobilité
du parc locatif social (RPLS — hors mises en service et mutations
internes) · D-18 migration résidentielle annuelle (MIGCOM — personnes,
résidence un an auparavant). Le registre des définitions du cadrage est
complet.

Hypothèses : **H-06** — seuil de vacance structurelle, valeur centrale 2 ans
(convention C-01), plage plausible 1-3 ans (sensibilité complète possible
seulement avec les fichiers LOVAC détaillés). **H-07** — surface habitable
par personne à la relocation, RECENTRÉE le 2026-08-07 (revue
contradictoire) : valeur centrale 35 m²/personne (emménagés récents,
tranche 30-39 ans de S-12), plage plausible 35-51,2 — la borne haute est
l'ancien centre (parc en place) ; le taux d'effort R-06 est linéaire en
H-07 (classement invariant, sensibilité orientée à la hausse).
**H-08** — seuil de vacance de fluidité, valeur centrale 6 % (bande
optimale 6-7 % de S-14), plage plausible 5-7 (borne basse S-15) ;
confiance basse — ordre de grandeur professionnel, sensibilité désormais
propagée dans R-07, R-09 ET R-10. **H-12** — taux d'existence du gisement
structurel LOVAC, créée le 2026-08-07 (revue contradictoire) : valeur
centrale 0,75 (~25 % de faux vacants, Cour des comptes S-22), plage
plausible 0,6-0,9, propagée des deux côtés du test de tension C-06
(gisement effectif ET vacance disponible) ; ne couvre PAS la
mobilisabilité comportementale (limite qualitative L-17).

Valeur normative déjà posée par le cadrage (`INTRO.md` §3) :

- **V-01** — Une résidence principale occupée est pleinement utilisée ; elle ne
  peut jamais être comptée comme capacité disponible ni comme inefficience.

- **R-03** — Vacance structurelle × dynamique d'emploi par ZE (sortie
  reproductible `data/processed/vacance-emploi-ze.json`) : Spearman −0,36
  [−0,45 ; −0,26] (métropole −0,47 [−0,55 ; −0,37]), taux médian 4,5 %
  dans les 63 ZE à emploi déclinant contre 2,9 % ailleurs, mais 78-88 %
  des volumes dans des ZE où l'emploi croît (84,9 % au visible, borne de
  secrétisation publiée). Lecture : **I-03** — H-02 confirmée en
  intensité, réfutée comme explication dominante en volume sur toute la
  borne ; les causes de blocage sont ailleurs (H-03/H-05). Limites
  L-05..L-08 (L-07 corrigée : l'emploi ZE récent existe, variante
  planifiée).

- **R-04** — Pression du coût résidentiel × vacance par ZE (sortie
  reproductible `data/processed/cout-residentiel-ze.json`) : Spearman
  −0,43 [−0,52 ; −0,33] (métropole −0,54 [−0,62 ; −0,45]), vacance
  médiane 2,5 % dans les ZE chères contre 3,9 % dans les ZE bon marché.
  Lecture : **I-04** — le coût marque la tension, il n'explique pas
  la vacance ; le cumul coût élevé + vacance élevée est ultramarin
  (La Réunion, Martinique — revenus faibles), pas corse ni « résidences
  secondaires » (correction vérifiée, exploration 05). Limites L-09
  (complétée : niveaux surestimés — loyers 2025/revenus 2021, charges
  comprises —, classements insensibles).

- **R-05** — Résidences secondaires × coût × vacance par ZE (sortie
  reproductible `data/processed/residences-secondaires-ze.json`) :
  corrélation RS × vacance faible mais SIGNIFICATIVE (+0,15
  [0,04 ; 0,26]) et de signe opposé au contraste touristique (les ZE
  touristiques ont une vacance PLUS BASSE — non-monotonie, effet de
  structure) ; RS × coût compatible avec zéro (−0,05 [−0,16 ; 0,06]) ;
  cumul RS+vacance dans un sous-groupe corse et rural-touristique (8 ZE).
  Lecture : **I-05** (inchangée, énoncée honnêtement) — la capacité
  saisonnière retirée est dans la catégorie RS et ses effets d'éviction
  infra-territoriaux, pas dans la vacance. Limites L-10.

- **R-06** — Taux d'effort brut à la relocation par ZE (sortie reproductible
  `data/processed/taux-effort-relocation-ze.json`, H-07 recentrée le
  2026-08-07) : médiane CENTRALE 27,4 % (27,4-40,1 selon H-07 — borne
  haute = relocation au standard du parc en place, l'ancien titre),
  Paris 63,9 % (63,9-93,5) puis les ZE réunionnaises et martiniquaises
  (~50-58 %) ; Spearman effort × vacance −0,40 [−0,49 ; −0,30]
  (métropole −0,51 [−0,59 ; −0,41]). Lecture : **I-06** — la tension de
  I-04 en unité interprétable : ~27 % au central (proche du standard
  30 %) mais jusqu'à 40 % en borne haute ; à Paris et dans les DOM
  couverts, la relocation est hors de portée du ménage médian local à
  toutes les valeurs de H-07 (classement invariant) ; fournit le terme
  coût pour instruire H-04. Limites L-09/L-11 (directions des biais
  écrites).

- **R-07** — Tension et manque absolu par ZE (sortie reproductible
  `data/processed/tension-manque-absolu-ze.json` — recalculé le
  2026-08-07 : H-12 propagée des deux côtés, écrêtage, variantes) :
  97 ZE tendues en vacance disponible (15,26 M de parc) ; besoin
  national de détente 194 488 logements (écrêté), gisement structurel
  EFFECTIF local 206 664 (LOVAC × 0,75), couverture 1,06 — 0,69 au
  périmètre des seules communes TLV ; la grille H-08 × H-12 traverse 1
  (0,82-1,85) ; couverte dans 56 ZE, pas dans 41 — 68 % du besoin en ZE
  non couvertes, déficit incompressible 57 945 ; variante d'assiette
  (seuil recalibré 4,31 %) : 28 ZE, couverture 1,19 ; 31 ZE « tendues
  par structurelle record » (37 % du gisement). Lecture : **I-07**
  (reformulée) — la suffisance en volume est MARGINALE et
  conditionnelle ; le gisement n'est pas là où est le besoin (inter-ZE
  ni infra-ZE) : la détente par la seule remobilisation n'est PAS
  démontrée — contribution substantielle (~137 000 rénovables) dont le
  verrou est institutionnel (H-05). Limites L-12 (corrigée),
  L-16..L-19, L-21.

- **R-08** — État du bâti × vacance par ZE (sortie reproductible
  `data/processed/etat-bati-ze.json`) : en métropole, l'ancienneté du
  bâti est fortement corrélée à la vacance (Spearman +0,56
  [0,47 ; 0,63]) — du MÊME ORDRE que le coût (−0,54) et l'effort
  (−0,51) à périmètre égal (superlatif abandonné), au-dessus de F+G
  (+0,40 [0,30 ; 0,49]) ; couverture DPE × vacance −0,14 (le 0,40 est
  plutôt une borne basse) ; F+G × âge 0,62 — la diagonale rurale ;
  contraste DOM : vacance médiane 11 % sur bâti récent et pourvu du
  confort. Lecture : **I-08** (au conditionnel) — première instruction
  de H-05 : SI l'état des vacants suit celui du parc observable (L-13 —
  hypothèse, pas mesure), remobiliser a un coût de remise en usage ; le
  Datalab S-23 conforte la piste obsolescence/successions logement par
  logement ; aux DOM tout le mesurable est éliminé, reste la piste
  successions/indivisions derrière la frontière de données. Limites
  L-13 (complétée).

- **R-09** — Coût de la remobilisation, règle MIXTE (sortie reproductible
  `data/processed/cout-remobilisation-ze.json` — C-07 corrigé le
  2026-08-07) : détendre les 97 ZE tendues coûterait ~15,8 Md€ TTC 2023
  (14,9-17,1 ; 136 544 rénovables à ~43 800 €/logement + 57 945 en
  déficit facturés au neuf, 9,8 Md€), contre ~32,9 Md€ en construction
  neuve — ratio 2,1 (1,9-2,2) ; rénovation seule (trace) : 8,6 Md€,
  ratio 3,8 ; propagation H-08 : 5,5-37,5 Md€, ratios 2,3-1,9 ; stress
  réhabilitation lourde ×2 : 21,8 Md€, ratio 1,5. Lecture : **I-09**
  (reformulée) — ~2 × moins cher au central, ≥ 1,5 sous stress : solide
  en DIRECTION, plus étroit en AMPLEUR (le « ~4 × » ne valait que pour
  la part rénovable) ; investissement total ≠ coût public, canal
  incitatif historiquement faible (S-22). Limites L-14 (corrigée),
  L-17/L-18/L-20.

- **R-11** — Rotation résidentielle par ZE (sortie reproductible
  `data/processed/mobilite-residentielle-ze.json`, ajoutée le
  2026-08-08, revue le 2026-08-09 — première instruction de H-04) : la
  part des RP occupées depuis moins de 2 ans passe de 13,14 % (2012) à
  11,97 % (2023) et la baisse s'accélère (−0,92 pt sur 2017-2023) —
  ~364 000 emménagements récents « manquants » dans le stock 2023
  (ordre descriptif), dont ~45 % attribuables au seul vieillissement
  (shift-share T-16 ; borne externe INSEE : 14 %, S-33) ; 293 ZE sur
  305 en baisse ; le NIVEAU de rotation suit la fonction du territoire
  (+0,40 avec le coût, métropole) ; la CHUTE est publiée en trois
  vues : plus forte en ZE tendues en points (−1,54 vs −1,27, MW
  p = 0,003) et en relatif (−12,2 vs −10,7 %), mais le gradient de
  coût DISPARAÎT à niveau 2012 contrôlé (partiel −0,07 ≈ 0) — fait
  significatif, non discriminant. Lecture : **I-11** (requalifiée) —
  gel général, part démographique bornée minoritaire, fenêtre du choc
  du crédit non séparée (S-36) ; le signal restant est l'ACCÉLÉRATION,
  que le vieillissement ne produit pas. Limites L-22, L-26.

- **R-12** — Mobilité du parc social par ZE (sortie reproductible
  `data/processed/mobilite-parc-social-ze.json`, ajoutée le 2026-08-08,
  revue le 2026-08-09 — deuxième instruction de H-04) : chute nationale
  9,29 → 7,11 % (2019-2025), qui s'accélère (−1,43 pt sur 2022-2025 —
  fenêtre du choc du crédit, S-36), généralisée (286 ZE sur 303) —
  uniforme en POINTS (médianes −2,40/−2,45) mais EXCÉDENTAIRE dans les
  marchés chers en relatif et à niveau 2019 contrôlé (−26,0 vs
  −22,5 % ; partiel −0,50) ; un NIVEAU miroir du marché depuis au
  moins 2013 : mobilité × coût rho métropole −0,70 (2013) → **−0,80**
  (2025, parmi les plus fortes de la chaîne, ≈ R-13/R-14), médiane
  6,74 % en ZE tendues (vacance sociale 1,63 %) vs 8,88 ailleurs ; le
  croisement brut −0,20 avec la rotation totale est un corollaire des
  deux gradients de coût (partiel +0,21 à coût contrôlé). Lecture :
  **I-12** (requalifiée) — le niveau reflète l'accessibilité du marché
  local (trait structurel), la chute est générale et au moins aussi
  forte dans les marchés chers ; part démographique bornée (ANCOLS
  9 %, S-34), part cyclique non séparée. Convention C-09 (agrégation
  pondérée contrôlée au national non arrondi, ≤ 0,010 pt). Limites
  L-23, L-26.

- **R-13** — Migrations résidentielles des personnes par ZE (sortie
  reproductible `data/processed/migrations-residentielles-ze.json`,
  ajoutée le 2026-08-08, revue le 2026-08-09 — troisième instruction de
  H-04) : 9,87 % de mobiles annuels (fenêtres 2020-2024 ; la série
  publiée est passée sous 9 % en 2023, S-33), portés par le LOCATIF
  PRIVÉ (19,51 % d'entrées de l'année contre 8,34 % en HLM et 5,73 %
  en propriété) et décroissant fortement avec l'âge (O-36) ; cohérence
  interne logements/personnes rho +0,80 (R-11 × R-13 — même appareil
  EAR ; la validation inter-appareils est MIGCOM-HLM ≈ RPLS) ; les
  flux internes vident les cœurs chers (Paris −1,40 %/an) avec un
  profil par âge de CYCLE DE VIE (seul groupe positif : 15-24 ;
  sorties nettes aux âges famille et retraite, O-36) ; en niveau, pas
  de gel spécifique aux zones tendues sur un an. Lecture : **I-13**
  (requalifiée) — le locatif privé est le canal principal des
  mobilités (le renchérir comprime la mobilité de tous) ; les soldes
  parisiens relèvent du cycle de vie, l'éviction reste une question
  ouverte. Limites L-24, L-26.

- **R-14** — Coût de transaction à l'achat par ZE (sortie reproductible
  `data/processed/cout-transaction-ze.json`, ajoutée le 2026-08-08,
  revue le 2026-08-09 — quatrième instruction de H-04) : péage presque
  uniforme en taux (6,7-8,1 % du prix : droits TERRITORIALISÉS S-31 +
  émoluments exacts S-32 + CSI S-37) mais très inégal en poids —
  médiane 6,15 MOIS de niveau de vie médian par UC (millésime 2021),
  7,87 mois en ZE tendues vs 5,59 ailleurs, jusqu'à ~11-13 mois
  (Paris, Bayonne, littoraux, DOM chers) ; 5,81 mois en médiane au
  scénario primo-accédant ; annualisé : 2,6 %/an à 20 ans de
  détention, ~10-13 %/an pour un ménage mobile tous les 5 ans ; le
  rho +0,81 avec le coût locatif est quasi mécanique (mois × prix
  +0,98). Lecture : **I-14** (requalifiée) — le ménage des zones
  tendues est pris en tenaille (relocation locative jusqu'à ~64 % du
  revenu à Paris, R-06 ; péage d'achat record, frappant d'abord la
  mobilité répétée) ; ~83 % du péage est fiscal (droits + CSI) :
  paramètre institutionnel direct pour la proposition P-xx — mais pas
  une confirmation indépendante de la géographie du gel (L-26).
  Convention C-10 (assiette publiée avec ce qu'elle écarte), limites
  L-25 (plancher — ni agence ni débours ; prix 2025 / revenus 2021).

- **R-10** — Foncier immobilisé par le non-résidentiel vacant (sortie
  reproductible `data/processed/foncier-friches-ze.json`) : 2 736
  friches « sans projet » dans 93 des 97 ZE tendues, 14 383 ha
  plafonnés → ~2,12 M de logements de capacité à densité haussmannienne
  (H-11 dérivée et contrôlée) = 10,9 × le besoin (5,2-16,7 sur H-11 ;
  5,1-28,6 sur H-08) ; à la densité CONSTATÉE des opérations du fonds
  friches (30,3 logements/ha, S-25/S-26) : 2,2 × — plancher
  opérationnel ; 80 des 93 ZE pourvues couvrent leur besoin. Lecture :
  **I-10** (reformulée — conclusion de l'arc) — le foncier n'est pas la
  contrainte et le coût est favorable là où il y a gisement, mais le
  volume vacant ne suffit qu'à l'échelle agrégée et au taux d'existence
  central : la contrainte institutionnelle n'est plus la conséquence de
  la suffisance, elle en est la CONDITION — lever les verrous de
  propriété (H-05), construire sur friches là où le gisement manque,
  maintenir le flux de construction (L-19). Limites L-15 (complétée),
  L-19/L-20.

Choix de conception arrêtés (2026-08-03) — désormais dans le graphe
(`evidence/claims.yaml`) : **C-01** (convention de vacance structurelle > 2 ans,
seuil paramétré 1-3 ans), **C-02** (national d'abord, puis LOVAC). Ajoutés le
2026-08-05 : **C-04** (taux d'effort sans ménage type — H-07 × ratio
personnes/UC observé), **C-05** (loyer = mix appartement/maison pondéré par
la composition des RP de la ZE), **C-06** (tension = vacance DISPONIBLE
< H-08 — correction tracée du test « vacance totale », qui ne classait
tendue aucune grande métropole TLV), **C-07** (modèle du coût de remise en
usage), **C-08** (modèle du foncier immobilisé, densité H-11). Complétés le
2026-08-07 (revue contradictoire) : C-06 intègre H-12 des deux côtés et
publie la sensibilité d'assiette (seuil recalibré, ZE tendues-par-
structurelle marquées) ; C-07 porte la CORRECTION TRACÉE de la règle mixte
(rénovation = min(besoin, gisement effectif local), déficit au prix du
neuf).

Résultats stabilisés (2026-08-03) :

- **R-02** — Vacance structurelle du parc privé (sortie reproductible
  `data/processed/vacance-structurelle.json`) : ~1,15 M de logements au
  dernier millésime pré-rupture (24, aligné C-03 — le millésime 26,
  1,18 M, est post-GMBI, source dégradée ; contrôle externe Apur S-24 à
  Paris : ~18 600 vs 32 091, écart à instruire), taux national 3,5 %
  (millésime 24), gradient départemental d'un ordre de grandeur (DOM et
  diagonale des faibles densités vs zones tendues). Lecture : **I-02** —
  deux régimes distincts, intensité rurale/ultramarine vs volume urbain,
  premier indice cohérent avec H-02. Limites L-04 (ruptures 2023/2025 +
  GMBI, complétée), L-05 (secrétisation), L-06 (parc privé ≠ INSEE).

- **R-01** — Comparaison parc / ménages / population 1982-2025 (sortie
  reproductible `data/processed/parc-menages.json`, rebâtie par
  `uv run logement reproduce`, verrouillée par le test de régression
  `tests/test_reproduce.py`). Lecture : **I-01** — le parc suit les ménages
  (décohabitation), régime inversé vers 2005-2006, la remontée de la capacité
  hors résidence principale depuis 2006 est de la vacance. Limites L-01..L-03
  (national seulement, 2023-2025 provisoires, écart conceptuel ménage/RP).
