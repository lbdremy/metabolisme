# NEXT-STEPS — ce qui vient ensuite

Ce qui est déjà fait est consigné dans [`PREV-STEPS.md`](PREV-STEPS.md).
Mis à jour à chaque fin de session de travail significative.

## État au sortir de la session 3 (2026-08-07)

La **revue contradictoire** (méthode INTRO étape 12) est faite et INTÉGRÉE :
compte rendu dans `evidence/revue-contradictoire-2026-08-07.md` (+ annexes),
26 sources (S-22..S-26 : Cour des comptes mai 2025, SDES Datalab
déterminants, Apur, Cerema fonds friches), 7 hypothèses (H-07 RECENTRÉE sur
les emménagés récents — changement tracé ; H-12 taux d'existence du
gisement LOVAC), graphe à 85 nœuds (L-16..L-21, O-24), 82 tests verts,
document de preuve re-rendu et auto-vérifié. Les chiffres-titres ont
changé : couverture 1,65 → **1,06** (0,69 aux seules communes TLV), besoin
285 665 → **194 488**, coût de détente 12,5 → **15,8 Md€** (règle mixte,
ratio 3,9 → **2,1**), effort médian 40,1 → **27,4 %**, foncier 11,5 →
**10,9 ×** (plancher opérationnel 2,2 ×). La conclusion s'est DÉPLACÉE :
la contrainte institutionnelle n'est plus la conséquence de la suffisance,
elle en est la **condition** (I-07/I-10 reformulées). Tag :
**`efficacite-parc-v0.3`**.

## Prochaines étapes (dans l'ordre)

1. **Instruire H-04 (mobilités empêchées)** — l'éclairage données est FAIT
   (session 3, agent éclaireur) ; par rapport effort/valeur :
   1. RP INSEE **ancienneté d'emménagement** : base « Logement en 2023 »
      (RP2023, publiée 08/2026, https://www.insee.fr/fr/statistiques/8997194,
      CSV/Parquet, diffusée NATIVEMENT à la maille ZE, DOM hors Mayotte ;
      vérifier que ANEM y figure à cette maille ; caveat concepts européens
      2023, tables de passage fournies). Sinon base IRIS RP2022
      (P22_MEN_ANEM0002/0204/0509/10P,
      https://www.insee.fr/fr/statistiques/8647012). La mesure la plus
      directe de la rotation effective.
   2. **RPLS SDES 2025** (zip communes/EPCI 20 Mo,
      https://www.statistiques.developpement-durable.gouv.fr/media/8938/download?inline=) :
      taux de mobilité du parc social 7,1 % (2025) vs 9,3 % (2019) — la
      chute EST le phénomène ; + vacance sociale 2,1 %.
   3. Fichier détail **migrations résidentielles RP2022**
      (https://www.insee.fr/fr/statistiques/8589858, Parquet 17,2 M obs.) :
      taux de mobilité annuel par ZE + flux entre ZE.
   4. **DVF géolocalisées** (https://files.data.gouv.fr/geo-dvf/latest/csv/,
      par département) : prix → coût de transaction via une H-xx à déclarer
      (DMTO ~5,8 %, notaire, agence) ; pas d'Alsace-Moselle ni Mayotte.
   5. SNE : ressource data.gouv MORTE (404) ; portail vivant
      https://www.data.logement.gouv.fr/statistiques/ = exports par
      territoire sans bulk (effort élevé) ; raccourci possible par les
      indicateurs SNE de l'Observatoire des Territoires (maille à vérifier
      à la main). EnL 2020 : microdonnées sous habilitation — calibration
      nationale seulement.
   Le terme « coût de la mobilité résidentielle » (R-06) est disponible.
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
uv run logement reproduce   # rebâtit les 10 artefacts data/processed/
./check.sh && ./test.sh     # portes qualité (82 tests)
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
