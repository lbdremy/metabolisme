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
