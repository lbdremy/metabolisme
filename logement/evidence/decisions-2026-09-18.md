# Journal des décisions — session 7 (proposition institutionnelle), 2026-09-18

Rémy a donné l'autonomie jusqu'à l'écriture du second article, à une
condition : **chaque choix entre plusieurs options est consigné ici** —
ce qui est abandonné, ce à quoi l'on renonce, et la justification du
choix retenu. Les choix qui entrent dans le graphe portent aussi un
nœud `C-xx` dans `evidence/claims.yaml` (référencé ci-dessous) ; ce
fichier est la trace lisible à côté de la chaîne, dans l'ordre où les
décisions ont été prises. Aucune décision n'a été soumise à Rémy pendant
la session : ce journal remplace les `AskUserQuestion` des sessions
précédentes et Rémy peut en renverser chaque ligne à la lecture.

Format : **DEC-nn — objet.** Options considérées · abandonné (et ce
qu'on y perd) · retenu · pourquoi · trace dans le graphe.

---

## DEC-01 — Périmètre de la session : l'article 2 est la proposition institutionnelle

- **Options** : (a) exécuter d'abord l'étape 1 de NEXT-STEPS (les trois
  observations qui trancheraient H-04 : discontinuités DMTO × DVF,
  rotation par âge × ZE, millésimes post-choc), puis la proposition ;
  (b) la proposition d'abord (étape 2), l'étape 1 réduite à ce qui est
  à portée sans acquisition lourde ; (c) les deux en un seul article.
- **Abandonné** : (a) et (c). On renonce, pour cette session, au test
  maison des discontinuités départementales (SE-12) et à la rotation
  par âge (fichier détail RP). On perd une instruction causale propre
  du péage et la lecture territoriale fine de I-11.
- **Retenu** : (b).
- **Pourquoi** : l'article v1.0 annonce explicitement la proposition
  comme prochain article ; la matière quantifiée existe (I-07, I-09,
  I-10, R-14, S-22) ; les arbitres de H-04 ne sont pas disponibles —
  le RPLS au 01/01/2026 n'est pas paru au 2026-09-18 (page SDES « Les
  logements sociaux » vérifiée : dernier millésime 01/01/2025) ; le
  test SE-12 sur la seule coupe DVF 2025 serait confondu par les
  votes départementaux de 2025 (la faculté 5,00 % s'applique aux
  actes à partir du 01/04/2025, département par département) — la
  réforme 2025 est une meilleure expérience naturelle, exploitable
  quand DVF 2026 sera figé. À la place, la chaîne enregistre la
  littérature d'expérience naturelle déjà publiée sur la hausse
  2014 (Bérard & Trannoy 2018, S-43), qui donne l'ordre de grandeur
  causal dont la proposition a besoin.
- **Trace** : NEXT-STEPS mis à jour (étape 1 reportée avec ses
  conditions), S-43.

## DEC-02 — Forme de la trace des décisions

- **Options** : (a) un nouveau statut de nœud dans `claims.yaml`
  (« DEC ») ; (b) ce fichier + un nœud `C-xx` pour les choix qui
  entrent dans le graphe ; (c) tout dans les `notes:` des nœuds.
- **Abandonné** : (a) — un statut hors INTRO §4 casserait le contrat
  du site (`packages/evidence`, douze statuts) et le schéma pydantic ;
  (c) — illisible d'un seul tenant.
- **Retenu** : (b).
- **Pourquoi** : INTRO §4 a déjà le statut `C` (choix de conception) ;
  ce fichier ajoute ce que le graphe ne porte pas — les options
  écartées et l'ordre chronologique.
- **Trace** : ce fichier ; `EVIDENCE.md` y pointe.

## DEC-03 — Les mécanismes comparés (et non un mécanisme défendu d'avance)

- **Options** : (a) défendre d'emblée une « Sécurité sociale du
  logement » (INTRO méthode §17 la cite comme sujet adapté) ; (b)
  comparer plusieurs mécanismes sur les mêmes contraintes chiffrées,
  puis assembler la proposition à partir de ce que la comparaison
  établit ; (c) un article purement qualitatif de principes.
- **Abandonné** : (a) — INTRO logement §2.2 et méthode §18 (« chercher
  uniquement les données qui justifient une solution préexistante »)
  l'interdisent ; (c) — la méthode exige des ordres de grandeur.
- **Retenu** : (b), avec CINQ mécanismes dont quatre chiffrés :
  M-A canal incitatif actuel (référence, S-22) ; M-B opérateur
  collectif qui ACQUIERT et rénove le gisement local et construit sur
  friches là où il manque ; M-C opérateur SANS acquisition (bail à
  réhabilitation, CCH L252-1) ; M-D bascule du péage de transaction
  (DMTO) vers une charge de détention ; M-E sécurisation de la
  mobilité locative (qualitatif — pas de source ouverte pour
  garanties/frais d'agence, L-25).
- **Pourquoi** : les scénarios de l'INTRO logement §16 (référence,
  remise en usage, meilleure localisation, mobilité sécurisée,
  institutionnel) se projettent exactement sur M-A..M-E ; chaque
  mécanisme répond à une contrainte établie par l'arc (I-07/I-09/I-10
  → M-B/M-C ; L-17 → M-A vs M-B ; R-14/I-14 → M-D ; R-13 → M-E).
- **Trace** : C-11 (grille de comparaison), R-15..R-17, P-01.

## DEC-04 — Prix d'acquisition du gisement par l'opérateur (M-B)

- **Options** : (a) le prix médian local observé (DVF 2025, assiette
  C-10, R-14) sans décote ; (b) une décote « logement vacant dégradé »
  tirée de la littérature ; (c) le prix de revient du neuf S-18
  (169 200 €, foncier compris) comme majorant.
- **Abandonné** : (b) — aucune source ouverte figée ne mesure la
  décote d'un vacant durable ; l'inventer serait une constante enfouie
  (INTRO §21 règle 1). (c) — mélange stock ancien et neuf.
- **Retenu** : (a) comme valeur centrale, avec une hypothèse de décote
  H-15 dont le central est 1,0 (pas de décote) et la plage [0,5 ; 1,0]
  publiée en sensibilité (orientée à la baisse du coût : le central
  est conservateur).
- **Pourquoi** : c'est le principe légal de l'expropriation —
  « l'indemnité principale correspond à la valeur vénale du bien »
  (Service-Public F762, S-45) — donc le prix que paierait l'outil de
  contrainte ultime ; le prix médian de la ZE est déjà calculé et
  contrôlé par la chaîne (C-10).
- **Trace** : H-15, C-12, L-27 (le vacant durable est plus petit et
  plus ancien que le logement médian vendu — L-18 — la médiane est
  donc un majorant plausible du prix unitaire, ce qui va dans le même
  sens que l'absence de décote).

## DEC-05 — Financement de l'opérateur : taux et durée

- **Options** : (a) prêt PLUS de la Banque des Territoires (Livret A
  + 0,60 %, bâti jusqu'à 40 ans — S-41/S-42) ; (b) taux d'État (OAT) ;
  (c) durées longues foncier (50-80 ans).
- **Abandonné** : (b) — le circuit existant du logement social est le
  Livret A, il n'y a pas à en inventer un autre pour chiffrer ; (c) —
  la part foncière n'est pas séparée dans le prix médian DVF, on
  ne peut pas lui appliquer une durée propre sans hypothèse
  supplémentaire ; la durée bâti (40 ans) s'applique donc à tout —
  conservateur (annuité plus élevée).
- **Retenu** : H-16 taux 2,30 % (Livret A 1,70 % au 01/08/2026 + 0,60)
  plage [1,50 (PLAI : LA − 0,20) ; 2,81 (PLS : LA + 1,11)] ; H-17
  durée 40 ans, plage [30 ; 50].
- **Trace** : H-16, H-17, C-13.

## DEC-06 — Charges d'exploitation de l'opérateur

- **Options** : (a) ignorer les charges (loyer = annuité) ; (b) un coût
  en €/logement de la littérature ; (c) la structure observée du
  secteur : « pour 100 € de loyers nets, 54,9 € couvrent les charges
  d'exploitation et 43,8 € les annuités » (Perspectives 2025, S-40,
  p. 15).
- **Abandonné** : (a) — sous-estime le loyer d'équilibre d'un facteur
  ~2 ; (b) — le document ne publie pas ce ratio au grain voulu
  (charges de gestion 27,8, maintenance 15,5, TFPB 11,6 sont en % des
  loyers, pas en €).
- **Retenu** : (c) — H-18 part des charges d'exploitation dans le
  loyer net = 0,549, plage [0,40 ; 0,60] ; loyer d'équilibre =
  annuité / (1 − H-18).
- **Pourquoi** : c'est la structure du seul opérateur collectif
  existant à cette échelle ; elle inclut la TFPB (un opérateur public
  pourrait en être exonéré — c'est la borne basse de la plage).
- **Trace** : H-18, C-13, D-20.

## DEC-07 — Assiette de la bascule DMTO → détention (M-D)

- **Options** : (a) tous les logements (parc S-02) ; (b) les seules
  résidences principales de propriétaires occupants ; (c) une assiette
  en valeur (cadastrale ou vénale).
- **Abandonné** : (c) — aucune base de valeurs figée ; (b) — les DMTO
  frappent aussi les bailleurs et les résidences secondaires, une
  bascule sur les seuls occupants changerait l'incidence sans le dire.
- **Retenu** : (a), en €/logement/an uniforme : c'est la conversion la
  plus neutre (elle ne préjuge pas de la progressivité, qui est un
  choix de conception ultérieur — l'OCDE S-44 recommande une assiette
  en valeurs cadastrales à jour, que la France n'a pas).
- **Pourquoi** : le résultat cherché est un ordre de grandeur de
  redistribution entre ménages mobiles et immobiles, pas un barème.
- **Trace** : C-14, R-17, L-28.

## DEC-08 — Le canal incitatif de référence (M-A) : taux de sortie

- **Options** : (a) paramétrer un taux de sortie annuel du gisement
  attribuable au canal incitatif depuis S-22 (ZLV : ~3 % de sorties en
  4 ans en zone tendue, L-17) ; (b) le laisser à zéro (« rien ne se
  déclenche ») ; (c) un taux tiré des bilans Anah.
- **Abandonné** : (b) — caricatural ; (c) — pas de source figée
  donnant une fraction du gisement.
- **Retenu** : (a) — H-14 = 0,75 %/an (3 %/4 ans), plage
  [0,25 ; 2,50] ; horizon de comparaison 10 ans (grille publiée
  5/10/20).
- **Trace** : H-14, R-15.

## DEC-09 — Le consentement des propriétaires (M-C) : grille, pas hypothèse

- **Options** : (a) une hypothèse H-xx « taux d'adhésion au bail à
  réhabilitation » ; (b) une grille de scénarios (10/25/50/100 %)
  publiée sans valeur centrale ; (c) supposer 100 %.
- **Abandonné** : (a) — aucune source ne donne une fraction ; une
  hypothèse sans justification violerait INTRO §9 ; (c) — c'est
  précisément l'inconnue qui distingue M-C de M-B.
- **Retenu** : (b), sur le modèle de la grille d'annualisation de R-14
  (HOLDING_YEARS_GRID) : arithmétique descriptive, pas de central.
- **Trace** : R-16, L-29.

## DEC-10 — Durée d'amortissement du bail à réhabilitation (M-C)

- **Options** : (a) H-17 (40 ans, la durée du prêt) ; (b) la durée
  moyenne du bail observée par la source (30 ans, S-46) en constante
  documentée ; (c) une hypothèse H-xx propre au bail.
- **Abandonné** : (a) — le preneur ne possède pas le bien, il ne peut
  amortir au-delà du bail ; (c) — S-46 donne une valeur, pas une plage
  (« entre 12 et 99 ans, en moyenne 30 ans » : les bornes sont des
  bornes légales, pas plausibles).
- **Retenu** : (b), constante `BAR_AMORTISATION_YEARS = 30` dans
  `core/institution.py`, sourcée S-46 dans le code et dans C-13.
- **Trace** : C-13, R-16.

## DEC-11 — Périmètre de la charge de détention (M-D)

- **Options** : (a) rapporter les 9,9 Md€ au parc France entière
  (S-02, 38,4 M) ; (b) au parc du MÊME périmètre que le produit (OFGL
  hors 75/69/2A/2B/972/973, recensement S-11 : 34,6 M).
- **Abandonné** : (a) — la lecture attentive de la fiche OFGL (champ
  des graphiques 6, décompte 94 + 3 = 96 départements) montre que le
  9,9 Md€ EXCLUT Paris, le Rhône, la Corse, la Guyane et la
  Martinique ; le rapporter au parc national sous-estimerait la charge
  d'environ 10 %.
- **Retenu** : (b) ; la charge (286 €/logement/an) ne vaut pas pour les
  cinq territoires exclus (L-28), dont Paris — précisément l'un des
  cas où le péage est le plus lourd. C'est dit dans R-17.
- **Trace** : C-14, L-28, S-39 (note).

## DEC-12 — Coûts de rénovation au central seulement (R-16)

- **Options** : (a) propager H-09/H-10 (coûts de rénovation) dans R-16
  comme dans R-09 ; (b) les garder au central et ne propager que les
  paramètres nouveaux (H-15..H-18).
- **Abandonné** : (a) — la sensibilité H-09/H-10 est déjà publiée dans
  R-09 (14,9-17,1 Md€ sur 15,8) ; la rénovation pèse 6,0 Md€ sur 44,6
  dans M-B : l'incertitude dominante est l'ACQUISITION (H-15), pas les
  travaux.
- **Retenu** : (b), dit dans C-11.
- **Trace** : C-11.

## DEC-13 — Le test SE-12 et les observations H-04 : reportés, pas abandonnés

- Consigné dans NEXT-STEPS avec les conditions de reprise : DVF 2026
  figé (la réforme 2025 est l'expérience naturelle, par date de vote
  départemental) ; RPLS 01/01/2026 dès parution ; fichier détail RP
  (ANEM × AGEMEN8) pour la rotation par âge.

---

## Intégration de la revue contradictoire du 2026-09-18 (61 objections)

Quatre relecteurs indépendants (sources alternatives SA-1..15, hypothèses
et définitions HD-1..18, scénarios d'échec SE-1..15, statistique
ST-1..13) ; rapports bruts commités AVANT intégration (commit 0498b4c,
dossier `evidence/revue-contradictoire-2026-09-18/`). Compte rendu :
`evidence/revue-contradictoire-2026-09-18.md`. Les décisions ci-dessous
sont celles de l'intégration — Rémy n'a pas été consulté (autonomie
donnée) ; chacune est réversible à la lecture.

## DEC-14 — Charges d'exploitation : forme fixe par logement (révise DEC-06)

- **Options** : (a) garder la proportion « 54,9 % du loyer » ; (b)
  passer aux euros par logement (S-40 p. 24 : 2 652 €) ; (c) publier
  les deux formes en central.
- **Abandonné** : (a) — HD-2/ST-1 : la proportion du secteur appliquée
  à un loyer d'équilibre ~3 × plus haut faisait porter à l'opérateur
  3 × les charges observées et décidait seule le titre « au-dessus du
  marché partout » ; DEC-06 reposait sur un motif inexact (SA-13 : S-40
  publie bien les €/logement). (c) — un central est un central ; la
  forme proportionnelle reste en trace dans le compte rendu.
- **Retenu** : (b), H-18 refondue (2 652 € ; plage 2 093 hors TFPB —
  3 978 conventionnelle), D-23 créée.
- **Trace** : H-18, D-23, C-13.

## DEC-15 — Unités : tout au m² (ST-1 / SE-1 / HD-1)

- **Options** : (a) corriger seulement la surface du neuf (66 m² S-18) ;
  (b) porter TOUS les coûts au m² (prix DVF au m², rénovation au m²,
  neuf 2 550 €/m²) et convertir avec la surface du segment.
- **Abandonné** : (a) — laissait le segment rénové sur un prix par
  logement vendu (~69 m²) divisé par une surface de RP (~96 m²).
- **Retenu** : (b). Conséquence assumée : les totaux d'acquisition
  utilisent la surface C-07 des RP (majorant, L-27) — une surface
  propre aux vacants n'existe pas en open data.
- **Trace** : C-12, C-13, T-17, L-27.

## DEC-16 — Indemnité de remploi : hypothèse H-20 (SA-4)

- **Options** : (a) laisser « non chiffrée » (L-27 initiale) ; (b) H-20
  = 10 % [0 ; 10,5] sur la trace administrative du barème (S-50, dossier
  de DUP) ; (c) attendre la capture de Légifrance R322-5.
- **Abandonné** : (a) — c'est chiffrable et cela pèse + 7 % sur
  l'acquisition ; (c) — Cloudflare, et l'article ne fixe pas le barème
  (pratique jurisprudentielle) : le dossier de DUP est la trace
  publique du barème appliqué.
- **Retenu** : (b), en disant que S-50 n'est pas le texte réglementaire.
- **Trace** : H-20, S-50, C-12.

## DEC-17 — M-D : millésime 2025, numérateur départemental, périmètre (SA-1 / ST-2 / ST-3 / SE-9)

- **Options** : (a) garder 2024 et le péage fiscal total ; (b) central
  2025 (S-47, 11,9 Md€), 2024 en sensibilité ; numérateur = droit
  départemental seul ; ZE < 50 % dans le périmètre hors quantiles ;
  charge publiée en % du prix médian.
- **Abandonné** : (a) — 2025 était publié avant la session ; le
  numérateur total contredisait L-28(2) ; Porto-Vecchio et Paris
  étaient cités pour une charge qui ne s'applique pas chez eux.
- **Retenu** : (b). Le seuil de 50 % est une convention (Paris à 61 %
  reste dedans, Lyon à 8 % sort) — publiée, avec la liste des ZE
  partielles.
- **Trace** : C-14, R-17, L-28, S-47, S-53.

## DEC-18 — P-01 : l'acquisition sécurise, le bail est offert (SE-2 / HD-4 / SE-3)

- **Options** : (a) garder l'enchaînement « offre → repli rend l'offre
  préférable » ; (b) l'inverser honnêtement : l'acquisition est l'outil
  (à créer en droit), le bail une option dont la préférence n'est pas
  établie ; (c) chiffrer un prix de repli sous la valeur vénale qui
  rendrait le bail préférable.
- **Abandonné** : (a) — la revue a montré (valeur actuelle du bail
  28-67 % de la vente) que la cession domine ; (c) — aucune source
  pour un tel prix, et il contredirait C-12 (valeur vénale = principe
  légal) ; c'est un paramètre à concevoir, nommé dans C-15, pas chiffré.
- **Retenu** : (b), C-15 créé, I-16 requalifiée, P-01 réécrite.
- **Trace** : C-15, I-16, P-01.

## DEC-19 — H-14 : majorant par propriétaire contacté (HD-3 / SA-2 / SE-10)

- **Options** : (a) recentrer H-14 plus bas (le canal réel contacte une
  fraction) ; (b) garder 0,75 %/an en le déclarant MAJORANT et en
  plafonnant par ZE au besoin local.
- **Abandonné** : (a) — la fraction contactée n'a pas de source ; un
  recentrage serait une constante inventée.
- **Retenu** : (b) — conservateur pour I-15 (le canal, même majoré, ne
  détend pas) ; la description de H-14 dit désormais ce que S-22 dit.
- **Trace** : H-14, R-15, L-33 (TVLH 2027).

## DEC-20 — Ce qui n'est PAS intégré, et pourquoi

- **ST-5 (médianes pondérées en central)** : les médianes simples par
  ZE restent le central (convention de R-14, une ZE = un point) ; les
  médianes pondérées (ventes, rénovables) sont publiées à côté.
- **HD-10 (« opérateur collectif » comme définition)** : sa forme
  juridique (agrément, fiscalité) est un choix de conception, pas une
  définition de source — porté par C-15, pas par un D-xx.
- **HD-6 (part résidentielle des DMTO en hypothèse)** : aucune source
  n'isole cette part ; consigné en L-28(1), pas en H-xx.
- **SE-14 (propager H-08/H-12 dans R-16)** : la sensibilité au seuil
  est publiée dans R-09 (facteur ~4,6 sur les volumes) ; R-16 le
  rappelle dans C-11 plutôt que de tripler son artefact.
- **SA-10 (communiqué Bercy pour le Livret A)** : S-42 suffit (la page
  cite le taux et sa date) ; à enregistrer si S-42 disparaît.
- **SA-12 (bilan national du bail à réhabilitation)** : aucune source
  trouvée par le relecteur non plus — reste en L-29.
- **SE-13 (M-D agit sur le statut le moins mobile)** : intégré en texte
  (L-28(6)), pas de calcul supplémentaire possible sans source sur les
  mobilités des propriétaires.
