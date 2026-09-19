# EVIDENCE — index de la chaîne de preuves

Index humain des éléments de preuve de l'étude, par statut épistémique
(méthode Métabolisme, INTRO §4). Les registres machine font foi :
`sources/sources.yaml`, `sources/definitions.yaml`, `sources/hypotheses.yaml`,
puis `evidence/claims.yaml` pour le graphe de dépendances ; les mesures
sont dans `data/processed/rente-d15.json`, rebâti par `uv run autoroutes
reproduce`.

État au 2026-09-18 (session 1, autonome, non relue) : 17 sources figées
(20 fichiers, dont 4 non servis par le site), 9 définitions, 10
hypothèses, 28 observations, 1 transformation, 4 mesures, 4 résultats, 4
interprétations, 1 valeur, 5 choix, 1 proposition, 10 limites — 94 nœuds.
Document de preuve : `evidence/autoroutes-rente.qmd` ; article :
`articles/2026-09-autoroutes-la-rente-en-fin-de-contrat.md` ; décisions :
`evidence/decisions-2026-09-18.md`.

| Code | Statut | Registre / emplacement | État |
|------|--------|------------------------|------|
| S | Sources | `sources/sources.yaml` | S-01 cadrage monopoles/ au tag v1.0 · S-02 ART EGC3 2024 · S-03 ART Focus rentabilité 2023 · S-04 ART synthèse des comptes 2024 · S-05 Sénat n° 709 (2020) tome I · S-06 IGF-CGEDD 2021 · S-07 Sénat n° 65 (2024) · S-08 ASF rapport financier 2023 · S-09 Cofiroute 2023 · S-10 APRR comptes consolidés 2024 · S-11 VINCI comptes 2023 · S-12 contrat ASF consolidé 2024 · S-13 Autorité de la concurrence 14-A-13 · S-14 DGITM rapport 2020 · S-15 ART EGC1 2020 · S-16 ASFA chiffres clés 2025 · S-17 DGITM rapport 2024 |
| D | Définitions | `sources/definitions.yaml` | D-01 rente mesurable (monopoles:D-15) · D-02 base d'actifs (monopoles:D-21) · D-03 TRI de la concession / de la privatisation, actionnaire / projet (ART) · D-04 biens de retour (CCP L. 3132-4) · D-05 amortissement de caducité (Cofiroute) · D-06 TEITLD (APRR) · D-07 rachat de la concession (ASF art. 38) · D-08 fin anticipée pour dépassement de recettes (ASF art. 36.2) · D-09 coût du capital (ART) |
| H | Hypothèses | `sources/hypotheses.yaml` | H-01 taux de référence 5,0 % [4,0 ; 8,8] (monopoles:H-06) · H-02 coût du capital ART 7,0 [6,0 ; 7,8] · H-03 taux négocié par l'État 5,9 [5,9 ; 6,5] · H-04 CMPC de marché EDHECinfra 2,28 [2,28 ; 5,51] · H-05 linéarité TRI → chiffre d'affaires 7,86 %/pt [7,86 ; 8,0] · H-06 durée technique 60 ans [40 ; 100] · H-07 part Sanef-SAPN 17,4 % · H-08 part des prélèvements spécifiques 0,853 [0,75 ; 0,95] · H-09 extrapolation Sanef-SAPN (qualitative) · H-10 classement : non duplicable (monopoles:H-17) |
| O | Observations | `evidence/claims.yaml` | O-01 cadrage · O-02 TRI par société 2023 · O-03 coût du capital ≈ 7 %, ± 1 pt · O-04 0,7 pt ≈ 5,5 % du CA · O-05/O-06 coût du capital (Focus) · O-07 1 pt ≈ 8 % du CA · O-08 échéances · O-09 dividendes et TRI actionnaires (Sénat 2020) · O-10 privatisation 14,8 Md€, rachat 45-50 Md€ · O-11 6,5 → 5,9 % · O-12 EDHECinfra · O-13 caducité · O-14 impôts et taxes APRR · O-15 fiscalité 36 % (Sénat 2024) · O-16 CA 2024 par société (ASFA) · O-17 agrégats ART 2023-2024 · O-18/O-19/O-20 comptes 2023 ASF, Cofiroute, APRR · O-21 pôles VINCI · O-22 contrat ASF · O-23 IGF-CGEDD · O-24 Sénat 2024 · O-25 marges 2013 (ADLC) · O-26 flux 2024-2036 (ART) · O-27 concédant · O-28 méthode MEA (ART 2020) |
| T | Transformations | `evidence/claims.yaml` | T-01 transcription des comptes (`data/transcribed/comptes-2023.csv`, rebouclage du bilan) |
| M | Mesures | `evidence/claims.yaml` → `data/processed/rente-d15.json` | M-01 D-15 par groupe (deux bases × deux amortissements × six taux ; sept concessions) · M-02 agrégats du secteur · M-03 forme du régulateur (écart de TRI) · M-04 témoin |
| R | Résultats | `evidence/claims.yaml` | R-01 de combien (5,1-6,1 Md€ en 2023 ; 1,8-3,6 base brute ; 0,8-2,6 par TRI) · R-02 à qui (État ≈ 40 %, actionnaires ≈ 60 %, usager 0) · R-03 coût collectif · R-04 quatre configurations |
| I | Interprétations | `evidence/claims.yaml` | I-01 rente de position (témoin) · I-02 pourquoi deux mesures (la base) · I-03 le statu quo n'est pas un point fixe · I-04 le prix de 2006 |
| V | Valeurs | `evidence/claims.yaml` | V-01 reprise de monopoles:V-01/V-05 (destination dite) |
| C | Choix | `evidence/claims.yaml` | C-01 cadrage = source · C-02 périmètre et année · C-03 prélèvements = destination · C-04 deux bases · C-05 témoin |
| P | Propositions | `evidence/claims.yaml` | P-01 ce qui découle SI V-01 |
| L | Limites | `evidence/claims.yaml` | L-01 taux = jugement · L-02 linéarité · L-03 durée technique · L-04 Sanef-SAPN · L-05 ventilation des taxes · L-06 non-duplicabilité par le droit · L-07 IFRS · L-08 une année · L-09 coûts externalisés · L-10 second rang |

Fichiers non servis par le site (`redistributable: false`) : les rapports
financiers d'ASF, de Cofiroute, d'APRR et de VINCI et les chiffres clés de
l'ASFA — copies de vérification, empreintes contrôlées, non redistribuées.
