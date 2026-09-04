# Monopoles naturels et collectivisation des rentes — document de preuve du cadrage

*Version du 2026-09-04. Document de preuve (méthode Métabolisme, INTRO
§11) de l'article de cadrage
[`../articles/2026-09-monopoles-naturels-grille.md`](../articles/2026-09-monopoles-naturels-grille.md).
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
communes, grille d'identification, définition mesurable de la rente,
position normative isolée, gabarit des études sectorielles. Périmètre : le
cadrage seul ; aucun secteur n'est instruit.

## 2. Définitions

Quatorze définitions (D-01 à D-14), toutes dans `../sources/definitions.yaml`.

| Id | Terme | Nature | Source |
|---|---|---|---|
| D-01 | monopole naturel | officielle, verbatim (anglais) | S-01, index PDF 346 |
| D-02 | rente économique | officielle, verbatim (anglais) | S-01, index PDF 452 |
| D-03 | rente de position | construite (C-02), ancrée sur Ricardo | S-02, p. 38 (1847) |
| D-04 | rente d'innovation | construite (C-02), ancrée sur la quasi-rente | S-01, index PDF 452 |
| D-05 | substituabilité de l'infrastructure | construite (C-02), dérivée de D-01 | S-01 |
| D-06 | rivalité | manuel, verbatim (anglais) | S-06 |
| D-07 | différenciabilité du bien livré | construite (C-02) | S-06 (ancrage faible, voir caveats) |
| D-08 | captivité de l'usager | construite (C-02) | S-06 (ancrage faible, voir caveats) |
| D-09 | concurrence pour / sur le marché | littérature + citation juridique | S-03 |
| D-10 | contrat de concession | légale, verbatim | S-03, CCP L1121-1 (01/04/2019) |
| D-11 | régie | légale, verbatim | S-04, CGCT L1412-1 (03/05/2025) + L2221-1 |
| D-12 | délégation de service public | légale, verbatim | S-04, CGCT L1411-1 (01/04/2019) |
| D-13 | coût moyen pondéré du capital reconnu par un régulateur | réglementaire, verbatim | S-07, index PDF 4 et 9 |
| D-14 | domaine public | légale, verbatim | S-05, CG3P L2111-1 + L3111-1 (01/07/2006) |

Ambiguïtés qui persistent : la délimitation du « marché particulier » de
D-01 (infrastructure seule ou infrastructure et service) est un choix de
l'analyste, que la grille tranche en séparant les deux (C-01) ; « coût
raisonnable » dans D-05 n'est pas quantifié ; les traductions des
définitions anglophones sont de travail (L-07).

## 3. Sources

Sept sources (S-01 à S-07), toutes figées le 2026-09-04 dans `../data/raw/`
avec empreinte sha256, dans `../sources/sources.yaml`.

| Id | Source | Date | Ce qu'on en tire | Limite |
|---|---|---|---|---|
| S-01 | OCDE, Glossary of Statistical Terms, 2008 (PDF, 605 p.) | 2008 | D-01, D-02, D-04 (entrées reprises du glossaire Khemani & Shapiro 1993) | glossaire de 1993 plus servi (HTTP 410) ; pas d'entrée « public good », « switching cost », « franchise bidding » |
| S-02 | Ricardo, Principes, ch. II, trad. 1847 (Wikisource, rév. 6570316) | 1817 / 1847 | D-03 (citation d'ouverture) | traduction, pas l'original |
| S-03 | Légifrance, CCP art. L1121-1 | version 01/04/2019 | D-09, D-10 | capture navigateur (L-08) |
| S-04 | Légifrance, CGCT art. L1411-1, L1412-1, L2221-1 | 2019 / 2025 / 1996 | D-11, D-12 | capture navigateur (L-08) |
| S-05 | Légifrance, CG3P art. L2111-1, L3111-1 | version 01/07/2006 | D-14 | capture navigateur (L-08) |
| S-06 | OpenStax, Principles of Economics 3e, § 13.3 | 2022-12-14 | D-06 ; ancrage de D-07, D-08 | CC BY-NC-SA ; page rendue par navigateur |
| S-07 | CRE, délibération n° 2025-77 (TURPE 7 HTB) | 2025-03-13 | D-13, O-01 | propre au transport d'électricité |

Source envisagée et non enregistrée : Demsetz, « Why regulate utilities? »
(1968), accès payant ; la distinction concurrence pour / sur le marché
(D-09) est donc portée par sa seule partie juridique.

## 4. Transformations

Aucune. Ce cadrage ne transforme aucune donnée.

## 5. Hypothèses

Cinq hypothèses directrices qualitatives (H-01 à H-05, `../INTRO.md` §7,
hors registre) et trois paramètres chiffrés (`../sources/hypotheses.yaml`).

| Id | Nom | Centrale | Plage | Unité | Confiance | Justification |
|---|---|---|---|---|---|---|
| H-06 | `normal_return_on_capital` | 5,0 | 4,0 – 8,0 | % nominal avant impôts | moyenne | O-01, D-13, C-02 |
| H-07 | `price_maker_share_threshold` | 35 | 30 – 40 | % du parc locatif | faible | L-03, C-03 |
| H-08 | `water_delegation_cost_gap` | 15 | 10 – 20 | % du prix à qualité comparable | faible | L-06 |

Pourquoi : H-06 est le terme « normale » de la définition mesurable de la
rente (C-02) — sans lui, rien n'est mesurable. H-07 et H-08 sont les deux
ordres de grandeur de la note d'origine conservés comme paramètres nommés,
avec une confiance faible parce qu'aucune source ne les porte encore.

## 6. Résultats

Aucun. Les mesures (M-xx) et résultats (R-xx) relèvent des études
sectorielles (`../INTRO.md` §9).

## 7. Sensibilité

Non calculable ici ; mais la sensibilité structurante est connue d'avance :
toute mesure de rente dépend de H-06, et deux points de taux peuvent faire
disparaître ou doubler une rente sur un actif capitalistique
(`../INTRO.md` §15). Chaque étude sectorielle présentera sa mesure aux deux
bornes de la plage.

## 8. Interprétation

Une observation (O-01 : CMPC de RTE à 5,0 % au TURPE 7, 4,6 % au TURPE 6),
deux interprétations :

- **I-01** — classement provisoire des dix secteurs par la grille ; chaque
  ligne est une hypothèse, pas un résultat (limité par L-04) ;
- **I-02** — les télécommunications comme cas où la grille décrit un
  dispositif existant (limité par L-04).

Ce qu'elles ne montrent pas : aucune rente, aucun destinataire, aucun
montant. Inférence prudente : la grille est applicable et discriminante
(elle ne classe pas tous les secteurs de la même façon) ; rien de plus.

## 9. Implications de conception

Quatre choix (C-01 grille ; C-02 notions construites et définition
mesurable de la rente ; C-03 logement : parc faiseur de prix, privé
conservé, trois configurations ; C-04 ordre des études) et quatre valeurs
(V-01 à V-04). Les contraintes que tout système devra respecter sont dans
`../INTRO.md` §11 (propriété d'usage, continuité du service, règle
publique, chaque mesure tient seule, transparence des fins). Ce qui reste
politique : la destination de la rente (V-01), explicitement.

## 10. Limites et objections

Huit limites (L-01 à L-08) dans `claims.yaml` : brevet hors périmètre ;
plateformes non éprouvées ; seuil de bascule sans estimation ; régimes
actuels non sourcés ; orbite et spectre sans autorité ni source ; écart
régie / délégation sans source et biaisé par la sélection ; définitions
traduites et notions construites ; captures Légifrance non reproductibles
par script.

Objections examinées (article, section « Objections examinées ») :
concurrence entre logements → H-01 comme test ; étatisme → V-03 ; efficacité
de la gestion publique → H-03 / L-06 ; spoliation → V-02 ; mise en
concurrence des concessions → H-02. Validations supplémentaires
nécessaires : toutes — c'est l'objet des études sectorielles.

Données écartées et pourquoi : les chiffres logement de la note d'origine
(Vienne 60 %, 80 % au plafond en zone tendue, 27,8 €/m² à Paris, un tiers à
40 %, prix ×2,3 / ×2,6, 3,5 % / 50 %, 58 %) — contredits par les sources
déjà figées du dépôt ou sans source ; consignés dans le préambule de
`../exploration/2026-09-grille-deux-questions-note-de-travail.md` et dans
`../INTRO.md` §12.

## 11. Reproduction

Pas de commande de calcul. Contrôle des registres :

```bash
cd site && pnpm content        # dérive le graphe du post depuis monopoles/ ; échoue sur référence non résolue
```

Vérification indépendante possible avec les schémas de l'étude `logement`
(mêmes formats) : charger les quatre registres avec `SourceRecord`,
`DefinitionRecord`, `HypothesisRecord`, `ClaimRecord` de
`logement/src/logement/models.py`, résoudre les références, recomparer les
empreintes de `../data/raw/` — exécuté le 2026-09-04 : 7 sources, 14
définitions, 3 hypothèses, 19 nœuds, aucune erreur.

Fichiers produits : aucun. Environnement : aucun (documents et registres
seulement). Version : commit portant ce document dans le dépôt
`metabolisme` ; le tag de publication sera posé avec le post.
