# Revue contradictoire — angle STATISTIQUE (relecteur n°4)

**Date** : 2026-08-09. **Périmètre** : les seuls ajouts de la session 4 — R-11/I-11 (S-27), R-12/I-12 (S-28, C-09), R-13/I-13 (S-29), R-14/I-14 (S-30/S-31/S-32, C-10, H-13) — et leurs claims O-28..O-35, T-12..T-15, L-22..L-25. **État examiné** : commit `d563df4`, tag `efficacite-parc-v0.4`. **Méthode** : recalculs indépendants depuis les données brutes figées (`data/raw/`), avec re-dérivation complète des transformations de session 4 (lectures Parquet/xlsx/csv.gz propres, carte PLM propre, barème d'émoluments propre, Spearman via scipy) ; seuls les intrants amont déjà revus le 2026-08-07 (drapeau tendue R-07, indice de coût R-04, vacance structurelle R-02, table d'appartenance) sont repris de `src/logement`. Scripts : `00_upstream.py`, `01_r11.py`, `02_r12.py`, `03_r13.py`, `04_r14.py` (scratchpad de session, sorties reproduites ci-dessous). Environnement : env figé du projet + scipy 1.18.0 en surcouche éphémère (`uv run --with scipy`), repo intact.

---

## Recalculs

Tous les recalculs partent du brut. Verdicts : **exact** (identique à l'arrondi publié), **écart de convention** (explicable par une convention, à documenter), **erreur**.

### R-11 (S-27, artefact `mobilite-residentielle-ze.json`)

| Chiffre | Publié | Recalculé | Verdict |
|---|---|---|---|
| Parts nationales < 2 ans (F, hors Mayotte) | 13,14 / 12,89 / 11,97 % | 13,139 / 12,893 / 11,972 | **exact** (FM donnerait 13,131/12,898/11,989 — le périmètre F est bien tenu) |
| Delta 2012→2023 ; accélération | −1,17 pt ; −0,25 puis −0,92 | −1,1673 ; −0,2458 / −0,9215 | **exact** |
| « ~364 000 emménagements manquants » | 364 418 | 364 418 (−delta non arrondi × 31 220 147) | **exact** |
| ZE en baisse | 293 / 305 | 293 / 305 (les 305 ZE ont les deux millésimes) | **exact** |
| Distribution 2023 (min/q25/méd/q75/max) | 5,97/9,82/10,58/11,69/23,45 | idem | **exact** |
| Médianes delta tendues/autres | −1,54 / −1,27 (97 tendues) | −1,5365 / −1,2723 (n=97/208) | **exact** |
| rho métropole niveau×coût | +0,40 [+0,30;+0,49] n=287 | +0,4005 [+0,299;+0,493] n=287 | **exact** |
| rho niveau×vacance ; delta×coût ; delta×vacance (MET) | −0,22 ; −0,29 ; +0,25 | −0,2199 ; −0,2917 ; +0,2541 (IC conformes) | **exact** |
| Cohérence interne classes L_STAY | tolérance 1e-6 | dérive max 1,98e-9 | **exact** |

**Test distributionnel de l'écart de médianes (demandé par le mandat)** : Mann-Whitney bilatéral p = 0,0028 (unilatéral p = 0,0014) ; test de permutation sur la différence de médianes (20 000 tirages) p = 0,0030 ; KS p = 0,0083 ; en métropole seule, médianes −1,53 vs −1,23, MW p = 0,0006. **L'écart tendues/autres est significatif et robuste au périmètre — l'énoncé « chute concentrée » survit**, avec la nuance que l'effet est modeste (−0,26 pt sur des médianes de ~−1,3 ; sur les moyennes, Welch p = 0,094 non significatif) : la formulation des claims (« général mais SE CONCENTRE ») est proportionnée, celle du titre qmd (« surtout dans les marchés verrouillés ») s'appuie autant sur le gradient de rho (−0,29/+0,25, p < 1e-4) que sur les médianes — défendable.

### R-12 (S-28, C-09, artefact `mobilite-parc-social-ze.json`)

| Chiffre | Publié | Recalculé | Verdict |
|---|---|---|---|
| Série nationale (extraits) | 9,87 / 9,29 / 7,11 ; creux 7,55 (2021), rebond 8,54 (2022) | identique (13 millésimes relus de la feuille REGION) | **exact** |
| Contrôle C-09 | −0,000 / −0,007 / **0,014** pt | dérive réelle : −0,0006 / −0,0065 / **+0,0102** | **écart de convention** (voir ST-5 : la référence nationale est arrondie à 2 déc. avant soustraction) |
| n_ze 303 (306 − 3 sous seuil) ; en baisse 286 (2019) / 285 (2013) | idem | 303 ; 286 ; 285 | **exact** |
| Distribution 2025 ; médianes tension | 2,64/6,80/8,27/9,53/18,12 ; 6,74/8,89 ; vac. soc. 1,63/2,80 ; delta −2,40/−2,44 | identiques (6,740/8,886 ; 1,631/2,801 ; −2,398/−2,442 ; n_tendues 95) | **exact** |
| rho MET : niveau×coût ; ×vac. privée ; ×rotation R-11 ; delta×delta ; delta×coût ; ×vac. sociale | −0,80 [−0,84;−0,76] n=285 ; +0,48 ; −0,20 ; +0,19 ; +0,03 [−0,09;+0,14] ; +0,46 | −0,8026 ; +0,4799 ; −0,2038 ; +0,1856 ; +0,0272 ; +0,4646 (IC conformes) | **exact** |
| « chute UNIFORME » | rho +0,03 compatible zéro | confirmé ; MW delta tendues vs autres p = 0,998 | **exact** — l'uniformité est fortement soutenue |
| Piège NaN de `_weighted_rate` (num sans min_count) | — | 0 commune avec taux présent/parc absent ou l'inverse, aux trois millésimes ; variante « poids masqués si taux NaN » : écart max 0,0 pt | **pas d'effet** (fragilité latente, voir ST-9) |
| Sensibilité pondération C-09 | — | parc fixe 2025 : écart médian par ZE 0,05 pt (max 3,8) ; deltas médians −2,36/−2,39 (conclusion inchangée) ; non pondéré : max 15,5 pt (rejeté à raison) | **robuste** |
| Sensibilité seuil ≥ 500 | — | seuils 0/100/500/1000/2000 : rho MET −0,795…−0,817, médianes 6,74-6,90/8,88-8,89 | **robuste** |

### R-13 (S-29, artefact `migrations-residentielles-ze.json`)

| Chiffre | Publié | Recalculé | Verdict |
|---|---|---|---|
| Champ : 17 357 182 obs., poids 67,06 M ; rattachement 196 347 ; population 66 859 433 | idem | identiques | **exact** |
| Taux 9,87 % (3,18 / 6,25 / 0,44) | idem | 9,8653 (3,1819/6,2456/0,4377) | **exact** |
| Parts par statut | 32,98/19,51/13,38/8,34/5,73 | 32,9785/19,5104/13,3769/8,3372/5,7281 | **exact** |
| Ratios « 2,3 × » et « 3,4 × » | — | 2,340 et 3,406 | **exact** |
| Bouclage des flux O-D | — | somme des soldes = **0,0 exactement** ; index = union résidence ∪ origine ; ZE 0601 (Mayotte) gardée en origine seule, 5 347 sortants (O-33 ✓), taux NaN jamais 0 | **exact** |
| Paris | −1,40 %/an ; 225 906 sortants / 133 371 entrants | −1,400 ; 225 905,55 / 133 370,76 | **exact** |
| Couverture | 67 communes, poids 79 331 ; 11 406 sans origine ; flux inter-ZE 2 088 333 | identiques | **exact** |
| rho MET mobilité×rotation | +0,80 [+0,76;+0,84] n=287 | +0,8034 [+0,758;+0,841] | **exact** |
| rho FR solde×coût | −0,15 [−0,26;−0,04] n=297 | −0,1549 [−0,264;−0,042] ; MET −0,1085 [−0,221;+0,007] | **exact** (fragile — voir ST-3) |
| Médianes tension 9,5/9,4 « pas de gel en niveau » | — | 9,496/9,402 ; MW p = 0,14 — l'absence d'écart est correcte | **exact** |

### R-14 (S-30/S-31/S-32, C-10, H-13, artefact `cout-transaction-ze.json`)

| Chiffre | Publié | Recalculé | Verdict |
|---|---|---|---|
| Assiette | 3 514 036 ventes ; 733 529 un-seul-logement ; 727 209 après bornes | 3 714 829 lignes totales ; 3 514 036 ; 733 529 ; 727 209 | **exact** |
| Prix médians | 182 000 / 200 000 / 166 000 ; 2 658 €/m² | 182 000 / 200 000 / 166 000 ; 2 658,23 | **exact** |
| Barème émoluments | contrôle 1 995,25 € HT à 200 000 € | 1 995,25 (et test unitaire présent, `tests/test_transaction.py:77`) | **exact** |
| Péage en % du prix | 7,43-8,02, médiane 7,60 | 7,426 / 7,601 / 8,018 | **exact** |
| Mois de niveau de vie | min 2,76, méd 6,14, max 13,24 ; tendues 7,76 vs 5,53 (prix 198 990/133 629) | 2,756 / 6,137 / 13,244 ; 7,765/5,532 ; prix identiques ; MW p = 4,6e-25 | **exact** |
| rho MET mois×coût | +0,81 [+0,77;+0,85] n=278 | +0,8122 [+0,768;+0,849] | **exact** |
| 296 ZE ; médiane 1 380 ventes ; min 22 ; part fiscale ~83 % | idem | 296 ; 1 379,5 → 1 380 ; 22 ; 83,8 % (droits seuls ; la TVA des émoluments est aussi fiscale — l'énoncé est conservateur) | **exact** |
| Sensibilité bornes C-10 (mandat) | — | prix min 1 k€→20 k€, surface 10→20 m², prix/m² 100-50 000→500-20 000, aucune borne : médiane nationale 180 100-185 000 €, mois médians 6,11-6,19, tendues 7,76-7,91 vs autres 5,52-5,61 | **très robuste** |
| Sensibilité plancher ventes/ZE | — | seuils 0/50/100/200 : mois médians 6,09-6,14, rho +0,812…+0,824 | **robuste** |
| Diviseur commun (mois et indice partagent le niveau de vie au dénominateur) | — | rho brut-à-brut (coût € × loyer €) = **+0,866** > +0,812 ; benchmark « prix permutés, diviseur seul » : rho moyen −0,08 | **pas d'inflation** — le +0,81 publié est même conservateur |

---

## Objections

**ST-1 — Le superlatif « la corrélation la plus forte de la chaîne » (R-12) ne survit pas à R-14, publié dans le même état.**
**Cible** : R-12 (claims.yaml), I-12, qmd §R-12 (« la plus forte de toute la chaîne »), NEXT-STEPS.md l.15-16. **Gravité** : sérieuse. **Énoncé** : au périmètre métropole que la claim R-12 cite (−0,80, n=285), R-14 publie +0,81 (n=278 ; non arrondi : +0,8122 vs −0,8026) et R-13 +0,80 (+0,8034) ; en France entière, R-12 (−0,82) et R-14 (+0,82) sont à égalité. Les IC se recouvrent massivement ([−0,84;−0,76] vs [+0,77;+0,85] en valeur absolue) : le classement n'est ni vrai à 2 décimales ni statistiquement établi. C'est exactement le motif que la revue du 2026-08-07 a corrigé en C1 (superlatif R-08 ABANDONNÉ pour IC chevauchants) — la règle actée est ré-enfreinte par un texte écrit avant que R-14 n'existe et non réconcilié ensuite. **Preuve** : sorties `02_r12.py` / `04_r14.py` ci-dessus. **Effet si retenue** : aucune valeur ne change ; une phrase d'interprétation tombe. **Disposition proposée** : remplacer par « parmi les plus fortes de la chaîne (indistinguable des +0,80/+0,81 de R-13/R-14) » dans R-12, I-12, le qmd et NEXT-STEPS — ou motiver explicitement un critère (« la plus forte entre deux phénomènes distincts ») s'il est revendiqué.

**ST-2 — Les « mois de niveau de vie » de R-14 mélangent prix 2025 et revenus 2021 sans note de direction du biais.**
**Cible** : R-14, O-35, I-14, L-25. **Gravité** : sérieuse. **Énoncé** : `cout_en_mois_niveau_vie` divise un péage sur prix DVF **2025** par le niveau de vie Filosofi **2021** (S-10, seul millésime figé). Le chiffre-titre « 6,14 mois » (et 7,76/5,53, 11-13 mois) est donc surestimé en tant qu'énoncé 2025, de l'ordre de la croissance nominale du revenu médian 2021→2025 (à chiffrer avec une source si on veut le quantifier) ; les classements, l'écart tendues/autres et le rho sont insensibles (transformation quasi monotone commune). La revue précédente a traité le même hybride pour R-06 (C2 : « loyers 2025 ÷ revenus 2021 (direction tue) » → directions écrites dans L-09/L-11) ; L-25 liste cinq limites mais pas celle-ci. **Preuve** : `sources.yaml` S-10 (Filosofi 2021), `shell/build.py:657-671`, précédent C2 dans `evidence/revue-contradictoire-2026-08-07.md` l.101. **Effet si retenue** : caveat, pas de recalcul — sauf si « 6,1 mois » est titré dans l'article, auquel cas il doit porter sa condition (« en niveau de vie 2021 »). **Disposition proposée** : ajouter à L-25 un point (6) sur le modèle de L-09/L-11 : « prix 2025 / niveau de vie 2021 — niveaux de mois surestimés, classements et corrélations insensibles ».

**ST-3 — 32 rho publiés en une session : les corrélations faibles de second rang ne survivent pas à une correction de multiplicité.**
**Cible** : R-13 (solde×coût −0,15 FR), R-12 (« chutes faiblement co-localisées » +0,19), R-11 (delta×vacance FR +0,17) ; transversal. **Gravité** : sérieuse (comme caveat manquant), aucune conclusion-titre atteinte. **Énoncé** : la session 4 publie 16 paires × 2 périmètres = 32 rho. Sous Bonferroni à 16 tests (α = 0,0031) : solde×coût FR p = 0,0074 **ne tient pas** (et son pendant métropole −0,11 englobe déjà zéro), delta×vacance FR p = 0,0037 ne tient pas (mais le périmètre métropole +0,25, p = 1,3e-5, tient), delta×delta R-12 p = 0,0016 est limite. Les quatre conclusions principales reposent sur des rho à p ≪ 1e-6 (+0,80, −0,80, +0,81, +0,40, −0,29) ou sur des faits non corrélationnels (Paris 225 906/133 371) et survivent à toute correction. Mais I-13 appuie « les flux vident les cœurs chers » en partie sur le −0,15 : sans le fait parisien, ce rho seul ne suffirait pas. **Preuve** : p-valeurs recalculées (bloc « weak rhos »). **Effet si retenue** : caveat de fragilité sur les trois rho cités ; I-13 reformule sa hiérarchie de preuve (soldes observés d'abord, rho en appui). **Disposition proposée** : une phrase de réserve de multiplicité dans les claims R-12/R-13 (ou une note transversale dans le qmd), et marquer −0,15 / +0,19 comme « faibles, non robustes à la correction de tests multiples ».

**ST-4 — L'IC de Fisher avec SE = 1/√(n−3) est anti-conservateur pour un rho de Spearman aux |rho| élevés.**
**Cible** : `core/stats.py` (fisher_ci95), tous les IC publiés. **Gravité** : mineure. **Énoncé** : pour Spearman, la variance recommandée (Bonett-Wright 2000) est (1+ρ²/2)/(n−3) : à ρ = ±0,80-0,81, l'IC s'élargit de ~15 % (R-12 : [−0,845;−0,749] au lieu de [−0,840;−0,757] ; R-14 : [+0,760;+0,854] au lieu de [+0,768;+0,849] — soit [−0,85;−0,75] et [+0,76;+0,85] à 2 déc.). Aux |rho| ≤ 0,4 la différence est au 3e chiffre. Aucune conclusion ne bascule (vérifié sur les 8 blocs recalculés) ; ST-1 (chevauchement) en sort même renforcée. **Preuve** : colonnes « BW » des sorties `01`-`04`. **Disposition proposée** : soit adopter le facteur √(1+ρ²/2) dans `fisher_ci95`, soit documenter dans la docstring que l'IC est de type Pearson, légèrement étroit pour |rho| > 0,6.

**ST-5 — Le contrôle C-09 publié soustrait une référence nationale arrondie à 2 décimales.**
**Cible** : C-09, `core/social.py` (`parse_rpls_national` arrondit, `control_aggregation` compare ensuite), artefact (« 2025 : 0,014 »). **Gravité** : mineure. **Énoncé** : la dérive réelle 2025 est +0,0102 pt (agrégat 7,1241 vs national non arrondi 7,1139) ; le 0,014 publié contient jusqu'à ±0,005 de bruit d'arrondi de la référence. Sans effet sur la tolérance (0,05) ni sur la validité de C-09 — la claim « écarts ≤ 0,014 pt » reste vraie (et conservatrice). **Preuve** : sortie `02_r12.py`, lignes « C-09 ». **Disposition proposée** : comparer au national non arrondi (ou le noter dans C-09) ; mettre à jour le commentaire de code « ≤ 0.011 » qui décrit la dérive réelle alors que l'artefact publie la dérive contre référence arrondie.

**ST-6 — O-35 : « Porto-Vecchio 13,0 » — l'artefact et le recalcul disent 13,1.**
**Cible** : O-35 (claims.yaml). **Gravité** : mineure (coquille de transcription). **Énoncé** : valeur exacte 13,1316 → 13,1 dans `peage_le_plus_lourd` ; la claim écrit 13,0. **Preuve** : recalcul exact + artefact. **Disposition** : corriger en 13,1.

**ST-7 — O-33 : les énumérations de soldes sont des sélections présentées comme des classements.**
**Cible** : O-33 (claims.yaml). **Gravité** : mineure. **Énoncé** : la liste des soldes négatifs (« Savanes −2,49, Paris −1,40, Roissy −1,11, Evry −0,96 ») saute **La Tarentaise (−1,05, 4e)** ; la liste positive (« littoral et ouest : Les Sables-d'Olonne +1,91, Brignoles +1,81, La Rochelle +1,43, Dinan +1,41 ») saute **Marie-Galante (+1,54), Carhaix-Plouguer (+1,53), Ghisonaccia (+1,48), Draguignan (+1,45)** — la sélection soutient la lecture « littoral et ouest » plus nettement que le vrai top-8 (qui contient une ZE DOM et la Corse). Les artefacts publient les vrais classements (tri stable) ; seule la prose de la claim est sélective. **Preuve** : listes de l'artefact. **Disposition** : compléter les listes ou marquer « exemples » — la règle maison « classements publiés : tri stable + clé de départage » mérite un pendant « les énumérations de claims suivent le classement ou se déclarent sélectives ».

**ST-8 — R-14 ne publie pas sa couverture de jointure (332 ventes sans ZE).**
**Cible** : R-14, T-15, artefact `cout-transaction-ze.json`. **Gravité** : mineure. **Énoncé** : 332 ventes (0,05 %) dans 21 communes (dont 97127, écarts de COG) ne joignent aucune ZE et disparaissent sans trace publiée, alors que R-13 publie un bloc `couverture` pour le même type de perte (79 331 / 11 406). Asymétrie de discipline, sans effet mesurable sur les médianes. **Preuve** : sortie « ventes non jointes : 332, communes : [14623, …, 97127] ». **Disposition** : publier un bloc couverture dans l'artefact R-14.

**ST-9 — Fragilité latente de `_weighted_rate` (R-12) : pas de garde min_count ni de masquage des poids quand le taux est manquant.**
**Cible** : `core/social.py:120-123`. **Gravité** : mineure (aucun effet sur les données figées — vérifié : 0 commune où taux et parc ne sont pas manquants ensemble, aux trois millésimes ; variante masquée strictement identique). **Énoncé** : si un futur RPLS publiait un parc sans son taux (ou l'inverse), le numérateur perdrait la commune pendant que le dénominateur garderait son poids (taux biaisé vers le bas), ou une ZE toute masquée sortirait à 0 au lieu de NaN — le piège `min_count` déjà attrapé deux fois dans la chaîne. Le contrôle national C-09 le détecterait seulement si l'effet est > 0,05 pt au national. **Preuve** : sortie `02_r12.py`, lignes « rate present/weight NaN: 0 ». **Disposition** : masquer les poids où le taux est NaN + `sum(min_count=1)`, avec un test de propriété (cohérence avec le contrat « unknown keeps » affiché dans la docstring du module).

**Notes sans objection** (constats vérifiés, pour mémoire) : (a) le masque DOM inclut bien Mayotte 0601 partout (`DOM_ZE_PREFIXES` avec « 06 » ; n métropole 285/287/278 tous vérifiés) ; (b) aucun rho n'est publié sans IC ni périmètre, et aucune comparaison inter-périmètres indue n'a été trouvée dans la prose de session 4 (le seul rho cité en France entière, solde×coût, est étiqueté comme tel et son pendant métropole est publié) — la règle de la revue précédente est appliquée, à l'exception du superlatif ST-1 ; (c) le soupçon de « corrélation de diviseur commun » sur le +0,81 de R-14 (niveau de vie au dénominateur des deux variables) est **écarté par le calcul** : le rho brut-à-brut est plus élevé (+0,87) et le benchmark à prix permutés montre que le diviseur seul produirait ~−0,08 ; (d) H-13 à valeur centrale = borne haute est cohérent avec le statut « plancher » revendiqué (pas de scénario haussier : débours/agence exclus et documentés L-25) ; s'y ajoute, non documenté, le fait que les actes de début 2025 (avant l'entrée en vigueur des taux votés à 5,00 %) étaient à 5,81 % — couvert par la plage H-13, une demi-ligne dans L-25 suffirait ; le barème S-32 est explicitement métropole, appliqué aux ZE DOM (sens plancher, cohérent) ; (e) le recoupement RPLS 8,34 % ≈ 8,0-8,5 % (O-32) et « une libération tous les 20-25 ans » (1/4,1 %-1/4,7 %) sont arithmétiquement corrects ; Marseille 4,69 % vérifié pour la fourchette « 4,1-4,7 » du qmd.

---

## Verdict

**Arithmétique : exacte.** Sur ~60 chiffres recalculés indépendamment depuis le brut (parts nationales, deltas, comptages de ZE, distributions, médianes par tension, couvertures, flux, prix, barème, 16 rho et leurs IC/n), **aucune divergence** avec les artefacts publiés ; les artefacts, le qmd et les claims correspondent exactement, aux deux exceptions de transcription près (ST-6 Porto-Vecchio 13,0→13,1 ; ST-7 énumérations sélectives d'O-33). Les deux conventions nouvelles tiennent : C-09 est contrôlée (dérive réelle ≤ 0,011 pt — ST-5 sur la référence arrondie) et insensible au schéma de pondération comme au seuil ; C-10 est remarquablement robuste (médiane nationale ±1,6 %, mois médians ±0,05, rho ±0,01 sous toutes les variantes de bornes et de plancher testées).

**Survit tel quel** : R-11 en entier — y compris « chute concentrée », désormais étayée par un test (MW p = 0,003, permutation p = 0,003, métropole p = 0,0006) que je recommande de publier ; R-12 sauf son superlatif ; « chute uniforme » est fortement soutenue (MW p = 0,998) ; R-13 en entier, la validation croisée +0,80 et le fait parisien étant très solides ; R-14 en entier en géographie et en taux, le +0,81 étant même conservateur (pas d'artefact de diviseur commun).

**Ne survit pas tel quel** : (1) « la corrélation la plus forte de la chaîne » (R-12/I-12/qmd/NEXT-STEPS) — faux à 2 décimales face à R-14 au même périmètre et indistinguable statistiquement ; récidive du motif C1 déjà acté (ST-1) ; (2) les niveaux en « mois de niveau de vie » de R-14 comme énoncés 2025 sans le caveat prix 2025/revenus 2021 (ST-2 — même traitement que C2 : direction du biais dans L-25, classements insensibles) ; (3) les rho faibles −0,15 (R-13) et +0,19 (R-12) présentés sans réserve de multiplicité alors qu'ils ne tiennent pas une correction à 16 tests (ST-3). Ces trois corrections sont des reformulations et des caveats — **aucun recalcul d'artefact n'est nécessaire**.
