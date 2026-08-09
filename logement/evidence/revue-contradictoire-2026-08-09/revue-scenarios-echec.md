# Revue contradictoire — angle « SCÉNARIOS D'ÉCHEC » — R-11..R-14

- **Angle** : relecteur n°3 — scénarios d'échec (conditions d'inversion des conclusions, incohérences inter-résultats) — méthode INTRO étape 12.
- **Date** : 2026-08-09.
- **Périmètre** : les seuls ajouts de la session 4 (R-11/I-11, R-12/I-12, R-13/I-13, R-14/I-14, O-25..O-35, T-12..T-15, L-22..L-25, C-09/C-10, H-13, D-16..D-18, S-27..S-32) et leur cohérence avec l'arc revu R-01..R-10. Les objections déjà intégrées par la revue du 2026-08-07 ne sont pas re-soulevées.
- **État examiné** : commit `d563df4` (HEAD, vérifié), tag `efficacite-parc-v0.4` (`4933719`, ancêtre direct). Fichiers lus : `evidence/claims.yaml`, `evidence/efficacite-parc-immobilier.qmd` (sections R-11..R-14, §7-§11), `evidence/revue-contradictoire-2026-08-07.md`, `sources/{sources,definitions,hypotheses}.yaml`, `PREV-STEPS.md`, `NEXT-STEPS.md`, `src/logement/core/{mobilite,social,migrations,transaction,stats}.py`, `src/logement/shell/build.py`, `data/processed/{mobilite-residentielle,mobilite-parc-social,migrations-residentielles,cout-transaction}-ze.json`.
- **Méthode** : lecture seule sur le dépôt ; recomputations adverses exécutées depuis les données figées via le code du projet (scripts dans le scratchpad de session : `adverse_r11_r12_r14.py`, `adverse_d_e.py`, `adverse_b2.py` — mêmes fonctions `core/`, mêmes périmètres, mêmes conventions `stats.spearman_by_perimeter`). Tous les chiffres publiés recalculés à l'identique avant tout test adverse (arithmétique exacte partout).

---

## Objections

### SE-1 — R-11 : le « gel concentré dans les marchés verrouillés » est indiscernable d'une chute proportionnelle uniforme (artefact du niveau initial)

**Cible** : R-11 (chiffre-titre « la CHUTE suit le gradient inverse : −0,29 avec le coût ; tendues −1,54 pt vs −1,27 »), I-11, L-22, qmd §R-11. — **Gravité : MAJEURE.**

**Énoncé du scénario adverse.** Si toutes les ZE perdaient la même *fraction* de leur rotation (chute proportionnelle, sans aucun mécanisme territorial), la chute en points serait mécaniquement la plus forte là où le niveau est le plus haut — c'est-à-dire là où le coût est le plus haut (niveau × coût = +0,40). Le « sens opposé niveau/chute sur le même gradient de coût », présenté par I-11 comme ce qui *écarte* l'explication structurelle, est en réalité la signature *attendue* d'une chute uniforme proportionnelle : l'argument central d'I-11 est logiquement inversé.

**Preuve/chiffrage** (recalculé depuis S-27 + T-04/T-05/T-08, périmètre métropole, mêmes conventions que la chaîne) :

| Test | Résultat |
|---|---|
| rho(chute en pts, **niveau 2012**) | **−0,52** [−0,60 ; −0,42], n = 287 — plus fort que le rho publié chute × coût (−0,29) |
| Niveau 2012 médian : tendues 12,59 % vs autres 11,78 % | les tendues partent de plus haut |
| Chute **relative** médiane : tendues **−12,2 %** vs autres **−10,7 %** | le contraste-titre (−1,54/−1,27 pt) se réduit à 1,5 pt de % relatif |
| rho(chute relative, coût) | −0,20 [−0,30 ; −0,08] — subsiste, faible |
| **rho partiel(chute, coût \| niveau 2012)** | **−0,07** (abs) / **−0,09** (rel) ≈ **zéro** |

À niveau 2012 contrôlé, le coût n'apporte *rien* au gradient de la chute. Ce qui reste comme fait : « les ZE à forte rotation 2012 ont perdu le plus, en points et même en proportion ». Trois explications concurrentes non séparables : (i) convergence/régression vers la moyenne ; (ii) composition — la contraction nationale de la population jeune mobile (cf. SE-2) frappe mécaniquement le plus les ZE étudiantes à forte rotation ; (iii) verrouillage des marchés chers. Le texte publie (iii) en titre.

**Effet si retenu.** Le chiffre-titre « le gel se concentre dans les marchés verrouillés — signature attendue d'une mobilité EMPÊCHÉE » ne survit pas tel quel ; R-11 redevient : « la rotation baisse partout, ~11 % en proportion, un peu plus là où elle était haute ». La première instruction de H-04 passe de « signature positive » à « compatible avec H-04 mais non discriminante ».

**Disposition proposée.** (a) Publier dans T-12/R-11 la variante en chute relative et le rho partiel à niveau contrôlé (calculables immédiatement, code trivial) ; (b) reformuler I-11 : retirer « la signature attendue d'une mobilité empêchée » et l'argument « le sens opposé niveau/chute écarte… », qui est réfuté par le test ci-dessus ; (c) l'observation qui trancherait : rotation par âge de la personne de référence (le fichier détail Logement du RP croise ANEM × AGEMEN8 par territoire) — si la chute à âge donné suit encore le gradient de coût, I-11 renaît, réfutable proprement.

---

### SE-2 — R-11 : la part démographique de la chute nationale est chiffrable et n'est pas chiffrée (~1/3, plausiblement jusqu'à ~1/2)

**Cible** : R-11 (−1,17 pt ; « ~364 000 emménagements récents manquants »), O-26, L-22(1), I-11. — **Gravité : SÉRIEUSE.**

**Énoncé.** L-22 concède « une partie de la chute nationale est démographique » sans ordre de grandeur ; le chiffre-titre circule donc entier. Or la chaîne possède déjà de quoi le borner : S-29 (MIGCOM) donne les taux de mobilité par âge.

**Preuve/chiffrage.** Taux de mobilité annuelle par âge recalculés depuis S-29 (pondération IPONDI, taux national recalculé 9,87 % = contrôle exact) : 20-24 ans 24,2 %, 25-29 ans 24,2 %, 30-39 ans 14,8 %, 50-59 ans 5,4 %, 65-74 ans 3,4 %. Structure par âges INSEE (bilan démographique) : 2012 → 2023, part des 20-59 ans 52,0 → 49,1 %, part des 65 ans et plus 17,1 → 21,2 % ([INSEE, Évolution de la population — Bilan démographique 2023](https://www.insee.fr/fr/statistiques/7746154?sommaire=7746197)). Shift-share (taux par âge constants, structure 2012 → 2023, classes grossières) : **−0,35 pt** sur une mobilité de ~10,2 %, soit **−3,4 % relatif**, contre −8,9 % relatif observé sur la rotation (13,14 → 11,97) — **≈ 35-40 % de la chute nationale**, borne *basse* (classes grossières ; le vieillissement interne des 20-59 et l'application aux taux plus hauts de 2012 poussent vers la moitié). En revanche l'**accélération** (−0,25 pt sur 2012-2017 vs −0,92 sur 2017-2023) ne peut pas être démographique (le vieillissement est lisse) — c'est le morceau qui résiste.

**Effet si retenu.** Le « −1,17 pt » et les « ~364 000 manquants » doivent porter une décote démographique de l'ordre d'un tiers à une moitié ; la partie robuste du fait national est l'accélération récente, pas le total.

**Disposition.** Publier ce shift-share comme variante chiffrée (S-29 est figée ; il manque seulement une source S-xx de structure par âges à figer — un fichier INSEE de pyramide, trivial), et réécrire L-22(1) avec l'ordre de grandeur au lieu du qualitatif.

---

### SE-3 — R-11/R-12 : le choc de taux d'intérêt 2022-2025 est absent de toute la chaîne — le « gel » peut être cyclique, pas structurel

**Cible** : I-11, I-12, O-29, L-22, L-23 ; par ricochet le « Bilan H-04 » de PREV-STEPS (« le gel est réel, s'accélère »). — **Gravité : SÉRIEUSE (majeure pour la formulation « s'accélère » lue comme structurelle).**

**Énoncé.** Les deux fenêtres où le signal s'intensifie coïncident exactement avec le choc de taux : la classe « moins de 2 ans » du millésime 2023 recouvre ~2021-2023 (L-22(3) ne nomme que le COVID) ; la chute RPLS « la plus raide de la série » est 2022-2025 (O-29). Or le taux moyen des crédits immobiliers est passé d'environ 1,1 % (2021) à plus de 4 % (fin 2023) avant de refluer vers ~3 %, et les transactions dans l'ancien ont chuté d'environ 20 % dès 2023 ([historique des taux, toutsurmesfinances.com](https://www.toutsurmesfinances.com/argent/a/taux-de-credit-immobilier-taux-immobilier-et-historique) ; [Pretto, historique](https://www.pretto.fr/taux-immobilier/historique-taux-immobilier/)). Mécanisme adverse complet : les sorties du parc social vers l'achat gèlent (chute RPLS uniforme, nationale — exactement le profil observé), les emménagements récents chutent — sans qu'aucun « verrouillage » territorial nouveau ne soit nécessaire. Le mot « taux d'intérêt » n'apparaît nulle part dans `claims.yaml` (vérifié par grep).

**Preuve/chiffrage du reste structurel.** L'érosion pré-choc existe mais est 3 à 4 fois plus lente : R-11 −0,25 pt sur 2012-2017 ; R-12 −0,58 pt sur 2013-2019. Si le cyclique explique l'accélération, H-04 reste instruite par une érosion lente + des niveaux structurellement bas en zone chère (SE-5), pas par un « gel qui s'accélère ».

**Effet si retenu.** « Le gel s'accélère » (PREV-STEPS, O-26/O-29) devient « le gel s'est accéléré pendant un choc de financement dont l'effet propre n'est pas séparé ». I-11/I-12 doivent porter la branche cyclique comme alternative vivante.

**Disposition.** (a) Ajouter le choc de taux à L-22 et L-23 (au même titre que le COVID) ; (b) l'observation qui tranche, à inscrire dans NEXT-STEPS : les millésimes suivants après normalisation des taux — RPLS 2026/2027 (mobilité qui rebondit → cyclique ; qui reste ≤ 7 % → structurel) et le prochain millésime L_STAY ; (c) en attendant, aucune formulation qui attribue l'accélération au verrouillage territorial.

---

### SE-4 — R-12 : la « chute UNIFORME » ne survit pas mieux que la « chute concentrée » de R-11 — l'asymétrie de cadrage entre les deux résultats n'est pas argumentée

**Cible** : R-12 (« d'ampleur UNIFORME », « médianes −2,40/−2,44 »), I-12(2) (« la file d'attente s'allonge partout, pas seulement en zone tendue »), cohérence R-11 ↔ R-12 (mandat n°6). — **Gravité : SÉRIEUSE.**

**Énoncé.** R-11 et R-12 utilisent le même cadrage (chute en points absolus, sans contrôle du niveau initial) et en tirent deux récits opposés — « concentrée » pour R-11, « uniforme » pour R-12. Les deux récits sont des artefacts du cadrage, dans des directions opposées.

**Preuve/chiffrage** (recalculé depuis S-28, seuil parc ≥ 500, C-09, métropole) :

| Test | Résultat |
|---|---|
| Chute **relative** 2019-2025 médiane | tendues **−26,0 %** vs autres **−22,4 %** ; rho(chute rel., coût) = −0,24 [−0,35 ; −0,13] |
| rho(chute en pts, niveau 2019) | −0,51 — même mécanique de niveau que R-11 |
| **rho partiel(chute, coût \| niveau 2019)** | **−0,50** (pts) / **−0,51** (rel) |

Autrement dit : l'« uniformité » en points est la compensation de deux effets — la composante proportionnelle (le rural à forte mobilité perd plus de points) masque une chute *excédentaire* dans les marchés chers, qui partent de niveaux déjà bas et tombent quand même autant. À cadrage contrôlé, la chute sociale est *concentrée* là où le marché est cher — un résultat en fait PLUS favorable à H-04 que ce que le texte publie, pendant que le même contrôle *déconstruit* le titre de R-11 (SE-1). [Réserve honnête : le contrôle du niveau initial est lui-même attaquable — régression vers la moyenne, bruit de la base 2019 dans les petits parcs — c'est pourquoi la disposition est de publier les deux cadrages, pas d'inverser le titre.]

**Effet si retenu.** I-12(2) (« pas seulement en zone tendue ») et le contraste rhétorique « R-11 concentrée / R-12 uniforme » ne survivent pas tels quels ; le couple de résultats a besoin d'un cadrage unique (relatif + contrôle de niveau publiés pour les deux) et d'une lecture commune.

**Disposition.** Publier pour R-11 ET R-12 les trois vues (pts, relatif, partiel à niveau contrôlé) et faire porter les interprétations sur ce qui est invariant aux trois. Ce qui est invariant : la baisse est générale ; pour R-12, les marchés chers tombent au moins autant que les autres depuis des niveaux déjà minimaux.

---

### SE-5 — R-12 : le rho −0,80 est un gradient ANCIEN (−0,70 dès 2013) — il n'instruit pas la dynamique de H-04, et sa lecture mécanique n'est pas écartée

**Cible** : R-12 (« la corrélation la plus forte de la chaîne »), I-12(1) (« ajoute un gel de NIVEAU »), L-23. — **Gravité : SÉRIEUSE.**

**Énoncé.** (1) Recalculé sur les séries S-28 : mobilité sociale × coût = **−0,70 en 2013**, −0,68 en 2019, −0,80 en 2025 (métropole). Le « miroir du marché » préexiste à toute la période étudiée : c'est un trait d'équilibre structurel du système HLM français, pas un fait nouveau du « gel ». Ce qui est nouveau se réduit au creusement −0,68 → −0,80 — réel, mais d'une autre ampleur que le chiffre-titre. (2) La lecture mécanique du niveau — là où le marché est détendu, un sortant trouve à se loger *et* le bailleur reloge (l'offre de logements libérables est haute), là où il est tendu l'inverse — produit le même rho sans « blocage » ; I-12 l'assume à moitié (« la sortie vers le privé est le déterminant dominant ») mais le mot « gel de NIVEAU » et le statut de « corrélation la plus forte de la chaîne » donnent au gradient statique une valeur probante pour H-04 qu'il n'a pas. (3) Angle mort de composition : le vieillissement des locataires HLM (mécanisme identique à L-22(1)) est absent de L-23 — une partie de la chute nationale RPLS est démographique aussi.

**Effet si retenu.** I-12 se reformule : « le niveau de mobilité sociale reflète depuis au moins 2013 l'accessibilité du marché local (−0,70 → −0,80) ; la période ajoute une chute générale dont la part conjoncturelle (SE-3) et démographique n'est pas séparée ».

**Disposition.** Publier les rho 2013/2019/2025 dans R-12 (une ligne de code, données déjà dans la frame) ; ajouter le vieillissement des locataires à L-23 ; l'observation qui trancherait la lecture « blocage des sorties » : les motifs/destinations de sortie du parc social (EnL 2020 sous habilitation, ou SNE) — déjà en frontière NEXT-STEPS.

---

### SE-6 — R-12 : le croisement −0,20 est une construction de l'axe coût (le partiel change de signe)

**Cible** : R-12 (« croisement des segments NÉGATIF −0,20 »), I-12 (« le signe NÉGATIF … montre que la rotation d'ensemble MASQUE le gel social »). — **Gravité : MINEURE à SÉRIEUSE.**

**Preuve.** rho partiel(mobilité sociale, rotation RP | coût) = **+0,21** (métropole, n = 285) : à coût donné, les deux segments co-varient *positivement* (facteurs locaux communs de rotation). Le −0,20 brut est entièrement fabriqué par les deux corrélations opposées avec le coût (+0,40 et −0,80) — il n'existe aucune association négative résiduelle entre segments. L'énoncé qualitatif « la rotation étudiante/privée masque le gel social » reste vrai (c'est une conséquence des deux gradients de coût), mais le −0,20 présenté comme un troisième fait indépendant (« croisement des segments ») est une double lecture du même axe.

**Disposition.** Reformuler : présenter le masquage comme corollaire des deux gradients, publier le partiel, ou retirer le −0,20 des chiffres mis en avant.

---

### SE-7 — R-13 : « validation croisée entre sources indépendantes » — S-27 et S-29 sont le même appareil de mesure

**Cible** : R-13 (« rho +0,80 … entre deux sources indépendantes »), I-13(1) (« pas un artefact de source »), qmd §R-13 (« source indépendante »). — **Gravité : SÉRIEUSE (sur la formulation, pas sur le fait).**

**Énoncé.** S-27 (L_STAY, RP 2023) et S-29 (MIGCOM, RP 2022) sont deux produits du même recensement — mêmes enquêtes annuelles de recensement, millésimes chevauchants (2021-2025 vs 2020-2024), mêmes répondants pour une large part, et deux variables quasi liées par définition (un logement occupé depuis < 2 ans contient des personnes qui ont changé de logement dans l'année). Le +0,80 est un excellent contrôle de cohérence *interne* du recensement ; il ne protège pas contre un artefact commun de collecte ou de pondération EAR. La *vraie* validation externe de la session est ailleurs et devrait porter le titre : MIGCOM-HLM 8,34 % ≈ RPLS 8,0-8,5 % (deux appareils réellement disjoints, recensement vs répertoire administratif SDES).

**Effet si retenu.** I-13(1) se reformule (« cohérence interne du recensement entre l'unité logement et l'unité personne ; validation externe par le recoupement RPLS ») ; rien d'autre ne bouge.

**Disposition.** Correction de formulation dans R-13/I-13 et L-24.

---

### SE-8 — R-13 : les soldes négatifs des cœurs chers sont un trait métropolitain vieux de plusieurs décennies, et « CONTRE la géographie de l'emploi » n'est adossé à aucun croisement emploi

**Cible** : R-13 (« les flux internes vident les cœurs chers », Paris −1,40 %/an), I-13(3) (« des mobilités qui se font CONTRE la géographie de l'emploi — partir n'est pas toujours choisi »). — **Gravité : SÉRIEUSE.**

**Énoncé du scénario adverse.** Le déficit migratoire interne du cœur parisien précède de très loin la période et le niveau de tension actuels : dès 2012, la métropole du Grand Paris perdait ~46 100 personnes/an en migrations internes (151 300 entrants, 197 400 sortants, ≈ −0,7 %/an — [INSEE Analyses IdF n°59](https://www.insee.fr/fr/statistiques/2666500)) ; ~120 000 personnes/an quittaient Paris vers un autre département sur 2013-2017 ([INSEE Analyses IdF n°143](https://www.insee.fr/fr/statistiques/5871250)). Un solde durablement négatif est le cycle de vie normal d'une métropole (arrivées 15-29 ans, départs de familles et de retraités — choisis) ; il ne peut instruire « empêchées » que par sa *composition* ou son *aggravation*, ni l'une ni l'autre mesurées ici. Les destinations gagnantes de R-13 (Sables-d'Olonne, Brignoles, La Rochelle, Dinan) sont des littoraux d'aménité/retraite — le profil des départs choisis. Enfin, deux faiblesses internes : le rho solde × coût vaut −0,15 France entière mais **−0,11 [−0,22 ; +0,01] en métropole — compatible avec zéro** ; et T-14 ne croise *pas* l'emploi (l'emploi de la chaîne s'arrête à 2018, L-07/NEXT-STEPS) — « contre la géographie de l'emploi » est une inférence via le coût, pas une mesure.

**Effet si retenu.** I-13(3) ne survit pas tel quel ; le retournement rhétorique de R-13 (« pas de gel de niveau → le blocage se lit dans QUI bouge et dans les SOLDES ») reste défendable pour le QUI (les statuts : fait solide) mais pas pour les SOLDES, qui sont sous-déterminés entre cycle de vie et éviction. Condition de réfutabilité du retournement : il est réfutable si la composition par âge des soldes est celle du cycle de vie (départs concentrés aux âges famille/retraite) — et **cette décomposition est calculable immédiatement** : S-29 contient AGEREVQ.

**Disposition.** (a) Calculer les soldes parisiens (et des cœurs chers) par âge depuis S-29 — si les 25-39 ans avec enfants dominent les sorties vers la grande couronne, publier le solde comme fait de cycle de vie avec la question de l'éviction en limite ; si les sorties sont anormalement étalées en âge ou croissantes, I-13(3) se renforce ; (b) retirer « contre la géographie de l'emploi » tant que l'emploi récent n'est pas figé (reste ouvert n°2 de la revue précédente) ; (c) affaiblir « partir n'est pas toujours choisi » en question ouverte.

---

### SE-9 — R-14 : l'écart en mois est ~intégralement le prix ; le rho +0,81 est quasi tautologique ; l'annualisation manquante change la lecture « barrière »

**Cible** : R-14 (« 7,8 mois vs 5,5 », rho +0,81), I-14 (« tenaille », « superpose la barrière … au verrouillage locatif »), L-25. — **Gravité : SÉRIEUSE.**

**Preuve/chiffrage** (recalculé depuis S-30/S-31/S-32 + Filosofi) :

| Test | Résultat |
|---|---|
| Écart tendues/autres à **niveau de vie national constant** (prix seul) | 8,15 vs 5,56 mois — écart **2,59** contre 2,23 observé : le dénominateur revenu *réduit* l'écart ; 100 % du signal territorial est le prix |
| Dispersion inter-ZE (IQR/médiane) | prix 0,47 ; niveau de vie **0,08** |
| rho(mois, prix médian) | **+0,98** — la métrique « mois » est un re-classement du prix |
| rho(prix, indice de coût locatif T-05) | +0,79 → le +0,81 « mois × coût locatif » est la corrélation loyers-prix, connue, pas une découverte de superposition |
| Péage médian annualisé (6,14 mois amortis) | détention 20 ans : **2,6 %** du niveau de vie annuel ; 12 ans : 4,3 % ; 9 ans : 5,7 % ; mobile tous les 5 ans : ~10 % |
| Part fiscale médiane | 83,1 % (confirmée) |

**Énoncé.** (1) Le taux étant appliqué uniforme (H-13 central partout), la géographie du péage est *par construction* celle du prix : « le péage est le plus lourd exactement là où R-11/R-12 localisent le gel » est une reformulation de « les prix sont hauts là où les loyers sont hauts » — déjà le contenu de R-04. L'apport propre de R-14 se réduit à deux choses (qui suffisent à le justifier) : le *niveau absolu* en mois et la décomposition fiscale ~83 %. (2) Le scénario « péage trop petit pour geler » : amorti sur une détention longue, 2,6-4 %/an de niveau de vie — un second ordre face aux écarts de prix eux-mêmes (R-04/R-06) ; le péage ne mord que sur la mobilité *répétée* (~10 %/an pour un ménage mobile tous les 5 ans). Ce n'est pas fatal à I-14 — une taxe sur la transaction pénalise précisément le comportement dont H-04 déplore la rareté, et la littérature sur les droits de mutation documente un effet négatif réel sur la mobilité — mais le texte ne donne au lecteur aucun des deux termes (annualisation, fréquence) qui permettent de juger si « barrière » est le bon mot.

**Effet si retenu.** Les chiffres de R-14 survivent tous ; la mise en récit d'I-14 (« superpose », « écrasant là où tout se cumule ») doit être requalifiée : un fait de *prix* re-exprimé en mois + un paramètre institutionnel, pas une quatrième confirmation indépendante de la géographie du gel.

**Disposition.** (a) Publier l'annualisation paramétrée par la durée de détention (arithmétique pure, aucune source nouvelle nécessaire si la durée est une H-xx à plage) ; (b) noter dans R-14/L-25 que le rho +0,81 est quasi mécanique (taux uniforme × corrélation loyers-prix) ; (c) l'observation qui trancherait la causalité : les discontinuités de taux DMTO existantes (départements à 5,81/5,09 vs 6,32, S-31 — territorialisable, déjà prévu en piste NEXT-STEPS n°2) croisées avec les volumes DVF.

---

### SE-10 — Transverse : la « cohérence d'ensemble de H-04 » est en partie une auto-corrélation de construction (un seul axe lu quatre fois)

**Cible** : I-14 (« Cohérence d'ensemble de H-04 : la mobilité repose sur le segment le plus cher, le parc social est gelé, la rotation chute là où tout cela se cumule »), Bilan H-04 de PREV-STEPS (« quatre mesures indépendantes qui se recoupent »). — **Gravité : SÉRIEUSE.**

**Énoncé.** Les quatre *mesures* (S-27/S-28/S-29/S-30) sont bien des fichiers distincts, mais les quatre *croisements* passent tous par les deux mêmes constructions : T-05 (indice de coût) et T-08 (statut de tension — lui-même dérivé de la vacance LOVAC via C-06, la même vacance T-04 qui sert aussi de deuxième axe à R-11 : « chute là où la vacance est rare » et « chute dans les tendues » sont largement le même énoncé). La convergence géographique revendiquée est donc en grande partie *une* variable latente (cherté/tension du marché) projetée quatre fois — les tests SE-1, SE-6 et SE-9 montrent chacun un croisement qui se vide (partiel ≈ 0, signe inversé, ou tautologie) une fois l'axe commun contrôlé. Ce qui se recoupe réellement entre chaînes indépendantes : MIGCOM-HLM ≈ RPLS, et la cohérence personnes/logements du recensement (avec la réserve SE-7). C'est moins que « quatre mesures indépendantes qui se recoupent ».

**Disposition.** Reformuler la phrase de cohérence d'I-14 (et le Bilan H-04 de PREV-STEPS s'il est repris dans un article) : distinguer « quatre mesures indépendantes » (vrai) de « quatre confirmations indépendantes de la même géographie » (non démontré) ; créer une limite transverse (L-xx) « axes de croisement partagés T-05/T-08 » portée par R-11..R-14.

---

### SE-11 — Cohérence avec l'arc v0.3 : deux inférences que l'état v0.3 interdit restent disponibles au lecteur

**Cible** : articulation R-11..R-14 ↔ I-07/I-10 revus ; qmd §6 vs §8. — **Gravité : MINEURE.**

**Énoncé.** Les chiffres v0.3 sont inchangés (vérifié) et le qmd marque bien R-11..R-14 comme postérieurs à la revue. Mais : (1) R-11 établit « la chute est plus forte là où la vacance disponible est rare » à côté d'un arc qui propose de remobiliser la vacance — un lecteur peut composer les deux en « remobiliser restaurerait la rotation », causalité que rien dans la chaîne n'établit (et que SE-1 fragilise) ; (2) I-14 (« ~83 % fiscal — paramètre institutionnel direct ») peut se lire « baisser les DMTO est la réponse », alors que la part causale du péage est explicitement non identifiée et que l'arc v0.3 conclut que la contrainte de la détente est la levée des verrous de propriété — deux diagnostics institutionnels différents dont l'articulation n'est écrite nulle part ; (3) le §8 « Interprétation » du qmd s'arrête à I-10 : le lecteur de la section conclusive ne voit ni I-11..I-14 ni leur statut provisoire.

**Disposition.** Une phrase de garde dans le qmd (fin de §6 ou §8) : les résultats H-04 sont descriptifs, n'établissent aucun lien causal vacance→rotation ni péage→gel, et ne modifient pas la conclusion conditionnelle de l'arc ; intégrer I-11..I-14 au §8 après la passe contradictoire.

---

### SE-12 — Test de réfutabilité systématique des quatre interprétations

**Cible** : I-11..I-14 (mandat n°8). — **Gravité : récapitulatif.**

| Interprétation | Se dit descriptive ? | L'observation manquante qui la réfuterait | Disponible ? |
|---|---|---|---|
| I-11 (mobilité empêchée par le marché) | Oui (« reste descriptive », L-22) — mais le titre affirme la « signature » que SE-1 dissout | Rotation par âge × ZE (fichier détail Logement RP) : chute à âge contrôlé sans gradient de coût → réfutée | Open data, à figer |
| I-12 (personne ne quitte le parc social) | Oui (« blocage et stabilité non séparables ») — mais « gel de NIVEAU » suggère un fait nouveau (SE-5) | Rebond RPLS 2026-2027 post-taux (→ cyclique) ; destinations de sortie (EnL/SNE) montrant des sorties élevées là où le privé est cher → réfutée | Millésimes futurs ; habilitation |
| I-13 (canal privé + soldes = blocage) | Partiellement — « partir n'est pas toujours choisi » et « contre la géographie de l'emploi » dépassent le démontré (SE-8) | Décomposition par âge des soldes (S-29, AGEREVQ) : profil pur cycle de vie → I-13(3) réfutée ; croisement emploi récent | **Calculable immédiatement** (S-29 figée) |
| I-14 (péage = barrière, tenaille) | Oui (« la part de causalité … n'est PAS identifiée ») — le plus honnête des quatre | Élasticité mobilité/DMTO sur les discontinuités départementales S-31 × DVF ≈ 0 → « barrière » réfutée ; annualisation rendant le péage < 3 %/an pour la détention observée | Territorialisation prévue (NEXT-STEPS n°2) |

---

## Verdict

**Survit tel quel.**
- Toute l'arithmétique publiée (recalculée à l'identique avant chaque test adverse) ; l'intégrité des conventions C-09 (contrôle ≤ 0,014 pt confirmé par relecture du code) et C-10 ; la part fiscale 83,1 % ; les niveaux absolus de R-14 en mois ; les distributions et classements de O-27/O-30/O-33/O-34.
- Les *faits* nationaux de baisse (13,14 → 11,97 % ; 9,87 → 7,11 % ; les 293/305 et 286/303) — comme faits, pas comme « gel structurel ».
- La structure par statut de R-13 (19,51 / 8,34 / 5,73 %) et son recoupement RPLS — la seule validation réellement externe de la session, qui mérite le premier rôle.
- Le gradient de niveau de R-12 comme fait structurel — renforcé même (il tient depuis 2013) — et, résultat inattendu de cette revue, une version *contrôlée* de la chute sociale (partiel −0,50 à niveau 2019 contrôlé) qui est PLUS favorable à H-04 que le texte publié.

**Ne survit pas tel quel.**
- **I-11 en l'état** : « la chute se concentre dans les marchés verrouillés — signature d'une mobilité empêchée » et l'argument « le sens opposé niveau/chute écarte l'explication structurelle » (SE-1 : partiel −0,07 ; l'argument est logiquement inversé).
- **« Chute UNIFORME » de R-12 et I-12(2)** en tant que contraste avec R-11 (SE-4 : le même contrôle qui dissout R-11 inverse R-12).
- **« Sources indépendantes »** de R-13/I-13(1) (SE-7) et **« contre la géographie de l'emploi »** d'I-13(3) (SE-8 : aucun croisement emploi dans T-14).
- **Le rho +0,81 de R-14 comme « superposition » découverte** (SE-9 : quasi-construction, rho(mois, prix) = 0,98).
- **« Quatre mesures indépendantes qui se recoupent »** du Bilan H-04 (SE-10) et **« le gel s'accélère »** lu comme structurel sans mention du choc de taux (SE-3).
- Les chiffres-titres −1,17 pt / « ~364 000 manquants » publiés sans leur décote démographique chiffrable (SE-2).

**Indécidable en l'état** (et c'est la vraie frontière de H-04) :
- La part respective **démographie / cycle de taux / verrouillage territorial** dans les chutes — les trois scénarios adverses reproduisent chacun une partie du signal ; trancher demande : rotation par âge × ZE (SE-1), millésimes post-normalisation des taux (SE-3), shift-share figé (SE-2).
- **Choisi vs empêché** dans les soldes des cœurs chers — décidable en partie *dès maintenant* par la décomposition AGEREVQ de S-29 (SE-8), la seule des observations manquantes qui ne demande ni nouvelle source ni attente.
- La **causalité du péage** (SE-9) — décidable partiellement par les discontinuités S-31.

Bilan d'ensemble : les quatre *mesures* de la session 4 sont solides et le travail de limites (L-22..L-25) est réel ; ce qui ne tient pas, c'est l'étage interprétatif qui convertit des gradients statiques anciens et des chutes nationales non décomposées en « signature d'une mobilité empêchée par le marché ». La version défendable de H-04 après cette passe : *la mobilité résidentielle baisse partout (part démographique chiffrable, part conjoncturelle non séparée) ; elle repose structurellement sur le segment le plus cher ; le parc social des zones chères est à rotation minimale depuis au moins 2013 et sa chute récente y est au moins aussi forte qu'ailleurs ; la sortie par l'achat y paie un péage majoritairement fiscal* — c'est encore une instruction substantielle de H-04, mais aucune de ses quatre phrases n'est celle des titres actuels.

Sources externes citées (ordres de grandeur des scénarios adverses uniquement) : [INSEE, Bilan démographique 2023 — évolution de la population](https://www.insee.fr/fr/statistiques/7746154?sommaire=7746197) · [INSEE Analyses IdF n°59 (MGP, migrations 2012)](https://www.insee.fr/fr/statistiques/2666500) · [INSEE Analyses IdF n°143 (sorties de Paris 2013-2017)](https://www.insee.fr/fr/statistiques/5871250) · [historique des taux de crédit immobilier](https://www.toutsurmesfinances.com/argent/a/taux-de-credit-immobilier-taux-immobilier-et-historique) · [Pretto, historique des taux](https://www.pretto.fr/taux-immobilier/historique-taux-immobilier/). Scripts de recomputation : `adverse_r11_r12_r14.py`, `adverse_d_e.py`, `adverse_b2.py` (scratchpad de session — à recopier en annexe de revue si le compte rendu d'intégration veut les tracer).
