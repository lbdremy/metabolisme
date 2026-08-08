# NEXT-STEPS — ce qui vient ensuite

Ce qui est déjà fait est consigné dans [`PREV-STEPS.md`](PREV-STEPS.md).
Mis à jour à chaque fin de session de travail significative.

## État au sortir de la session 4 (2026-08-08)

**H-04 est ouverte, trois résultats posés** (112 tests, 107 nœuds,
13 stages) : **R-11** (rotation résidentielle, S-27 — RP2023 Melodi,
maille ZE native, millésimes 2012/2017/2023) : rotation en baisse dans
293 ZE sur 305, chute CONCENTRÉE dans les marchés chers et sans vacance
(tendues −1,54 pt vs −1,27) alors que le niveau suit la fonction du
territoire. **R-12** (mobilité du parc social, S-28 — RPLS 2025, séries
2013-2025) : chute nationale 9,29 → 7,11 % qui s'accélère, généralisée
(286/303 ZE) et UNIFORME, mais niveau miroir du marché (rho −0,80 avec
le coût — la plus forte corrélation de la chaîne ; médiane 6,74 % en ZE
tendues, vacance sociale 1,63 %) ; croisement des segments NÉGATIF
(−0,20) : la rotation étudiante/privée des métropoles masque le gel
social (I-12, convention C-09 contrôlée, L-23). **R-13** (migrations des
personnes, S-29 — MIGCOM RP2022, 17,4 M obs.) : 9,87 % de mobiles
annuels PORTÉS par le locatif privé (19,5 % d'entrées contre 8,3 % HLM
— recoupe RPLS — et 5,7 % propriété), validation croisée
logements/personnes +0,80 (R-11 × R-13), les flux internes vident les
cœurs chers (Paris −1,40 %/an). R-11, R-12 et R-13 sont POSTÉRIEURS à
la revue du 2026-08-07 — à couvrir par la prochaine passe
contradictoire. L'état v0.3 (couverture 1,06, besoin 194 488, détente
15,8 Md€ ratio 2,1, foncier 10,9 ×) est inchangé.

## Prochaines étapes (dans l'ordre)

1. **Poursuivre H-04 (mobilités empêchées)** — R-11 (rotation RP),
   R-12 (parc social) et R-13 (migrations des personnes, MIGCOM
   8589767 — la variante « pays antérieur » 8589858 de l'éclairage
   initial était la mauvaise) sont FAITS (session 4) ; suite :
   1. **DVF géolocalisées** (https://files.data.gouv.fr/geo-dvf/latest/csv/,
      par département) : prix → coût de transaction via une H-xx à déclarer
      (DMTO ~5,8 %, notaire, agence) ; pas d'Alsace-Moselle ni Mayotte.
   2. SNE : ressource data.gouv MORTE (404) ; portail vivant
      https://www.data.logement.gouv.fr/statistiques/ = exports par
      territoire sans bulk (effort élevé) ; raccourci possible par les
      indicateurs SNE de l'Observatoire des Territoires (maille à vérifier
      à la main). EnL 2020 : microdonnées sous habilitation — calibration
      nationale seulement.
   Le terme « coût de la mobilité résidentielle » (R-06) est disponible ;
   la prochaine passe contradictoire devra couvrir R-11, R-12 ET R-13
   (postérieurs à la revue du 2026-08-07). Licence S-28 (RPLS) à
   confirmer avant citation dans l'article, comme S-09 (L-09). Piste
   ouverte par R-13 : STOCD × IRAN permettrait un taux de mobilité par
   statut PAR ZE (privé vs HLM territorialisé) si un résultat le
   demande.
2. **Restes ouverts de la revue** (voir la section dédiée du compte rendu) :
   - figer l'emploi localisé INSEE récent à la maille ZE (2012-2023) et
     re-exécuter R-03 en variante (L-07 corrigée le promet) ;
   - instruire l'anomalie de réconciliation LOVAC communal vs départemental
     (masqués ~11,2/commune > plafond 10 — l'écart n'est pas entièrement
     expliqué par la secrétisation : périmètre du fichier communal ?) ;
   - vérifier le point Paris 32 091 (LOVAC 26) vs ~18 600 (Apur 2022) —
     partie du dossier « source dégradée post-GMBI » (L-04) ;
   - sourcer proprement les référentiels de besoin en flux (L-21) si le
     premier article veut les citer.
3. **Lever les frontières H-05 par convention** : PPPI (DREAL/DDT),
   fichiers fonciers/successions (Cerema — statut « acteur public » à
   clarifier) ; seule voie pour la piste successions/indivisions (I-08),
   devenue centrale depuis que H-12 rappelle que l'EXISTENCE même du
   gisement se joue là.
4. **Frontières de données actées** (ne pas re-tenter sans nouveau
   levier) : fichiers LOVAC détaillés = habilitation (sensibilité H-06 ET
   désormais L-18 taille/époque des vacants) ; éviction saisonnière
   infra-territoriale = non tranchable en open data (notebook 06).
5. **Chemin de publication** : la revue étape 12 est faite ; le premier
   article dans `articles/` peut s'écrire sur l'état v0.3 — ATTENTION, sur
   le récit corrigé (couverture ~1 conditionnelle, ratio ~2, contrainte
   institutionnelle = condition), pas sur les chiffres d'avant revue ;
   licence du millésime loyers 2025 à confirmer avant publication (L-09).

## Outillage (sans urgence — ne mord qu'avec la croissance de l'étude)

Deux écarts identifiés le 2026-08-07 en confrontant le process aux leçons
d'architecture des systèmes de données (graphes explicites, détection de
changement) ; à traiter quand l'occasion s'y prête, pas avant :

- **DAG de stages explicite.** La dépendance R-07 → R-09/R-10 est enfouie
  dans le shell : `build_remob` et `build_foncier` RECALCULENT la frame de
  tension (`tension.tension_by_ze`) au lieu de consommer l'artefact de
  R-07, et `reproduce` est une liste ordonnée, pas un graphe. Déclarer les
  dépendances entre stages (et faire consommer les artefacts amont) rendra
  la propagation visible et permettra la recomputation sélective le jour
  où le full refresh (~1 min aujourd'hui) coûtera. Le graphe épistémique
  (`claims.yaml` depends_on, `hypotheses.yaml` affects) est déjà la source
  de vérité — l'exécution doit finir par le refléter.
- **Veille de fraîcheur des sources.** Les S-xx figées garantissent la
  reproductibilité mais RIEN ne signale qu'un millésime plus récent
  existe : L-07 (emploi arrêté à 2018 alors que 2023 était publié) n'a été
  détectée que par la revue contradictoire, l'annulation de Filosofi 2022
  par recherche active, et l'URL de S-25 était morte avant même le
  figement. Un contrôle léger (commande `logement freshness` : re-vérifier
  périodiquement URL vivantes + dernier millésime annoncé par source, en
  simple rapport, jamais en refigement automatique) fermerait la boucle de
  détection de changement côté monde extérieur.

## Comment reprendre (5 minutes)

```bash
cd logement
uv sync                     # env figé (uv.lock)
uv run logement validate    # registres + sha256 + graphe : doit être vert
uv run logement reproduce   # rebâtit les 13 artefacts data/processed/
./check.sh && ./test.sh     # portes qualité (112 tests)
```

Lire dans l'ordre : `CLAUDE.md` (doctrine + décisions arrêtées),
`EVIDENCE.md` (index humain), `evidence/revue-contradictoire-2026-08-07.md`
(l'état de la critique), puis `evidence/claims.yaml`.
Le rendu du document de preuve : `QUARTO_PYTHON=.venv/bin/python quarto
render evidence/efficacite-parc-immobilier.qmd` (Quarto 1.10.18 installé).

## Pièges connus (ne pas redécouvrir)

- **LOVAC** : niveaux de vacance *totale* non comparables au travers des
  ruptures 2023/2025 (L-04) — et le millésime de référence 24 est le
  PREMIER post-GMBI (campagne 2023 chaotique, S-22) : volumes-titres sur le
  dernier millésime pré-rupture ; parc privé ≠ vacance INSEE (L-06) ;
  LOVAC SURESTIME (~25 % de faux vacants, H-12 — ne plus publier de
  gisement brut sans le taux d'existence) ; secrétisation « s » < 11
  (L-05) ; cp1252, `;`, milliers en espaces insécables ; millésimes
  mélangés normalisés par `core/lovac.py`.
- **Secrétisation** : le sens du biais sur la couverture R-07 est
  CONTRE-INTUITIF — quand gisement > besoin, la masse masquée fait BAISSER
  la couverture vers 1 (L-12 corrigée l'explique) ; `min_count=1` partout
  (unifié en session 3, test de propriété dans la suite).
- **PLM** : Paris/Lyon/Marseille par arrondissement — toujours agréger via
  `lovac.aggregate_plm` / `plm_parent`.
- **INSEE** : colonnes « (p) » provisoires ; espaces insécables ; concept
  « ménage » remplacé au 31/08/2025 (D-05 → D-06) ; la table
  d'appartenance (COM) ne contient PAS les arrondissements PLM ; certains
  xlsx cassent openpyxl → moteur calamine.
- **Classements publiés** : tri stable + clé de départage explicite.
- **pandas** : `groupby().sum()` transforme les NaN en 0 — `min_count=1`
  obligatoire (attrapé deux fois : notebook 06, puis R-04/R-05 en revue —
  le rho R-05 a bougé de 0,17 à 0,15 en le corrigeant).
- **Corrélations** : TOUJOURS publier IC de Fisher + périmètre
  (France/métropole) via `core/stats.py` ; ne jamais comparer des rho de
  périmètres différents (le « corrélat le plus fort » de R-08 n'a pas
  survécu à l'harmonisation).
- **Méthode** : aucun chiffre publié sans S-xx ; les constats d'un notebook
  se vérifient depuis les sorties ; les chiffres-titres doivent porter
  leurs conditions (l'erreur de la session 2 était de titrer « 1,65
  robuste » en publiant les caveats ailleurs).
- **Vacance recensement ≠ tension** : tout test de tension retranche la
  structurelle EFFECTIVE (× H-12) et documente L-12 ; vacances disponibles
  négatives (Corse) écrêtées du besoin, jamais comptées en besoin.
- **Zonage TLV (S-13)** : colonnes « Code EPCI »/« Libellé EPCI »
  INVERSÉES ; UTF-8 ; codes déjà à la commune parente pour PLM.
- **Recensement** : P22_RP_BDWC n'est renseignée que dans les DOM.
- **API ADEME data-fair** : ne jamais paginer les lignes (429) ; passer par
  values_agg (`logement acquire-dpe`) ; DPE quasi absents des DOM.
- **Cartofriches (S-20)** : inventaire PARTIEL bottom-up — planchers ;
  bati_surface vide ; plafonner par site (C-08) ; « NA » littéraux.
- **H-11 auto-contrôlée** : `core/foncier.py` recalcule la densité depuis
  S-11 × S-21 et refuse la dérive du registre.
- **Wayback** : l'URL S-25 (présentation RNA) est morte à l'origine — figée
  via archive.org ; vérifier les URL gouvernementales anciennes avant de
  les citer.
- **RPLS (S-28)** : la version « secret_donnees » masque les COMPTAGES
  en valeurs manquantes mais publie les RATIOS partout ; PLM par
  arrondissement (toujours `plm_parent`) ; le fichier contient Mayotte
  (ZE 0601 — DOM_ZE_PREFIXES de core/stats inclut « 06 » depuis la
  session 4) ; agrégation supra-communale UNIQUEMENT par la convention
  C-09 (pondération par le parc du millésime + contrôle national) ; le
  millésime « 2025 » décrit les emménagements 2024.
- **MIGCOM (S-29)** : COMMUNE est DÉJÀ en commune parente PLM mais
  DCRAN est en arrondissements (plm_parent sur l'origine seulement) ;
  IRAN = 0 (rattachement) hors champ ; le statut STOCD est celui de la
  date d'enquête (= statut d'ARRIVÉE pour un mobile) ; Mayotte
  n'apparaît qu'en ORIGINE de flux (aucun résident dans le champ) —
  l'index des flux doit unir résidence et origine pour que les soldes
  bouclent à zéro (attrapé par le test de propriété).
- **Melodi (api.insee.fr)** : les gros téléchargements décrochent en
  HTTP/2 — reprendre en HTTP/1.1 avec `curl -C -` et une détection de
  décrochage (`--speed-limit`) ; la taille exacte du Parquet est publiée
  dans le catalogue (`tailleFichierParquetEnOctets`) — contrôle
  d'intégrité gratuit ; le niveau FRANCE contient DEUX séries (F = hors
  Mayotte, FM = métropole — ne jamais mélanger, cf. T-12) ; les classes
  L_STAY 2023 ne se raccordent PAS à l'ANEM des diffusions antérieures
  (D-16).
