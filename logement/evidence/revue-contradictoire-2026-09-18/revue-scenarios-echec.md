# Revue contradictoire — scénarios d'échec (session 7, proposition P-01)

Relecteur « scénarios d'échec » (méthode INTRO étape 12 et §13.4 :
« un scénario dans lequel la proposition échoue »), 2026-09-18, sans
accès aux autres relecteurs. État examiné : arbre de travail non commité
après `265d6e1` (session 7 : `core/institution.py`,
`scenarios-institutionnels-ze.json`, bloc « Session 7 » de
`claims.yaml`, H-14..H-18, `decisions-2026-09-18.md`, § R-15..R-17 et
§ 9 du qmd).

## Méthode et matière lue

Lu dans l'ordre demandé : `INTRO.md` (§1.2, §13.4, §15-18),
`logement/INTRO.md` (§3, §7, §16-18), `logement/EVIDENCE.md`,
`evidence/decisions-2026-09-18.md` (DEC-01..DEC-13), le bloc
« Session 7 » de `evidence/claims.yaml` (V-02..V-04, C-11..C-14,
O-37..O-40, T-17, R-15..R-17, I-15..I-17, L-27..L-31, P-01) et, plus
haut, I-07, I-09, I-10, L-12, L-14, L-16..L-21 ; H-14..H-18 dans
`sources/hypotheses.yaml` ; `src/logement/core/institution.py` en
entier ; l'artefact `data/processed/scenarios-institutionnels-ze.json`
(clés `perimetre`, `m_a_*`, `m_b_*`, `m_c_*`, `m_d_*`) ; les sections
« R-15 à R-17 » et « 9. Implications » du qmd ; le compte rendu
`revue-contradictoire-2026-08-09.md` (et le tableau de la revue du
2026-08-07 pour L-14..L-21). Recalculs faits avec `uv run python`
depuis `logement/` sur `institution.annuity_factor` /
`equilibrium_rent` et les artefacts figés ; deux vérifications de
source dans le PDF S-18 (`pdftotext`).

Angle unique : **dans quel monde P-01 échoue-t-elle, et le texte le
dit-il ?** Pour chaque objection je distingue ce qui est déjà nommé
(L-27..L-31, L-19, L-20 — « bien nommé, mais visible ? ») de ce qui
manque. Je ne reviens pas sur ce que les revues des 2026-08-07/09 ont
tranché (H-08 sans meilleure source, H-12, unité L-18 pour R-07, les
requalifications I-11..I-14) : je ne les cite que là où la session 7
les réactive.

Ce que les recalculs confirment : **l'arithmétique publiée est exacte**
(facteur d'annuité 0,03851 ; 286 €/logement ; 33/44 ans ; 15 500
sorties M-A ; 4,22 €/m² M-C ; subvention 2,38 Md€/an). Comme aux deux
revues précédentes, les objections portent sur les modèles, les
unités et la mise en récit, pas sur les calculs.

---

## Objections

### SE-1 — Le segment neuf ne « s'équilibre pas au marché » : erreur d'unité entre S-18 et la surface C-07

**Gravité : majeure.** C'est la phrase porteuse de I-15 (« le segment
neuf sur friches s'équilibre au loyer de marché sans subvention
d'investissement »), reprise dans R-16, P-01 (« R-16 : le neuf
s'équilibre au marché ») et le qmd § 9.

**Énoncé.** Le loyer d'équilibre du neuf est calculé dans
`operator_frame` comme `169 200 € × af / (1 − H-18) / 12 / surface_m2`,
où `surface_m2` est le mix des résidences principales de la ZE
(`part_maison × 114,3 + (1 − part_maison) × 65,5`, C-07). Or S-18 donne
ce prix « par logement » pour des logements sociaux dont « la surface
moyenne des logements financés est quasi stable […] autour de 66 m² de
surface utile » et un prix « de 2 550 €/m² de surface utile » (PDF
S-18, texte extrait, lignes 146-147 et 278-279). Le modèle divise donc
le prix d'un logement de 66 m² par une surface de 96 m² (surface
implicite du loyer médian publié : 14 446 €/an ÷ 12 ÷ 12,47 = 96,5 m²).

**Preuve (recalcul).** À 66 m², le loyer d'équilibre du neuf est
**18,2 €/m²/mois** (14 446 / 12 / 66 = 18,24) — au-dessus du loyer de
marché médian (12,29) dans toutes les ZE tendues, et égal au segment
rénové (18,34). L'artefact le confirme ZE par ZE : Lens 11,37 €/m² pour
le neuf correspond à une surface de 106 m² (part_maison 0,83) ; Annecy
14,22 à 85 m². Autrement dit le « neuf au marché » est d'autant plus
vrai que la ZE est pavillonnaire, ce qui n'a aucun rapport avec le
coût d'un logement social. Conséquences : (a) le pôle favorable de
P-01 (« ≈ 0 si le bail domine et le neuf prend le déficit ») tombe —
au loyer social le neuf demande ~0,54 Md€/an (11,81 €/m² × 12 × 66 m²
× 57 945) au lieu des 0,41 publiés, et **~0,27 Md€/an rien que pour
atteindre le marché** ; (b) l'« arbitrage logement par logement »
d'I-15 perd son étage : rénové et neuf s'équilibrent au même loyer.

**Aggravation territoriale (non nommée).** Le 169 200 € est une
moyenne nationale ; S-18 lui-même écrit qu'« un logement social [en
zone A bis] coûte environ 50 % de plus qu'en zone A », et « l'écart
entre la zone A et B1 est de l'ordre de 20 % » (lignes 372-377). Les
97 ZE tendues sont en A/A bis/B1 : le prix de revient qui leur revient
est supérieur à la moyenne (ordre de grandeur, en décomposant la
moyenne aux poids publiés 6/30/37/15/12 % : zone A ≈ +8 %, A bis
≈ +60 %). L-14 nomme le biais « social vs libre », pas le biais
territorial.

**Dépollution (bien nommée dans L-30, non chiffrée).** S-25 : 780 k€
HT/ha de remise en état (médiane ~400 k€), projets résidentiels
2,5 × plus chers. À la densité constatée 30,3 log/ha : **+25,7 k€ par
logement (+15 %)**, +64 k€ (+38 %) au coefficient résidentiel ; à
H-11 (147,2 log/ha) : +5,3 k€ (+3 %), +13,2 k€ (+8 %). Combiné à la
surface de 66 m² : 21-25 €/m² pour le neuf sur friche dépolluée à la
densité constatée. L-30 le dit « en creux » ; I-15 et P-01 disent le
contraire en clair.

**Disposition.** Recalcul de T-17 : surface du segment neuf = 66 m²
(S-18) ou coût = 2 550 €/m² × surface C-07 (les deux sont
cohérents, le résultat est le même en €/m²) ; publier la variante
« dépollution 30,3 log/ha » dans la sensibilité de R-16 ; **retirer**
de I-15, R-16, P-01 et du qmd § 9 « le neuf s'équilibre au loyer de
marché » ; nouvelle limite (ou L-30 complétée) : prix de revient
national appliqué à des ZE de zones A/A bis/B1 — direction : favorable
au neuf, donc à l'étage (3) de P-01.

### SE-2 — L'enchaînement « offre → repli » est inversé : le repli à la valeur vénale sans décote est une aubaine, pas une menace

**Gravité : majeure.** I-16 : « [le repli] fixe le prix de sortie du
propriétaire (la valeur vénale) et rend l'offre de bail préférable à
la cession » ; P-01 : « c'est le repli qui rend l'offre préférable et
sécurise le volume ».

**Énoncé.** Aucun nœud n'établit cette préférence. Le propriétaire
d'un vacant durable compare : (a) vendre maintenant à la valeur vénale
— au central, la **médiane des logements vendus de la ZE, que L-27
qualifie de majorant** pour un bien plus petit et plus ancien ; (b) un
bail de 30 ans **sans loyer** (les 4,22 €/m² de M-C ne comportent
aucune rémunération du bailleur ; `lease_scenario` amortit les seuls
travaux), au terme duquel il récupère un bien rénové.

**Preuve (recalcul).** Bien médian : prix 204 k€ (248 038 − 43 800 de
travaux), travaux 43,8 k€. Valeur actuelle de (b) = (204 + 43,8) k€
actualisés 30 ans : **67 % de la vente à 2 %, 50 % à 3 %, 28 % à 5 %**
(sans appréciation réelle du bien). Pour tout propriétaire qui n'a pas
d'attachement patrimonial spécifique — et le gisement est biaisé vers
successions et indivisions (S-23 : ~20 %), c'est-à-dire vers des
détenteurs qui cherchent une sortie —, la cession domine. Le
mécanisme sélectionne donc **M-B, pas M-C** : le pôle « ≈ 0 si le
bail domine » n'a pas de raison d'être le cas central ; le cas
central est le tout-acquisition (44,6 Md€, 2,38 Md€/an), c'est-à-dire
le « pire cas » de P-01. Pire : ce que la chaîne appelle « repli »
est, pour un détenteur de bien dégradé payé à la médiane, un
**débouché** — la politique crée un acheteur public qui surpaie le bas
de gamme (voir SE-5).

**Ce qui est nommé.** L-29 : « le consentement au bail à
réhabilitation n'a aucune source (grille) ». Vrai, mais L-29 traite le
consentement comme une inconnue neutre ; l'arithmétique ci-dessus
donne une DIRECTION : à prix de repli = valeur vénale pleine, le
consentement au bail est structurellement bas.

**Disposition.** Requalifier I-16 : l'offre n'est préférable que si
le prix de repli est **inférieur** à ce que vaut le bail — donc soit
une valeur vénale expertisée sur le bien dégradé (H-15 < 1, ce que
C-12 n'assume pas au central), soit un loyer au propriétaire dans le
bail (à ajouter au 4,22 €/m² ; disparaît alors « sous le social
partout » ?), soit une contrainte non pécuniaire. Écrire cette
condition dans P-01 comme paramètre de conception (« l'écart de prix
offre/repli est le levier du consentement »), et dans L-29 la
direction du biais.

### SE-3 — Le repli suppose un outil de contrainte inexistant, et M-B est chiffré sans horizon alors que M-A l'est à 5/10/20 ans

**Gravité : majeure** (pour la mise en récit ; sérieuse pour le calcul).

**Énoncé.** L-29 dit bien : « le taux de remobilisation par
acquisition suppose que l'outil de contrainte existe et s'applique
(utilité publique à créer — D-22) ». Mais R-16/I-15/P-01 écrivent
« la seule voie qui SÉCURISE le volume » et « sécurise le volume » au
présent de l'indicatif, et M-B est comparé à M-A sur des bases
asymétriques : **M-A livre 8 % « en dix ans » ; M-B livre 100 % « un
jour »**. Aucun paramètre de rythme (acquisitions/an, durée d'une
déclaration d'utilité publique, capacité de portage) n'existe dans
T-17 ; le tableau qui fait tomber M-A (grille 5/10/20) n'est pas
appliqué à M-B.

**Preuve.** 136 544 acquisitions = 13 650/an sur dix ans, 6 830/an
sur vingt. La chaîne ne possède aucune source figée sur la capacité
d'acquisition publique de logements diffus (EPF, organismes de
foncier solidaire, Anah — frontière à consigner, pas à inventer). Sans
l'outil, P-01 = M-C seul = la grille de consentement, c'est-à-dire un
M-A amélioré d'un montant inconnu — et I-15 (« ne peut pas être le
mécanisme de la détente ») s'applique alors à P-01 elle-même.

**Disposition.** (i) Grille 5/10/20 ans pour M-B avec un paramètre de
rythme explicite (H-19 « acquisitions par an », plage à sourcer, ou
grille descriptive DEC-09-style si aucune source) ; (ii) requalifier
« sécurise » en « sécuriserait, si l'outil d'utilité publique existait
et s'exécutait à un rythme que la chaîne n'instruit pas » ; (iii)
nommer dans L-29 le risque juridique (proportionnalité de
l'expropriation de vacants — hors chaîne, mais c'est LE scénario
d'échec de l'étage 2).

### SE-4 — Sortie de la cible : la porte latérale « résidence secondaire / meublé » n'est pas nommée

**Gravité : sérieuse.**

**Énoncé.** Sous menace d'acquisition, un propriétaire peut sortir du
gisement autrement qu'en louant ou en vendant à l'opérateur :
déclarer une résidence secondaire, louer en meublé touristique,
« occuper » nominalement. Ces sorties vident le gisement **sans
détendre** (R-05 : c'est déjà le régime des ZE littorales et
touristiques). Or les ZE au loyer d'équilibre le plus haut de R-16 —
Annecy 29,32, Bayonne 26,97, Porto-Vecchio 26,74, La Maurienne — sont
exactement celles-là. H-12 (taux d'existence) devient **endogène** à
la politique : plus la menace est crédible, plus le taux d'existence
observé baisse (déclarations), et la chaîne l'a déjà constaté pour
la TLV (S-22 : « biais déclaratif fiscal possible en zone tendue »).

**Ce qui est nommé.** Rien dans L-27..L-31 sur ce déplacement ; L-17
parle de « rétention volontaire », pas de reclassement.

**Disposition.** Compléter L-29 (déplacement vers RS/meublé,
endogénéité de H-12 à la politique) ; dans P-01, la condition
d'articulation avec la régulation des meublés/RS (hors chaîne) ; pour
les ZE « tendues par structurelle record » (31 ZE, 37 % du gisement,
R-07) le scénario d'échec est le cas central, pas la queue.

### SE-5 — Sélection adverse : deux régimes de prix se cachent derrière « valeur vénale », et les biais ne sont pas tous du même côté

**Gravité : sérieuse.**

**Énoncé.** L-27 : « la médiane est vraisemblablement un MAJORANT, dans
le même sens que l'absence de décote ». C'est vrai **seulement** si le
prix est fixé bien par bien (expertise d'expropriation, D-22). Si
l'opérateur fait une OFFRE au prix médian de la ZE (ce que C-12 modélise
littéralement : « prix médian des logements vendus dans la ZE × H-15 »),
la sélection est adverse : n'acceptent que les détenteurs de biens
valant moins que la médiane ; l'opérateur surpaie tout ce qu'il
obtient, les biens décents attendent le repli. P-01 ne dit pas lequel
des deux régimes elle retient.

**Preuve.** Sous le régime bien par bien, le stress « réhabilitation
lourde » ×2 de L-14 s'applique précisément aux biens acquis (les
pires) : 248 038 → **~292 k€** par logement ; R-16 cite L-14 dans ses
`limitations` mais ne publie pas ce stress pour M-B (DEC-12 le juge
dominé par l'acquisition — vrai en volume, faux en sélection : les
deux se cumulent sur les mêmes biens). Sous le régime « offre à la
médiane », c'est le prix qui est biaisé vers le haut ET les travaux.
Enfin, le €/m² du segment rénové est calculé sur les surfaces du parc
OCCUPÉ (65,5/114,3 m²) alors que L-18 établit que le gisement est
biaisé vers < 35 m² : le loyer d'équilibre au m² des vrais vacants
n'est pas celui publié (signe ambigu — prix plus bas, surface plus
basse — mais la comparaison « sous/au-dessus du marché » n'est pas
établie logement par logement).

**Disposition.** Préciser C-12 (prix par bien expertisé, pas prix de
ZE) et le dire dans P-01 ; publier le stress ×2 dans la sensibilité de
R-16 ; compléter L-27 : direction du biais de sélection (prix) sous le
régime « offre », et surfaces L-18 pour le €/m².

### SE-6 — Effets d'équilibre général : la politique se défait elle-même en réussissant

**Gravité : sérieuse.**

**Énoncé.** (i) **Prix d'achat.** 13 650 acquisitions/an sur dix ans,
rapportées aux ventes des ZE tendues (ordre de grandeur : 727 209
ventes retenues en 2025 au national, C-10, dont ~40 % du parc en ZE
tendues → ~290 k/an) : ~5 % du flux — négligeable en masse, mais
l'opérateur n'achète pas « le marché » : il achète le segment petit /
ancien / vacant, où il devient un acheteur récurrent et annoncé. Le
prix payé est celui d'AVANT (DVF 2025), pas celui d'un marché qui sait
qu'un acheteur public à la médiane existe. (ii) **Loyers.** L'objet de
P-01 est de faire baisser les loyers relatifs (D-15/H-08 ; L-20 nomme
les perdants patrimoniaux). Si elle y parvient, le loyer de marché
(12,29) baisse ; le loyer d'équilibre (18,34 ; 18,2 pour le neuf
corrigé SE-1) ne bouge pas : **la subvention croît avec le succès**.
Le modèle financier compare l'opérateur à un marché figé que P-01 a
précisément pour but de déplacer.

**Ce qui est nommé.** L-20 (effet-prix, perdants) — sur les
propriétaires, jamais sur le bilan de l'opérateur ; L-30 fige les
loyers en euros courants 2025 « sur 40 ans » sans dire que le
comparateur est mobile par construction.

**Disposition.** Nouvelle L-32 : « l'opérateur est exposé au succès de
sa propre politique » ; requalifier toute comparaison au marché en
« au marché d'avant détente » ; publier une variante « marché − 10 % »
(ou à la baisse de loyer qu'impliquerait le passage de la vacance
disponible au seuil H-08, si une élasticité sourcée existe — sinon la
grille descriptive).

### SE-7 — Le besoin est un besoin de FLUIDITÉ ; l'opérateur produit de l'ATTRIBUTION sociale

**Gravité : sérieuse.**

**Énoncé.** R-07 (D-15, L-21) chiffre le volant de vacance
DISPONIBLE manquant pour que les marchés tournent. Un logement attribué
au loyer social à un ménage éligible (V-04, C-13 « ramener chaque
logement au loyer social local ») n'est pas de la vacance disponible ;
c'est une résidence principale à mobilité 7 %/an (R-12). Le gain de
fluidité passe alors par la chaîne de déménagements (l'attributaire
libère un logement) — indirect, non modélisé, et nul si l'attributaire
vient d'une autre ZE, d'une décohabitation ou de l'hébergement. La
« subvention d'équilibre » chiffre donc le coût de l'objectif
d'accessibilité (V-04), pas celui du diagnostic (fluidité). P-01
enchaîne les deux sans le dire (« Attribution au loyer social local
(V-04) »).

**Preuve (ordre de grandeur).** Écart médian au marché 6,05 €/m² contre
11,91 au social : la subvention nécessaire pour mettre les logements
**sur le marché** (l'objectif de R-07) est d'environ la moitié
(~1,2 Md€/an par rapport de médianes — à recalculer par ZE, l'artefact
ne publie pas cette variante). Et au loyer d'équilibre brut (18,34,
+44 % sur le marché), personne ne loue : les logements restent
vacants — l'échec le plus simple, non nommé.

**Disposition.** Publier deux subventions dans R-16 : « au loyer de
marché » (fluidité, R-07) et « au loyer social » (accessibilité, V-04) ;
I-15/P-01 doivent dire que les deux objectifs ne coïncident pas et que
l'attribution sociale ne produit la fluidité que par ricochet.

### SE-8 — Stock vs flux : 194 488 logements = 1,4 an de formation de ménages des ZE tendues

**Gravité : sérieuse** (bien nommé dans L-19, invisible dans P-01).

**Énoncé.** L-19 : ~140 000 ménages supplémentaires par an dans les ZE
tendues. Recalcul : 15 256 479 × 0,92 % = 140 360/an ; **1,4 M en dix
ans** ; le besoin de détente vaut **1,39 an de flux**. Un opérateur qui
met dix à vingt ans à livrer (SE-3) livre un stock que le flux a
absorbé dix fois. P-01 le range dans « ce que la proposition NE
démontre PAS : […] le flux de construction nécessaire au-delà du stock
(L-19) » — comme un résidu, alors que c'est **l'ordre de grandeur qui
ramène la proposition à sa taille** : un complément de stock, pas une
« détente des zones tendues ».

**Disposition.** Phrase dans P-01 et dans le titre de l'article :
« gain de stock unique équivalant à environ un an de flux ; la
détente durable dépend du flux de construction, hors chaîne » ; ne pas
titrer « détendre ».

### SE-9 — M-D : la charge uniforme n'est pas « neutre », elle est régressive, capitalisée à l'envers de l'intention, et V-03 est aussi son objection

**Gravité : sérieuse.**

**Énoncé et preuve.**
(a) *Régressivité.* 286 €/logement/an = **0,44 % de la valeur à
Montluçon (64 500 €) contre 0,09 % à Paris (322 000 €)** — et Paris
est hors périmètre (L-28). En revenu : ~1,2 % d'un niveau de vie médian
(~23 k€), le double pour un petit revenu. L-28(3) appelle cela une
« convention de neutralité » ; en incidence, l'uniforme par logement
est la conversion **la plus régressive** possible, pas la plus neutre.
(b) *Capitalisation* (L-28(5) : « non modélisée »). En perpétuité à
3 %, 286 €/an = **9 533 €** de baisse de prix, uniforme en euros. Net
du péage supprimé : Montluçon 4 140 − 9 533 = **−5 393 € (−8,4 %)** ;
Paris 20 668 − 9 533 = **+11 135 € (+3,5 %)** (à 2,3 % : −12,9 % /
+2,6 % ; à 5 % : −2,4 % / +4,6 %). La bascule uniforme transfère du
patrimoine des marchés bon marché — détendus, propriétaires modestes,
le régime « intensité » d'I-02 — vers les marchés chers. C'est
l'inverse de l'intention, et la direction est robuste au taux
d'actualisation.
(c) *V-03.* Le nœud V-03 a deux moitiés : mobilité volontaire ET droit
à l'ancrage (« les liens avec un lieu […] sont des usages réels »).
M-D honore la première en taxant la seconde : le retraité propriétaire
d'un bien de faible valeur paie 286 €/an pour ne pas bouger. I-17 cite
V-03 comme **justification** alors que V-03 est aussi l'**objection**.
(d) *Départements.* I-17 range « départements dont la recette devient
assise sur la détention » parmi les perdants ; c'est discutable — une
recette de détention est stable là où les DMTO sont procycliques
(S-39 : −13,5 % en 2024). Le perdant réel n'est pas nommé : la
transition (double paiement des acquéreurs récents, L-28(5)) et
l'assiette (Paris/Rhône/Corse hors base : 286 € sous-estimé d'environ
10 %, DEC-11).

**Disposition.** Requalifier L-28(3) (« uniforme = régressive, pas
neutre ») ; publier la capitalisation en sensibilité (perpétuité à
2,3/3/5 %, net du péage, par ZE) ; I-17 : « justifiée par une moitié de
V-03 et contredite par l'autre » ; P-01 : toute version publiable de
M-D est en valeur (S-44) ou exonère la résidence principale de faible
valeur — sinon retirer M-D de la proposition et le garder comme
comparaison.

### SE-10 — M-A : le taux de sortie ZLV est mesuré sur les logements taxés, appliqué au gisement effectif entier

**Gravité : mineure** (direction favorable à M-A, donc conservatrice
pour I-15 — mais l'assiette est incohérente et doit être dite).

**Énoncé.** H-14 = 3 %/4 ans (S-22 : 6 700 sorties ZLV « en zone
tendue »), appliqué à 206 664 logements. Mais la TLV ne s'applique
qu'en communes TLV, où le gisement effectif des ZE tendues est de
134 223 (artefact R-07, `gisement_structurel_communes_tlv`) ; hors
communes TLV, le canal « existant » est la THLV facultative ou rien.
Recalcul sur l'assiette taxée : **~10 000 sorties en dix ans (5 % du
besoin)** au lieu de 15 500. Par ailleurs 6 700 / 118 330 (stock > 2 ans
en communes TLV 2022, S-22 p. 16) = 5,7 %, pas 3 % : la base de la
Cour n'est pas la même que celle de la chaîne, ce que H-14 ne dit pas.
Enfin la « référence prolongement des tendances » (INTRO logement §16)
n'est pas M-A : le stock durable est stationnaire (R-02), donc entrées
≈ sorties naturelles ; une partie des 136 544 sortirait sans politique
et une partie équivalente y entrerait — L-29 nomme les entrées, pas la
contrefactuelle de sortie.

**Disposition.** H-14 : préciser l'assiette (taxée vs effective) et
publier les deux ; R-15 : « 5-8 % selon l'assiette » ; L-29 :
contrefactuel de sortie naturelle non instruit.

### SE-11 — Livret A à 3 % : la plage H-16 couvre les marges du circuit, pas le taux du Livret A

**Gravité : sérieuse.**

**Énoncé.** H-16 = 2,30 % (Livret A 1,70 + 0,60), plage [1,50 ; 2,81] =
PLAI/PLS **au Livret A du jour**. L-30 le nomme (« Livret A figé,
révisable deux fois par an »). Mais un Livret A à 3 % — niveau de 2023,
hors registre, à sourcer — donne 3,60 % : facteur d'annuité 0,04756
(**×1,235**), loyer rénové médian **22,65 €/m²**, annuité **2,12 Md€/an**,
neuf 15,40 (22,5 à 66 m², SE-1), subvention d'équilibre de l'ordre de
3 Md€/an ; à 4,00 % (Livret A 3,4) : ×1,31, 24,06 €/m². Sur 40 ans le
Livret A sera révisé quatre-vingts fois ; la borne haute publiée
(2,81) est **inférieure au taux en vigueur il y a trois ans**. La
sensibilité publiée est donc trop étroite pour une hypothèse
« confidence: medium ».

**Disposition.** Élargir la plage H-16 à [1,50 ; 4,00] (ou publier une
variante « Livret A 3 % » dans R-16, sourcée) ; L-30 : dire que le
coin défavorable (26,73) est calculé à Livret A 1,70 et n'est donc pas
un coin.

### SE-12 — « ≤ 2,4 Md€/an à comparer aux 271 M€ de TLV et aux 9,9 Md€ de DMTO » : la comparaison n'est pas honnête

**Gravité : sérieuse.**

**Énoncé.** P-01 juxtapose une **dépense récurrente sur 40 ans** à une
recette (TLV, 9 × plus petite) et à une recette départementale que
P-01 propose de basculer — pas de supprimer, donc pas disponible. Le
lecteur en déduit un ordre de grandeur « finançable » ; les chiffres
disent autre chose : 2,38 Md€ × 40 = **~95 Md€ nominal**, soit deux
fois l'investissement (44,6). Par logement : **12 250 €/an** (14 450
pour le segment rénové) pendant 40 ans = **~580 k€ par logement
rénové, 2,3 × son coût d'acquisition-rénovation**. C'est le chiffre
qui dit ce que « ramener au loyer social » coûte ; il n'est publié
nulle part.

**Disposition.** Publier la subvention par logement et le cumul dans
R-16 ; retirer de P-01 la juxtaposition TLV/DMTO ou l'énoncer comme
« sans commune mesure » ; ne pas titrer sur « 2,4 Md€/an ».

### SE-13 — Le volet mobilité agit sur le canal le moins mobile ; le canal principal reste en « principes »

**Gravité : sérieuse** (L-31 est honnête, P-01 ne l'est pas tout à fait).

**Énoncé.** R-13 : le locatif privé est le canal des mobilités (19,51 %
d'entrées de l'année contre 5,73 % en propriété) ; I-13 : « le
renchérir comprime la mobilité de tous ». Le seul levier de mobilité
chiffré de P-01 (M-D) porte sur le statut le moins mobile, avec un
effet causal « de court terme et petit » (O-39) ; le canal principal
(M-E) reste « principes seulement ». L-31 le dit. Mais P-01 se présente
comme répondant à I-14/H-04 (« le péage de mobilité ») : le volet
mobilité est incomplet sur le canal qui compte, et la chaîne le sait
depuis R-13.

**Disposition.** P-01 : « le volet mobilité ne couvre pas le canal
principal » en clair, pas seulement par renvoi à L-31 ; ne pas titrer
sur la mobilité. M-E non chiffré est acceptable (INTRO §21 règle 18 :
une limite explicite vaut mieux qu'une précision artificielle) à
condition que le poids relatif des canaux (R-13) soit rappelé à côté.

### SE-14 — La taille de l'opérateur hérite de R-07 sans propagation de H-08/H-12

**Gravité : mineure.**

**Énoncé.** C-11/DEC-12 ne propagent que H-15..H-18. Or R-07 traverse 1
(0,82-1,85) et à H-08 = 5 % le besoin tombe à 74 083 (R-09 : 5,5 Md€
au lieu de 15,8). Les 44,6 Md€, 1,72 Md€/an et 2,38 Md€/an de R-16 sont
donc des centraux d'une grandeur dont la chaîne a déjà publié une
plage de ×0,35 à ×2,4. Ce n'est pas dit dans R-16.

**Disposition.** Une ligne dans R-16 (« au seuil H-08 = 5 % : ≈ ×0,35 ;
= 7 % : ≈ ×2,4, cf. R-09 ») ou propagation.

### SE-15 — L'unité « un vacant remobilisé = un logement du besoin » réactivée par P-01

**Gravité : mineure** (déjà jugée pour R-07 en L-18 ; réactivée).

**Énoncé.** L-18 a été tranchée pour R-07 (couverture en unités
hétérogènes). Mais P-01 ajoute l'**attribution** : l'opérateur attribue
au loyer social des studios anciens (S-23 : ×2,8 si < 35 m²) à des
ménages du besoin ; la chaîne ne dit pas qui. R-16 cite L-18 via L-27,
sans le mot « attribution ». L-20(4) (« qui s'y loge ») reste non
instruite alors que P-01 est la « future proposition » qu'elle
annonçait.

**Disposition.** P-01 : dire que l'attribution n'est pas instruite
(L-20(4) reste ouverte) au lieu de « Attribution au loyer social local
(V-04) ».

---

## Ce que l'article annoncé ne peut pas titrer

Phrases-titres qui seraient fausses ou survendues au vu de ce qui
précède :

1. « **Un opérateur public peut détendre les zones tendues pour
   2,4 Md€/an** » — faux trois fois : le 2,4 est le coût de
   l'accessibilité, pas de la fluidité (SE-7) ; c'est 95 Md€ sur 40 ans
   et 580 k€ par logement (SE-12) ; le stock vaut un an de flux (SE-8).
2. « **Le neuf sur friches s'équilibre au marché sans subvention** » —
   artefact d'unité (SE-1) : 18,2 €/m² à 66 m², au-dessus du marché
   partout.
3. « **Le bail à réhabilitation loge à 4 €/m²** » — sans loyer au
   propriétaire, sans acquisition, sur un consentement dont la
   direction est défavorable (SE-2).
4. « **Le repli par acquisition rend l'offre préférable** » — inversé
   (SE-2) ; et l'outil n'existe pas (SE-3).
5. « **Basculer les DMTO rend la mobilité cinq fois moins chère** » —
   effet causal petit et court (déjà dit dans I-17), charge régressive
   et capitalisée à l'envers (SE-9), Paris hors base, canal principal
   non touché (SE-13).
6. « **Le canal incitatif ne peut pas détendre** » — c'est le seul titre
   qui survit à toutes les objections (I-15, robuste même à SE-10).

## Scénarios d'échec non nommés (liste)

1. **L'aubaine** : à prix de repli = valeur vénale pleine, les
   propriétaires vendent au lieu de louer ; P-01 devient M-B au pire cas
   (44,6 Md€ + 2,4 Md€/an) dès le cas central (SE-2).
2. **La porte latérale** : dans les ZE touristiques, les vacants
   deviennent des résidences secondaires ou des meublés ; le gisement
   fond, rien ne se détend, H-12 baisse (SE-4).
3. **L'outil absent** : l'utilité publique de l'acquisition de vacants
   n'est jamais créée, ou ne survit pas au contrôle de proportionnalité ;
   P-01 = M-C = M-A amélioré (SE-3).
4. **Le succès qui ruine** : la détente fait baisser les loyers ; le
   loyer d'équilibre ne bouge pas ; la subvention croît (SE-6).
5. **Le loyer que personne ne paie** : sans subvention, 18,34 €/m²
   (+44 % sur le marché) — les logements remobilisés restent vacants
   (SE-7).
6. **Le stock rattrapé par le flux** : 10-20 ans de mise en œuvre, 1,4 M
   de ménages nouveaux entre-temps (SE-8, SE-3).
7. **Le Livret A à 3 %** : +24 % de loyer d'équilibre, ~3 Md€/an de
   subvention (SE-11).
8. **La bascule à l'envers** : M-D uniforme transfère du patrimoine des
   marchés bon marché vers les marchés chers et taxe l'ancrage que V-03
   protège (SE-9).
9. **L'acheteur public du bas de gamme** : offre à la médiane →
   sélection adverse, biens acquis = biens à réhabilitation lourde
   (SE-5).
10. **Le neuf qui ne s'arbitre pas** : au coût de zone A/A bis + dépollution
    à la densité constatée, le neuf sur friche vaut 21-25 €/m² ; l'étage
    3 de P-01 n'est jamais préféré (SE-1).
11. **Le bailleur social de plus** : 194 k logements attribués à 7 % de
    mobilité — la chaîne produit de l'accessibilité, pas la fluidité
    qu'elle a diagnostiquée (SE-7, SE-15).

## Verdict global

**P-01 ne survit pas telle quelle** : ses trois phrases porteuses
(« le neuf s'équilibre au marché », « le repli rend l'offre
préférable », « ≈ 0 si le bail domine ») reposent respectivement sur
une erreur d'unité, une préférence non établie et inversée par
l'arithmétique, et un pôle sans raison d'être central.
**Elle survit requalifiée** comme ce que la comparaison C-11 établit
vraiment : le canal incitatif ne peut pas détendre (I-15, robuste),
sécuriser le volume coûte le prix du marché des zones tendues
(~250-290 k€/logement) plus 12-14 k€/an/logement pendant 40 ans pour le
rendre social — un complément de stock d'un an de flux, dont le levier
réel (l'écart offre/repli) et l'outil (utilité publique) restent à
concevoir. M-D doit être requalifié en comparaison (régressif, capitalisé
à l'envers, V-03 retourné) ou reformulé en valeur avant d'entrer dans la
proposition.
