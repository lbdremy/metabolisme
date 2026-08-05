# NEXT-STEPS — ce qui vient ensuite

Ce qui est déjà fait est consigné dans [`PREV-STEPS.md`](PREV-STEPS.md).
Mis à jour à chaque fin de session de travail significative.

## Prochaines étapes (dans l'ordre)

L'état à la fin de la session 1 est tagué **`efficacite-parc-v0.1`** ;
le milieu de session 2 est tagué **`efficacite-parc-v0.2`** (R-01..R-08).
La session 2 a ajouté **R-06** (taux d'effort — S-12, H-07, C-04/C-05),
**R-07** (tension et manque absolu — S-13..S-15, H-08, C-06, correction
tracée), **R-08** (état du bâti, première instruction de H-05 — S-16,
L-13) et **R-09** (coût de remobilisation ~12,5 Md€ vs ~48,3 Md€ en neuf
— S-17..S-19, H-09/H-10, C-07). Le détail est dans `PREV-STEPS.md` ; les
items ci-dessous sont ce qui reste à ouvrir. NOTE DE REPRISE : l'arc
quantifié de la proposition est complet (R-07 volume → R-08 état → R-09
coût) — l'item 4 (chemin de publication) est devenu praticable sans
attendre les items 1-3, si la prochaine session veut privilégier la
revue contradictoire et le premier article.

1. **Lever les frontières H-05 par convention** : PPPI (DREAL/DDT) et
   fichiers fonciers/successions (Cerema — statut « acteur public » à
   clarifier pour un chercheur indépendant) ; c'est la seule voie pour
   instruire la piste successions/indivisions des DOM (I-08).
2. **Instruire H-04 (mobilités empêchées).** Données candidates :
   demandes de logement social et délais (SNE / data.gouv), taux de
   rotation du parc, DVF pour les frais de transaction. Le terme « coût de
   la mobilité résidentielle » est désormais disponible (R-06). Levier à
   surveiller : le volet financier définitif de l'enquête Logement 2020
   (S-12 provisoire) donnerait des taux d'effort NETS observés à
   confronter à R-06. Les 41 ZE tendues non couvertes de R-07 (tension
   touristique) rejoignent la frontière infra-territoriale du notebook 06.
3. **Frontières de données actées** (ne pas re-tenter sans nouveau
   levier) : fichiers LOVAC détaillés = habilitation collectivités/État/
   Anah (sensibilité H-06) ; éviction saisonnière infra-territoriale =
   non tranchable en open data secrétisé (notebook 06) — leviers
   possibles : convention avec un partenaire habilité, registre des
   meublés de tourisme, monographies communales.
4. **Chemin de publication** : revue contradictoire (méthode INTRO
   étape 12 — chercher activement les objections), premier article dans
   `articles/` pointant le tag, licence du millésime loyers 2025 à
   confirmer avant publication (L-09), puis tag suivant.

## Comment reprendre (5 minutes)

```bash
cd logement
uv sync                     # env figé (uv.lock)
uv run logement validate    # registres + sha256 + graphe : doit être vert
uv run logement reproduce   # rebâtit les 9 artefacts data/processed/
./check.sh && ./test.sh     # portes qualité
```

Lire dans l'ordre : `CLAUDE.md` (doctrine + décisions arrêtées),
`EVIDENCE.md` (index humain du graphe), puis `evidence/claims.yaml`.
Le rendu du document de preuve : `QUARTO_PYTHON=.venv/bin/python quarto
render evidence/efficacite-parc-immobilier.qmd` (Quarto 1.10.18 installé).

## Pièges connus (ne pas redécouvrir)

- **LOVAC** : niveaux de vacance *totale* non comparables au travers des
  ruptures 2023/2025 (L-04) — seule la série structurelle est robuste ;
  parc privé ≠ vacance INSEE (L-06) ; secrétisation « s » < 11 (L-05) ;
  cp1252, `;`, milliers en espaces insécables ; millésimes mélangés
  (`2026` vs `_26`) normalisés à 4 chiffres par `core/lovac.py`.
- **PLM** : Paris/Lyon/Marseille arrivent par arrondissement — toujours
  agréger (le secret se propage) via `lovac.aggregate_plm`.
- **INSEE** : colonnes années suffixées « (p) » = provisoires ; libellés
  avec espaces insécables ; concept « ménage » remplacé au 31/08/2025
  (D-05 → D-06) — documenter toute jonction de séries ; la table
  d'appartenance (feuille COM) ne contient PAS les arrondissements PLM
  (feuille ARM) — toujours ramener les codes LOVAC à la commune parente
  avant jointure ; certains xlsx INSEE cassent openpyxl → moteur calamine.
- **Classements publiés** : tri stable + clé de départage explicite (les
  taux arrondis créent des ex æquo dont l'ordre varie selon la plateforme —
  attrapé par la CI, corrigé dans `build_summary`).
- **pandas** : `groupby().sum()` transforme silencieusement les NaN
  (secret) en 0 — toujours passer par `lovac.aggregate_plm` ou
  `min_count` (attrapé au notebook 06).
- **Méthode** : aucun chiffre publié sans S-xx enregistré ; les constats
  d'un notebook se vérifient depuis les sorties avant d'être écrits (une
  erreur de ce type a déjà été interceptée en session 1 — indice parc vs
  ménages).
- **Vacance recensement ≠ tension** : la vacance totale du recensement est
  haute partout (médiane ZE 8,6 % en 2022) et surestime l'offre disponible
  dans les centres denses (Paris commune 9,8 %) — tout test de tension
  doit retrancher la structurelle (C-06) et documenter L-12 ; à Ajaccio la
  structurelle LOVAC excède même les vacants recensés (artefact de
  périmètres, signalé dans l'artefact R-07).
- **Zonage TLV (S-13)** : colonnes « Code EPCI »/« Libellé EPCI »
  INVERSÉES par rapport aux en-têtes ; UTF-8 (pas cp1252), codes déjà à
  la commune parente pour PLM.
- **Recensement** : P22_RP_BDWC (confort sanitaire) n'est renseignée que
  dans les DOM — somme NULLE sur toute la métropole (vérifié session 2).
- **API ADEME data-fair** : débit anonyme étranglé (HTTP 429) — ne jamais
  paginer les lignes ; passer par values_agg par département × étiquette
  (agg_size max 1000, script `logement acquire-dpe`) ; DPE quasi absents
  des DOM ; jeu virtuel filtrant dpe_desactive=0.
