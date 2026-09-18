# NEXT-STEPS — ce qui vient ensuite

Ce qui est déjà fait est consigné dans [`PREV-STEPS.md`](PREV-STEPS.md).
Mis à jour à chaque fin de session de travail significative.

## État au sortir de la session 7 (2026-09-18)

**Le second article est ÉCRIT** (tag `article-proposition-institutionnelle-v1.0`,
chaîne `efficacite-parc-v0.6`) :
`articles/2026-09-proposition-institutionnelle.md`, sur les résultats
R-15..R-17 et la proposition P-01 revus le jour même (61 objections,
`evidence/revue-contradictoire-2026-09-18.md`). Toutes les décisions
prises en autonomie sont dans `evidence/decisions-2026-09-18.md`
(DEC-01..DEC-20) — **Rémy doit les relire** : chacune est réversible,
en particulier DEC-01 (périmètre), DEC-04/DEC-16 (prix d'acquisition à
la valeur vénale + remploi, sans décote), DEC-17 (seuil de 50 % du
périmètre M-D), DEC-18 (l'acquisition sécurise, le bail est offert),
DEC-20 (objections écartées). État : 53 sources, 23 définitions, 15
hypothèses, 144 nœuds, 15 stages, 172 tests.

## Prochaines étapes (dans l'ordre)

1. **Lecture de Rémy** : article 2, journal des décisions, compte rendu
   de revue ; puis tag/déploiement du site (post enregistré, contenu
   reconstruit, non déployé).
2. **Ce que P-01 laisse ouvert et qui est instruisable** :
   - le **prix de repli** qui rendrait le bail préférable à la cession
     (C-15(2)) — un paramètre de conception sans source : chercher les
     précédents (OFS/BRS, portage EPF, préemption avec décote) ;
   - l'**outil d'acquisition** (utilité publique d'une acquisition de
     logements vacants, D-22) — instruction juridique, pas
     statistique ;
   - la **surface des vacants durables** (L-27 : les totaux de M-B
     utilisent la surface des RP, majorant) — fichiers LOVAC détaillés
     ou Fidéli, sous habilitation ;
   - l'**assiette foncière** préalable à M-D (CPO S-51) ;
   - le **flux** (L-32 : ~24 Md€/an au prix S-18) — Sit@del par ZE.
3. **Observations qui trancheraient H-04** (reportées, DEC-13) :
   - **DVF 2026** : la réforme DMTO 2025 (passage à 5,00 % département
     par département, dates de vote S-31/S-35) est l'expérience
     naturelle propre — doubles différences à la Bérard-Trannoy (S-43)
     sur les volumes mensuels ; figer DVF 2026 dès parution ;
   - **RPLS au 01/01/2026** (non paru au 2026-09-18, page SDES
     vérifiée) puis 2027 : rebond → cyclique, persistance →
     structurel ;
   - **rotation par âge × ZE** (fichier détail RP, ANEM × AGEMEN8).
4. **Restes ouverts des revues précédentes** (inchangés) : emploi ZE
   récent (L-07) et re-exécution de R-03 ; réconciliation LOVAC
   communal/départemental ; Paris 32 091 vs Apur ~18 600 (L-04) ;
   référentiels de besoin en flux (L-21).
5. **Frontières H-05 et frontières de données** : inchangées (voir
   sessions précédentes) ; s'y ajoute : aucune source ouverte sur la
   décote des vacants durables (SA-14), aucun bilan national du bail à
   réhabilitation (SA-12), aucune évaluation de la TVLH 2027 (L-33).

## État de la chaîne R-01..R-14 (sessions 1-6)

Résumé de lecture de l'arc et de l'instruction de H-04 : voir
`PREV-STEPS.md` (session 5 pour les énoncés à retenir de R-11..R-14,
session 3 pour l'arc R-01..R-10) et `EVIDENCE.md`. L'état v0.3 de l'arc
(couverture 1,06, besoin 194 488, détente 15,8 Md€ ratio 2,1, foncier
10,9 ×) et les quatre mesures de mobilité sont inchangés par la
session 7, qui les CONSOMME (C-11).

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
uv run logement reproduce   # rebâtit les 15 artefacts data/processed/
./check.sh && ./test.sh     # portes qualité (172 tests)
```

Lire dans l'ordre : `CLAUDE.md` (doctrine + décisions arrêtées),
`EVIDENCE.md` (index humain), `evidence/decisions-2026-09-18.md` (le
journal des décisions de conception), les trois comptes rendus de revue
(`evidence/revue-contradictoire-2026-08-07.md`, `-2026-08-09.md`,
`-2026-09-18.md`), puis `evidence/claims.yaml`.
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
- **Scénarios institutionnels (core/institution.py)** : TOUT au m² —
  un prix par logement divisé par la surface d'un autre segment a coûté
  une revue (ST-1) ; S-18 = 169 200 € pour ~66 m² (2 550 €/m²), pas pour
  la surface des RP ; charges d'exploitation en €/logement (S-40 p. 24),
  jamais en proportion d'un loyer d'équilibre ; le produit DMTO OFGL est
  au périmètre constant (hors 75/69/2A/2B/972/973) — rapporter au parc
  du même périmètre et ne basculer que le droit départemental (taux
  voté × prix), pas le péage total ; le millésime OFGL de l'année N est
  publié en juin N+1 (pré-rapport) — vérifier avant de figer.
- **Cour des comptes S-22, p. 24** : les 6 700 sorties ZLV sont « 6,6 %
  des 102 000 logements dont les propriétaires ont été contactés », et
  « 3 % » en zone tendue = parmi les contactés — jamais « du stock ».
