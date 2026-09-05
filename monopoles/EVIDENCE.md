# EVIDENCE — index de la chaîne de preuves

Index humain des éléments de preuve de l'étude, par statut épistémique
(méthode Métabolisme, INTRO §4). Les registres machine font foi :
`sources/sources.yaml`, `sources/definitions.yaml`, `sources/hypotheses.yaml`,
puis `evidence/claims.yaml` pour le graphe de dépendances.

État au 2026-09-05 (cadrage révisé après la revue contradictoire du
2026-09-04) : 16 sources figées, 21 définitions, 20 hypothèses, 9
observations, 5 choix, 6 valeurs, 3 interprétations, 12 limites — 92
nœuds ; aucun calcul. Document de preuve : `evidence/monopoles-naturels.md` ;
article : `articles/2026-09-reconnaitre-une-rente-de-position.md` ; revue :
`evidence/revue-contradictoire-2026-09-04.md` (compte rendu) et
`evidence/revue-contradictoire-2026-09-04/` (rapports bruts, synthèse).

| Code | Statut | Registre / emplacement | État |
|------|--------|------------------------|------|
| S | Sources | `sources/sources.yaml` | S-01 glossaire OCDE 2008 (non servi, L-10) · S-02 Ricardo ch. II · S-03 CCP L1121-1 · S-04 CGCT L1411-1 / L1412-1 / L2221-1 · S-05 CG3P L2111-1 / L3111-1 · S-06 OpenStax § 13.3 · S-07 CRE délib. 2025-77 · S-08 ART, économie des concessions autoroutières 2024 · S-09 ARCEP décision 2025-2047 (JORF) · S-10 Eaufrance, prix de l'eau · S-11 Carpentier et al. 2006 · S-12 Sénat n° 709 (2019-2020) · S-13 FIPECO · S-14 IGEDD, tunnel de Friggit · S-15 Sénat n° 498 (2025-2026), hydroélectricité · S-16 ART, glossaire (19 fichiers figés sha256/LFS dans `data/raw/`, empreintes recalculées au build) |
| D | Définitions | `sources/definitions.yaml` | D-01 monopole naturel · D-02 rente économique · D-03 rente de position (construite) · D-04 rente d'innovation (construite) · D-05 non-duplicabilité (construite) · D-06 rivalité · D-07 différenciabilité (construite) · D-08 captivité (construite) · D-09 concurrence pour / sur le marché (en partie construite) · D-10 concession · D-11 régie · D-12 DSP · D-13 CMPC régulé · D-14 domaine public · D-15 rente mesurable, surprofit sur base d'actifs (construite) · D-16 fixité positionnelle (construite) · D-17 exclusion · D-18 économies d'envergure · D-19 coûts irrécupérables · D-20 barrières à l'entrée · D-21 base d'actifs régulés |
| H | Hypothèses | `sources/hypotheses.yaml` | H-01..H-05 directrices (énoncé + condition de réfutation) · H-06 taux de référence du capital 5,0 % [4,0 ; 8,8] · H-07 seuil de part du parc ouvert (qualitative) · H-08 écart brut délégation / régie 10 % [0 ; 27] · H-09..H-20 hypothèses de classement de l'inventaire (dont témoins H-10, H-11) |
| O | Observations | `evidence/claims.yaml` | O-01 CMPC CRE · O-02 ARCEP 5,0 % nominal / 3,0 % réel · O-03 ART échéances 2031-2036, TRI [5,3 ; 8,8] · O-04 Eaufrance · O-05 Carpentier et al. · O-06 Sénat 6,5 → 5,9 % · O-07 FIPECO TRI · O-08 IGEDD loyers / prix · O-09 Sénat, réforme hydro |
| C | Choix | `evidence/claims.yaml` | C-01 la grille (Q1 à trois réponses, objet dit) · C-02 notions construites + D-15 · C-03 logement (rente de position, parc ouvert, 4 configurations) · C-04 ordre des études · C-05 quatre configurations, configurations à instruire par secteur |
| V | Valeurs | `evidence/claims.yaml` | V-01 la rente de position ne revient pas au propriétaire privé · V-02 propriété d'usage non visée · V-03 rente temporaire légitime · V-04 rente collectivisée visible · V-05 deux destinations dites · V-06 continuité du service |
| I | Interprétations | `evidence/claims.yaml` | I-01 lecture de l'inventaire · I-02 télécoms, cas à instruire · I-03 attribuer un surprofit à une position exige un témoin |
| L | Limites | `evidence/claims.yaml` | L-01 brevets · L-02 plateformes · L-03 seuil de bascule · L-04 régimes actuels · L-05 orbite et spectre · L-06 écart régie / délégation · L-07 traductions et notions construites · L-08 captures navigateur · L-09 propriétés physiques sans source · L-10 redistribution du PDF OCDE · L-11 surprofit ≠ rente, cas d'échec · L-12 observations de second rang |
| T/M/R/P | Transformations, mesures, résultats, propositions | — | relèvent des études sectorielles (gabarit INTRO §9) |

Modes de capture (L-08) : Légifrance (S-03, S-04, S-05, S-09) et OpenStax
(S-06) sont des captures de navigateur (DOM rendu) ; les autres copies sont
des téléchargements directs. Le PDF de l'OCDE est conservé pour
vérification et non servi par le site (L-10).

Matériau exploratoire (jamais cité comme établi) :

- `exploration/2026-09-grille-deux-questions-note-de-travail.md` — la note
  de travail d'origine, avec en préambule les divergences relevées contre
  les sources figées du dépôt.
