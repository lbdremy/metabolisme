# Monopoles naturels, rentes de position et collectivisation des rentes — document de preuve du cadrage

*Version du 2026-09-05, après intégration de la revue contradictoire du
2026-09-04 (compte rendu `revue-contradictoire-2026-09-04.md`, annexe
`revue-contradictoire-2026-09-04/`). Document de preuve (méthode
Métabolisme, INTRO §11) de l'article de cadrage
[`../articles/2026-09-reconnaitre-une-rente-de-position.md`](../articles/2026-09-reconnaitre-une-rente-de-position.md).
L'étude ne calcule rien à ce stade : ce document n'a ni transformation ni
résultat, et le dit. Les registres font foi : `../sources/sources.yaml`,
`../sources/definitions.yaml`, `../sources/hypotheses.yaml`,
`claims.yaml`.*

## 1. Question étudiée

Dans quels secteurs le prix payé par l'usager rémunère-t-il une position
plutôt qu'une production ; à qui cette rente revient-elle, de combien
est-elle, que coûte-t-elle à la collectivité ; et sous quelles formes
institutionnelles pourrait-elle revenir à l'usager, pour quel gain et avec
quelle part laissée au privé ? (`../INTRO.md` §1.)

Ce que ce document doit éclairer : non pas une décision sectorielle, mais
la **méthode** qui rendra ces décisions instruisables — définitions
communes, grille d'identification capable de répondre « non », définition
mesurable de la rente, position normative isolée, gabarit des études
sectorielles. Périmètre : le cadrage seul ; aucun secteur n'est instruit.
Deux mécanismes sont séparés : le monopole naturel (réseau qu'il est
inefficace de dupliquer) et la fixité positionnelle (ressource que rien
n'augmente).

## 2. Définitions

Vingt et une définitions (D-01 à D-21), toutes dans
`../sources/definitions.yaml` ; huit construites par l'étude (C-02), avec
leur lien au choix qui les formule porté dans le graphe (`constructed_by`).

| Id | Terme | Nature | Source (page du PDF) |
|---|---|---|---|
| D-01 | monopole naturel | officielle, verbatim (anglais) ; définition ART en caveat | S-01 p. 353 ; S-16 |
| D-02 | rente économique | officielle, verbatim (anglais) | S-01 p. 462 |
| D-03 | rente de position (deux cas) | construite, ancrée sur Ricardo | S-02 p. 38 (1847) |
| D-04 | rente d'innovation | construite ; citation OCDE complète (quasi-rente marshallienne) | S-01 p. 462 |
| D-05 | non-duplicabilité de l'infrastructure | construite, critère opératoire | S-01 |
| D-06 | rivalité | manuel, verbatim (anglais) | S-06 |
| D-07 | différenciabilité du bien livré | construite (ancrage faible, dit) | S-06 |
| D-08 | captivité de l'usager (physique / réglementaire ; échelle) | construite (ancrage faible, dit) | S-06 |
| D-09 | concurrence pour / sur le marché | en partie construite ; concession verbatim | S-03 |
| D-10 | contrat de concession | légale, verbatim | S-03, CCP L1121-1 (01/04/2019) |
| D-11 | régie | légale, verbatim | S-04, CGCT L1412-1 (03/05/2025) + L2221-1 |
| D-12 | délégation de service public | légale, verbatim | S-04, CGCT L1411-1 (01/04/2019) |
| D-13 | CMPC reconnu par un régulateur | réglementaire, verbatim (valeur en O-01) | S-07 p. 4, 18, 97-99 |
| D-14 | domaine public | légale, verbatim | S-05, CG3P L2111-1 + L3111-1 (01/07/2006) |
| D-15 | rente mesurable — surprofit sur base d'actifs | construite (définition opératoire) | S-07 p. 14, 18 |
| D-16 | fixité positionnelle | construite | S-02 |
| D-17 | exclusion | manuel, verbatim (anglais) | S-06 |
| D-18 | économies d'envergure | officielle, verbatim (anglais) | S-01 p. 163 |
| D-19 | coûts irrécupérables et contestabilité | officielle, verbatim (anglais) | S-01 p. 525 |
| D-20 | barrières à l'entrée | officielle, verbatim (anglais) | S-01 p. 47 |
| D-21 | base d'actifs régulés, charges de capital normatives | réglementaire, verbatim | S-07 p. 18 |

Ambiguïtés qui persistent : la délimitation du « marché particulier » de
D-01 est un choix de l'analyste, que la grille traite en imposant de dire
l'objet classé (C-01) ; « coût raisonnable » dans D-05 n'est quantifié que
par l'étude sectorielle ; les échelles de captivité (D-08) restent à
chiffrer ; les traductions des définitions anglophones sont de travail
(L-07).

## 3. Sources

Seize sources (S-01 à S-16), figées le 2026-09-04 (S-01..S-07) et le
2026-09-05 (S-08..S-16) dans `../data/raw/` avec empreinte sha256
recalculée au build du site.

| Id | Source | Date | Ce qu'on en tire | Limite |
|---|---|---|---|---|
| S-01 | OCDE, Glossary of Statistical Terms, 2008 (PDF, 605 p.) | 2008 | D-01, D-02, D-04, D-18, D-19, D-20 | glossaire 1993 plus servi ; © OCDE, non servi par le site (L-10) |
| S-02 | Ricardo, Principes, ch. II, trad. 1847 (Wikisource, rév. 6570316) | 1817 / 1847 | D-03, D-16 | traduction, pas l'original |
| S-03 | Légifrance, CCP art. L1121-1 | version 01/04/2019 | D-09, D-10 | capture navigateur (L-08) |
| S-04 | Légifrance, CGCT art. L1411-1, L1412-1, L2221-1 | 2019 / 2025 / 1996 | D-11, D-12 | capture navigateur (L-08) |
| S-05 | Légifrance, CG3P art. L2111-1, L3111-1 | version 01/07/2006 | D-14 | capture navigateur (L-08) |
| S-06 | OpenStax, Principles of Economics 3e, § 13.3 | 2022 / page 2026-07-09 | D-06, D-17 ; ancrage de D-07, D-08 | CC BY-NC-SA, clause anti-ingestion ; capture navigateur |
| S-07 | CRE, délibération n° 2025-77 (TURPE 7 HTB) | 2025-03-13 | D-13, D-15, D-21, O-01 | propre au transport d'électricité |
| S-08 | ART, Économie des concessions autoroutières, 3e éd. | 2024-12-02 | O-03 ; régime des autoroutes (H-17) | figure 1.2 non extraite en texte |
| S-09 | ARCEP, décision n° 2025-2047, via le JORF (Légifrance) | 2025-10-28 / JORF 2026-02-14 | O-02 | PDF de l'ARCEP inaccessible (pare-feu) ; capture navigateur du JORF |
| S-10 | Eaufrance, Quel prix pour l'eau ? (SISPEA 2022) | 2024-09-12 | O-04 ; H-03, H-08 | chiffres par mode de gestion dans les rapports SISPEA, non figés |
| S-11 | Carpentier, Nauges, Reynaud, Thomas, Économie & Prévision 174 (Persée) | 2006 | O-05 ; méthode de H-03 | page Persée, PDF intégral non figé |
| S-12 | Sénat, rapport n° 709 (2019-2020), p. 130 | 2020-09-16 | O-06 | — |
| S-13 | FIPECO, Fallait-il concéder et privatiser les autoroutes ? | s. d. | O-07 | source secondaire (L-12) |
| S-14 | IGEDD, Tunnel de Friggit (FAQ) | 2022 / m. à j. 2025-08-01 | O-08 | séries non figées |
| S-15 | Sénat, rapport n° 498 (2025-2026), PPL hydroélectricité | 2026-04-01 | O-09 ; régime hydro (H-14) | promulgation non vérifiée (L-12) |
| S-16 | ART, glossaire « monopole naturel » | s. d. | caveat de D-01 | définition par le régime, non par le coût |

Sources envisagées et non enregistrées : Demsetz, « Why regulate
utilities? » (1968) — pas d'accès libre chez l'éditeur, vérifié le
2026-09-05 ; les sources de la note privée sur le parc social (à
enregistrer avant tout usage chiffré, CR-3).

## 4. Transformations

Aucune. Ce cadrage ne transforme aucune donnée.

## 5. Hypothèses

Vingt hypothèses dans `../sources/hypotheses.yaml` : cinq directrices
(H-01..H-05), un paramètre et deux ordres de grandeur (H-06..H-08), douze
hypothèses de classement (H-09..H-20). Règles adoptées après la revue :
justification par S, O ou I seulement ; limites dans `limitations` ;
confiance « moyenne » seulement si une observation figée porte l'énoncé ;
chaque hypothèse qualitative dit ce qui la réfuterait.

| Id | Hypothèse directrice | Confiance | Justification | Limites |
|---|---|---|---|---|
| H-01 | Là où l'infrastructure n'est pas duplicable (ou la ressource fixe) ET où le prix n'est pas administré, le prix se décorrèle du coût — test par D-15 avec témoin | faible | O-08 | L-11 |
| H-02 | La mise en concurrence des concessions déplace la rente sans la supprimer | faible | O-06, O-07 | — |
| H-03 | À service, ressource, investissement et fiscalité comparables, la délégation coûte plus cher que la régie | faible | O-04, O-05 | L-06 |
| H-04 | Un parc à loyers administrés ne discipline les loyers privés que s'il est OUVERT et assez large | faible | — | L-03 |
| H-05 | Le coût système serait mieux optimisé par un opérateur intégré — question de recherche, non fondée | faible | — | — |

| Id | Nom | Centrale | Plage | Unité | Confiance | Justification |
|---|---|---|---|---|---|---|
| H-06 | `reference_return_on_capital` | 5,0 | 4,0 – 8,8 | % nominal avant impôts | moyenne | O-01, O-02, O-03 (L-11) |
| H-07 | `open_stock_price_maker_threshold` | — | — | qualitative | faible | — (L-03) |
| H-08 | `water_delegation_gross_price_gap` | 10 | 0 – 27 | % du prix, écart brut | faible | O-04, O-05 (L-06) |

Pourquoi : H-06 est le taux de référence de D-15 — deux régulateurs
convergent sur sa valeur centrale (O-01, O-02), sa borne haute est le haut
de l'intervalle du TRI projet des autoroutes (O-03) ; la mesure au taux
reconnu est nulle par construction sur un secteur régulé (L-11). H-07 a
perdu sa valeur numérique : l'ancienne fourchette (30-40 % du parc
locatif) était contredite par les deux observations disponibles (France,
Vienne) et la variable est l'ouverture, pas la part. H-08 est un écart
BRUT, pas une rente ; sa plage inclut zéro.

Les hypothèses de classement H-09 à H-20 (une par ligne de l'inventaire,
dont deux témoins) sont toutes de confiance faible, sauf H-17 (autoroutes,
moyenne : O-03, O-06, O-07) et H-13/H-14 qui s'appuient sur O-01 et O-09.

## 6. Résultats

Aucun. Les mesures (M-xx) et résultats (R-xx) relèvent des études
sectorielles (`../INTRO.md` §9).

## 7. Sensibilité

Non calculable ici ; mais deux sensibilités structurantes sont connues
d'avance et documentées par des observations :

- au **taux de référence** H-06 : sur les autoroutes, le taux reconnu par
  l'État a varié de 6,5 à 5,9 % (O-06) et l'intervalle du TRI projet va de
  5,3 à 8,8 % (O-03) — aux deux bornes de H-06, une même concession peut
  montrer un surprofit ou un déficit ;
- à la **base d'actifs** : au prix de cession de 2006, le rendement des
  actionnaires apparaît ordinaire ou négatif (O-07) ; au coût historique
  net des subventions (D-15, D-21), la rente apparaît — c'est pourquoi la
  base est fixée par la définition et non laissée au choix.

Chaque étude sectorielle présentera sa mesure aux deux bornes, au taux
reconnu par son régulateur, et avec sa sensibilité à la base.

## 8. Interprétation

Neuf observations (O-01 à O-09), trois interprétations :

- **I-01** — lecture d'ensemble de l'inventaire : la grille révisée répond
  « non » deux fois (témoins), sépare la fixité du monopole naturel (trois
  lignes), ne classe l'électricité qu'une fois le réseau séparé de la
  production ; aucune ligne n'est confirmée avant son étude sectorielle
  (L-04, L-09). La version antérieure disait la grille « applicable et
  discriminante » alors qu'elle répondait « non » dix fois sur dix ;
- **I-02** — les télécommunications comme cas à instruire, non cas
  témoin : trois faits à figer peuvent retourner la lecture ;
- **I-03** — attribuer un surprofit (D-15) à une position est une
  interprétation, qui exige un témoin et le contrôle des causes
  concurrentes ; sans témoin, H-01 n'est pas réfutable.

Ce qu'elles ne montrent pas : aucune rente, aucun destinataire, aucun
montant. Inférence prudente : la grille est applicable et sait désormais
répondre « non » ; la définition mesurable est fixée dans sa forme ; rien de
plus.

## 9. Implications de conception

Cinq choix (C-01 grille révisée ; C-02 notions construites et D-15 ; C-03
logement : rente de position, parc ouvert faiseur de prix, quatre
configurations ; C-04 ordre des études ; C-05 quatre configurations
comparées et configurations à instruire par secteur) et six valeurs (V-01
à V-06), chaque C et I portant sa clause « ce qui le renverserait ». Ce que
les données ne tranchent pas : ces valeurs et ces choix de méthode. Ce qui
reste politique et est dit tel : la destination de la rente (V-01, V-05).
Les contraintes normatives de `../INTRO.md` §11 ont deux nœuds (V-02, V-06) ;
les autres relèvent de l'article ultérieur sur la mise en œuvre.

## 10. Limites et objections

Douze limites (L-01 à L-12) dans `claims.yaml` : brevet et plateformes hors
périmètre (sans assertion) ; seuil de bascule sans estimation ; régimes
actuels sourcés pour deux lignes seulement ; orbite et spectre sans
source ; écart régie / délégation ≠ rente ; traductions et notions
construites ; captures navigateur ; propriétés physiques affirmées sans
source ; redistribution du PDF OCDE non établie ; D-15 mesure un
surprofit, cas d'échec connus ; observations de second rang.

**Critiques examinées** : la revue contradictoire du 2026-09-04 — quatre
relecteurs indépendants, 58 objections (7 bloquantes, 33 sérieuses, 18
mineures), toutes intégrées sur décision de Rémy ; compte rendu avec
dispositions dans `revue-contradictoire-2026-09-04.md`. Les objections
anticipées par la note d'origine sont reprises dans l'article (section
« Objections anticipées »), avec, pour chacune, ce qui la tranche ; celles
qui ne sont pas reprises y sont listées avec leur renvoi.

**Données écartées et pourquoi** : les chiffres logement de la note
d'origine (Vienne 60 %, 80 % au plafond, 27,8 €/m², un tiers à 40 %, prix
×2,3 / ×2,6, 3,5 % / 50 %, 58 %) — contredits par les sources figées du
dépôt ou sans source (`../INTRO.md` §12) ; les chiffres de la note privée
sur le parc social (31 %, 43 %, ~50 %) retirés des hypothèses parce que
leurs sources ne sont pas enregistrées ici (CR-3) ; la fourchette 30-40 %
de l'ancien H-07 (HD-5) ; l'ancien index de pages OCDE (HD-8).

**Validations supplémentaires nécessaires** : toutes — c'est l'objet des
études sectorielles ; en premier, les autoroutes (S-08, S-12, S-13 et les
comptes des concessionnaires) et l'eau (rapports SISPEA).

## 11. Reproduction

Pas de commande de calcul. Contrôle des registres au build du site :

```bash
cd site && pnpm content        # dérive le graphe du post ; échoue sur référence non résolue ou empreinte sha256 divergente
```

Vérification indépendante possible avec les schémas de l'étude `logement`
(mêmes formats pour les sources, définitions et paramètres chiffrés ; les
hypothèses qualitatives et les champs `constructed_by` / `redistributable`
/ `limitations` des hypothèses ne sont pas dans son schéma pydantic, voir
`../CLAUDE.md`).

Fichiers produits : aucun. Environnement : aucun (documents et registres
seulement). Version : commit portant ce document dans le dépôt
`metabolisme` ; le tag de publication (`monopoles-cadrage-v1.0`) sera posé
avec le post, après relecture.
