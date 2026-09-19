# NEXT-STEPS — ce qui vient ensuite

Ce qui est déjà fait est consigné dans [`PREV-STEPS.md`](PREV-STEPS.md).
Mis à jour à chaque fin de session de travail significative.

## État au sortir de la session 7 (2026-09-18/19) — deux articles écrits en autonomie

**Articles 2 et 3 sont ÉCRITS** : la proposition institutionnelle (tag
`article-proposition-institutionnelle-v1.0`, chaîne v0.6) et le flux
(tag `article-flux-v1.0`, chaîne `efficacite-parc-v0.7`). Chacun a subi
sa revue contradictoire le jour même (`evidence/revue-contradictoire-2026-09-18.md`
et `-flux.md`). Toutes les décisions prises sans Rémy sont dans
`evidence/decisions-2026-09-18.md` (DEC-01..DEC-28) — **Rémy doit les
relire** ; les plus réversibles : DEC-04/16 (valeur vénale + remploi),
DEC-17 (périmètre M-D), DEC-18 (acquisition sécurise, bail offert),
DEC-20 et DEC-28 (objections écartées), DEC-21 (sujet de l'article 3),
DEC-26 (H-21 uniforme), DEC-27 (affectation RS observée). État : 60
sources, 24 définitions, 16 hypothèses, 151 nœuds, 16 stages, 180 tests.

## Prochaines étapes (dans l'ordre)

1. **Lecture de Rémy** : articles 2 et 3, journal des décisions, deux
   comptes rendus de revue ; puis déploiement du site (trois posts
   enregistrés, contenu reconstruit, non déployé).
2. **Article 4 annoncé par l'article 3** : la production neuve — qui
   porte le chantier quand le marché s'arrête ? Structure de la
   production (promotion, bailleurs sociaux, particuliers — Sitadel
   liste des permis, datafile 8b35affb, avec RES_PRINCIP_OU_SECOND et
   catégorie de maître d'ouvrage), financement (Perspectives S-40,
   agréments SDES), ce qui l'a arrêtée (taux S-36, coûts S-18/S-19).
3. **Ce que R-18 laisse instruisable** : l'affectation réelle du neuf par
   ZE (fichier détail RP2022, ACHL × CATL, 500 Mo — SA-4) ; le
   sous-compte par département (série estimée départementale SDES) ; la
   ventilation TLV / hors TLV des commencés (SE-5, faisable avec S-13) ;
   le millésime 2025 des commencés (série communale, printemps 2027).
4. **Ce que P-01 laisse ouvert** (inchangé) : prix de repli, outil
   d'acquisition, surface des vacants, assiette foncière (CPO), flux —
   désormais instruit par R-18 dans le sens défavorable.
5. **Observations qui trancheraient H-04** (reportées, DEC-13) : DVF
   2026 (réforme DMTO 2025), RPLS 01/01/2026, rotation par âge × ZE.
6. **Restes ouverts des revues précédentes** et **frontières de données** :
   inchangés (voir sessions 3-5 ; s'ajoutent : décote des vacants,
   bilan du bail à réhabilitation, évaluation TVLH 2027).

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
uv run logement reproduce   # rebâtit les 16 artefacts data/processed/
./check.sh && ./test.sh     # portes qualité (180 tests)
```

Lire dans l'ordre : `CLAUDE.md` (doctrine + décisions arrêtées),
`EVIDENCE.md` (index humain), `evidence/decisions-2026-09-18.md` (le
journal des décisions de conception), les quatre comptes rendus de revue
(`evidence/revue-contradictoire-2026-08-07.md`, `-2026-08-09.md`,
`-2026-09-18.md`, `-2026-09-18-flux.md`), puis `evidence/claims.yaml`.
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
- **Sitadel (S-56/S-57)** : la série COMMUNALE (même en date réelle)
  ne compte que les déclarations remontées — ~15 % des chantiers ne
  remontent jamais (S-58) : toujours publier la lecture estimée (× H-21)
  et jamais comparer une série communale à la statistique publiée sans
  ce facteur ; en date réelle, une année est CLOSE dès qu'elle est
  passée (un événement 2023 déclaré en 2025 est compté en 2023) — ne
  pas écarter les dernières années comme « incomplètes » ; le fichier
  liste Paris en commune parente ET en arrondissements (ne pas sommer) ;
  2025 n'a que les autorisations ; codes au COG de l'événement →
  remapper par les mouvements de communes (S-59) avant toute jointure.
- **Ménages ≡ résidences principales** dans le recensement : un « besoin
  de flux » à structure constante est la croissance observée du parc ;
  un ratio construction / besoin ne mesure jamais une formation de
  ménages empêchée.
