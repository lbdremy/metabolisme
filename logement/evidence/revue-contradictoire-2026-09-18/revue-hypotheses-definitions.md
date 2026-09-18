# Revue contradictoire du 2026-09-18 — relecteur « hypothèses et définitions »

Méthode : étape 12 de la chaîne de preuves exécutable (INTRO §14),
angle « hypothèses, définitions, statuts épistémiques » (INTRO §1.3,
§4, §8, §9, §15). Relecture seule, sans accès aux autres relecteurs ;
aucun fichier du dépôt n'a été modifié en dehors de ce rapport.

Lu, dans l'ordre : `INTRO.md` (§1.3, §4, §8, §9, §15, §17, §21) ;
`logement/INTRO.md` (§3, §16, §17) ; `logement/CLAUDE.md` ;
`logement/EVIDENCE.md` ; `logement/evidence/decisions-2026-09-18.md`
(DEC-01..DEC-13) ; le bloc « Session 7 » de `evidence/claims.yaml`
(l. 2041-2451 : V-02..V-04, C-11..C-14, O-37..O-40, T-17, R-15..R-17,
I-15..I-17, L-27..L-31, P-01) ; `sources/sources.yaml` S-39..S-46 (et
S-09, S-18, S-22, S-23, S-28 pour le contexte) ;
`sources/definitions.yaml` D-19..D-22 (et D-10) ;
`sources/hypotheses.yaml` H-06..H-18 en entier ;
`src/logement/core/institution.py` ; `build_institution` dans
`src/logement/shell/build.py` (l. 842-950) ; les constantes de
`core/remob.py` (l. 40-46) ; l'artefact
`data/processed/scenarios-institutionnels-ze.json` ; les sections
« R-15 à R-17 » (l. 1098-1177) et « 9. Implications de conception »
(l. 1350-1379) du document de preuve ; les nœuds antérieurs cités
(R-07, R-09, R-14, C-06, C-07, C-10, I-09, I-10, I-14, L-14..L-20,
L-25) ; `tests/test_institution.py` (noms des tests).

Vérifications à la main (aucun recalcul lourd) : facteur d'annuité
(2,30 % / 40 ans → 0,03851 ✔ ; 30 ans → 0,04651 ✔) ; surface implicite
du segment neuf au loyer médian publié ; variante « charges fixes » de
H-18 ; numérateur/dénominateur des « années équivalentes » de R-17 ;
quatre passages des PDF figés relus au texte (`pdftotext`) : S-18
(surface et prix au m² du logement social), S-22 (les 6 700 sorties
ZLV et leur dénominateur), S-40 (schéma p. 15), S-46 (avantages du
bail — TFPB, nue-propriété).

---

## Objections

### HD-1 — majeure — « Le neuf s'équilibre au marché » est un artefact de surface : 169 200 € (S-18) divisés par la surface moyenne du parc de la ZE (~96 m²) au lieu des 66 m² de surface utile que ce prix paie

**Énoncé.** Le loyer d'équilibre du segment neuf est calculé en
divisant l'annuité d'un logement social neuf à 169 200 € par la
surface mixte de la ZE (part maison × 114,3 + (1 − part) × 65,5 m²,
constantes S-12 du parc OCCUPÉ). Or le PDF figé S-18 dit
explicitement (p. 10-11 du rendu texte) : « Le prix de revient moyen
par mètre carré d'un logement social est passé de 2 300 €/m² à
2 550 €/m² de surface utile » et « La surface moyenne des logements
financés est quasi stable sur la période, autour de 66 m² de surface
utile par logement ». Le prix par logement et la surface par logement
de la MÊME source ne sont pas appariés : le loyer au m² du neuf est
sous-estimé d'environ 96/66 ≈ 1,45.

**Preuve.** `core/institution.py` l. 211-220 (surface_m2 = mix S-12 ;
`loyer_equilibre_{segment}_m2 = annual / 12 / surface_m2` pour les
deux segments, `neuf` compris, l. 215-218) ; `core/remob.py` l. 40-45.
Vérification : au central, annuité neuf = 169 200 × 0,03851 =
6 516 €/an ; /(1 − 0,549) = 14 448 €/an = 1 204 €/mois ; la médiane
publiée 12,47 €/m² (artefact, `m_b_operateur_acquisition.central.loyer_equilibre_neuf_m2.median`)
implique une surface de 1 204 / 12,47 = 96,5 m². Au prix au m² de la
source (2 550 €/m² SU) : 2 550 × 0,03851 / 0,451 / 12 = 18,1 €/m²/mois,
au-dessus du marché médian (12,29). La phrase « le segment NEUF
s'équilibre à 12,47 €/m² ≈ le marché » (R-16, `claims.yaml` l. 2231 s.),
reprise par I-15 (l. 2302 : « s'équilibre au loyer de marché sans
subvention d'investissement »), par P-01 (l. 2423 s. : « R-16 : le neuf
s'équilibre au loyer de marché ») et par le document de preuve
(l. 1368), ne tient pas sur la source citée.

Le même défaut touche le segment rénové : le prix médian DVF est
celui d'un logement vendu de surface inconnue (ni 65,5 ni 114,3), et
L-18 rappelle que le vacant durable est plus petit encore ; la
surface est ici une hypothèse enfouie (voir HD-13) alors que la
chaîne dispose déjà de `prix_m2_median` (`core/transaction.py` l. 213)
et de coûts de rénovation en €/m² (H-09/H-10) — le loyer d'équilibre
au m² du segment rénové peut se calculer SANS surface.

**Disposition.** Recalculer (relecteur statistique) les deux loyers au
m² en €/m² de bout en bout : neuf = 2 550 €/m² SU (S-18, à enregistrer
dans O-38 ou une O-41) ; rénové = prix DVF au m² × H-15 + coût de
rénovation au m² (H-09/H-10 actualisés) ; ne garder les surfaces que
pour les totaux par logement. Reformuler R-16, I-15, P-01 (étage 3),
EVIDENCE.md et le .qmd l. 1368 selon le résultat. Tant que ce n'est
pas fait, requalifier l'énoncé « le neuf s'équilibre au marché » en
limite (L-30) et retirer la justification « R-16 » de l'étage 3 de P-01.

### HD-2 — majeure — H-18 applique des charges PROPORTIONNELLES au loyer à un loyer 2,9 × plus élevé que celui qui a produit le ratio : le modèle attribue à l'opérateur ~3 × les charges du secteur, et la conclusion « au-dessus du marché dans les 93 ZE » ne survit pas à une modélisation en charges fixes

**Énoncé.** Le ratio 54,9 % (S-40, p. 15) est observé sur un loyer net
moyen du parc social (~6,43 €/m² en ZE tendues, O-40). Les postes qu'il
agrège ne sont pas proportionnels au loyer : les charges de gestion
sont un coût par logement, la maintenance un coût par m² et par an, la
TFPB une fonction de la valeur locative cadastrale. Appliqué à un loyer
d'équilibre de 18,34 €/m², H-18 charge l'opérateur de 10,07 €/m²/mois
de frais d'exploitation (18,34 × 0,549), contre 3,53 €/m²/mois pour le
secteur qui a fourni le ratio (6,43 × 0,549). L-30 admet le sens
(« SURESTIME […] majorant ») mais pas l'ampleur : l'écart est un
facteur ~3 sur le poste dominant du loyer.

**Preuve.** `core/institution.py` l. 87-91 (`equilibrium_rent =
annuity / (1 − operating_share)`) ; `hypotheses.yaml` l. 363-388
(H-18, « Les charges sont supposées proportionnelles au loyer ») ;
`claims.yaml` L-30 l. 2391 s. Vérification à la main (variante
« charges en € du secteur, annuité recalculée ») : rénové =
18,34 × 0,451 + 3,53 = 11,80 €/m² (< marché 12,29, contre 18,34
publié) ; neuf = 12,47 × 0,451 + 3,53 = 9,15 €/m² (avec la surface
de HD-1 corrigée : 2 550 × 0,03851 / 12 + 3,53 = 11,7 €/m² ≈ marché).
Les deux titres de R-16 (« au-dessus du marché dans les 93 ZE »,
« ratio médian 1,44 ; 2,81 × le social ») et la subvention d'équilibre
2,38 Md€/an dépendent donc d'un choix de forme fonctionnelle que ni
DEC-06 ni C-13 ne présentent comme tel : DEC-06 compare (a) « ignorer
les charges », (b) « un coût en €/logement de la littérature » et (c)
la structure en %, et écarte (b) parce que « le document ne publie
pas ce ratio au grain voulu » — or S-40 publie précisément des
montants (maintenance 4,2 Md€ en 2023, p. 19, notée dans S-40
`notes`) pour un parc de 5,6 M de logements, soit ~750 €/logement/an,
et le ratio de gestion 27,8 % d'un loyer net moyen connu se convertit
en €/logement.

**Disposition.** Requalifier H-18 : confiance `low` (pas `medium`) ;
scinder en deux paramètres, H-18a « charges de gestion + maintenance
en €/logement/an » (central dérivé de S-40 : 27,8 % + 15,5 % du loyer
net moyen 2023 du macro-organisme, ou 4,2 Md€/5,6 M pour la
maintenance) et H-18b « TFPB » (en % de la valeur locative, ou
exonérée — S-46 pour le bail, cf. HD-13), et publier le loyer
d'équilibre sous les DEUX formes fonctionnelles (proportionnelle =
majorant, fixe = plancher) comme la chaîne l'a fait pour la règle
mixte de C-07. Réécrire DEC-06 (l'option (b) a été écartée sur un
motif inexact). I-15 et P-01 ne doivent plus affirmer « paie au prix du
marché » tant que la fourchette n'est pas publiée.

### HD-3 — majeure — H-14 cite un dénominateur qui n'est pas celui de la source : les « 3 % » de S-22 sont des sorties parmi les logements dont les PROPRIÉTAIRES ONT ÉTÉ CONTACTÉS, pas « du stock ciblé en zone tendue » ; et M-A n'est pas un scénario de « prolongement des tendances »

**Énoncé.** H-14 (central 0,75 %/an) est justifiée ainsi : « la Cour
des comptes (S-22) chiffre ~6 700 sorties de vacance attribuables au
dispositif ZLV en 4 ans, soit ~3 % du stock ciblé en zone tendue
(L-17), donc 0,75 %/an en linéaire ». Le PDF figé dit autre chose :
« Entre 2020 et 2024, 6700 logements identifiés grâce à ZLV sont
sortis de vacance, représentant 6,6 % des 102 000 logements dont les
propriétaires ont été contactés » ; et, sur l'enquête de 28 104
logements contactés (note 44), « 12 % des propriétaires en zone
détendue ont accepté d'être accompagnés, pour 6 % de logements sortis
de vacance in fine (contre respectivement 4,7 % et 3 % dans les zones
tendues) ». Le 3 % est un rendement PAR CAMPAGNE DE CONTACT, sur les
logements contactés, pas un taux annuel sur le gisement ; le
convertir en 0,75 %/an « linéaire » sur 10-20 ans suppose (i) que
tout le gisement est contacté, (ii) que le rendement se reproduit
chaque année sans épuisement des propriétaires réceptifs — deux
hypothèses non écrites. De plus, ZLV est un outil de repérage et de
contact ; la Cour dit de la TLV (le canal incitatif fiscal proprement
dit) que sa « montée en puissance effective […] n'a en rien endigué le
phénomène » : H-14 mêle deux instruments sous le nom
`incentive_channel_exit_rate`.

Second point, de statut : R-15 se présente comme « la référence
“prolongement des tendances” » (INTRO logement §16, scénario de
référence). Or M-A ne modélise ni les sorties naturelles de vacance
(hors dispositif) ni les entrées (L-29 : « Les flux d'entrée en
vacance ne sont pas soustraits ») ; le stock LOVAC a en réalité
augmenté entre millésimes (R-02 : 1,15 → 1,18 M). M-A mesure le
rendement MARGINAL d'un canal, pas la tendance ; un vrai scénario de
référence aurait un besoin qui bouge (L-19) et un gisement qui bouge.

**Preuve.** `hypotheses.yaml` l. 260-284 ; S-22 (`data/raw/cour-des-comptes-logements-vacants-2025.pdf`,
passage « Entre 2020 et 2024, 6700 logements… 6,6 % des 102 000
logements dont les propriétaires ont été contactés » et note 44) ;
`claims.yaml` R-15 l. 2213 s. (« la référence “prolongement des
tendances” ne détend pas ») ; L-17 l. 1278 s. (« ~3 % de taux de sortie
en zone tendue ») porte la même lecture erronée.

**Disposition.** À sourcer et recentrer : réécrire la justification de
H-14 avec le bon dénominateur (3 % des logements contactés en zone
tendue, 6,6 % toutes zones, par campagne 2020-2024) ; expliciter les
deux hypothèses de conversion (couverture des contacts = 100 % ;
rendement constant d'une campagne à l'autre) — la seconde justifie une
borne basse plus basse que 0,25 %/an ou une décroissance ; renommer
(`outreach_campaign_exit_rate…`) ; corriger L-17 dans le même sens.
Requalifier R-15 : « rendement du canal de contact + fiscalité
existante », et retirer « prolongement des tendances » (ou construire
le vrai scénario de référence avec flux, en L-19). Le verdict I-15
(« le canal incitatif ne peut pas être le mécanisme de la détente »)
survit probablement — mais il doit être re-dérivé sur la bonne base.

### HD-4 — majeure — « Le repli rend l'offre de bail préférable à la cession » (I-16, P-01) est une hypothèse comportementale sans source, présentée comme interprétation ; l'architecture de P-01 « tient à cet enchaînement »

**Énoncé.** I-16 (l. 2317) : la contrainte de repli « fixe le prix de
sortie du propriétaire (la valeur vénale) et rend l'offre de bail
préférable à la cession ». P-01 (l. 2423 s.) : « c'est le repli qui
rend l'offre préférable et sécurise le volume ». Rien dans la chaîne
n'établit la préférence d'un propriétaire entre (a) recevoir
aujourd'hui la valeur vénale sans décote (H-15 = 1,0) et (b) confier
son bien 30 ans sans loyer (S-46 : l'avantage du propriétaire est de
« ne pas supporter les charges », pas de percevoir un revenu) pour le
récupérer rénové. Pour un héritier en indivision (~20 % du gisement,
S-23), pour un propriétaire âgé, ou dans une ZE à prix stables, (a)
domine (b) ; la chaîne dit elle-même que le consentement au bail « n'a
aucune source » (L-29, DEC-09). L'enchaînement offre → repli est
donc un CHOIX de conception (C) reposant sur une hypothèse
QUALITATIVE (le précédent existe : `monopoles/sources/hypotheses.yaml`
accepte des hypothèses qualitatives disant ce qui les réfuterait). Il
manque aussi deux paramètres de conception que P-01 nomme sans les
fixer : le « délai » avant repli, et les cas d'exemption (vacance
« indépendante de la volonté du propriétaire », motif d'exonération
de TLV rappelé par S-22 note 45 ; successions en cours).

**Preuve.** `claims.yaml` l. 2306-2321 (I-16), l. 2423-2450 (P-01) ;
`definitions.yaml` D-21 l. 431-457 (caveat « Outil VOLONTAIRE ») ;
S-46 (« conserve la nue-propriété du bien mais ne supporte pas les
charges durant la durée du bail »).

**Disposition.** Créer C-15 « enchaînement offre de bail → repli par
acquisition → arbitrage neuf » (l'architecture de P-01 n'a aujourd'hui
aucun nœud C propre : C-11..C-14 sont des choix de chiffrage) ; créer
une hypothèse qualitative H-19 « préférence du propriétaire pour le
bail face à une cession à la valeur vénale », avec ce qui la
réfuterait (taux d'adhésion observé < x % dans une expérimentation
ZLV/BAR), rattachée à L-29 ; retirer de I-16 la clause « rend l'offre
préférable » ou la reformuler « vise à rendre » ; ajouter à P-01 le
délai et les exemptions comme paramètres nommés (C), même non chiffrés.

### HD-5 — sérieuse — R-17 compare un péage fiscal TOTAL (départemental + communal + frais d'assiette + CSI) à une charge calibrée sur le seul produit DÉPARTEMENTAL : les « 33 ans d'équivalence » sont surévalués d'environ un quart, et le « péage résiduel 1,02 mois » contredit L-28 (2)

**Énoncé.** `annees_equivalentes = peage_fiscal_eur / charge` où
`peage_fiscal_eur = prix_median × taux_dmto_pct/100 + CSI` et
`taux_dmto_pct` est le taux TOTAL H-13 (6,32 % = 5,00 départemental +
1,20 communal + frais d'assiette), tandis que `charge = 9,9 Md€ / parc`
ne redistribue que la part départementale (S-39, L-28 (2) : « seule la
part départementale est basculée (la taxe communale 1,20 % et les
frais d'assiette restent) »). Le numérateur contient donc ~1,3 point
de prix qui n'est pas basculé. Symétriquement, le « péage RÉSIDUEL
(émoluments seuls) » de R-17 (l. 2270) suppose que la taxe communale
et la CSI disparaissent aussi.

**Preuve.** `core/institution.py` l. 492-499 ; `core/transaction.py`
l. 164 (`dmto_total_rate_pct`) ; `claims.yaml` L-28 l. 2359 s. (point
2) et R-17 l. 2261 s. Vérification : prix médian implicite 9 419 /
0,0642 ≈ 146 700 € ; part départementale seule 5,00 % → 7 335 € ;
7 335 / 286 = 25,6 ans (contre 32,9 publié).

**Disposition.** Recalculer avec un numérateur homogène (droit
départemental seul, taux S-31 territorialisé) et un résiduel qui
conserve communal + frais d'assiette + CSI + émoluments ; ou, si la
bascule vise tout le péage fiscal, changer C-14 et le produit (il
faudrait alors ajouter la part communale au 9,9 Md€, ce que S-39 ne
donne pas). Reformuler R-17/I-17 (« 5,15 → 1,02 mois »). D-19 porte
déjà la décomposition — la définition est bonne, c'est le calcul qui
ne la respecte pas.

### HD-6 — sérieuse — Deux hypothèses enfouies dans `DMTO_PRODUCT_2024_EUR` : (i) 100 % du produit est assis sur le logement ; (ii) l'année 2024, « point BAS du cycle » de l'aveu de S-39, est le seul étalon

**Énoncé.** (i) Les DMTO départementaux frappent toutes les mutations
immobilières (locaux commerciaux, terrains, immeubles entiers), pas les
seuls logements ; rapporter la totalité du 9,9 Md€ au parc de
logements suppose une part résidentielle de 100 % — hypothèse ni
nommée ni sourcée, qui gonfle la charge par logement. (ii) S-39 dit
lui-même que « 2021-2022 étaient des records » et que le produit 2024
est « un point BAS du cycle » ; la charge de 286 €/logement/an et les
33 ans d'équivalence sont inversement proportionnels à ce choix
d'année. L'un et l'autre sont des paramètres au sens d'INTRO §9
(« Une hypothèse ne doit pas être enfouie dans une formule »), et
S-39 couvre « les évolutions 2021-2024 » : la matière d'une plage est
dans le fichier figé.

**Preuve.** `core/institution.py` l. 48-51 (constante) et l. 488 ;
`sources.yaml` S-39 `notes` (« point BAS du cycle […] la bascule est
calibrée sur ce point bas ») ; L-28 (1) l. 2359 s. (mentionne le point
bas, sans sensibilité) ; aucun DEC ne porte le choix de l'année.

**Disposition.** Créer H-20 « produit DMTO départemental de référence »
(central 9,9 Md€ 2024, plage tirée des exercices 2021-2024 de S-39) et
H-21 « part du produit DMTO assise sur le logement » (à sourcer — DGFiP
ou S-43 s'il ventile ; à défaut plage déclarée, confiance `low`) ;
propager les deux dans R-17 comme sensibilité ; ajouter un DEC.

### HD-7 — sérieuse — P-01 annonce une subvention d'équilibre « ≤ 2,4 Md€/an au pire cas », mais l'artefact publie 4,12 Md€/an au coin défavorable des hypothèses

**Énoncé.** P-01 (l. 2439), le .qmd (l. 1371) et EVIDENCE.md (l. 445)
écrivent « ≤ 2,4 Md€/an au pire cas tout-acquisition ». « Pire cas »
désigne ici le mix de mécanismes, au central des hypothèses ; mais
la sensibilité publiée dans le même artefact donne
`sensibilite.defavorable.subvention_equilibre_social_mdeur_an = 4.12`
(H-15 = 1,0, H-16 = 2,81, H-17 = 30, H-18 = 0,60). R-16 cite le coin
défavorable pour le loyer (26,73 €/m²) mais tait sa subvention. Une
borne « ≤ » qui n'est pas la borne de la plage publiée viole INTRO §15
(« Toute donnée sensible à une hypothèse importante doit être
accompagnée d'une fourchette »).

**Preuve.** `data/processed/scenarios-institutionnels-ze.json`,
`m_b_operateur_acquisition.sensibilite.defavorable` ; `claims.yaml`
l. 2231 s. (R-16) et l. 2439 (P-01).

**Disposition.** Reformuler : « 2,4 Md€/an au central, 0,07-4,1 sur
les coins H-15..H-18 (avant HD-1/HD-2) » dans R-16, P-01, EVIDENCE.md
et le .qmd ; supprimer « pire cas ».

### HD-8 — sérieuse — V-02 affirme qu'« aucun mécanisme comparé ne touche un logement occupé » : M-D crée une charge annuelle sur CHAQUE logement, résidences principales occupées comprises ; la tension avec le « droit à l'ancrage » (§17) n'est pas nommée, et la « charge de détention » n'a ni définition ni redevable

**Énoncé.** V-02 (l. 2053) ne vaut que pour M-B. M-D fait payer
286 €/logement/an au ménage qui reste — V-03 le reconnaît (« le
perdant est le ménage qui reste ») mais présente ce transfert comme
un arbitrage justifié par la mobilité volontaire, sans le confronter à
la contrainte voisine du même §17, « Droit à l'ancrage : les liens
avec un lieu […] doivent être considérés comme des usages réels » —
une charge sur la détention est, littéralement, une taxe sur
l'ancrage. La chaîne n'a pas non plus dit CE QU'EST la charge : un
impôt nouveau ? une majoration de TFPB ? Qui la doit (propriétaire,
occupant, bailleur social, résidence secondaire) ? DEC-07 choisit
l'assiette « tous les logements » pour ne pas « changer l'incidence
sans le dire », mais l'incidence sur les propriétaires occupants
modestes (retraités notamment) n'est pas dite non plus. INTRO §1.3
demande que « les arbitrages qui restent politiques » soient nommés.

**Preuve.** `claims.yaml` V-02 l. 2048-2055, V-03 l. 2057-2066, C-14
l. 2130-2145 ; `logement/INTRO.md` §17 « Droit à l'ancrage » ;
`decisions-2026-09-18.md` DEC-07 l. 143-157 ; `definitions.yaml` :
aucune entrée « charge de détention ».

**Disposition.** Reformuler V-02 (« aucun mécanisme d'ACQUISITION… ;
M-D touche tous les logements par une charge, cf. V-03/V-05 ») ; créer
V-05 « arbitrage mobilité / ancrage » explicitant que M-D taxe la
détention et ce que la conception fait des propriétaires occupants
modestes (exemption ? plafonnement ? — un C ultérieur, dont l'effet
sur l'assiette et donc sur la charge doit être annoncé) ; créer D-23
« charge de détention » (nature, redevable, assiette, articulation
avec la TFPB et l'IFI) ; compléter L-28 par l'incidence intra-ménages.

### HD-9 — sérieuse — Statuts : R-15..R-17 sont des SIMULATIONS hypothétiques non étiquetées ; I-15 contient un choix de conception et une affirmation que R-16 n'établit pas ; I-17 invoque une « durée de détention médiane du ménage mobile » qu'aucun nœud ne mesure

**Énoncé.** (a) INTRO §15 : « Toute estimation doit indiquer si elle
est : observée ; calculée ; extrapolée ; simulée ; hypothétique. »
R-01..R-14 sont des mesures sur données figées ; R-15..R-17 sont des
scénarios sur cinq paramètres nouveaux à confiance basse ou moyenne.
Ni les titres (« investissement 44,6 Md€ », « charge de
286 €/logement/an ») ni EVIDENCE.md ne portent le mot « simulé » ; le
.qmd dit « chiffrés ». (b) I-15 (l. 2287-2304) affirme que
« l'opérateur, en portant à la fois le gisement et les friches, peut
arbitrer logement par logement » — c'est une capacité de conception
(un C), pas une lecture de R-16 — et que « le segment neuf sur friches
s'équilibre au loyer de marché » alors que R-16 chiffre le neuf au
prix S-18, dont L-30 dit lui-même que ce n'est « pas un prix sur friche
dépolluée (S-25 : + 780 k€/ha) » (et cf. HD-1). (c) I-17 (l. 2329) :
« un point d'équivalence (33 ans…) qui dépasse la durée de détention
médiane du ménage mobile » — aucun R/O ne mesure cette durée (R-11
mesure l'ancienneté d'emménagement du STOCK, D-16 : « rotation du
parc, pas mobilité des personnes »).

**Preuve.** `claims.yaml` l. 2213-2285, 2287-2304, 2323-2343 ;
`EVIDENCE.md` l. 420-446 ; `.qmd` l. 1100-1106.

**Disposition.** Préfixer les titres R-15..R-17 par « [simulé] » (ou
ajouter un champ `estimate_kind` au schéma des claims — un petit
changement de `models.py`, à décider) ; déplacer « arbitrer logement
par logement » dans le C-15 proposé en HD-4 ; remplacer « neuf sur
friches » par « neuf au prix S-18 (hors surcoût friche, L-15/L-30) » ;
sourcer ou supprimer la « durée de détention médiane » d'I-17.

### HD-10 — sérieuse — Quatre notions porteuses de la proposition n'ont pas de définition : « loyer d'équilibre » (enfoui dans D-20 comme « construction de l'étude »), « opérateur collectif », « gisement effectif », « valeur vénale » (assimilée au prix médian des ventes par un caveat, pas par un nœud)

**Énoncé.** INTRO §8 : « Les définitions doivent être documentées et
identifiées. » (a) D-20 mélange une définition de source (loyer net
quittancé, S-40) et une construction de l'étude (« La chaîne appelle
“loyer d'équilibre” […] construction de l'étude, pas une définition
de la source ») : une définition qui contient un modèle est un C
déguisé, et l'on ne peut la changer (HD-2) sans toucher un D. (b)
« Opérateur collectif » n'est défini nulle part ; or sa forme
juridique décide de tout le chiffrage : l'accès au prêt PLUS (S-41 :
organismes de logement social), l'agrément L365-2 du CCH exigé du
preneur d'un bail à réhabilitation (S-46), l'exonération de TFPB
(S-46 : « peut bénéficier d'une exonération […] pendant toute la durée
du bail »), le régime des droits de mutation à l'acquisition (L-27),
la TVA sur travaux. (c) « Gisement effectif » (LOVAC × H-12) est
défini dans C-06/H-12 mais pas dans le registre, alors que R-15 et
R-16 le prennent pour assiette. (d) D-22 définit l'expropriation, pas
la « valeur vénale » ; l'égalité valeur vénale = prix médian DVF des
logements vendus dans la ZE (biens plus grands, plus récents, en état
— L-18/L-27) est posée dans un caveat (« valeur vénale = prix médian
local DVF, C-12 ») : c'est une hypothèse, pas une définition.

**Preuve.** `definitions.yaml` D-20 l. 403-430 (phrase « construction
de l'étude »), D-22 l. 458-481 (caveat 1) ; `grep` de « opérateur
collectif », « gisement effectif », « charge de détention » dans
`definitions.yaml` : aucune entrée.

**Disposition.** Créer D-23 « loyer d'équilibre (construction de
l'étude) » — ou, mieux, le sortir des D pour n'en faire qu'un C-13
étendu — et ramener D-20 à la seule citation de S-40 ; créer D-24
« opérateur collectif de détente » (forme juridique retenue et ce
qu'elle emporte : PLUS, agrément L365-2, TFPB, DMTO, TVA) avec un C
si la forme est un choix ; créer D-25 « gisement effectif » ; D-26
« valeur vénale » (citation d'une source de droit — Légifrance non
figé, cf. S-08 ; à défaut, S-45 suffit) en notant que l'assimilation
au prix médian est C-12/H-15 ; D-27 « charge de détention » (HD-8).

### HD-11 — sérieuse — Trois loyers de définitions différentes sont comparés comme s'ils étaient homogènes : loyer d'annonce CHARGES COMPRISES (S-09), loyer social HORS CHARGES (S-28 `loymoy`), loyer d'équilibre NET DE VACANCE (D-20)

**Énoncé.** S-09 `notes` : « loypredm2 = loyer prédit €/m² charges
comprises ». Le loyer RPLS est un loyer principal hors charges
récupérables. Le loyer d'équilibre est un loyer net « déjà corrigé
des pertes de loyers liées à la vacance » (D-20) et hors charges
récupérables. Les ratios « équilibre / marché » (1,44) et « équilibre /
social » (2,81), les comptes de ZE « sous le marché » et la
subvention d'équilibre (écart au social) mélangent donc des assiettes
différentes : le marché charges comprises est surévalué de l'ordre des
charges récupérables (il faudrait le déflater) ; l'équilibre net de
vacance est un loyer ENCAISSÉ, qu'il faut majorer de la vacance de
l'opérateur pour obtenir un loyer AFFICHÉ (S-28 : vacance RPLS 2,12 %
au 01/01/2025). Aucune définition, aucun choix, aucune limite ne le
dit ; le sens net du biais n'est pas trivial (le premier joue contre la
conclusion « au-dessus du marché », le second pour).

**Preuve.** `sources.yaml` S-09 `notes` (« charges comprises ») ;
`definitions.yaml` D-20 ; `core/institution.py` l. 229-234 (ratios
bruts) ; C-13 l. 2113-2128 (« comparé au loyer de marché (S-09, mix
C-05) et au loyer social (S-28) ») sans mention des assiettes.

**Disposition.** Créer D-28 « loyer : assiettes comparées » (annonce
CC / principal HC / net quittancé), ajouter une hypothèse H-22 « part
des charges récupérables dans un loyer d'annonce charges comprises »
(à sourcer — l'OLL ou S-09 si une variante HC existe) ou, à défaut,
une limite L-32 explicite avec le sens des deux biais ; propager la
vacance de l'opérateur (taux RPLS S-28) dans le passage net → affiché.

### HD-12 — sérieuse — Cohérence décisions ↔ graphe : plusieurs choix consommés par R-15..R-17 n'ont ni DEC ni nœud C ; et P-01 n'a pas de C propre

**Énoncé.** Le journal promet « chaque choix entre plusieurs options
est consigné ici ». Vérifié : DEC-03→C-11, DEC-04→C-12/H-15,
DEC-05→C-13/H-16/H-17, DEC-06→C-13/H-18, DEC-07→C-14, DEC-08→H-14,
DEC-10→C-13, DEC-11→C-14/L-28, DEC-12→C-11 : cohérents. Manquent, en
revanche — décidés dans le code ou le texte sans trace :
1. la référence de la subvention d'équilibre au loyer SOCIAL (et non au
   marché ou à un loyer intermédiaire) — porté par V-04/C-13 mais aucun
   DEC n'expose l'alternative ;
2. la grille de consentement 10/25/50/100 % « sans central » (DEC-09)
   n'a pas de nœud C alors qu'elle structure R-16 et L-29 ;
3. le choix des surfaces S-12 comme dénominateur des €/m² (HD-1) ;
4. le choix du péage TOTAL au numérateur des années équivalentes et du
   « résiduel = émoluments seuls » (HD-5) ;
5. le choix de l'année 2024 et de la part résidentielle 100 % (HD-6) ;
6. l'application des centraux H-16/H-18 seuls à M-C, sans sensibilité,
   alors que M-C est l'étage 1 de P-01 (`build.py` l. 943-944 :
   `_load_hypothesis(root, "H-16").central_value`) ;
7. l'ARCHITECTURE de P-01 (trois étages, ordre, délai, exemptions)
   n'a aucun nœud C : P-01 dépend de C-11..C-14 (des choix de
   chiffrage) et tire son enchaînement d'une interprétation (I-16,
   HD-4). Inversement, DEC-01/DEC-02/DEC-13 sont des décisions de
   procédure, correctement hors graphe.

**Preuve.** `decisions-2026-09-18.md` l. 3-14 (engagement), DEC-09
l. 172-182 (« Trace : R-16, L-29 » — pas de C) ; `claims.yaml` P-01
`depends_on` l. 2450 ; `build.py` l. 943-944.

**Disposition.** Ajouter DEC-14..DEC-18 pour les points 1, 3, 4, 5, 6 ;
créer C-15 (architecture de P-01, HD-4) et C-16 (grille de
consentement descriptive, avec la raison du « pas de central ») ;
publier la sensibilité H-16/H-18 (et H-19 durée du bail, HD-13) pour
M-C.

### HD-13 — sérieuse — Constantes du code qui sont des paramètres : `BAR_AMORTISATION_YEARS`, `SURFACE_MAISON_M2`/`SURFACE_APPART_M2` ; et H-18 appliqué au bail avec la TFPB que S-46 dit exonérée

**Énoncé.** (a) `BAR_AMORTISATION_YEARS = 30` : DEC-10 la justifie
comme « valeur, pas plage » (S-46 : « entre 12 et 99 ans, en moyenne
30 ans »). Mais dans P-01 la durée du bail est un terme que
l'OPÉRATEUR fixe (« bien rendu rénové après 30 ans ») — c'est un choix
de conception, et le loyer M-C y est sensible (facteur d'annuité 30 →
40 ans : 0,0465 → 0,0385, − 17 %). INTRO §9 vaut pour toute valeur
« introduite dans le modèle ». (b) `SURFACE_MAISON_M2 = 114,3`,
`SURFACE_APPART_M2 = 65,5` (S-12, parc occupé) sont des constantes
depuis C-07 ; elles étaient neutres pour un ratio (R-09), elles
deviennent PORTEUSES pour un loyer au m² (HD-1) et L-18 dit qu'elles
ne décrivent pas le gisement. (c) `lease_scenario` reçoit H-18 central
(0,549, TFPB 11,6 comprise) alors que S-46 précise que le preneur
« peut bénéficier d'une exonération de la TFPB pendant toute la durée
du bail » et que H-18 réserve sa borne basse à ce cas : incohérence
interne entre la source de M-C et le paramètre qu'on lui applique.
`TLV_YIELD_2023_EUR` et `DMTO_PRODUCT_2024_EUR` sont des observations
(O-37) et peuvent rester des constantes — sous réserve de HD-6 pour la
seconde ; `HORIZON_YEARS_GRID`, `CONSENT_SHARE_GRID`, `DISCOUNT_GRID`
sont des grilles descriptives, statut acceptable (précédent R-14) à
condition d'un nœud C (HD-12, point 2).

**Preuve.** `core/institution.py` l. 41-62, l. 425 ; `core/remob.py`
l. 40-41 ; `build.py` l. 943-944 ; S-46 (« exonération de la taxe
foncière sur les propriétés bâties (TFPB) pendant toute la durée du
bail ») ; `hypotheses.yaml` H-18 l. 372-374 (« borne basse = opérateur
exonéré de TFPB »).

**Disposition.** Créer H-19 « durée du bail à réhabilitation »
(central 30, plage [20 ; 40] par exemple, justification S-46 + choix
de conception, confiance `low`) et la propager dans M-C ; soit
promouvoir les surfaces en H (avec la borne L-18 vers le bas), soit
les rendre inutiles en calculant au m² (HD-1) ; appliquer à M-C la
borne basse de H-18 ou une variante « hors TFPB » (0,549 − 0,116 =
0,433) et le dire dans C-13.

### HD-14 — sérieuse — Hypothèses implicites du modèle financier non listées par L-30

**Énoncé.** Outre celles que L-30 nomme (Livret A figé, pas
d'inflation, charges proportionnelles, pas de subvention
d'investissement, pas de valeur résiduelle, TFPB), le modèle suppose
sans le dire :
1. occupation à 100 % dès l'année 1 — le loyer d'équilibre est un
   loyer NET DE VACANCE (D-20), l'opérateur doit afficher plus (HD-11) ;
2. zéro impayé — S-40 p. 15 isole « Risques locatifs − 2,2 » HORS des
   54,9 de charges, et H-18 ne les reprend pas (les « autres
   produits + 2,4 » non plus : le solde est ~nul, mais il faut le dire) ;
3. pas de coût de portage : 136 000 acquisitions puis rénovations et
   58 000 constructions produisent des loyers dès le premier jour
   (intérêts intercalaires d'un chantier de 12-24 mois : ~2,3 % ×
   44,6 Md€ ≈ 1 Md€ d'ordre de grandeur, une fois) ;
4. programme instantané : l'annuité 1,72 Md€/an vaut pour tout le stock
   d'un coup ; une montée en charge sur N années change le profil, pas
   le total (à dire) ;
5. droits de mutation payés par l'opérateur à l'acquisition (L-27 le
   nomme, mais le régime dépend de la forme juridique — HD-10 b) ;
6. TVA : 5,5 % sur les travaux (L-14 (3) : 10 % hors énergie), et TVA
   sur le neuf (S-18 est un prix de revient TTC pour du logement
   social — à confirmer sur la source) ;
7. aucun renouvellement de composants à 20-25 ans au-delà de l'effort
   de maintenance de 15,5 % (sur 40 ans, un gros entretien est
   certain) ;
8. loyer social local S-28 pris comme loyer d'attribution de
   l'opérateur (V-04) sans ses plafonds réglementaires (PLAI/PLUS/PLS)
   — le « social médian 6,43 » mêle les trois.

**Preuve.** S-40 p. 15 (schéma : « Risques locatifs − 2,2 », « Autres
produits 2,4 ») ; `core/institution.py` l. 199-228 (aucun terme de
vacance, d'impayé, de portage) ; `claims.yaml` L-30 l. 2391-2407.

**Disposition.** Compléter L-30 des points 1-8 avec le sens de chaque
biais ; promouvoir en H ceux qui ont une source figée (vacance :
S-28 ; impayés : S-40 2,2 %) ; laisser en L ceux qui n'en ont pas
(portage, montée en charge) ; ajouter à O-38 les deux postes ignorés
du schéma p. 15 pour que le lecteur voie que 100 = 54,9 + 43,8 + 1,5
+ 2,2 − 2,4.

### HD-15 — sérieuse — Le besoin de 194 488 est un besoin de STOCK ; P-01 l'admet (L-19 dans ses limites) mais ne donne pas l'ordre de grandeur du flux que son propre étage 3 (« construire ») devrait porter

**Énoncé.** P-01 est honnête sur le principe (« Ce que la proposition
NE démontre PAS : […] le flux de construction nécessaire au-delà du
stock (L-19) »). Mais tous ses chiffres financiers (44,6 Md€, 1,72
Md€/an, subvention ≤ 2,4 Md€/an) sont ceux d'une opération UNIQUE de
rattrapage, mis en regard de flux annuels récurrents (271 M€ de TLV,
9,9 Md€ de DMTO). L-19 chiffre déjà le flux (~140 000 ménages
supplémentaires par an dans les ZE tendues) : au prix S-18, c'est de
l'ordre de 140 000 × 169 200 € ≈ 24 Md€ d'investissement PAR AN,
c'est-à-dire plus, chaque année, que tout le programme de stock. Un
« opérateur de détente » qui construit sur friches est de fait un
opérateur de FLUX ; le taire dans les ordres de grandeur laisse croire
que 44,6 Md€ « détendent ».

**Preuve.** `claims.yaml` L-19 l. 1313 s. (« ~140 000 ménages
supplémentaires par an ») ; P-01 l. 2423-2450 (chiffres) ; C-11
l. 2082-2097 (« le besoin de 194 488 logements […] et non sur une
définition nouvelle du besoin »).

**Disposition.** Ajouter à P-01 (et à L-19) l'ordre de grandeur du
flux au prix S-18 en le qualifiant de « extrapolé » (INTRO §15), et
dire que le programme de stock est un rattrapage à côté d'un flux
qu'il ne finance pas ; qualifier l'étage 3 d'outil de flux.

### HD-16 — mineure — H-15 : la plage [0,5 ; 1,0] est justifiée par des rapports de cotes de S-23 (probabilité d'être vacant) qui ne mesurent pas une décote de prix

**Énoncé.** H-15 (l. 296-299) : « la borne basse représente l'état
dégradé et la petite taille des vacants durables (S-23 : × 2,8 si
< 35 m², × 3,3 si avant 1900 — L-18), qui abaissent la valeur vénale
sous la médiane ». Les × 2,8 et × 3,3 sont des multiplicateurs de la
probabilité d'être durablement vacant, pas des rapports de prix ; ils
justifient le SENS de la décote, pas sa valeur 0,5. La plage est donc
plausible mais non sourcée (DEC-04 le reconnaît : « aucune source
ouverte figée ne mesure la décote »). Le central 1,0 « conservateur »
n'est majorant que du côté de la valeur du bien ; du côté du prix
PAYÉ, les indemnités accessoires et de remploi (D-22), non chiffrées,
jouent en sens inverse — L-27 le dit, H-15 non.

**Preuve.** `hypotheses.yaml` l. 286-312 ; `sources.yaml` S-23 `notes`.

**Disposition.** À sourcer : reformuler la justification (« sens
documenté par S-23, valeur 0,5 = convention de sensibilité ») ; noter
dans H-15 que 1,0 n'est pas un majorant du prix payé ; garder la
confiance `low`.

### HD-17 — mineure — H-16 : la plage [1,50 ; 2,81] couvre les marges PLAI-PLS au Livret A du jour, mais pas le Livret A lui-même, qui était à 3,00 % il y a dix-huit mois

**Énoncé.** H-16 le dit (« pas la révision future du Livret A ») et
L-30 aussi, mais une plage « plausible » (INTRO §9) sur 40 ans
d'annuité qui exclut la valeur observée de 2023-2024 (Livret A 3,00 %
→ PLUS 3,60 %) est trop étroite ; la confiance `medium` est celle du
taux du jour, pas du taux de l'emprunt.

**Preuve.** `hypotheses.yaml` l. 314-336 ; S-42 (« après plusieurs
baisses successives en 2025 et au début de l'année 2026 »).

**Disposition.** À élargir : plage [1,50 ; 3,60] (PLAI au Livret A bas ;
PLUS au Livret A 2023-2024, à sourcer par une page Banque des
Territoires ou Banque de France figée) ; propager.

### HD-18 — mineure — M-A : sorties non plafonnées par le besoin LOCAL ; assiette TLV (> 1 an) ≠ gisement D-10 (> 2 ans) ; nom de H-14

**Énoncé.** (a) `incentive_scenario` applique H-14 au gisement effectif
agrégé (206 664) et compare au besoin agrégé (194 488) ; les sorties
d'une ZE dont le gisement dépasse le besoin local comptent pour
d'autres ZE — contraire à la règle mixte C-07 que C-11 dit reprendre.
Sans effet numérique au central (7,5 % du gisement), mais à 2,50 %/an
× 20 ans (50 %) le plafond local mordrait. (b) Les 271 M€ de TLV
frappent 810 000 logements vacants depuis plus d'UN an en zone TLV
(S-22), pas le gisement D-10 (> 2 ans) des ZE tendues C-06 : O-37 met
côte à côte deux assiettes. (c) `incentive_channel_exit_rate` — cf.
HD-3, c'est un rendement de campagne de contact.

**Preuve.** `core/institution.py` l. 125-162 ; S-22 (« assujettis à la
TLV […] 810 000 en 2024 ; […] 271 M€ ») ; O-37 l. 2147-2155.

**Disposition.** Plafonner par ZE (min(sorties, besoin local)) dans
T-17 ; préciser l'assiette de la TLV dans O-37 ; renommer H-14.

---

## Tableau des hypothèses (session 7)

| Id | Nom | Central | Plage | Confiance déclarée | Verdict | Motif |
|----|-----|---------|-------|--------------------|---------|-------|
| H-14 | incentive_channel_exit_rate_pct_per_year | 0,75 %/an | [0,25 ; 2,50] | low | **à sourcer** (et à recentrer) | dénominateur de S-22 mal lu (logements CONTACTÉS, par campagne) ; conversion annuelle linéaire non explicitée ; mêle ZLV et TLV (HD-3, HD-18) |
| H-15 | vacant_acquisition_price_discount_factor | 1,0 | [0,5 ; 1,0] | low | **à sourcer** | central défendable (valeur vénale, S-45) ; borne 0,5 justifiée par des rapports de cotes qui ne sont pas des prix (HD-16) ; « conservateur » à nuancer (L-27) |
| H-16 | operator_borrowing_rate_pct | 2,30 % | [1,50 ; 2,81] | medium | **à élargir** | plage = marges PLAI-PLS au Livret A du 01/08/2026 ; exclut le Livret A 2023-2024 (3,00 %) sur un emprunt à 40 ans (HD-17) ; confiance à ramener à low |
| H-17 | operator_amortisation_years | 40 ans | [30 ; 50] | medium | **tenable** | central = durée bâti PLUS (S-41), bornes sourcées ; mais la durée du bail (30 ans, M-C) doit devenir H-19 (HD-13) |
| H-18 | operator_operating_cost_share_of_net_rent | 0,549 | [0,40 ; 0,60] | medium | **à recentrer** (forme fonctionnelle) | central fidèle à S-40 p. 15, mais appliqué à un loyer ~3 × plus élevé en proportionnel : surestimation d'un facteur ~3 des charges ; à scinder charges fixes €/logement + TFPB ; borne haute 0,60 non sourcée ; TFPB à exclure pour M-C (S-46) ; confiance à ramener à low (HD-2, HD-13) |
| (constante) | BAR_AMORTISATION_YEARS | 30 | — | — | **à créer H-19** | terme du bail fixé par l'opérateur = choix ; S-46 donne 12-99, moyenne 30 (HD-13) |
| (constante) | SURFACE_MAISON/APPART_M2 | 114,3 / 65,5 | — | — | **à créer H ou à supprimer** | porteuses des €/m² de R-16 ; ne décrivent ni le vacant (L-18) ni le neuf S-18 (66 m² SU) (HD-1, HD-13) |
| (constante) | DMTO_PRODUCT_2024_EUR | 9,9 Md€ | — | — | **à créer H-20/H-21** | point bas du cycle (S-39) ; part résidentielle implicite 100 % (HD-6) |
| (implicite) | vacance / impayés / portage de l'opérateur | 0 | — | — | **à créer H ou L** | S-40 (risques locatifs 2,2), S-28 (vacance 2,12 %) donnent des centraux ; portage sans source → L (HD-14) |
| (implicite) | préférence bail vs cession du propriétaire | — | — | — | **à créer H qualitative** | porte l'enchaînement de P-01 ; aucune source (HD-4) |

Hypothèses antérieures réutilisées sans changement (H-08, H-09, H-10,
H-12 aux centraux ; DEC-12) : conformes à leur registre ; la
non-propagation de H-09/H-10 dans R-16 est justifiée (6,0 Md€ sur
44,6) mais celle de H-08/H-12 (qui fixent le BESOIN, facteur ~4,6 sur
la plage H-08 d'après R-09) n'est pas discutée par DEC-12 — à dire
dans C-11.

---

## Verdict global

La session 7 est méthodologiquement exemplaire dans sa forme (cinq
mécanismes comparés avant tout choix, journal des décisions,
sensibilités une-à-une, limites nommées) mais deux de ses trois
résultats clés reposent sur des défauts d'appariement d'unités et de
forme fonctionnelle qui inversent ou effacent leurs titres : « le neuf
s'équilibre au marché » (surface S-18 non appariée, HD-1) et
« l'opérateur paie au prix du marché dans 93 ZE sur 93 » (charges
proportionnelles, HD-2), tandis que H-14 cite un dénominateur que la
source ne dit pas (HD-3) et que l'enchaînement offre → repli de P-01
tient à une préférence des propriétaires que rien n'établit (HD-4).

Rien n'est irrémédiable : les corrections sont locales (calcul au m²
de bout en bout, charges en € + TFPB, bonne lecture de S-22,
numérateur départemental pour R-17), les sources figées contiennent
déjà ce qu'il faut (S-18 p. 10-11, S-40 p. 15 et 19, S-22, S-39
2021-2024), et les statuts se réparent par des nœuds (C-15 pour
l'architecture de P-01, H-19..H-22, D-23..D-28, V-05, L-32).

Tant que HD-1..HD-4 ne sont pas traitées, P-01 ne devrait pas être
publié avec ses chiffres actuels ; I-15 et I-16 doivent être
requalifiées en conjectures ; R-15..R-17 doivent porter la mention
« simulé ». V-01 et les contraintes §17 sont respectées par M-B/M-C ;
M-D est en tension non nommée avec le droit à l'ancrage (HD-8) — un
arbitrage politique à afficher, pas à cacher dans V-03.
