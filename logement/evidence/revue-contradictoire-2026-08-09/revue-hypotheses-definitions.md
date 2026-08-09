# Revue contradictoire n°2 — angle « Hypothèses et définitions » (session 4, R-11..R-14)

- **Date** : 2026-08-09
- **État examiné** : commit `d563df4`, tag `efficacite-parc-v0.4`
- **Périmètre** : H-13 ; D-16/D-17/D-18 ; C-09/C-10 ; O-25..O-35, T-12..T-15, R-11..R-14, I-11..I-14, L-22..L-25 ; usage amont de T-05 (indice de coût), T-08 (tension, H-08/H-12) et C-04 dans les quatre croisements. Les objections déjà intégrées le 2026-08-07 (`evidence/revue-contradictoire-2026-08-07.md`) ne sont pas re-soulevées.
- **Méthode de la passe** : lecture des registres (`logement/sources/*.yaml`), du graphe (`logement/evidence/claims.yaml`), du code stabilisé (`logement/src/logement/core/{mobilite,social,migrations,transaction,stats}.py`, `shell/build.py`), des artefacts (`logement/data/processed/*.json`), du document de preuve (qmd) et des notebooks 12-15 ; **recalculs indépendants en lecture seule** sur les sources figées (S-28 RPLS, S-30 DVF) — les scripts sont restés dans le scratchpad, aucun fichier du dépôt n'a été modifié.

L'arithmétique publiée a été recontrôlée par sondage : exacte partout où je l'ai refaite (barème S-32 : 1 995,25 € HT à 200 000 € ✓ ; 6,32/5,81/5,09 = 5,00/4,50/3,80 + 1,20 + 2,37 % du droit départemental ✓ ; part fiscale 83,8 % au prix médian ✓ ; 19,51/8,34 = 2,3 ✓ ; 1/4,1 %-1/4,7 % = 21-24 ans ✓ ; −1,17 pt × 31,22 M RP = 364 418 ✓ ; rho/IC conformes aux artefacts). Comme en session 3, les objections portent sur les modèles, les conventions et la mise en récit, pas sur les calculs.

---

## Objections

### HD-1 — « Validation croisée +0,80 entre deux sources indépendantes » : S-27 et S-29 ne sont pas indépendantes

**Cible** : R-13, I-13(1), qmd §R-13 (« R-11, source indépendante »), `EVIDENCE.md` l. 281, PREV-STEPS (« quatre mesures indépendantes »), NEXT-STEPS. — **Gravité : majeure** (l'interprétation I-13(1) ne survit pas telle quelle ; la corrélation, elle, survit).

**Énoncé.** S-27 (RP « Logement 2023 », L_STAY) et S-29 (MIGCOM RP2022, IRAN) sont deux produits du **même appareil de mesure** : le recensement de la population, alimenté par les mêmes enquêtes annuelles (EAR). Le millésime 2023 agrège les EAR ~2021-2025, le millésime 2022 les EAR 2020-2024 : **3 à 4 enquêtes sur 4-5 sont communes** (l'EAR 2021 ayant été annulée pour cause de COVID, chaque millésime repose en réalité sur quatre enquêtes, dont trois partagées : 2022, 2023, 2024). Un même ménage enquêté en 2023 alimente les DEUX fichiers, et son « emménagé depuis moins de 2 ans » (L_STAY) et son « résidence différente un an avant » (IRAN) sont des réponses **du même questionnaire** décrivant en partie les mêmes événements. Un rho de +0,80 entre les deux est attendu quasi mécaniquement ; surtout, une erreur de mode commun (collecte, pondération IPONDI, années COVID) survivrait dans les deux — c'est exactement ce qu'une « validation croisée entre sources indépendantes » prétend exclure.

**Preuve.** `claims.yaml` R-13 : « rho métropole +0,80 […] entre deux sources indépendantes » ; I-13 : « (1) la validation croisée +0,80 (R-11 × R-13, sources indépendantes) établit que la géographie de la rotation est un fait robuste, pas un artefact de source ». Or S-27 `temporal_scope: millésimes RP 2012, 2017 et 2023` et S-29 `millésime RP 2022` sont tous deux `publisher: INSEE`, produits du RP ; D-18 caveat 1 reconnaît lui-même la mécanique EAR.

**Effet si retenue.** Le +0,80 reste publié comme **cohérence interne du recensement entre l'axe logements et l'axe personnes** (ce qui a une valeur : deux variables distinctes, deux pondérations) — mais ne peut plus « établir que ce n'est pas un artefact de source ». La **vraie** validation externe de la session 4 est ailleurs et déjà dans la chaîne : MIGCOM 8,34 % HLM ≈ série RPLS 8,5/8,0 (recensement déclaratif × répertoire administratif des bailleurs — appareils réellement disjoints).

**Disposition proposée.** Reformuler R-13/I-13/qmd/EVIDENCE.md : « deux fichiers distincts du même recensement — cohérence interne logements/personnes » ; promouvoir le recoupement MIGCOM×RPLS au rang de validation croisée inter-appareils ; corriger la phrase « quatre mesures indépendantes » du bilan H-04 (PREV-STEPS) en « quatre mesures issues de trois appareils (recensement ×2, RPLS, DVF) ». Voir aussi HD-14 (le « cinq enquêtes » de D-18).

### HD-2 — Les quatre croisements convergent contre le MÊME étalon (T-05, T-08) ; le contraste tendues/autres n'a aucune sensibilité H-08×H-12

**Cible** : T-12/T-13/T-14/T-15, I-14 (« cohérence d'ensemble »), médianes « tendues/autres » de R-11..R-14. — **Gravité : sérieuse.**

**Énoncé.** Les quatre résultats sont corrélés au même indice de coût T-05 (loyers 2025 / Filosofi 2021) et partitionnés par le même drapeau « tendue » T-08, recalculé dans chaque stage **aux seuls centraux** H-08 = 6 % et H-12 = 0,75 (`build.py` : `tension.tension_by_ze(…, h08.central_value, h12.central_value)` dans les quatre `build_*`). La « cohérence d'ensemble » d'I-14 (rho +0,40 / −0,80 / +0,81 « là où tout cela se cumule ») est donc une convergence de quatre mesures **contre un étalon partagé** : une erreur de T-05 ou du drapeau (bande grise ± 1 pt : 43 ZE tendues sur 97, L-12) se propagerait identiquement aux quatre. Contrairement à R-07 (grille H-08×H-12 publiée), aucun des contrastes-titres de la session 4 (−1,54 vs −1,27 pt ; 6,74 vs 8,89 % ; 7,8 vs 5,5 mois) n'est publié à une autre valeur de H-08/H-12. Accessoirement, `build_summary` fait partout `frame["tendue"].fillna(False)` : une ZE au statut de tension **inconnu** (Mayotte dans R-12, hors champ du recensement 2022) est classée « autres » — contraire à la règle « unknown keeps » (sa mobilité 18,12 % gonfle légèrement la médiane « autres », dans le sens favorable au contraste).

**Preuve.** `claims.yaml` liste honnêtement T-05/T-08/H-08/H-12 dans les `depends_on` des quatre T-xx — la dépendance est déclarée, mais aucun énoncé R/I ne la porte ; `social.py`/`mobilite.py`/`migrations.py`/`transaction.py` : `tendues = frame["tendue"].fillna(False)`.

**Effet si retenue.** Les énoncés de convergence restent vrais mais doivent dire contre quoi ils convergent ; les contrastes tendues/autres doivent être montrés stables sur la plage H-08 (ou au moins signalés sensibles à la bande grise).

**Disposition proposée.** Une phrase dans I-14 (« convergence contre le même indice de coût et le même statut de tension — dépendance partagée, pas quatre confirmations indépendantes ») ; publier le contraste tendues/autres d'au moins R-11 et R-14 aux bornes H-08 = 5 et 7 % ; traiter tension NaN comme « inconnue » (exclue des deux médianes, poids publié).

### HD-3 — La sensibilité H-13 annoncée par T-15 n'est publiée nulle part ; le scénario « haut » duplique le central

**Cible** : H-13, T-15, R-14, artefact `data/processed/cout-transaction-ze.json`. — **Gravité : sérieuse** (règle INTRO §21-11 ; promesse du graphe non tenue).

**Énoncé.** T-15 annonce « droits de mutation aux trois scénarios H-13 (5,09/6,32/6,32) » ; `transaction_frame` calcule bien `cout_transaction_bas/central/haut`, mais `build_summary` ne publie **que** le central : l'artefact JSON ne contient aucune clé `bas`/`haut` (vérifié), la section « Sensibilité » du qmd couvre C-03 et H-07 mais pas H-13. De plus `haut = plausible_range[1] = 6,32 = central` : les « trois scénarios » sont en réalité deux, et le scénario réellement informatif — **5,81 %** (droit commun 4,50, appliqué aujourd'hui à ~10 départements et à tous les primo-accédants, et taux de retour si la faculté temporaire s'éteint au 31/03/2028) — n'existe pas.

**Preuve.** Inspection du JSON : clés = `{cout_pct_prix, distribution_mois_niveau_vie, hypothesis, …}`, aucune occurrence de `bas`/`haut`. `transaction.py` l. 118-124 : seules les colonnes `central` sont dérivées en `%` et en mois.

**Effet si retenue.** À 5,81 % la médiane passe de ~6,1 à ~5,7 mois, à 5,09 % à ~5,2 mois ; tendues ~7,8 → ~7,3/6,5. La conclusion (péage record là où tout se cumule, majoritairement fiscal) **survit sur toute la plage** — raison de plus pour publier la fourchette, qui est ici gratuite.

**Disposition proposée.** Publier mois/`%` aux trois scénarios dans l'artefact et le qmd ; remplacer le scénario « haut » fantôme par un vrai scénario intermédiaire 5,81 (registre : plage inchangée, scénarios {5,09 ; 5,81 ; 6,32}).

### HD-4 — H-13 uniforme à 6,32 % alors que S-31 permet le calcul exact — et le « central » est la borne haute de sa propre plage

**Cible** : H-13, C-10/T-15, L-25(2), médianes tendues de R-14. — **Gravité : sérieuse.**

**Énoncé.** La table S-31 est figée **par département** ; DVF porte `code_commune` : territorialiser est une jointure déterministe à coût quasi nul. La convention « 6,32 partout » surestime le péage de ~0,51 pt de prix (≈ 6,5 % du péage) dans les départements restés à 4,50 % — dont le **06** (Nice, Menton, Cannes : exactement les ZE que R-12 met en vitrine du gel social) et le **971** (Guadeloupe, ZE déjà fragiles, cf. HD-7). Le biais va **dans le sens de la thèse** (péage surestimé en zone tendue emblématique) — le cas que la méthode demande de traquer en priorité. Par ailleurs, prendre pour « valeur centrale » la borne haute de la plage inverse la sémantique du registre (partout ailleurs le central est le cas type, les bornes le stress) ; le vrai « cas type » pondéré par les ventes est légèrement sous 6,32.

**Preuve.** S-31 notes : « restent à 4,50 % une dizaine de départements (05, 06, 07, 16, 26, 27, 48, 60, 71, 971) ; Indre (36) […] à 3,80 % ». L-25(2) documente la limite mais ne chiffre rien et aucun résultat ne la déclenche (« si un résultat en dépend » — R-12/R-14 citent Nice et Menton : un résultat en dépend déjà).

**Effet si retenue.** Nice/Menton : mois × ~0,935 ; médiane des 96 tendues quasi inchangée (une poignée de ZE concernées) ; les classements-titres (Paris, Bayonne, La Réunion — tous à 5,00 %) tiennent.

**Disposition proposée.** Territorialiser les droits depuis S-31 (département du `code_commune`) — c'est l'option la plus conforme à « parse at the boundary » ; à défaut, publier l'écart borné par ZE concernée dans l'artefact.

### HD-5 — Le primo-accédant, acteur central de la « mobilité de statut » d'I-14, ne paie pas 6,32 %

**Cible** : I-14, qmd §R-14 (« chaque achat paie un péage […] 6,32 % »), H-13/L-25(1). — **Gravité : sérieuse.**

**Énoncé.** I-14 raconte la tenaille du **locataire** des zones tendues : relocation à ~64 % du revenu à Paris OU sortie par l'achat. Or ce ménage-là, s'il achète, est très souvent **primo-accédant** — précisément le cas exclu du champ de H-13 (« hors primo-accédants », maintenus à 4,50 % départemental → 5,81 % total, S-31). Le taux central 6,32 % décrit l'acheteur **déjà propriétaire** (secundo-accession), pas la mobilité de statut locataire→propriétaire que l'interprétation met en avant. La formule du qmd « chaque achat paie un péage — droits de mutation (H-13 : 6,32 %…) » est inexacte pour une part importante des transactions (primo + 10 départements). L'assiette (H-13) et l'énoncé (I-14) ne désignent pas la même population.

**Preuve.** `hypotheses.yaml` H-13 : « hors primo-accédants » ; L-25(1) : « hors primo-accédants (maintenus à 4,50 % départemental) » — la limite existe mais l'interprétation ne la porte pas ; qmd l. 1015-1017.

**Effet si retenue.** Pour le primo, péage ~7,1 % du prix au lieu de ~7,6 (part fiscale ~82 %) : toujours record en zone tendue, mais le chiffre-titre au cas d'I-14 est ~6-7 % plus bas. La conclusion survit ; la phrase « chaque achat » non.

**Disposition proposée.** Le scénario 5,81 de HD-3 EST le scénario primo : le publier et l'appeler ainsi ; reformuler I-14/qmd (« 6,32 % hors primo-accédants, 5,81 % pour le primo-accédant — la tenaille tient aux deux taux »).

### HD-6 — C-10 écarte le tiers des logements vendus, et ce volume n'est publié nulle part

**Cible** : C-10, O-34, L-25. — **Gravité : sérieuse** (règle INTRO §21-9 : documenter les données écartées).

**Énoncé.** L'exclusion des mutations multi-logements est **conceptuellement juste** pour R-14 (le prix par logement y est indéterminé, et l'objet est l'achat d'UN logement par un ménage), mais son ampleur est matérielle et invisible du lecteur : recalcul sur S-30 — 1 245 125 mutations de vente, dont 127 555 portent ≥ 2 logements, soit **375 007 logements = 33,4 %** des logements vendus en 2025 hors de l'assiette (plus 13 029 mutations logement+local commercial, typiquement l'immeuble de centre-bourg avec commerce au rez-de-chaussée). Cette sélection n'est pas aléatoire (ventes en bloc, immeubles de rapport, mixité commerciale → urbaine et investisseurs) : le « prix médian France 182 000 € » est le médian **des achats unitaires**, pas des logements ayant changé de main. O-34 ne publie que « 733 529 mutations à un seul logement » — le lecteur ne peut pas voir ce que la convention retranche.

**Preuve.** Recalcul (script scratchpad) : `0 dwellings: 371 012 ; 1 dwelling no commercial: 733 529 ; 1 dwelling with commercial: 13 029 ; ≥2 dwellings: 127 555` ; logements dans les mutations exclues : 375 007.

**Effet si retenue.** Aucun chiffre ne change ; l'assiette devient honnête sur ce qu'elle couvre (≈ 2/3 des logements vendus, la totalité du concept visé).

**Disposition proposée.** Publier les comptages d'exclusion dans O-34 et l'artefact ; une ligne en L-25 (« l'assiette couvre l'achat unitaire — 33 % des logements vendus le sont en mutations multi-logements, hors champ par construction »).

### HD-7 — Bornes de plausibilité C-10 : sans effet en métropole (vérifié), structurantes dans les petites ZE DOM ; aucune sensibilité publiée, et pas de seuil de ventes pour les classements

**Cible** : C-10, O-34/O-35, L-25(3), listes `peage_le_plus_lourd`. — **Gravité : sérieuse.**

**Énoncé.** Les bornes (≥ 5 000 € ; ≥ 10 m² ; 200-30 000 €/m²) ne retirent que 6 320 ventes (0,86 %) et leur effet sur le prix médian de ZE est négligeable en métropole : recalcul — effet médian **+0,47 %**, q90 2,7 % ; le plafond 30 000 €/m² n'écarte que 328 ventes en France (125 à Paris ; médiane parisienne 322 000 vs 323 000 € sans plafond). MAIS dans les petites ZE de Guadeloupe l'assiette est si mince que la convention fait le résultat : ZE 0101 — 57 ventes unitaires dont 8 sous 5 000 € et 13 hors bornes €/m², 36 retenues, médiane 304 835 € (contre 24 000 € sans bornes) ; ZE 0103 (Marie-Galante) : 25 retenues, médiane +28 % vs sans bornes ; un resserrement raisonnable (10 000 € ; 15 m² ; 400-25 000) déplace des médianes de ZE jusqu'à ~36 %. Les extrêmes-titres réunionnais sont, eux, robustes (L'Ouest 1 022 ventes, Le Sud 1 596, ~1-2 % écartés). Enfin R-12 impose un seuil de robustesse (parc ≥ 500, hors classements sous le seuil) mais R-14 classe des ZE à 22 ventes — deux conventions de robustesse incohérentes dans la même session.

**Preuve.** Recalculs ci-dessus (scripts scratchpad sur S-30) ; `transaction.py` : aucune trace des bornes dans l'artefact au-delà de `n_ventes_retenues` ; `social.py` : `MIN_PARC_SOCIAL = 500`.

**Effet si retenue.** Les chiffres-titres (médiane 6,1 mois, tendues 7,8, Paris/Bayonne/La Réunion) tiennent ; les ZE guadeloupéennes ne devraient pas pouvoir entrer dans un classement sans avertissement, et la borne basse 200 €/m² doit être discutée (elle écarte du bâti dégradé réel en marché détendu — remonte mécaniquement la médiane des ZE pauvres).

**Disposition proposée.** Publier la sensibilité des bornes (n écartés par borne, effet sur la médiane par ZE) dans l'artefact ; ajouter un seuil de ventes pour les classements (symétrique du seuil R-12), publié dans C-10 ; compléter L-25(3).

### HD-8 — Les deltas C-09 2019→2025 mélangent variation des taux et recomposition du parc ; des chiffres publiés bougent de > 1 pt

**Cible** : C-09, T-13, O-30, R-12 (deltas), L-23, liste `plus_fortes_baisses` (Issoire). — **Gravité : sérieuse.**

**Énoncé.** `delta_2019_2025` = moyenne pondérée par `nb_ls` (parc 2025) moins moyenne pondérée par `nb_ls2019` : entre les deux, le parc passe de 5,08 à 5,40 M, 324 communes entrent (4 794 logements), 5 sortent, et les poids relatifs de toutes les communes bougent (livraisons, démolitions ANRU). Le delta publié n'est donc pas « la baisse du taux » à périmètre constant. Recalcul en panel équilibré à pondération fixe (communes à parc > 0 aux deux millésimes, poids 2025) : effet **négligeable sur les médianes** (tendues/autres −2,40/−2,44 publiés vs −2,41 à composition fixe — la conclusion d'uniformité de R-12 est robuste, vérifiée), mais fort sur des ZE individuelles publiées : **Issoire −13,18 publié vs −11,84 à composition fixe (1,3 pt)**, Porto-Vecchio 1,1 pt, ZE 9316 1,5 pt, Mayotte 1,8 pt ; q90 des écarts 0,22 pt.

**Preuve.** Recalcul (script scratchpad sur S-28) ; `social.py` `social_by_ze` l. 133-142 ; L-23(3) attribue le −13,2 d'Issoire à la volatilité des petits parcs — c'est en partie un effet de composition, non documenté.

**Effet si retenue.** R-12 (national, médianes, uniformité) survit tel quel ; la liste « plus fortes baisses » et tout commentaire sur un delta de ZE individuel doivent porter le caveat de composition.

**Disposition proposée.** Ajouter le point à L-23 (« le delta compare deux pondérations de deux parcs — variation de taux et recomposition confondues ») ; idéalement publier la variante panel équilibré dans l'artefact (le contrôle existe, il coûte dix lignes).

### HD-9 — Le secret statistique ne mord PAS sur les colonnes de C-09 : constat favorable à enregistrer, énoncés à préciser

**Cible** : C-09, O-28, S-28 (notes), L-23(1), commentaire de `social.py`. — **Gravité : mineure** (vérification qui RENFORCE R-12).

**Énoncé.** O-28 (« comptages masqués en valeurs manquantes ») et le piège consigné dans NEXT-STEPS laissent craindre un masquage corrélé à la taille du parc qui biaiserait la moyenne pondérée. Vérification sur S-28 : sur les 16 863 communes, **zéro valeur manquante** sur `nb_ls`, `nb_ls2019`, `nb_ls2013`, `tx_mob`, `tx_mob_2019`, `tx_mob_2013` ; les comptages sont publiés dès 1 logement (711 communes à nb_ls = 1) et `Σ nb_ls = 5 396 259` = le national exact. Le masquage réel touche les colonnes de loyers (`evol_loyer*`, ~5 700 NaN), hors usage. La question « le contrôle national valide-t-il la maille ZE ? » a donc une réponse plus solide que L-23 ne l'énonce : l'agrégat ZE est une moyenne pondérée **exacte de données complètes** ; la seule approximation restante est le proxy de poids (`nb_ls` = parc total ≠ « proposés à la location depuis ≥ 1 an », le vrai dénominateur de D-17), dont le contrôle national (écarts −0,000/−0,007/+0,014 pt) borne l'effet agrégé sans le borner ZE par ZE — ce que L-23(1) dit déjà. Détail : le commentaire de `social.py` (« ≤ 0.011 pt ») est périmé vs l'artefact (0,014).

**Disposition proposée.** Préciser O-28/S-28 (« le masquage touche les loyers ; comptages et taux de mobilité complets — vérifié ») ; reformuler L-23(1) sur le seul proxy de poids ; corriger le commentaire.

### HD-10 — « Locatif privé » = STOCD 21 « loué vide non HLM » : le label glisse ; le recoupement RPLS croise deux périmètres différents

**Cible** : O-32, R-13, I-13(2), `migrations.py` (`STOCD_LABELS`). — **Gravité : mineure.**

**Preuve.** Varmod S-29 : `21 ; Locataire ou sous-locataire d'un logement loué vide non HLM` — inclut le parc des bailleurs sociaux non-HLM (SEM…) et les institutionnels ; et le « 8,34 % HLM » est un statut **déclaré par le ménage**, comparé à un taux issu du répertoire des bailleurs (D-17), sur des unités différentes (personnes vs logements).

**Effet si retenue.** Le « 19,51 % » et la conclusion « canal principal » survivent largement (le non-HLM social est marginal dans le 21) ; le recoupement 8,34 ≈ 8,0-8,5 reste un ordre de grandeur, ce que L-24(6) couvre déjà pour les fenêtres mais pas pour les périmètres.

**Disposition.** Une ligne dans D-18 ou L-24 (« STOCD 21 = non-HLM, étiqueté “locatif privé” par approximation ; statut HLM déclaratif »).

### HD-11 — « La propriété est le statut le moins mobile » : glissement contre L-24(1)

**Cible** : R-14 (titre), I-14, qmd §R-14. — **Gravité : mineure.**

L-24(1) établit que le taux par statut est un **taux d'entrées dans le segment d'arrivée** ; R-13/O-32 le disent proprement (« entrées de l'année »), mais R-14/I-14 le réénoncent en propension (« le statut le moins mobile »). Défendable en régime permanent (entrées ≈ sorties), mais c'est précisément le raccourci que la limite interdit. Reformuler : « le statut dans lequel on entre le moins » — qui est d'ailleurs plus fort pour I-14 (la barrière est à l'entrée, là où est le péage).

### HD-12 — Texte de H-13 : la borne basse 5,09 confondue avec le droit commun 5,81

**Cible** : `hypotheses.yaml` H-13. — **Gravité : mineure** (exactitude du registre).

**Preuve.** « plage plausible [5,09 ; 6,32] — la borne basse est aussi le taux qui redeviendrait de droit commun (5,81) puis plancher si la faculté temporaire s'éteint en 2028 » : telle qu'écrite, la phrase identifie 5,09 à 5,81. En réalité : extinction de la faculté → retour au droit commun **5,81** ; 5,09 reste le plancher observé (Indre ; Mayotte hors champ). Réécrire — et la correction converge avec HD-3/HD-5 (faire de 5,81 un scénario nommé).

### HD-13 — O-26 embarque une interprétation non établie (« les ménages entrés récemment ne re-bougent plus aussi vite »)

**Cible** : O-26. — **Gravité : mineure** (discipline des types du graphe, INTRO §21-8).

Le gain de +0,74 pt de la classe 2-4 ans en 2023 s'explique aussi **mécaniquement** : quand le flux d'entrées chute en fin de période, les cohortes entrées 2019-2021 (avant la chute) vieillissent dans la classe 2-4 ans qui gonfle relativement — sans qu'aucun ménage ne « re-bouge moins vite ». Un O-xx doit rester observationnel ; la lecture cohorte appartient à I-11 avec sa réserve. Déplacer la phrase, ou la remplacer par le constat brut.

### HD-14 — D-18 : « cinq enquêtes annuelles (2020-2024) » — l'EAR 2021 a été annulée

**Cible** : D-18 (caveat 1), et par ricochet S-27/S-29. — **Gravité : mineure** (à vérifier sur la doc INSEE avant correction).

L'enquête annuelle de recensement 2021 a été reportée/annulée (COVID) : le millésime 2022 repose sur quatre EAR (2020, 2022, 2023, 2024), pas cinq. Fait notoire mais à re-sourcer proprement (page « information/2383290 » ou doc du millésime) avant de corriger le registre. Ce point **renforce HD-1** (le chevauchement S-27/S-29 passe à 3 enquêtes communes sur 4).

---

## Verdict

**Survit tel quel.**
- **R-11** intégralement (niveaux, deltas, gradients opposés niveau/chute) — L-22 couvre honnêtement composition et fenêtre COVID ; l'arithmétique du « ~364 000 » est un ordre descriptif correctement étiqueté.
- **R-12** : la chute nationale, l'uniformité de la chute et le miroir de niveau (−0,80) sont **robustes à la composition** (vérifié en panel équilibré : médianes −2,41 vs −2,44) ; C-09 sort **renforcée** de la vérification du secret (données complètes, contrôle national à 0,014 pt) ; seuls les deltas de ZE individuels (Issoire) demandent un caveat (HD-8).
- **R-13** : le taux national, la hiérarchie des statuts (en « entrées »), les soldes internes ; la corrélation +0,80 comme fait numérique.
- **R-14** : la direction (péage quasi uniforme en taux, très inégal en mois), la géographie (rho +0,81), la part fiscale ~83 %, les extrêmes réunionnais (assiette robuste, vérifiée) ; l'assiette C-10 est le bon concept pour la question posée ; la cohérence H-13 « ancien » × assiette « Vente » (le neuf/VEFA, à droits réduits, est hors champ des deux côtés) est bonne.

**Ne survit pas tel quel.**
- **I-13(1) et la formule « validation croisée +0,80 entre deux sources indépendantes »** (R-13, qmd, EVIDENCE.md, PREV/NEXT-STEPS) : deux produits du même recensement, enquêtes largement communes — à requalifier en cohérence interne ; la validation inter-appareils de la session est MIGCOM×RPLS (HD-1).
- **« Chaque achat paie […] 6,32 % »** et la tenaille d'I-14 énoncée au taux hors primo-accédants, uniformisé sur des départements à 5,81 (HD-4/HD-5).
- **L'artefact R-14 sans aucune sensibilité H-13** alors que T-15 annonce trois scénarios — promesse du graphe non tenue (HD-3).
- **La liste « plus fortes baisses » de R-12** sans caveat de composition (HD-8), et **les classements R-14 sans seuil de ventes** alors que R-12 en impose un (HD-7).

Aucune objection ne renverse la direction de l'instruction de H-04 : le gel est réel, il se concentre là où le marché est verrouillé, et le péage de transaction est bien un paramètre institutionnel dominant. Les corrections demandées portent sur la **qualification de l'indépendance des preuves**, la **publication des fourchettes et des données écartées**, et trois conventions (territorialisation H-13, scénario primo 5,81, seuils de robustesse) — toutes réalisables en code sur les sources déjà figées, sans nouvelle acquisition.
