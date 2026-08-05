# PREV-STEPS — ce qui est déjà fait

Journal des sessions de travail, la plus récente en premier. Les prochaines
étapes vivent dans [`NEXT-STEPS.md`](NEXT-STEPS.md).

## Session 2 — 2026-08-05 (taux d'effort · tension · état du bâti · coût de remobilisation)

Quatre livrables : **R-06/I-06** (premier item de NEXT-STEPS), **R-07/I-07**
(nouvelle question posée par Rémy en séance : zones tendues, volume
additionnel nécessaire à la détente, suffisance du gisement vacant local —
en nombres ABSOLUS), **R-08/I-08** (première instruction de H-05), puis
**R-09/I-09** (chiffrage du coût de remobilisation). Tag intermédiaire
**`efficacite-parc-v0.2`** posé après R-08.

**État en fin de session** : 19 sources figées (S-01..S-19), 15
définitions, 5 hypothèses (H-06..H-10), graphe à 71 nœuds
(O-01..O-21, T-01..T-10, R-01..R-09, I-01..I-09, C-01..C-07,
L-01..L-14), 9 stages reproductibles, 73 tests verts, document de
preuve auto-vérifié R-01..R-09, CI verte sur les 4 commits. **L'arc
quantifié de la proposition est complet** : le gisement des zones
tendues suffit en volume (R-07, couverture 1,65) → il est vieux et sa
remobilisation a un coût (R-08) → mais ~4 fois moindre que construire
(R-09, ~12,5 vs ~48,3 Md€). Toutes les hypothèses directrices
mesurables en open data sont instruites ; H-04 reste à ouvrir, H-05 à
approfondir par convention d'accès.

### Livrable 4 — R-09 : le coût de la remobilisation vs construire

| Élément | État |
|---|---|
| Sources | S-17 Enertech/ADEME 2016 (coûts rénovation performante €HT/m²) ; S-18 Banque des Territoires Éclairages n°33 (prix de revient logement social neuf 169 200 € en 2023) ; S-19 INSEE IPEA résidentiel (réponse SDMX figée, facteur 2016→2023 recalculé par la chaîne) |
| Hypothèses | H-09 maison 406 €HT/m² (348-496) ; H-10 collectif 250 (200-300) — plages sourcées S-17 |
| Choix | **C-07** — coût unitaire = €/m² mixés par la part maison de la ZE × surfaces S-12, TTC 5,5 %, actualisation IPEA ; comparateur = prix de revient social (conservateur) |
| Notebook | 10 (exploration, constats vérifiés depuis les sorties) |
| Stabilisation | `core/remob.py` + stage `cout-remobilisation` + 5 tests (73 au total) + R-09/I-09/C-07/L-14 + O-19..O-21/T-10 |

Ce que dit R-09 : détendre les 142 ZE tendues par remobilisation coûterait
**~12,5 Md€ TTC 2023** (10,6-15,3 ; ~43 800 €/logement en moyenne
pondérée) contre **~48,3 Md€** en construction neuve — **ratio 3,2-4,6**
(3,9 au central), robuste sur les plages. Tout le gisement des ZE
tendues : ~20 Md€. Limites portées avec le chiffre (L-14) :
investissement total ≠ coût public ; rénovation performante = proxy de la
remise en usage ; le verrou n'est pas que financier (I-08).

### Livrable 3 — R-08 : état du bâti × vacance (H-05, 1re instruction)

| Élément | État |
|---|---|
| Source | S-16 extrait DPE ADEME figé (14,8 M de DPE, commune × étiquette) — acquisition SCRIPTÉE `logement acquire-dpe` (shell/acquire.py) : agrégation API sans perte, choisie après échec de la pagination brute (throttle HTTP 429 : ~3 h → ~10 min) |
| Notebook | 09 (exploration, constats vérifiés depuis les sorties) |
| Stabilisation | `core/bati.py` + stage `etat-bati` + 6 tests (68 au total) + R-08/I-08/L-13 + O-16..O-18/T-09 dans le graphe |
| Frontières actées | PPPI (convention DREAL/DDT ; open 2015 obsolète), fichiers fonciers/successions (Cerema, acteurs publics), stats notariales (rien d'ouvert) |

Ce que dit R-08 : en MÉTROPOLE l'ancienneté du bâti est le corrélat
territorial le plus fort de toute la chaîne (Spearman 0,56 vs vacance
structurelle ; F+G des diagnostiqués 0,40 ; F+G × âge 0,62) — la
diagonale rurale de R-02/R-03 ; la remobilisation du gisement R-07 a un
coût de remise en usage, à chiffrer. CONTRASTE DOM : vacance médiane 11 %
sur bâti récent (1,9 % d'avant-1946) et pourvu du confort — par
élimination (emploi, coût, RS, bâti), reste la piste successions/
indivisions, derrière la frontière de données. Pièges vérifiés en
séance : P22_RP_BDWC nul en métropole (question DOM seulement) ; DPE
quasi absents des DOM (ZE 0303 Guyane : zéro) ; biais d'échantillon DPE
(les vacants durables ne sont pas diagnostiqués).

### Livrable 2 — R-07 : tension des usages et manque absolu

| Élément | État |
|---|---|
| Sources | S-13 zonage TLV figé (décret 2025-1267, 3 millésimes) ; S-14 DREAL PdL 2020 (bande optimale 6-7 %) ; S-15 observatoire CUA Alençon 2025 (borne 5 %) |
| Définitions | D-14 zone tendue (art. 232 CGI, verbatim) ; D-15 vacance de fluidité |
| Hypothèse | H-08 seuil de fluidité : 6 % (plage 5-7), confiance basse — sensibilité publiée |
| Choix | **C-06** — tension = vacance DISPONIBLE (totale − structurelle) < H-08 ; CORRECTION TRACÉE : le test « vacance totale » décidé en début de session échouait au contrôle de cohérence (aucune métropole TLV tendue — médiane nationale 8,6 %), correction validée par AskUserQuestion |
| Notebook | 08 (exploration, constats vérifiés depuis les sorties) |
| Stabilisation | `core/tension.py` + stage `tension-manque-absolu` + 7 tests (62 au total) + R-07/I-07/L-12 + O-14/O-15/T-08 dans le graphe |

Ce que dit R-07 : **142 ZE tendues** (23,8 M de logements) ; besoin absolu
national **285 665 logements à rendre disponibles** ; gisement structurel
dans ces mêmes ZE **472 022** → **couverture 1,65** (1,90 au seuil 5 %,
1,15 à 7 %). Le gisement suffit dans 101 ZE sur 142 ; les 41 non
couvertes sont littorales/touristiques (Sables-d'Olonne 0,20, Calvi
0,33…) — là, le parc hors RP est en résidences secondaires (R-05), pas en
vacance. Suffisance CONDITIONNELLE : mobiliser un parc sorti d'usage
suppose H-05 (état du bâti, successions) non instruite ; vacance
recensement surestime l'offre disponible dans les centres denses (besoin
métropolitain sous-estimé, L-12).

### Livrable 1 — R-06 : taux d'effort à la relocation (D-09)

| Élément | État |
|---|---|
| Source | S-12 figée (SDES Datalab n° 296, enquête Logement 2020 — surfaces habitables ; chiffres provisoires, champ métropole) |
| Hypothèse | H-07 `relocation_surface_per_person_m2` : 51,2 m²/personne (plage 35-71, bornes observées par âge dans S-12) |
| Choix | **C-04** — pas de ménage type : surface = H-07 × personnes, revenu = MED_SL × UC, donc seul le ratio personnes/UC OBSERVÉ par ZE (Filosofi NUM_PER/NUM_CU) intervient ; **C-05** — loyer = mix appartement/maison pondéré par la composition des RP de la ZE (S-11), variante appartement en sensibilité |
| Notebook | 07 (exploration, constats vérifiés depuis les sorties) |
| Stabilisation | `core/effort.py` + stage `taux-effort-relocation` + 9 tests (55 au total) + R-06/I-06/L-11 + O-10..O-13/T-07 dans le graphe |
| Document de preuve | Section R-06, sensibilité H-07, I-06 — re-rendu, auto-vérification R-01..R-06 verte |

Ce que dit R-06 : taux d'effort **brut** médian à la relocation **40,1 %**
du revenu du ménage médian (27,4-55,6 % selon H-07 — le niveau dépend de
H-07, le classement non). En tête Paris 93,5 % puis les ZE réunionnaises
et martiniquaises (75-85 %, revenus faibles) : la relocation y est hors de
portée du ménage médian local. Anticorrélation effort × vacance −0,40 :
la montée en réalisme (surface, composition, mix maison/appart — part
maison médiane 74 % des RP par ZE) ne change pas la lecture de I-04. Le
terme « coût de la mobilité résidentielle » pour H-04 est disponible.

Décisions prises en début de session (AskUserQuestion) : H-07 en m² par
UC → implémentée en m²/personne directement sourcée (S-12) × ratio
personnes/UC observé — raffinement tracé dans C-04 ; mix loyers pondéré
parc retenu contre appartement seul.

## Session 1 — 2026-08-03 (fondation) — tag `efficacite-parc-v0.1`

Une **première boucle complète** de la chaîne de preuves exécutable :
sources figées → définitions verbatim → hypothèse nommée → exploration →
stabilisation testée → résultats reproductibles → document de preuve rendu.

| Élément | État en fin de session |
|---|---|
| Harnais | Projet uv autonome calqué sur le dépôt `learn` : core/shell, pydantic aux frontières, CLI clypi, `check.sh` (ruff · ty · skylos) + `test.sh` (pytest + hypothesis), CI GitHub (checkout LFS) |
| Sources (S-01..S-11) | 9 fichiers INSEE/ANIL + 4 fichiers LOVAC figés (Git LFS, sha256) + collections définitions INSEE et Légifrance |
| Définitions (D-01..D-13) | citées verbatim, datées, avec limites — liste du cadrage complète |
| Hypothèses | H-06 seuil de vacance structurelle (2 ans, plage 1-3) |
| Graphe (`evidence/claims.yaml`) | 39 nœuds — O-01..O-09, T-01..T-06, R-01..R-05, I-01..I-05, V-01, C-01..C-03, L-01..L-10 |
| Résultats reproductibles | R-01..R-05 (`data/processed/*.json`) — verrouillés par tests de régression ; document de preuve auto-vérifié couvrant les cinq |
| Notebooks d'exploration | 01 parc/ménages · 02 vacance territoriale · 03 vacance × emploi · 04 coût résidentiel · 05 résidences secondaires · 06 cumuls RS+vacance (frontière de données) |
| Document de preuve | `evidence/efficacite-parc-immobilier.qmd` + HTML rendu (auto-vérifié : artefacts publiés == recalcul) |
| Qualité | 30 tests verts ; CI verte après correction d'un vrai bug de reproductibilité (ordre des ex æquo dépendant de la plateforme, attrapé par le test de régression au premier run CI) |

- **R-05/I-05** — Les résidences secondaires n'expliquent ni la vacance ni
  le coût à l'échelle ZE (les ZE touristiques ont une vacance PLUS basse) ;
  cumul RS+vacance dans un sous-groupe corse/rural-touristique. La
  vérification a corrigé une erreur d'interprétation de R-04 (ZE
  ultramarines, pas corses).

- **Notebook 06 (frontière de données)** — dans les 12 ZE à cumul, la
  vacance est diffuse et la secrétisation rend la question de l'éviction
  saisonnière non tranchable en open data ; consignée comme frontière,
  sans R-xx (c'est la limite qui est le résultat).

### Décisions arrêtées (voir aussi `CLAUDE.md` et le graphe)

- **C-01** — vacance structurelle = convention LOVAC (> 2 ans), seuil
  paramétré H-06 (plage 1-3 ans).
- **C-02** — acquisition : national d'abord, puis LOVAC territorial.
- **C-03** — millésime de référence LOVAC pour les taux : 24 (dernier
  complet avant la rupture 2025).
- Git LFS pour tout `data/raw/` ; notebooks en Jupytext py:percent ;
  documents de preuve en Quarto.

### Corrections attrapées par la vérification (à relire avant de conclure vite)

1. Indice parc vs ménages (notebook 01) — première conclusion fausse,
   corrigée depuis les sorties.
2. Ordre des ex æquo dépendant de la plateforme (R-02) — attrapé par la CI.
3. ZE « corses » de R-04 qui étaient réunionnaises/martiniquaises —
   corrigé en vérifiant les codes, correction tracée dans le graphe.
4. NaN → 0 silencieux de pandas dans les agrégats communaux (notebook 06).

### Ce que disent les premiers résultats

- **R-01/I-01** — Sur 40 ans le parc suit les ménages (décohabitation),
  pas la population ; depuis ~2006 le parc croît plus vite et l'écart part
  en vacance (7,7 % en 2025, ~3,0 M).
- **R-02/I-02** — La vacance structurelle du parc privé est ~1,15 M de
  logements (3,5 % du parc privé), robuste aux ruptures LOVAC, avec un
  gradient territorial d'un ordre de grandeur : intensité rurale/DOM vs
  volume urbain — premier indice pour H-02.
- **R-03/I-03** — Croisée avec l'emploi par zone d'emploi (1998-2018) :
  H-02 confirmée en intensité (Spearman −0,36 ; taux médian 4,5 % dans les
  ZE déclinantes vs 2,9 %) mais réfutée en volume — ~85 % de la vacance
  structurelle est dans des ZE où l'emploi croît (Paris 69,8 k en tête).
  Les causes de blocage dominantes sont donc ailleurs → H-03/H-05.
- **R-04/I-04** — Croisée avec le coût (loyers 2025 / Filosofi 2021) :
  anticorrélation nette (Spearman −0,42) — le coût marque la tension, il
  n'explique pas la vacance. Le cumul coût+vacance est ultramarin (La
  Réunion/Martinique, revenus faibles) — d'abord mal identifié comme
  corse, corrigé en vérifiant les codes ZE. L'exploration 05 (résidences
  secondaires, recensement 2022) écarte l'explication « saisonnière » à
  l'échelle ZE : les ZE à plus de 20 % de RS ont une vacance structurelle
  plus basse (2,6 % vs 3,3 %). La sensibilité H-06 est bloquée au niveau
  source ; D-12/D-13 complètent le registre des définitions.
