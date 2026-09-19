# Revue contradictoire — R-18, le flux (2026-09-18)

Compte rendu de la revue contradictoire (INTRO étape 12) menée le
2026-09-18 sur le résultat R-18 de l'article 3 — la construction neuve
couvre-t-elle la formation de ménages, par zone d'emploi ? État examiné :
commit `8317526`. Décisions d'intégration : `decisions-2026-09-18.md`,
DEC-25..DEC-28 (autonomie, sans consultation de Rémy).

## Méthode

Trois relecteurs indépendants (DEC-24 : hypothèses/définitions et
scénarios d'échec fusionnés, R-18 n'introduisant aucune hypothèse) :

1. **Sources alternatives** — SA-1..SA-7 (7 objections, 14 sources
   proposées, 8 fichiers téléchargés et sommés)
2. **Hypothèses, définitions et scénarios d'échec** — HD-1..HD-10,
   SE-1..SE-6 (16 objections, dix scénarios d'échec non nommés) — 31 objections en tout
3. **Statistique** — ST-1..ST-8 (8 objections, ~70 valeurs recalculées
   par un script indépendant `verify-flux.py`)

Rapports bruts en annexe dans `evidence/revue-contradictoire-2026-09-18-flux/`.
Allégations structurantes revérifiées par l'orchestrateur avant triage :
la citation « 15 % des mises en chantier […] ne remontent jamais »
(S-58, p. 7), les totaux de la série communale en date réelle et de la
série nationale estimée (rapports annuels 1,122-1,235, recalculés
depuis les fichiers figés), la mesure des sorties de parc (S-60, p. 66),
le fichier des mouvements de communes (S-59). Toutes confirmées.
L'arithmétique publiée était **exacte partout** ; les objections portaient
sur la source, les unités de mesure et ce que la mesure mesure.

## Verdict global

- **Survivent** : l'exécution ; la géographie littorale/alpine des
  déficits sur 2017-2022 ; l'intensité de construction double dans les
  ZE tendues.
- **Ne survivaient pas** : (1) la SÉRIE — la série communale sous-compte
  de 12 à 24 % (déclarations non remontées, SA-1), ce qui renverse le
  signe du solde des ZE tendues ; (2) la LECTURE des années 2023-2024,
  écartées comme « incomplètes » alors qu'elles sont closes en date
  réelle et montrent l'effondrement du flux (SE-1) ; (3) le TITRE « le
  flux n'est pas le problème national » (SE-1) ; (4) l'énoncé « ratio
  non corrélé au coût », porté par 72 petites ZE aux ratios dégénérés
  (ST-1 : + 0,20 au plancher) ; (5) « absorbé en 10,6 ans », quotient
  national qui mélangeait les ZE (SE-2) ; (6) la variante « hors RS »
  présentée comme « l'autre borne honnête » alors que l'affectation du
  neuf est une hypothèse (HD-2) ; (7) 943 codes de communes fusionnées
  perdus (HD-6/ST-3) ; (8) le « ratio de production » lu comme une
  couverture du besoin alors que ménages ≡ résidences principales
  (HD-1).
- **Après intégration** : lecture estimée (H-21), série en date réelle
  (S-56), COG (S-59), trois affectations, quatre fenêtres, années
  closes, absorption par ZE — ratio national 1,14 (2017-2022), ZE
  tendues 1,08 (+ 16 131/an), mais 2023-2024 : − 58 216/an dans les
  ZE tendues, 77 sur 97 en déficit, stock de détente consommé en trois
  ans. La conclusion change de nature : le flux est devenu la
  contrainte dominante.

## Objections structurantes et leur disposition

| # | Objection | Disposition |
|---|---|---|
| A1 | **Sous-compte de la série communale** (SA-1 majeure) : 15 % des DOC jamais remontées ; − 12,5 % vs statistique publiée | **H-21 créée** (1,155 [1,122 ; 1,235]), S-57/S-58 figées, double lecture déclaré/estimé partout (DEC-26) |
| A2 | **Série en date réelle du producteur** (SA-2 majeure) : DEC-22 se trompait | **S-56 figée**, entrée de R-18 ; S-54 en trace (DEC-25) |
| A3 | **Années 2023-2024 closes** (SE-1 haute) : chute d'un tiers, − 65 558/an en tendues | Publiées comme lecture centrale de l'article ; I-18 réécrite ; 2019-2024 en fenêtre (DEC-28) |
| A4 | **Quasi-identité comptable** (HD-1 haute) : ménages ≡ RP | C-16 et I-18 disent ce que le ratio mesure et ne mesure pas ; « couvre le besoin » abandonné |
| A5 | **Affectation RS = hypothèse** (HD-2 haute) | Trois variantes, centrale = part observée par ZE (DEC-27) ; L-34(3) |
| A6 | **Absorption par ZE** (SE-2 haute) : 5,5 ans, pas 10,6 | Calcul par ZE (médiane + agrégat), fenêtre et 2023-2024 |
| A7 | **COG** (HD-6, ST-3) : 943 codes perdus, Sables-d'Olonne change de signe | **S-59 figée**, remappage (1 833 codes, 25 822 commencés récupérés, 0 perdu) |
| A8 | **Corrélation au plancher** (ST-1 majeure, HD-9) : + 0,23 | Plancher appliqué aux corrélations, sans plancher publié |
| A9 | **Disparitions implicites** (HD-5, SA-3) | Retirées des titres ; **O-42** (S-60) en confrontation, L-34(2) |
| A10 | **Fenêtre la plus haute** (HD-4, ST-7) | Quatre fenêtres publiées |
| B | Mineures : ZE à besoin nul (ST-2), NaN sommés (ST-4), ordre PLM (ST-5), transcriptions (ST-6), Paris non tendue (HD-8), vacance à maintenir ≠ H-08 (HD-3), stock/flux non nettés (HD-7), infra-ZE (SE-5), H-08 (SE-6) | Compteurs publiés, textes corrigés, L-34(4)/(6), sensibilité H-08 ; SE-5 non intégré (DEC-28) |

## Tableau avant/après

| Grandeur / énoncé | Avant (8317526) | Après |
|---|---|---|
| Série | S-54, date de prise en compte, déclarée | S-56 date réelle × H-21 (estimée), déclarée à côté |
| Commencés France 2017-2022 | 347 340 | 344 987 déclarés / 398 460 estimés |
| Ratio France / tendues / autres | 1,04 / 0,97 / 1,11 | 1,14 / 1,08 / 1,20 (déclaré 0,98 / 0,94 / 1,04) |
| Solde ZE tendues | − 5 253/an, 46 ZE déficitaires | + 16 131/an, 38 ZE (2017-2022) ; **− 58 216/an, 77 ZE (2023-2024)** |
| Variante RS | « hors RS » + 20 423 | sans RS + 46 773 ; structure 2022 + 21 097 ; observée (central) + 16 131 |
| Ratio × coût | − 0,06 « non corrélé » | + 0,20 [0,06 ; 0,33] au plancher ; − 0,11 sans |
| Tendues vs autres (médianes) | 1,02 vs 0,98, p 0,59 | 1,11 vs 1,00 au plancher, p 0,049 |
| Absorption du stock | 10,6 ans (37,5 hors RS), national | par ZE : 6 ans (38 ZE, 38 % du besoin) sur 2017-2022 ; **2,9 ans (77 ZE, 86 % du besoin) au rythme 2023-2024** |
| Disparitions implicites | 15 198/an (titre) | 66 318/an confronté à 27 000 mesurés (O-42), en limite |
| Codes perdus | 943 codes, ~1 278 commencés/an | 0 |
| Titre | « le flux n'est pas le problème national » | « depuis 2023, le flux est devenu la contrainte dominante » |
| Sources / hypothèses / nœuds | 55 / 15 / 150 | 60 / 16 / 151 |
