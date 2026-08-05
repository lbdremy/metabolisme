# EVIDENCE — index de la chaîne de preuves

Index humain des éléments de preuve de l'étude, par statut épistémique
(méthode Métabolisme, INTRO §4). Les registres machine font foi :
`sources/sources.yaml`, `sources/definitions.yaml`, `sources/hypotheses.yaml`,
puis `evidence/claims.yaml` pour le graphe de dépendances.

| Code | Statut | Registre / emplacement | État |
|------|--------|------------------------|------|
| S | Sources | `sources/sources.yaml` | 19 sources (INSEE, LOVAC, ANIL, SDES, MTE, DREAL, ADEME, Enertech, Banque des Territoires, Légifrance ; 22 fichiers figés sha256/LFS + 2 collections vivantes) |
| D | Définitions | `sources/definitions.yaml` | 15 définitions citées verbatim, datées, avec limites |
| H | Hypothèses | `sources/hypotheses.yaml` | H-06 seuil de vacance structurelle · H-07 surface de relocation · H-08 seuil de fluidité · H-09/H-10 coûts de rénovation performante maison/collectif (S-17, euros 2016) |
| O/T/R | Observations, transformations, résultats | `evidence/claims.yaml` | O-01..O-21, T-01..T-10, R-01..R-09 (sorties dans `data/processed/`) |
| I/V/C/L | Interprétations, valeurs, choix, limites | `evidence/claims.yaml` | I-01..I-09, V-01, C-01..C-07, L-01..L-14 |
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

Définitions enregistrées : D-01 logement · D-02 résidence principale ·
D-03 logement vacant · D-04 résidence secondaire · D-05 ménage (recensement,
concept remplacé le 31/08/2025) · D-06 ménage-logement · D-07 zone d'emploi ·
D-08 bassin de vie · D-09 taux d'effort · D-10 vacance structurelle (LOVAC,
> 2 ans) · D-11 vacance frictionnelle (LOVAC, ≤ 2 ans) · D-12 habitat
indigne (loi MOLLE 2009, Légifrance) · D-13 passoire thermique (CCH
L173-1-1, classes F-G) · D-14 zone tendue (art. 232 CGI, zonage TLV) ·
D-15 vacance de fluidité. Le registre des définitions du cadrage est
complet.

Hypothèses : **H-06** — seuil de vacance structurelle, valeur centrale 2 ans
(convention C-01), plage plausible 1-3 ans (sensibilité complète possible
seulement avec les fichiers LOVAC détaillés). **H-07** — surface habitable
par personne à la relocation, valeur centrale 51,2 m²/personne (enquête
Logement 2020, S-12), plage plausible 35-71 (bornes observées par âge) ;
le taux d'effort R-06 est linéaire en H-07 (classement invariant).
**H-08** — seuil de vacance de fluidité, valeur centrale 6 % (bande
optimale 6-7 % de S-14), plage plausible 5-7 (borne basse S-15) ;
confiance basse — ordre de grandeur professionnel, sensibilité publiée
dans R-07.

Valeur normative déjà posée par le cadrage (`INTRO.md` §3) :

- **V-01** — Une résidence principale occupée est pleinement utilisée ; elle ne
  peut jamais être comptée comme capacité disponible ni comme inefficience.

- **R-03** — Vacance structurelle × dynamique d'emploi par ZE (sortie
  reproductible `data/processed/vacance-emploi-ze.json`) : Spearman −0,36,
  taux médian 4,5 % dans les 63 ZE à emploi déclinant contre 2,9 % ailleurs,
  mais ~85 % des volumes dans des ZE où l'emploi croît. Lecture : **I-03** —
  H-02 confirmée en intensité, réfutée comme explication dominante en
  volume ; les causes de blocage sont ailleurs (H-03/H-05). Limites
  L-05..L-08.

- **R-04** — Pression du coût résidentiel × vacance par ZE (sortie
  reproductible `data/processed/cout-residentiel-ze.json`) : Spearman −0,42,
  vacance médiane 2,5 % dans les ZE chères contre 4,0 % dans les ZE bon
  marché. Lecture : **I-04** — le coût marque la tension, il n'explique pas
  la vacance ; le cumul coût élevé + vacance élevée est ultramarin
  (La Réunion, Martinique — revenus faibles), pas corse ni « résidences
  secondaires » (correction vérifiée, exploration 05). Limites L-09.

- **R-05** — Résidences secondaires × coût × vacance par ZE (sortie
  reproductible `data/processed/residences-secondaires-ze.json`) : part RS
  sans lien avec la vacance (+0,17) ni le coût (−0,05) à l'échelle ZE ; les
  ZE touristiques ont une vacance PLUS BASSE ; cumul RS+vacance dans un
  sous-groupe corse et rural-touristique. Lecture : **I-05** — la capacité
  saisonnière retirée est dans la catégorie RS et ses effets d'éviction
  infra-territoriaux, pas dans la vacance. Limites L-10.

- **R-06** — Taux d'effort brut à la relocation par ZE (sortie reproductible
  `data/processed/taux-effort-relocation-ze.json`) : médiane 40,1 %
  (27,4-55,6 selon H-07), Paris 93,5 % puis les ZE réunionnaises et
  martiniquaises (~75-85 %) ; Spearman effort × vacance −0,40. Lecture :
  **I-06** — la tension de I-04 en unité interprétable ; à Paris et dans
  les DOM couverts, la relocation est hors de portée du ménage médian
  local ; fournit le terme coût pour instruire H-04. Limites L-09/L-11.

- **R-07** — Tension et manque absolu par ZE (sortie reproductible
  `data/processed/tension-manque-absolu-ze.json`) : 142 ZE tendues en
  vacance disponible (choix C-06 — correction tracée du test initial) ;
  besoin national de détente 285 665 logements, gisement structurel local
  472 022, couverture 1,65 (robuste sur la plage H-08) ; couverte dans
  101 ZE, pas dans 41 (littorales/touristiques). Lecture : **I-07** — en
  volume absolu le gisement suffit nationalement (I-03 quantifié), mais
  la suffisance suppose de lever les blocages H-05 et la tension
  touristique ne se résout pas par la vacance. Limites L-12.

- **R-08** — État du bâti × vacance par ZE (sortie reproductible
  `data/processed/etat-bati-ze.json`) : en métropole, l'ancienneté du
  bâti est le corrélat le plus fort de la chaîne (Spearman 0,56 ; F+G
  0,40 ; F+G × âge 0,62 — la diagonale rurale) ; contraste DOM : vacance
  médiane 11 % sur bâti récent et pourvu du confort. Lecture : **I-08** —
  première instruction de H-05 : remobiliser le gisement a un coût de
  remise en usage (métropole) ; aux DOM tout le mesurable est éliminé,
  reste la piste successions/indivisions derrière la frontière de
  données. Limites L-13.

- **R-09** — Coût de la remobilisation (sortie reproductible
  `data/processed/cout-remobilisation-ze.json`) : détendre les 142 ZE
  tendues coûterait ~12,5 Md€ TTC 2023 (10,6-15,3 sur les plages
  H-09/H-10 ; ~43 800 €/logement), contre ~48,3 Md€ en construction
  neuve — ratio 3,2-4,6 (modèle C-07 : coûts S-17 actualisés IPEA,
  surfaces S-12, mix maison/appart par ZE). Lecture : **I-09** —
  l'argument économique de la remobilisation est solide mais ne lève ni
  les verrous de propriété (I-08) ni la tension touristique sans
  gisement ; première brique quantifiée de la proposition. Limites L-14.

Choix de conception arrêtés (2026-08-03) — désormais dans le graphe
(`evidence/claims.yaml`) : **C-01** (convention de vacance structurelle > 2 ans,
seuil paramétré 1-3 ans), **C-02** (national d'abord, puis LOVAC). Ajoutés le
2026-08-05 : **C-04** (taux d'effort sans ménage type — H-07 × ratio
personnes/UC observé), **C-05** (loyer = mix appartement/maison pondéré par
la composition des RP de la ZE), **C-06** (tension = vacance DISPONIBLE
< H-08 — correction tracée du test « vacance totale », qui ne classait
tendue aucune grande métropole TLV).

Résultats stabilisés (2026-08-03) :

- **R-02** — Vacance structurelle du parc privé (sortie reproductible
  `data/processed/vacance-structurelle.json`) : ~1,18 M de logements
  (millésime 26), taux national 3,5 % (millésime 24, choix C-03), gradient
  départemental d'un ordre de grandeur (DOM et diagonale des faibles
  densités vs zones tendues). Lecture : **I-02** — deux régimes distincts,
  intensité rurale/ultramarine vs volume urbain, premier indice cohérent
  avec H-02. Limites L-04 (ruptures 2023/2025), L-05 (secrétisation),
  L-06 (parc privé ≠ INSEE).

- **R-01** — Comparaison parc / ménages / population 1982-2025 (sortie
  reproductible `data/processed/parc-menages.json`, rebâtie par
  `uv run logement reproduce`, verrouillée par le test de régression
  `tests/test_reproduce.py`). Lecture : **I-01** — le parc suit les ménages
  (décohabitation), régime inversé vers 2005-2006, la remontée de la capacité
  hors résidence principale depuis 2006 est de la vacance. Limites L-01..L-03
  (national seulement, 2023-2025 provisoires, écart conceptuel ménage/RP).
