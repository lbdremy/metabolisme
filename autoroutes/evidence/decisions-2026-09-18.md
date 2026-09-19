# Journal des décisions — session 1 (2026-09-18), étude « autoroutes »

Session menée **en autonomie** (Rémy : « reprend l'instruction du dossier
sur la rente de position en commençant par les autoroutes, arrête-toi après
l'écriture de l'article »). Chaque décision méthodologique qui aurait
autrement été posée à Rémy (AskUserQuestion) est consignée ici avec les
options écartées et sa justification, sur le modèle de
`../logement/evidence/decisions-2026-09-18.md`. Chacune est réversible à
la lecture ; Rémy n'a encore rien relu de cette étude.

## DEC-01 — Le cadrage `monopoles/` est une SOURCE figée de cette étude, pas un graphe partagé

- **Options** : (a) étendre le contrat du site pour résoudre des
  références inter-études (`monopoles:D-15` dans `depends_on`) ; (b)
  redéfinir localement les notions nécessaires (D-15, H-06, C-05, V-05)
  en recopiant leur texte ; (c) enregistrer le cadrage figé au tag
  `monopoles-cadrage-v1.0` comme source S-01 (copies figées des trois
  registres, empreintes), puis porter les notions reprises comme des
  définitions et hypothèses locales qui CITENT cette source.
- **Abandonné** : (a) — modification du contrat, du panneau et des ancres
  du site pour une seule étude ; à faire quand deux études sectorielles en
  auront besoin (INTRO §20) ; (b) — recopie sans lien : la définition
  perdrait son ancrage (S-07 de monopoles, C-02) et sa version.
- **Retenu** : (c). La convention existante du dépôt est que les
  identifiants préfixés d'une autre étude ne se résolvent pas dans un
  graphe (monopoles/INTRO §12) ; une étude sectorielle traite donc le
  cadrage comme n'importe quel document amont : figé, versionné,
  checksummé. Les notions reprises portent l'identifiant d'origine dans
  leur terme (« D-15 du cadrage ») et la copie figée fait foi de la
  version utilisée.
- **Trace** : S-01, D-01..D-06, H-01, C-01.

## DEC-02 — Projet `uv` dès l'ouverture

- **Options** : registres seuls comme `monopoles/` ; projet `uv` complet.
- **Retenu** : projet `uv` (monopoles/CLAUDE.md : « add a `uv` project the
  day a sector study computes something ») — l'étude calcule dès sa
  première mesure (D-15 appliquée). Schémas pydantic recopiés de
  `logement/` et étendus aux quatre champs du cadrage (`statement`,
  `limitations`, `constructed_by`, `redistributable`) : c'est la
  troisième étude, mais l'extraction d'un validateur partagé reste un
  chantier d'outillage distinct (monopoles/NEXT-STEPS) — noté, pas fait.
- **Trace** : `pyproject.toml`, `src/autoroutes/models.py`, CI
  `.github/workflows/autoroutes-ci.yml`, filtre LFS.

## DEC-03 — La mesure porte sur les comptes IFRS consolidés par groupe, exercice 2023, transcrits à la main

- **Options** : (a) attendre un jeu de données ouvert de l'ART par société
  (il n'existe pas : vérifié sur data.gouv.fr et opendata.autorite-transports.fr,
  seules des fiches PDF) ; (b) extraire les tableaux des PDF par script
  (fragile, une mise en page par éditeur) ; (c) transcrire à la main les
  lignes utiles dans un CSV où chaque valeur porte la source et la page,
  parsé au bord (pydantic) et contrôlé par le rebouclage du bilan avant
  toute mesure (T-01).
- **Abandonné** : (a) — bloque l'étude ; (b) — indéterministe d'un PDF à
  l'autre et invérifiable par un lecteur.
- **Retenu** : (c). Périmètre : les trois groupes dont les comptes 2023
  ont pu être figés (ASF-Escota, Cofiroute, APRR-Area, 83 % des recettes
  des sept) ; Sanef-SAPN extrapolé (H-07, H-09, L-04) ; comptes IFRS
  (IFRIC 12) plutôt que comptes sociaux — les seuls publiés en ligne par
  les groupes, l'Autorité de la concurrence ayant noté en 2014 l'absence de
  différence significative (O-25).
- **Trace** : T-01, C-02, `data/transcribed/comptes-2023.csv`,
  `core/accounts.py`.

## DEC-04 — Prélèvements spécifiques : destination, pas coût

- **Options** : compter la taxe d'aménagement du territoire, la redevance
  domaniale, la contribution à l'AFITF et la TEITLD (a) comme des coûts
  d'exploitation (ils sont dans « impôts et taxes » des comptes) ; (b)
  comme une destination du surprofit (part de l'État), à l'instar de l'IS
  dans D-15.
- **Retenu** : (b), C-03. Ces prélèvements n'existent que parce que la
  position existe (ils sont assis sur les kilomètres parcourus, le chiffre
  d'affaires, la marge) et le contrat lui-même les traite comme des
  éléments de l'équilibre à compenser par le péage (art. 32). La CET,
  impôt général, reste un coût. Effet sur la mesure : ± 70 M€ selon la
  part retenue (H-08). L'ART, elle, compte tout en charges — son TRI en
  est réduit d'autant ; la différence est dite (M-02, M-03).
- **Trace** : C-03, H-08, L-05.

## DEC-05 — Le témoin substituable est VINCI Energies / VINCI Construction, pas le marché des autocars

- **Options** : (a) le marché des autocars librement organisés (régulé par
  la même autorité, entrée libre) — ses rapports annuels ne publient pas de
  résultat d'exploitation ni de capitaux par opérateur (vérifié dans
  l'édition 2024) ; (b) les concessions récentes attribuées par appel
  d'offres (TRI 5,9 %) — même objet, pas substituable : c'est un témoin de
  monopoles:H-02 (mise en concurrence), à instruire ensuite ; (c) les
  pôles de travaux et de services du même groupe que VINCI Autoroutes,
  mesurés par la même forme sur la même année et les mêmes normes.
- **Retenu** : (c), C-05, M-04 ; (b) inscrit dans NEXT-STEPS.
- **Trace** : C-05, M-04, S-11.

## DEC-06 — Deux bases, deux amortissements, aucun retenu seul

- **Options** : présenter la mesure sur une seule base (nette comptable,
  modèle CRE) ; ou sur deux bases (nette, brute) et deux amortissements
  (caducité, technique), sans en privilégier une dans le graphe.
- **Retenu** : les quatre variantes, la nette-comptable en variante
  centrale (c'est le modèle D-21), la brute-comptable comme borne la plus
  favorable aux concessionnaires que D-15 admette (C-04). Le coût de
  remplacement de l'ART n'est pas une base admise ; il est rendu par M-03
  et la différence est interprétée (I-02) plutôt que tranchée.
- **Trace** : C-04, M-01, I-02, L-03, L-07.

## DEC-07 — Ce que le graphe propose (P-01) reste conditionnel à V-01

- **Options** : ne rien proposer (l'étude compare quatre configurations,
  monopoles:C-05) ; proposer une configuration comme conséquence des
  mesures ; proposer sous condition explicite de la valeur V-01.
- **Retenu** : la troisième. P-01 dit ce qui découle des mesures SI l'on
  tient que la rente revient aux usagers : ne pas reconduire une concession
  longue à recette privée, ne pas racheter avant terme, conserver la
  recette à l'échéance et déléguer l'exploitation par contrats courts, ou
  réguler sur base d'actifs au coût historique. Le rapporteur du Sénat de
  2024 conclut autrement (régie « inadaptée », modèle concessif court) ;
  son argument (risque et compétences portés par l'État) est rapporté dans
  R-04, pas écarté.
- **Trace** : P-01, R-04, V-01.
