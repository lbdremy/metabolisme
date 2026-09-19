# Journal des décisions — session 1 (2026-09-18), étude « autoroutes »

Session menée **en autonomie** (Rémy : « reprend l'instruction du dossier
sur la rente de position en commençant par les autoroutes, arrête-toi après
l'écriture de l'article »). Chaque décision méthodologique qui aurait
autrement été posée à Rémy (AskUserQuestion) est consignée ici sur le
modèle de `../logement/evidence/decisions-2026-09-18.md`, avec cinq
rubriques : les **options** ouvertes, ce qui est **abandonné** (choisir,
c'est renoncer : à quoi on renonce en retenant l'option), ce qui est
**retenu**, **pourquoi** cette option plutôt que les autres, et la
**trace** dans la chaîne de preuves (les nœuds du graphe qui portent la
décision ; chaque nœud C-xx cite son DEC-nn dans son titre, et c'est par
là que la décision est visible sur le site). Chacune est réversible à la
lecture ; Rémy n'a encore rien relu de cette étude.

## DEC-01 — Le cadrage `monopoles/` est une SOURCE figée de cette étude, pas un graphe partagé

- **Options** : (a) étendre le contrat du site pour résoudre des
  références inter-études (`monopoles:D-15` dans `depends_on`) ; (b)
  redéfinir localement les notions nécessaires (D-15, H-06, C-05, V-05)
  en recopiant leur texte ; (c) enregistrer le cadrage figé au tag
  `monopoles-cadrage-v1.0` comme source S-01 (copies figées des trois
  registres, empreintes), puis porter les notions reprises comme des
  définitions et hypothèses locales qui CITENT cette source.
- **Abandonné** : (a) — on renonce à ce que le lecteur du site « dépile »
  D-01 jusqu'à la CRE en un clic : il s'arrête à la copie figée du
  registre du cadrage et doit ouvrir le post du cadrage pour continuer ;
  on renonce aussi à modifier le contrat, le panneau et les ancres du
  site pour une seule étude. (b) — on renonce à la lisibilité immédiate
  (texte complet dans le nœud) ; retenu à moitié : D-01 recopie le texte
  en le citant. Ce qu'on perd avec (c) : la propagation automatique d'un
  changement du cadrage (il faut re-figer S-01 à un nouveau tag).
- **Retenu** : (c).
- **Pourquoi** : c'est la convention déjà en vigueur dans le dépôt — les
  identifiants préfixés d'une autre étude ne se résolvent pas dans un
  graphe (monopoles/INTRO §12, `logement:R-14`) — et la méthode traite
  tout document amont de la même façon : figé, versionné, checksummé
  (INTRO §7). La copie figée fait foi de la version du cadrage utilisée,
  ce qu'aucune résolution dynamique ne garantirait. L'extraction d'un
  mécanisme inter-études attendra une deuxième étude sectorielle (INTRO
  §20).
- **Trace** : S-01, D-01, D-02, H-01, H-10, V-01, C-01 (cite DEC-01).

## DEC-02 — Projet `uv` dès l'ouverture, schémas recopiés

- **Options** : (a) registres seuls, sans code, comme `monopoles/` ; (b)
  projet `uv` complet avec des schémas pydantic recopiés de `logement/` et
  étendus ; (c) projet `uv` avec extraction préalable d'un validateur de
  registres partagé entre les trois études.
- **Abandonné** : (a) — on renonce à la reproductibilité par code de la
  première mesure du programme (le site ne recalcule que les empreintes,
  pas les chiffres). (c) — on renonce à la dédoublonnage immédiat des
  schémas (troisième copie de `models.py`) ; ce qu'on perd : une
  divergence possible entre copies tant que l'extraction n'est pas faite.
- **Retenu** : (b).
- **Pourquoi** : monopoles/CLAUDE.md fixe la règle (« add a `uv` project
  the day a sector study computes something ») et cette étude calcule dès
  M-01 ; l'extraction (c) est un chantier d'outillage distinct du contenu,
  qui aurait consommé la session sans produire de chiffre, et INTRO §20
  demande de n'extraire qu'après un besoin commun avéré — il l'est
  maintenant, il est inscrit dans NEXT-STEPS.
- **Trace** : `pyproject.toml`, `src/autoroutes/models.py`, CI
  `.github/workflows/autoroutes-ci.yml`, filtre LFS ; pas de nœud du
  graphe (décision d'outillage, pas de contenu).

## DEC-03 — La mesure porte sur les comptes IFRS consolidés par groupe, exercice 2023, transcrits à la main

- **Options** : (a) attendre un jeu de données ouvert de l'ART par
  société ; (b) extraire les tableaux des PDF par script ; (c) transcrire
  à la main les lignes utiles dans un CSV où chaque valeur porte la source
  et la page, parsé au bord et contrôlé par le rebouclage du bilan (T-01) ;
  et, pour le périmètre : (d) les comptes sociaux des sept sociétés
  (immobilisations du domaine concédé au coût de revient historique,
  amortissement de caducité) ; (e) les comptes IFRS consolidés par groupe
  publiés en ligne (IFRIC 12) ; (f) les agrégats de l'ART seulement.
- **Abandonné** : (a) — il n'existe pas (vérifié sur data.gouv.fr et
  opendata.autorite-transports.fr : fiches PDF seulement) ; on renonce à
  attendre. (b) — on renonce à une chaîne entièrement automatique du PDF
  au chiffre, parce qu'elle serait indéterministe d'un éditeur à l'autre
  et invérifiable par un lecteur. (d) — on renonce aux comptes sociaux,
  qui sont pourtant la forme la plus proche de D-15 (coût de revient
  historique), parce qu'ils ne sont pas publiés en ligne (Infogreffe et
  pappers répondent 403) ; ce qu'on perd : la certitude que la base IFRS
  est bien le coût historique (L-07). (f) — on renonce à la seule mesure
  agrégée, sans base d'actifs. On renonce aussi à Sanef-SAPN (comptes non
  figés, pare-feu) et à une série pluriannuelle (une seule année, L-08).
- **Retenu** : (c) + (e), exercice 2023, trois groupes (83 % des recettes
  des sept), Sanef-SAPN extrapolé (H-07, H-09).
- **Pourquoi** : (c) est la seule forme où chaque chiffre reste
  vérifiable page par page par un lecteur et où une erreur de
  transcription est attrapée avant la mesure (rebouclage) — c'est la
  règle « parse at the boundary » appliquée à un PDF ; (e) parce que
  l'Autorité de la concurrence a constaté en 2014 que comptes sociaux et
  consolidés ne diffèrent pas significativement (O-25) et que les notes
  IFRS des trois groupes donnent bien le coût brut, les amortissements et
  les subventions ; 2023 parce que c'est le dernier exercice où les trois
  rapports et la synthèse de l'ART coexistent.
- **Trace** : T-01 (cite DEC-03), C-02 (cite DEC-03), L-04, L-07, L-08,
  `data/transcribed/comptes-2023.csv`, `core/accounts.py`.

## DEC-04 — Prélèvements spécifiques : destination, pas coût

- **Options** : compter la taxe d'aménagement du territoire, la redevance
  domaniale, la contribution à l'AFITF et la TEITLD (a) comme des coûts
  d'exploitation (ils sont dans « impôts et taxes » des comptes, et
  l'ART les compte ainsi dans son TRI) ; (b) comme une destination du
  surprofit (part de l'État), à l'instar de l'IS dans D-15 ; (c) les
  compter en coût mais publier la part de l'État à côté.
- **Abandonné** : (a) — on renonce à la comparabilité directe avec l'EBITDA
  et le TRI de l'ART, qui les comptent en charges ; ce qu'on perd : un
  surprofit plus petit de 0,85 à 1,2 Md€ et plus proche des chiffres
  publiés. (c) — on renonce à la cohérence avec D-15, qui a déjà tranché
  pour l'IS : un prélèvement assis sur la rente n'est pas un coût du
  service.
- **Retenu** : (b), avec la CET (impôt général) maintenue en coût, et la
  part des prélèvements spécifiques dans « impôts et taxes » lue chez le
  seul groupe qui la détaille, APRR (H-08), publiée en sensibilité.
- **Pourquoi** : ces prélèvements n'existent que parce que la position
  existe — ils sont assis sur les kilomètres parcourus, le chiffre
  d'affaires, la marge — et le contrat lui-même les traite comme des
  éléments de l'équilibre à compenser par le péage (art. 32, O-22) : ils
  prélèvent la rente, ils ne produisent pas le service. La question de
  l'étude est « à qui va le surprofit » ; les compter en coût cacherait
  la part de l'État. La différence avec l'ART est dite (M-02, M-03, I-02)
  plutôt qu'effacée, et l'effet de H-08 est de ± 70 M€ (L-05).
- **Trace** : C-03 (cite DEC-04), H-08, L-05, M-01, M-02, R-02.

## DEC-05 — Le témoin substituable est VINCI Energies / VINCI Construction

- **Options** : (a) le marché des autocars librement organisés, régulé par
  la même autorité, à entrée libre ; (b) les concessions récentes
  attribuées par appel d'offres (TRI 5,9 %) ; (c) les pôles de travaux et
  de services du même groupe que VINCI Autoroutes, mesurés par la même
  forme sur la même année et les mêmes normes ; (d) pas de témoin.
- **Abandonné** : (a) — on renonce à un témoin EXTERNE au groupe et
  sectoriel (transport), qui aurait été le plus convaincant, parce que les
  rapports de l'ART sur ce marché ne publient ni résultat d'exploitation
  ni capitaux par opérateur (vérifié dans l'édition 2024) ; ce qu'on
  perd : l'indépendance du témoin vis-à-vis de la gouvernance de VINCI.
  (b) — ce n'est pas un témoin substituable (même objet, non duplicable)
  mais un témoin de la mise en concurrence (monopoles:H-02) ; on renonce
  à l'instruire dans cette session, il est inscrit dans NEXT-STEPS. (d) —
  interdit par le cadrage (monopoles:I-03 : sans témoin, pas
  d'attribution).
- **Retenu** : (c), plus VINCI Autoroutes sur ses capitaux engagés au prix
  d'acquisition comme contre-exemple de base.
- **Pourquoi** : c'est le témoin qui contrôle le plus de causes
  concurrentes à la fois — même actionnaire, même année, mêmes normes
  comptables, même définition du résultat opérationnel — de sorte que
  l'écart mesuré (4-6 % contre plus de 45 %) ne peut venir ni de la
  gestion ni de la comptabilité ; l'Autorité de la concurrence avait fait
  la même comparaison en 2014 (O-25).
- **Trace** : C-05 (cite DEC-05), M-04, I-01, S-11.

## DEC-06 — Deux bases, deux amortissements, aucun retenu seul

- **Options** : (a) une seule base, nette comptable (modèle CRE, D-21 du
  cadrage) ; (b) une seule base, brute au coût historique ; (c) la base
  de l'ART (actif moderne équivalent, coût de remplacement en 2002) ;
  (d) les deux bases nette et brute, avec deux amortissements (caducité
  comptable, technique sur H-06), présentées côte à côte, la nette-
  comptable en variante centrale.
- **Abandonné** : (a) — on renonce à un chiffre unique, plus simple à
  lire ; ce qu'on perd : la réponse à l'objection « vous rémunérez un
  capital déjà amorti » resterait sans chiffre. (b) — on renonce à
  s'aligner sur la lecture la plus favorable aux concessionnaires ; ce
  qu'on perd : un chiffre moitié moindre. (c) — exclue par D-15 (une base
  qui contient la rente ne peut pas servir à la mesurer) ; on renonce donc
  à la comparabilité directe avec le TRI de l'ART, rendue par M-03 et
  interprétée par I-02 plutôt que tranchée.
- **Retenu** : (d).
- **Pourquoi** : le cadrage a fixé la forme (coût historique net des
  subventions) mais pas la question de l'amortissement déjà payé ; les
  deux bases bornent ce que D-15 admet, et le résultat est positif aux
  deux — ce qui rend la conclusion robuste au choix qu'un relecteur
  ferait. La variante centrale est la nette parce que c'est le modèle
  explicite de la CRE repris en D-02 ; l'amortissement technique est
  ajouté parce que les concessionnaires disent eux-mêmes que la caducité
  « ne constate pas une dépréciation technique » (O-13), mais sans source
  pour la durée (L-03) il reste en sensibilité.
- **Trace** : C-04 (cite DEC-06), M-01, I-02, H-06, L-03, L-07.

## DEC-07 — Ce que le graphe propose (P-01) reste conditionnel à V-01

- **Options** : (a) ne rien proposer — l'étude compare quatre
  configurations et s'arrête (monopoles:C-05 : « aucune défendue
  d'avance ») ; (b) proposer une configuration comme conséquence des
  mesures ; (c) proposer sous condition explicite de la valeur V-01, en
  rapportant la conclusion contraire du rapporteur du Sénat.
- **Abandonné** : (a) — on renonce à répondre à la cinquième question du
  cadrage (« sous quelles formes pourrait-elle revenir à l'usager ») ;
  ce qu'on perd : l'article s'arrêterait à un tableau. (b) — interdit par
  la méthode (INTRO §1.3 : les faits contraignent le choix sans le
  déterminer) ; on renonce à la force rhétorique d'un « il faut ».
- **Retenu** : (c). P-01 dit ce qui découle des mesures SI l'on tient que
  la rente revient aux usagers : ne pas reconduire une concession longue
  à recette privée, ne pas racheter avant terme, conserver la recette à
  l'échéance et déléguer l'exploitation par contrats courts, ou réguler
  sur base d'actifs au coût historique.
- **Pourquoi** : c'est la forme retenue dans `logement/` (P-01 y est
  conditionnel aux valeurs V-02..V-04) et celle que le cadrage demande
  (la destination de la rente est un choix, V-05) ; la conclusion
  contraire du rapporteur du Sénat de 2024 (régie « inadaptée ») est
  rapportée dans R-04 et O-24 parce que son argument — risque et
  compétences portés par l'État — porte sur l'exploitation, que P-01
  laisse déléguée, et non sur la recette.
- **Trace** : P-01 (cite DEC-07), R-04, V-01, O-24.
