# NEXT-STEPS — ce qui vient ensuite

Ce qui est déjà fait est consigné dans [`PREV-STEPS.md`](PREV-STEPS.md).
Mis à jour à chaque fin de session de travail significative.

## État au sortir de la session 5 (2026-08-09)

**R-11..R-14 sont REVUS et intégrés** (153 tests, 117 nœuds, 14 stages,
tag `efficacite-parc-v0.5`) : la passe contradictoire du 2026-08-09
(44 objections, 4 relecteurs — compte rendu
`evidence/revue-contradictoire-2026-08-09.md`) a confirmé toute
l'arithmétique et requalifié l'étage interprétatif. Les énoncés à
retenir : **R-11** — chute générale de la rotation (−1,17 pt, dont
~45 % démographiques au shift-share T-16 ; INSEE 14 %, S-33), contraste
tendues/autres significatif mais NON DISCRIMINANT (partiel ≈ 0 à
niveau 2012 contrôlé) ; le signal résiduel est l'ACCÉLÉRATION.
**R-12** — miroir du marché depuis au moins 2013 (−0,70 → −0,80, parmi
les plus fortes de la chaîne, ≈ R-13/R-14), chute uniforme en points
mais EXCÉDENTAIRE dans les marchés chers en relatif/partiel (−0,50).
**R-13** — cohérence interne du recensement (+0,80) et validation
inter-appareils MIGCOM×RPLS ; canal privé 19,51 % ; soldes parisiens =
profil du CYCLE DE VIE par âge (O-36), éviction = question ouverte.
**R-14** — péage territorialisé S-31 + CSI : 6,7-8,1 % du prix, médiane
6,15 mois (niveau de vie 2021), tendues 7,87 vs 5,59, 83,2 % fiscal,
primo 5,81 mois, annualisé 2,6-10 %/an ; rho +0,81 quasi mécanique
(mois × prix +0,98). Limite transverse L-26 (étalon T-05/T-08 partagé
par les quatre croisements). Part cyclique du choc du crédit 2022-2024
NON SÉPARÉE partout (S-36) — arbitres : millésimes 2026/2027. L'état
v0.3 de l'arc (couverture 1,06, besoin 194 488, détente 15,8 Md€ ratio
2,1, foncier 10,9 ×) est inchangé ; garde de lecture ajoutée au qmd.

## Prochaines étapes (dans l'ordre)

1. **Chemin de publication** : le premier article dans `articles/` peut
   s'écrire sur l'état v0.5 — l'arc v0.3 revu ET H-04 instruite/revue.
   Titres sur le récit REQUALIFIÉ : couverture ~1 conditionnelle,
   ratio ~2, contrainte institutionnelle = condition ; côté H-04 :
   chute générale + accélération non démographique + parc social
   miroir du marché + péage fiscal territorialisé — JAMAIS « signature
   d'une mobilité empêchée » ni « sources indépendantes » (les
   formulations exactes sont dans les claims). Licence à confirmer
   avant publication : loyers 2025 (S-09, L-09) — RPLS est réglée
   (Licence Ouverte, SA-6).
2. **Observations qui trancheraient H-04** (par coût croissant) :
   - **discontinuités DMTO × volumes DVF** (SE-12) — S-31 est
     territorialisée dans le code : le test de causalité du péage est
     à portée (comparer les volumes/prix aux frontières 5,81/6,32) ;
   - **rotation par âge × ZE** (SE-1c) — fichier détail Logement du RP
     (ANEM × AGEMEN8) : ferait renaître ou réfuterait proprement la
     lecture territoriale de I-11 ;
   - **millésimes post-choc** (SE-3) — RPLS au 01/01/2026 (non paru au
     2026-08-09) puis 2027, prochain L_STAY : rebond → cyclique,
     persistance → structurel. À figer dès parution.
3. **Restes ouverts de la revue du 2026-08-07** (inchangés) : emploi
   localisé récent à la maille ZE (L-07) et re-exécution de R-03 ;
   anomalie de réconciliation LOVAC communal/départemental ; point
   Paris 32 091 vs Apur ~18 600 (L-04) ; sourcer les référentiels de
   besoin en flux (L-21).
4. **Lever les frontières H-05 par convention** : PPPI (DREAL/DDT),
   fichiers fonciers/successions (Cerema) ; seule voie pour la piste
   successions/indivisions (I-08). Frontières consignées par la revue
   (SA-9) : Fidéli, EnL 2020, bases notariales BIEN/Perval, DV3F —
   toutes sous habilitation ; SNE : ressource data.gouv morte,
   portail territorial sans bulk.
5. **Frontières de données actées** (ne pas re-tenter sans nouveau
   levier) : fichiers LOVAC détaillés = habilitation ; éviction
   saisonnière infra-territoriale = non tranchable en open data ;
   frais d'agence = aucune source ouverte (l'écart OCDE ~14 % vs
   ~7,7 % calculés donne l'ordre de grandeur, S-33..S-38 notes).

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
uv run logement reproduce   # rebâtit les 14 artefacts data/processed/
./check.sh && ./test.sh     # portes qualité (153 tests)
```

Lire dans l'ordre : `CLAUDE.md` (doctrine + décisions arrêtées),
`EVIDENCE.md` (index humain), les deux comptes rendus de revue
(`evidence/revue-contradictoire-2026-08-07.md` et `-2026-08-09.md`),
puis `evidence/claims.yaml`.
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
- **DVF (S-30)** : une mutation = plusieurs lignes partageant la même
  valeur_fonciere — TOUJOURS passer par l'assiette C-10 (un seul
  logement par mutation, bornes de plausibilité) avant un prix ;
  code_commune SANS zéro initial (zfill) ; PLM par arrondissement ;
  hors Alsace-Moselle (livre foncier) et Mayotte ; ventes à l'euro
  symbolique présentes.
- **MIGCOM (S-29)** : COMMUNE est DÉJÀ en commune parente PLM mais
  DCRAN est en arrondissements (plm_parent sur l'origine seulement) ;
  IRAN = 0 (rattachement) hors champ ; le statut STOCD est celui de la
  date d'enquête (= statut d'ARRIVÉE pour un mobile) ; Mayotte
  n'apparaît qu'en ORIGINE de flux (aucun résident dans le champ) —
  l'index des flux doit unir résidence et origine pour que les soldes
  bouclent à zéro (attrapé par le test de propriété).
- **DMTO territorialisés (S-31)** : la table est encodée dans
  `core/transaction.py` (défaut 5,00 %, exceptions vérifiées ligne à
  ligne sur le PDF — le 65 manquait à la note initiale du registre) ;
  la composition des départements bouge au fil des délibérations
  (S-35) : dater toute énumération, ne jamais citer la liste sans son
  millésime de table.
- **Corrélations partielles et MW maison** : `core/stats.py` fournit
  partial_spearman (contrôle nommé, IC n−4) et mann_whitney_p
  (approximation normale, corrigée des ex æquo, None sous n = 8) — les
  IC de TOUTE la chaîne sont Bonett-Wright depuis le 2026-08-09 ;
  toute nouvelle corrélation delta × gradient doit publier son
  partiel à niveau initial contrôlé (leçon SE-1/SE-4).
- **Pyramide des âges (S-38)** : une feuille par année, bloc
  « Ensemble » colonnes 2-21, Mayotte incluse au champ France à
  partir de 2014 — exclure 976 pour le périmètre F de S-27 ; le
  parser refuse une feuille dont les classes ne re-somment pas aux
  totaux départementaux.
- **Melodi (api.insee.fr)** : les gros téléchargements décrochent en
  HTTP/2 — reprendre en HTTP/1.1 avec `curl -C -` et une détection de
  décrochage (`--speed-limit`) ; la taille exacte du Parquet est publiée
  dans le catalogue (`tailleFichierParquetEnOctets`) — contrôle
  d'intégrité gratuit ; le niveau FRANCE contient DEUX séries (F = hors
  Mayotte, FM = métropole — ne jamais mélanger, cf. T-12) ; les classes
  L_STAY 2023 ne se raccordent PAS à l'ANEM des diffusions antérieures
  (D-16).
