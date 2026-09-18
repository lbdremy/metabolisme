# Revue contradictoire — session 7 (proposition institutionnelle) — angle « SOURCES ALTERNATIVES »

Relecteur : agent « sources alternatives » (méthode INTRO §13.4 / étape 12), travaillant seul, sans accès aux autres relecteurs. Date : 2026-09-18. Aucun fichier du dépôt n'a été modifié en dehors de ce rapport.

## Méthode

1. Lecture dans l'ordre demandé : `INTRO.md` (§4, §7, §13, §21), `logement/CLAUDE.md`, `logement/EVIDENCE.md`, `logement/evidence/decisions-2026-09-18.md`, bloc « Session 7 » de `logement/evidence/claims.yaml` (V-02..V-04, C-11..C-14, O-37..O-40, T-17, R-15..R-17, I-15..I-17, L-27..L-31, P-01), S-39..S-46 de `sources/sources.yaml`, D-19..D-22 de `sources/definitions.yaml`, H-14..H-18 de `sources/hypotheses.yaml`, `src/logement/core/institution.py`, `build_institution` dans `src/logement/shell/build.py`, `data/processed/scenarios-institutionnels-ze.json`, section « R-15 à R-17 » et « 9. Proposition » de `evidence/efficacite-parc-immobilier.qmd`.
2. Vérification des huit fichiers figés (`data/raw/`) : sha256 recalculé (8/8 conformes à `sources.yaml`), texte extrait par `pdftotext -layout` (pages = index PDF, contrôlé contre les folios imprimés) ou par dépouillement HTML ; chaque citation des notes de source, définitions et hypothèses a été cherchée mot à mot dans le fichier figé.
3. Recalcul des constantes du code (`institution.py`, `remob.py`) et de l'assiette M-D à partir de S-11 (`base-cc-logement-2022`), par `uv run python` dans `logement/`.
4. Recherche de sources plus récentes, plus officielles ou contradictoires (WebSearch/WebFetch, date du jour 2026-09-18). URL vérifiées ce jour :
   - https://www.collectivites-locales.gouv.fr/files/files/Etudes-et-statistiques/OFGL/rapport%202026/Pr%C3%A9-Rapport%20OFGL%202026%20def.pdf (pré-rapport OFGL 2026, PDF du 11/06/2026, 176 p., sha256 `e351ef25…f264`) — texte extrait, p. 47-48 et annexe p. 110.
   - https://www.collectivites-locales.gouv.fr/files/files/Etudes-et-statistiques/OFGL/rapport%202026/4-%20Fiche%20sur%20les%20d%C3%A9partements.pdf (fiche départements du rapport final, PDF du 03/07/2026, 15 p., **image seule, texte non extractible**, sha256 `4c6b5381…456e`).
   - https://www.collectivites-locales.gouv.fr/etudes-et-statistiques/rapports-de-lobservatoire-des-finances-et-de-la-gestion-publique-locales-ofgl (page index : rapport 2026 « présenté au CFL le 8 juillet 2026 »).
   - https://www.collectivites-locales.gouv.fr/files/files/Etudes-et-statistiques/BIS/2024/BIS_190_DMTO.pdf (DGCL, BIS n° 190, « Les DMTO des départements en 2023 », sha256 `35088872…de16`).
   - https://www.ccomptes.fr/fr/publications/pour-une-fiscalite-du-logement-plus-coherente et https://www.ccomptes.fr/sites/default/files/2023-12/20231218-Fiscalite-du-logement.pdf (CPO, 18/12/2023, 115 p., sha256 `7589d3d7…ea43`).
   - https://presse.economie.gouv.fr/?p=181486 (communiqué Bercy du 15/07/2026, Livret A 1,7 % au 01/08/2026).
   - https://www.banquedesterritoires.fr/produits-services/prets-long-terme/pret-plai et https://www.banquedesterritoires.fr/produits-services/prets-long-terme/pret-locatif-social (conditions PLAI / PLS).
   - https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000029971412/ (art. R322-5 du code de l'expropriation, version 01/01/2015).
   - https://www.service-public.gouv.fr/particuliers/actualites/A18896 (TVLH, art. 108 de la loi n° 2026-103 du 19/02/2026 ; page du 21/05/2026 mise à jour le 02/09/2026).
   - https://www.anah.gouv.fr/actualites/la-maitrise-d-ouvrage-d-insertion-un-dispositif-vocation-sociale (Anah, 10/03/2023) ; https://www.fapil.fr/actualite-du-reseau/nouveau-panorama-de-la-maitrise-douvrage-dinsertion-decouvrez-les-enseignements-lors-de-notre-webinaire (Fapil, 06/07/2026).
   - https://soliha.fr/intermediation-locative-la-federation-soliha-et-koreis-publient-une-etude-qui-demontre-lefficacite-et-lefficience-du-dispositif/ (Soliha/Koreis, 02/12/2025).
   - https://www.ressources-consultants-finances.fr/augmentation-dmto-2025/ (16/01/2026 ; cabinet privé — non retenu comme source, utilisé pour orienter la recherche).

Les objections sont classées par gravité décroissante à l'intérieur de chaque thème ; chacune cite la page du fichier figé ou l'URL vérifiée.

---

## Objections

### SA-1 — Le produit DMTO 2025 est publié depuis juin 2026 : R-17 est calibré sur une donnée dépassée

**Gravité : majeure.**

**Énoncé.** M-D (R-17, C-14, O-37, L-28, P-01) rapporte « les 9,9 Md€ de DMTO départementaux 2024 » au parc. Or l'OFGL a publié, avant la session, le millésime 2025 sur le MÊME périmètre constant, avec la série 2022-2025 en annexe. La chaîne reconnaît que 2024 est « un point BAS du cycle » (S-39 note, L-28) mais calibre dessus alors que la donnée plus récente et la moyenne de cycle étaient disponibles.

**Preuve.** Pré-rapport OFGL 2026 (PDF « def » du 11/06/2026), fiche départements, p. 47 : « Au total, le produit des DMTO progresse de + 20,4 % en 2025 pour atteindre 11,9 Md€. À l'exception de Mayotte, l'ensemble des départements enregistre une hausse. […] sans pour autant retrouver les niveaux très élevés (plus de 14 Md€) de 2021 et 2022 ». Même page : « En 2025, deux départements ont de nouveau maintenu leur taux à 3,80 % (Indre et Mayotte) ; tous les autres ont adopté un taux correspondant au taux plafond, fixé à 5 % depuis avril 2025 (hors primo-accédants) » ; « Le nombre de transactions immobilières passe de 853 000 à 951 000 ventes entre décembre 2024 et décembre 2025 ». P. 48, champ du graphique 6a : « périmètre constant entre 2019 et 2025, donc hors Rhône, Martinique, Guyane, Corse et Paris » (même champ que S-39). Annexe p. 110, ligne « DMTO » : **14,60 (2022) · −21,8 % · 11,40 (2023) · −13,5 % · 9,86 (2024) · +20,4 % · 11,87 (2025)** Md€. Le rapport final a été présenté au CFL le 8 juillet 2026 (page index OFGL) ; sa fiche départements (PDF du 03/07/2026) est une image non extractible — le pré-rapport « def » porte le texte.

**Conséquence chiffrée** (recalcul sur l'artefact, parc 34 565 110) : charge de détention 343 €/logement/an au produit 2025 (vs 286), 345 € à la moyenne 2022-2025 ; années équivalentes médianes 27,4 (vs 33,0). Le chiffre « 33 ans (44 en zones tendues) » de R-17/I-17 et le « 9,9 Md€ » de P-01 et O-37 dépendent d'un choix de millésime qui n'est pas le plus récent.

**Disposition proposée.** Enregistrer S-47 = pré-rapport OFGL 2026 « def » (URL ci-dessus, sha256 `e351ef2581cc8937cbd5df48b3e32322d008e26a6e67478434f896d0ef65f264`, publication 2026-06-11, périmètre constant hors 75/69/2A/2B/972/973) ; remplacer la constante `DMTO_PRODUCT_2024_EUR` par une série (2022-2025) et publier R-17 au millésime 2025 avec la moyenne de cycle en sensibilité (ou l'inverse, mais dire lequel) ; corriger O-37, C-14, L-28 (1), P-01 et le §9 du .qmd ; garder S-39 pour 2024 et pour le contrôle de continuité de périmètre.

---

### SA-2 — H-14 : le « 3 % du stock ciblé en 4 ans » n'est pas ce que dit S-22

**Gravité : sérieuse.**

**Énoncé.** H-14 (0,75 %/an) est présenté comme « ~6 700 sorties de vacance attribuables au dispositif ZLV en 4 ans, soit ~3 % du stock ciblé en zone tendue (L-17), donc 0,75 %/an en linéaire ». La note de S-22 dit de même « ZLV 6 700 sorties de vacance en 4 ans (3 % de sorties en zone tendue) ». Les deux chiffres existent dans la source mais ne se rapportent ni au même dénominateur, ni à la même période, ni à un « stock ciblé ».

**Preuve.** S-22, p. 24 : « Entre 2020 et 2024, 6700 logements identifiés grâce à ZLV sont sortis de vacance, représentant **6,6 % des 102 000 logements dont les propriétaires ont été contactés** » ; puis : « 12 % des propriétaires en zone détendue ont accepté d'être accompagnés, pour 6 % de logements sortis de vacance in fine (contre respectivement 4,7 % et **3 % dans les zones tendues**) », avec la note 44 : « D'après une enquête menée par l'équipe ZLV sur **28 104 logements contactés** via l'outil à date d'**octobre 2022** ». Le 3 % est donc une part des logements CONTACTÉS en zone tendue, mesurée sur une enquête arrêtée en octobre 2022, pas une part du stock sur quatre ans. Le modèle applique 0,75 %/an au gisement effectif ENTIER (206 664 logements, `incentive_scenario`), c'est-à-dire à des logements dont la grande majorité n'a jamais été contactée.

**Sens.** Le taux par contact majore le taux par stock : R-15 surestime donc M-A, ce qui va dans le sens de I-15 (conservateur pour la conclusion) — mais l'hypothèse est documentée avec une citation inexacte, ce que §21 règle 2 et §13.5 interdisent. Aucune source figée ne donne la fraction du gisement contactée.

**Disposition proposée.** Réécrire la description de H-14 et la note de S-22 : « 6,6 % des logements contactés sortis en 2020-2024 (toutes zones) ; 3 % des logements contactés en zone tendue (enquête ZLV, oct. 2022, n = 28 104) » ; requalifier le central 0,75 %/an en MAJORANT explicite (taux par contact appliqué au stock), et le dire dans R-15/L-29. Ne pas changer la valeur sans nouvelle source ; la plage [0,25 ; 2,50] reste défendable comme grille.

---

### SA-3 — H-16 : les bornes PLAI (−0,20) et PLS (+1,11) ne sont dans aucune source enregistrée ; S-40 documente une marge plus basse

**Gravité : sérieuse.**

**Énoncé.** H-16 justifie sa plage [1,50 ; 2,81] par « PLAI, Livret A − 0,20 » et « PLS, Livret A + 1,11 » en citant S-41 et S-42. S-41 (page PLUS figée) ne contient ni l'un ni l'autre : la seule mention de « PLS » y est un lien « Prêt Locatif Social (PLS) : financer des logements sociaux — En savoir plus » ; le mot « PLAI » n'y figure pas. Les deux marges sont exactes mais viennent de la mémoire, pas d'un fichier figé (§21 règle 1).

**Preuve.** Dépouillement de `banque-territoires-pret-plus-2026.html` (texte : « Prêt PLUS : conditions financières — Durée du prêt Bâti : de 5 à 40 ans ; Partie foncière : de 5 à 50 ans, jusqu'à 80 ans maximum ; […] Taux Livret A + 60 pb ») ; aucune occurrence de « PLAI », « - 20 », « 111 ». Pages Banque des Territoires vérifiées le 2026-09-18 : PLAI « Livret A −0,20 % », « 5 à 40 ans pour la partie travaux », « 5 à 50 ans pour la partie foncière (jusqu'à 80 ans) », « exonération de taxe foncière sur les propriétés bâties » 25 ans ; PLS « Livret A + 111 pb », bâti « De 15 à 40 ans ». En outre, le fichier figé S-40 (p. 22 du PDF) documente des marges plus basses que la borne retenue : « une enveloppe pluriannuelle de 6 Md€ de prêts PLAI avec baisse de marge, soit **TLA − 40 bp** contre TLA − 20 bp précédemment » et « 2 Md€ de prêts PLUS à taux d'intérêt bonifié (soit un prêt à **TLA + 20 bp** au lieu de TLA + 60 bp) […] “PLUS Constructions Vertes” […] février 2024 ».

**Disposition proposée.** Enregistrer S-48 (page PLAI) et S-49 (page PLS) avec HTML figé et sha256 ; citer S-40 p. 22 pour la borne basse et, puisque la source figée l'établit, envisager 1,30 % (Livret A − 0,40) comme borne basse de la plage — la valeur centrale 2,30 n'est pas en cause.

---

### SA-4 — Les indemnités accessoires d'expropriation sont chiffrables : la pratique du remploi vaut ≈ +10 % du prix

**Gravité : sérieuse.**

**Énoncé.** L-27, D-22 et C-12 renvoient les indemnités accessoires à « non chiffrées ». Le remploi, la principale d'entre elles, a un ordre de grandeur standard et public.

**Preuve.** Art. R322-5 du code de l'expropriation (Légifrance, vérifié 2026-09-18) : « L'indemnité de remploi est calculée compte tenu des frais de tous ordres normalement exposés pour l'acquisition de biens de même nature moyennant un prix égal au montant de l'indemnité principale. […] il ne peut être prévu de remploi si les biens étaient notoirement destinés à la vente, ou mis en vente par le propriétaire exproprié au cours de la période de six mois ayant précédé la déclaration d'utilité publique. » Le barème usuel des juridictions de l'expropriation (20 % jusqu'à 5 000 €, 15 % de 5 001 à 15 000 €, 10 % au-delà) n'est pas dans l'article — il est de pratique jurisprudentielle, repris dans les dossiers publics de DUP (ex. dossier ZAC Enjalbert, préfecture de l'Hérault, pièce 8 « estimation des dépenses », https://www.herault.gouv.fr/contenu/telechargement/25559/182390/file/Dossier%20DUP%20ZAC%20Enjalbert%20-%20Piece%208%20estimation%20depenses.pdf). Recalcul sur l'artefact : prix d'acquisition moyen M-B 211 216 € (28,8 Md€ / 136 353) → remploi ≈ 22 100 € (10,5 %) → **+3,0 Md€** sur les 28,8 Md€ d'acquisition (+6,8 % de l'investissement M-B). La clause « biens mis en vente dans les six mois » est par ailleurs pertinente pour un vacant durable (il n'ouvre pas droit au remploi s'il était en vente).

**Disposition proposée.** Enregistrer S-50 = art. R322-5 (Légifrance) et un dossier public de DUP comme témoin du barème ; ajouter dans L-27 l'ordre de grandeur « ≈ +10 % du prix d'acquisition (remploi), hors déménagement/réinstallation » et, idéalement, une sensibilité H-15 × 1,10 dans R-16. Requalifier la phrase « ne sont pas chiffrées » en « chiffrées en ordre de grandeur, non modélisées ».

---

### SA-5 — H-18 applique la TFPB (11,6 points) au bail à réhabilitation, alors que S-46 dit que le preneur en est exonéré

**Gravité : sérieuse.**

**Énoncé.** `lease_scenario` (M-C) et `operator_frame` (M-B) utilisent le même central H-18 = 0,549, qui inclut « TFPB 11,6 » (S-40 p. 15). Le fichier figé S-46 contredit ce central pour M-C ; la page PLAI le contredit pour M-B.

**Preuve.** S-46 p. 1, rubrique « Avantages de l'outil » : « L'organisme porteur de la réhabilitation peut bénéficier d'une **exonération de la taxe foncière sur les propriétés bâties (TFPB) pendant toute la durée du bail** » (et « Article 1400 II du Code Général des impôts pour fiscalité foncière »). Page PLAI Banque des Territoires (2026-09-18) : « exonération de taxe foncière sur les propriétés bâties » 25 ans (30 ans pour certaines opérations). H-18 range la TFPB dans la borne basse (0,40) « opérateur exonéré » mais laisse le central à 0,549 pour les deux mécanismes.

**Disposition proposée.** Pour M-C, central source-fondé = 0,549 − 0,116 = 0,433 (S-46 p. 1), ce qui abaisse encore le loyer d'équilibre travaux (déjà sous le social) — sans effet sur la conclusion I-16, mais la chaîne doit être conforme à sa source ; pour M-B, dire dans L-30 que l'exonération 25 ans des opérations PLAI/PLUS (S-48) rapproche le cas réel de la borne basse. Compléter D-21 (exonération TFPB, art. 1400 II CGI) et la note de S-46.

---

### SA-6 — Une source française officielle recommande exactement M-D : le CPO (décembre 2023) n'est pas enregistré

**Gravité : sérieuse.**

**Énoncé.** O-39, I-17, C-14 et L-28 s'appuient sur la brochure OCDE (S-44) comme « littérature comparative » de la bascule. Le Conseil des prélèvements obligatoires a publié le 18/12/2023 « Pour une fiscalité du logement plus cohérente », qui formule la même orientation, pour la France, avec la condition de neutralité pour les collectivités et un chiffre national des DMTO.

**Preuve.** CPO, PDF (115 p.) : p. 17 « Il s'agit tout d'abord de chercher à taxer plus la détention que l'acquisition, au vu notamment des effets économiques peu efficients des droits de mutation à titre onéreux (DMTO) qui sont plus élevés en France que dans les autres pays européens. Cette orientation générale implique d'une part d'envisager une **bascule des DMTO vers la taxe foncière, sans perte pour les collectivités locales**, d'autre part d'engager une réflexion précise sur l'assiette foncière » ; p. 20, constat n° 16 : les droits « limitent le volume des transactions et ont un effet négatif sur la mobilité résidentielle et sur l'accession à la propriété » ; p. 21, **Recommandation n° 8** : « Une fois le lien rétabli entre l'assiette de la taxe foncière et la valeur économique des logements taxés, engager une réflexion sur le niveau et l'affectation des DMTO visant à moins taxer l'acquisition de logements et à compenser le manque à gagner pour les finances publiques par un relèvement des impôts portant sur leur détention » ; p. 32 : « droits de mutation à titre onéreux (DMTO, **16,8 Md€**) » (toutes collectivités, 2022) ; p. 39 : impôts sur les transactions « 0,9 % du PIB », « 2e rang, derrière la Belgique ».

**Disposition proposée.** Enregistrer S-51 (CPO 2023, sha256 `7589d3d7266b2342a45452302a084a90c3d5565780545ce8d8a742c6776eac43`, rapport public de la Cour des comptes) ; l'ajouter aux dépendances de O-39/I-17/C-14 ; noter dans L-28 que le CPO conditionne la bascule au préalable « assiette foncière rétablie » — la même condition que l'OCDE (valeurs cadastrales), mais formulée pour la France ; utiliser 16,8 Md€ comme total TOUTES collectivités (départements + communes) pour situer les 9,9/11,9 Md€ départementaux.

---

### SA-7 — Le « canal incitatif existant » (M-A) change de droit au 1er janvier 2027 : TLV et THLV sont remplacées par la TVLH

**Gravité : sérieuse.**

**Énoncé.** R-15/H-14/O-37 décrivent M-A comme « le canal incitatif existant (TLV/THLV/ZLV) » et P-01 compare la subvention d'équilibre aux « 271 M€/an de TLV ». La loi de finances pour 2026 a supprimé TLV et THLV au profit d'une taxe unique à compter de 2027, avec des taux majorables par les communes : le mécanisme de référence n'est plus celui de S-22 (mai 2025).

**Preuve.** Service-Public, actualité A18896 (21/05/2026, mise à jour 02/09/2026, vérifiée 2026-09-18) : art. 108 de la loi n° 2026-103 (LF 2026) ; « la taxe sur la vacance des locaux d'habitation » fusionne TLV et THLV « dans un souci de simplification et de lisibilité » ; application au 1er janvier 2027 ; zones tendues : 17 % la première année, 34 % ensuite, les communes pouvant porter à 30 %/60 % ; autres zones : taux fixé par le conseil municipal, plafond 50 %. Rendements 2024 relayés par la presse spécialisée (TLV ≈ 290 M€, THLV 178 M€) — NON vérifiés sur une source officielle (l'évaluation préalable de l'article ou le tome I « Voies et moyens » du PLF 2026) ; S-22 ne donne que 2023 (271 M€ TLV, 107 M€ THLV, p. 36 — la p. 5 du même rapport date la même série « 2017 à 2024 », incohérence interne à signaler dans la note).

**Disposition proposée.** Enregistrer S-52 = page Service-Public A18896 (HTML figé, LO 2.0) et référencer l'art. 108 de la loi n° 2026-103 ; dire dans R-15/L-29 que M-A est chiffré sur le rendement 2020-2024 de l'ancien dispositif et que la TVLH 2027 (taux jusqu'à 60 %) est une hypothèse de canal « renforcé » qui justifie la borne haute de H-14 mieux que « sans précédent documenté » ; ne citer 290 M€ qu'après enregistrement d'une source officielle.

---

### SA-8 — Note S-39 : décompte des départements erroné et écart de périmètre sous-estimé

**Gravité : mineure.**

**Énoncé.** La note S-39 écrit : « le décompte du texte — 94 départements en baisse + Nord, Belfort, Mayotte = 96 — confirme que le 9,9 Md€ est sur ce champ de 96 départements ». DEC-11 estime l'écart avec la France entière à « environ 10 % ».

**Preuve.** S-39 p. 4 : « Quatre-vingt-quatorze départements ont vu leur produit de DMTO diminuer en 2024 : à l'exception du Nord (− 4,5 %) et du Territoire de Belfort (− 4,8 %), tous enregistrent des baisses supérieures à − 5 % […]. Seul Mayotte voit ses DMTO croitre. » Le Nord et Belfort sont DANS les 94 (exceptions à l'ampleur, pas au sens) : 94 + Mayotte = 95 = 101 − 6 (75, 69, 2A, 2B, 972, 973). La conclusion (périmètre constant) tient, mieux même, mais l'arithmétique de la note est fausse. Écart réel : BIS n° 190 (DGCL, p. 1) « En 2023, les DMTO perçus par les départements s'élèvent à 13,0 Md€ » France entière, contre 11,40 Md€ au périmètre constant OFGL (annexe p. 110 du pré-rapport 2026) → **+14 %**, pas ≈ 10 % ; le BIS détaille (p. 3, encadré 1 p. 9) : ville de Paris 1 039 M€ (2023 ; « 1,3 Md€ » au titre des compétences départementales), métropole de Lyon 314 M€, CTU 139 M€, communes 3,1 Md€.

**Disposition proposée.** Corriger la note (95 départements) ; enregistrer S-53 = BIS n° 190 (sha256 `35088872f2ab8d86f39f932062751d8fa2449df8465985f0eaf2841e676ade16`) comme ancre France entière et pour Paris ; corriger DEC-11/L-28 (« ≈ 14 % en 2023 »).

---

### SA-9 — Références de pages inexactes dans les notes (S-40, S-43, S-44, D-19)

**Gravité : mineure** (mais ce sont des citations : §13.5).

**Preuve** (index PDF = folio imprimé pour S-40 et S-44, vérifié sur les pieds de page ; S-43 : PDF p. 1 = folio 187) :
- H-17 : « S-40, p. 33 : “une maturité allongée jusqu'à 30 ans” pour l'éco-prêt » → la phrase est **p. 22** (« Le lancement de la quatrième génération d'Éco-prêts, en juin 2023, avec une hausse du plafond éligible par logement, une maturité allongée jusqu'à 30 ans ») ; p. 33 traite des « Limites et sensibilité de l'analyse prospective ». La même p. 22 dit aussi « des prêts équivalents PLAI, PLUS et PLS à 40 ans » pour la « seconde vie du bâtiment » — meilleur appui pour H-17 = 40 ans en réhabilitation lourde.
- D-19 : « S-43, p. 3 du PDF » pour « La spécificité du cas français a trait au fait que les DMTO sont proportionnels… » → **p. 5 du PDF** (folio 191) ; la p. 3 contient « La spécificité des droits de mutation… » (Philadelphie), autre phrase.
- S-43 : « pp. 179-200 de la revue » → folios **187-209** (PDF 24 pages, 23 de texte).
- S-44 : « 30 des 38 pays … (p. 15) » → **p. 13** (encadré 1) ; « Renforcer le rôle des impôts périodiques … (pp. 5 et 17) » → **pp. 5 et 15** ; « Il existe de solides arguments … effets de manne … (p. 18) » → **p. 17**. La citation p. 4 (« entraver la mobilité résidentielle ») est exacte.

**Disposition proposée.** Corriger les six références ; le texte des citations est exact partout ailleurs (voir « chiffres recoupés »).

---

### SA-10 — S-42 (Livret A) : un article de communication du prêteur tient lieu d'acte officiel

**Gravité : mineure.**

**Preuve.** S-42 est l'article Banque des Territoires « Publié le 31 juillet 2026 » (« le taux du Livret A retrouvera un niveau de 1,7 % à compter du 1er août 2026 ») — exact. L'acte est la décision du ministre sur proposition du gouverneur : communiqué Bercy du 15/07/2026, « Épargne réglementée : le Livret A passe à 1,7 % et le LEP se maintient à 2,5 % à compter du 1er août 2026 » (https://presse.economie.gouv.fr/?p=181486 ; aussi https://www.info.gouv.fr/actualite/augmentation-du-taux-du-livret-a-a-compter-du-1er-aout-2026), « soit une hausse +0,2 point ». Le taux figé est bien le taux en vigueur au 2026-09-18 (prochaine révision 01/02/2027).

**Disposition proposée.** Enregistrer S-54 = communiqué Bercy (HTML figé) et faire porter H-16 dessus ; garder S-42 pour l'historique 2025-2026 (« 3 % → 2,4 % → 1,7 % → 1,5 % en février 2026 ») qu'il documente utilement.

---

### SA-11 — Assiette M-D : Mayotte est dans le produit, pas dans le parc

**Gravité : mineure.**

**Preuve.** S-11 est « France hors Mayotte » (registre) — recalcul : 0 ligne 976 dans `base-cc-logement-2022` ; le 9,9 Md€ OFGL inclut Mayotte (S-39 p. 4 : « Seul Mayotte voit ses DMTO croitre » ; BIS 190 : Mayotte 1,8 M€ en 2023, le plus faible). Effet < 0,02 % de la charge — négligeable, mais le périmètre doit être dit (§21 règle 10).

**Disposition proposée.** Une ligne dans C-14/L-28 ; aucune modification de valeur.

---

### SA-12 — Bail à réhabilitation : aucun bilan national trouvé ; l'échelle observée de l'outil est de l'ordre de la centaine de logements par an

**Gravité : mineure** (absence de source, mais informative).

**Preuve.** Aucune statistique nationale du nombre de baux à réhabilitation signés n'a été trouvée (Anah, USH, Soliha, Fapil, Sénat). Ordres de grandeur voisins : Anah (10/03/2023) — objectif de production en maîtrise d'ouvrage d'insertion « 306 logements en 2023 » ; Fapil, « Panorama de la maîtrise d'ouvrage d'insertion » (06/07/2026, PDF de 10 Mo non dépouillé) — opérations de « trois logements en moyenne », coûts de production +36 % en sept ans. Le mécanisme M-C suppose 13 654 à 136 544 logements (grille R-16) : deux à trois ordres de grandeur au-dessus de la pratique observée de la MOI, dont le BAR n'est qu'une fraction.

**Disposition proposée.** Enregistrer la page Anah comme ordre de grandeur de l'existant et le dire dans L-29 (« l'outil existe en droit ; son échelle observée est de quelques centaines de logements par an ») ; la grille de consentement reste la bonne réponse à l'absence de taux.

---

### SA-13 — Charges d'exploitation : S-40 publie bien un coût en €/logement, contrairement à ce que dit DEC-06

**Gravité : mineure** (lecture de source), avec effet possible sur L-30.

**Preuve.** DEC-06 écarte l'option (b) « un coût en €/logement » au motif que « le document ne publie pas ce ratio au grain voulu ». Or S-40 p. 24 (tableau 1) donne pour les charges d'exploitation : « en % des loyers 52,2 % · 52,9 % · 52,3 % · 53,8 % · 54,9 % · 54,9 % » ET « par logement (en €) 2 368 · 2 422 · 2 392 · 2 473 · 2 555 · **2 652** » (2018-2023). La convention proportionnelle de H-18 « SURESTIME les charges d'un loyer d'équilibre élevé » (L-30) : avec 2 652 €/logement/an au lieu de 54,9 % d'un loyer d'équilibre de 18,34 €/m² × 12 × surface, la charge unitaire M-B serait nettement plus basse (ordre de grandeur : 54,9 % de ~13 000 €/an ≈ 7 100 € vs 2 652 €). Le coût de la gestion en diffus, lui, reste sans source sectorielle ; seul proxy trouvé : Soliha/Koreis (02/12/2025), coût moyen de l'intermédiation locative 4 700 €/place/an (1 837 logements, 17 structures), accompagnement social inclus — non comparable directement.

**Disposition proposée.** Corriger DEC-06 ; ajouter dans R-16 une sensibilité « charges fixes 2 652 €/logement/an (S-40 p. 24) » à côté de la convention proportionnelle — sans changer le central (les deux conventions encadrent le vrai coût) ; enregistrer l'étude Soliha/Koreis si elle sert à la borne haute de H-18.

---

### SA-14 — Décote des vacants durables : toujours aucune source ; le seul proxy public est la « valeur verte » des notaires

**Gravité : mineure** (confirmation de L-27, pas d'objection).

**Preuve.** Recherche 2026-09-18 : aucune étude figée du prix des logements vacants durables vendus. Proxy le plus proche : étude annuelle du Conseil supérieur du notariat sur la décote DPE F/G vs D (−3 à −12 % selon type et région), non spécifique à la vacance. H-15 central 1,0 avec plage [0,5 ; 1,0] reste la bonne forme (INTRO §9).

**Disposition proposée.** Aucune ; mentionner dans L-27 que le proxy DPE existe et pourquoi il n'est pas retenu.

---

### SA-15 — Licences et champs : conformes, deux précisions

**Gravité : mineure.**

- S-39 / S-46 « Licence Ouverte 2.0 par défaut » : formulation prudente et correcte (CRPA) ; S-45 (DILA) LO 2.0 : exact ; S-43 : les publications INSEE sont réutilisables sous LO 2.0, exact ; S-40, S-41, S-42, S-44 `redistributable: false` : cohérent avec les mentions © des éditeurs.
- Champ S-40 « France hexagonale (468 bailleurs, 5,6 M de logements) » : exact (p. 15, note 12 précise que ce parc est « légèrement inférieur » à celui de la partie 1.1).
- Champ S-39 : la mention « périmètre constant » doit être portée dans `geographic_scope` (aujourd'hui « France (départements …) »), puisque c'est le champ du chiffre utilisé.

---

## Chiffres recoupés (constantes du code et des notes, page à l'appui)

| Constante / citation | Source, page | Verdict |
|---|---|---|
| `DMTO_PRODUCT_2024_EUR` = 9,9 Md€, « décroit de − 13,5 % » | S-39 p. 4 | **OK** (annexe OFGL 2026 : 9,86) — mais dépassé, voir SA-1 |
| « périmètre constant … hors Rhône, Martinique, Guyane, Corse et Paris » | S-39 p. 5 (graphique 6b) ; p. 11 | **OK** |
| « 3 départements à 3,80 % (Morbihan, Indre, Mayotte) », « 5 % en 2025 (hors primo-accédants) », « − 7,5 % de vente », « − 2,0 % » | S-39 p. 4 | **OK** |
| Décompte « 94 + 3 = 96 » | S-39 p. 4 | **KO** (95, SA-8) |
| `DMTO_PERIMETER_EXCLUDED_DEPARTEMENTS` → parc 34 565 110 | S-11, P22_LOG hors 75/69/2A/2B/972/973, PLM dédoublonnés | **OK** (recalcul indépendant 35,03 M avant dédoublonnage des arrondissements de Marseille ≈ cohérent) |
| 286 €/logement/an = 9,9e9 / 34 565 110 | artefact | **OK** (286,4) |
| `TLV_YIELD_2023_EUR` = 271 M€ | S-22 p. 36 (« de 80 M€ en 2014 à 271 M€ en 2023 pour la TLV ») | **OK** (p. 5 du même rapport date la série 2017-2024 : incohérence interne à noter) |
| ZLV « 6 700 sorties » | S-22 p. 24 | **OK** |
| « 3 % du stock ciblé en zone tendue, en 4 ans » (H-14) | S-22 p. 24 + note 44 | **KO** (3 % des CONTACTÉS, enquête oct. 2022 ; SA-2) |
| H-18 = 0,549 ; « 54,9 € … charges d'exploitation et 43,8 € … annuités » ; gestion 27,8 ; maintenance 15,5 ; TFPB 11,6 ; EBE 45,3 ; autofinancement 1,5 | S-40 p. 15 (schéma + note de lecture) | **OK** |
| « loyers quittancés … corrigés des pertes de loyers liées à la vacance » (D-20, note 13) | S-40 p. 15 | **OK** |
| 468 bailleurs, 5,6 M de logements | S-40 p. 15 | **OK** |
| Maintenance 4,2 Md€ (2,2 + 2,0) | S-40 p. 19 | **OK** |
| « maturité allongée jusqu'à 30 ans » (H-17, « p. 33 ») | S-40 **p. 22** | **KO page** (SA-9) |
| Charges d'exploitation « par logement 2 652 € » (absent des notes) | S-40 p. 24 | non cité — SA-13 |
| « Taux Livret A + 60 pb », « Bâti : de 5 à 40 ans », « Partie foncière : de 5 à 50 ans, jusqu'à 80 ans maximum » (H-16/H-17) | S-41 | **OK** |
| PLAI Livret A − 0,20 ; PLS Livret A + 1,11 (bornes H-16) | S-41 | **KO** (absents ; SA-3) |
| Livret A 1,7 % au 1er août 2026, article du 31/07/2026 | S-42 | **OK** |
| `BAR_AMORTISATION_YEARS` = 30 ; « entre 12 et 99 ans, en moyenne 30 ans » ; L252-1 à L252-6 ; mise à jour 23/06/2025 | S-46 p. 1 | **OK** |
| Exonération TFPB du preneur (absente de D-21/H-18) | S-46 p. 1 | non cité — SA-5 |
| `PRIX_REVIENT_NEUF_EUR_2023` = 169 200 € | S-18 p. 11 et p. 27 | **OK** |
| « indemnité principale … valeur vénale », « indemnités accessoires … remploi », « Vérifié le 28 novembre 2025 » | S-45 | **OK** |
| S-43 résumé : « 3.80 % à 4.50 % », « effet d'anticipation, un mois avant », « baisse … de l'ordre de 6 % sur les trois premiers mois », « environ 15 000 transactions », « aucune preuve d'un effet à moyen ou long terme » | S-43 p. 1 | **OK** |
| « partie ascendante de la courbe de Laffer » | S-43 p. 2 | **OK** |
| « La spécificité du cas français … » (D-19, « p. 3 ») | S-43 **p. 5** | **KO page** |
| « pp. 179-200 » | S-43 folios 187-209 | **KO** |
| OCDE : « entraver la mobilité résidentielle » (p. 4) ; recommandation « Renforcer le rôle des impôts périodiques … » ; « 30 des 38 » ; « solides arguments … effets de manne » | S-44 p. 4 ; pp. 5 et **15** ; **p. 13** ; **p. 17** | texte **OK**, trois pages **KO** |
| sha256 des 8 fichiers figés S-39..S-46 | `data/raw/` | **OK** (8/8) |

## Sources à enregistrer (avec URL)

1. **S-47 — OFGL, pré-rapport 2026 « def » (finances locales 2025)** — https://www.collectivites-locales.gouv.fr/files/files/Etudes-et-statistiques/OFGL/rapport%202026/Pr%C3%A9-Rapport%20OFGL%202026%20def.pdf — PDF du 11/06/2026, 176 p., sha256 `e351ef2581cc8937cbd5df48b3e32322d008e26a6e67478434f896d0ef65f264` ; p. 47 (11,9 Md€, + 20,4 %), p. 48 (champ), p. 110 (série 2022-2025). Fiche départements du rapport final (03/07/2026, image) : https://www.collectivites-locales.gouv.fr/files/files/Etudes-et-statistiques/OFGL/rapport%202026/4-%20Fiche%20sur%20les%20d%C3%A9partements.pdf (sha256 `4c6b538162c0d28e23323933baee3a2e1394aec350ccf3a3ccecbb4c94ee456e`). — SA-1.
2. **S-48 — Banque des Territoires, prêt PLAI (page produit)** — https://www.banquedesterritoires.fr/produits-services/prets-long-terme/pret-plai — SA-3, SA-5.
3. **S-49 — Banque des Territoires, prêt PLS (page produit)** — https://www.banquedesterritoires.fr/produits-services/prets-long-terme/pret-locatif-social — SA-3.
4. **S-50 — Code de l'expropriation, art. R322-5 (indemnité de remploi)** — https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000029971412/ (capture derrière Cloudflare : voir l'astuce monopoles/CLAUDE.md) + un dossier public de DUP témoin du barème 20/15/10 %, ex. https://www.herault.gouv.fr/contenu/telechargement/25559/182390/file/Dossier%20DUP%20ZAC%20Enjalbert%20-%20Piece%208%20estimation%20depenses.pdf — SA-4.
5. **S-51 — CPO, « Pour une fiscalité du logement plus cohérente » (18/12/2023)** — https://www.ccomptes.fr/sites/default/files/2023-12/20231218-Fiscalite-du-logement.pdf — 115 p., sha256 `7589d3d7266b2342a45452302a084a90c3d5565780545ce8d8a742c6776eac43` ; pp. 17, 20, 21 (reco n° 8), 32, 39. — SA-6.
6. **S-52 — Service-Public, « Une taxe unique pour les logements vacants à partir de 2027 » (A18896)** — https://www.service-public.gouv.fr/particuliers/actualites/A18896 — art. 108, loi n° 2026-103 du 19/02/2026 (LO 2.0). — SA-7.
7. **S-53 — DGCL, BIS n° 190 « Les DMTO des départements en 2023 »** — https://www.collectivites-locales.gouv.fr/files/files/Etudes-et-statistiques/BIS/2024/BIS_190_DMTO.pdf — sha256 `35088872f2ab8d86f39f932062751d8fa2449df8465985f0eaf2841e676ade16` ; 13,0 Md€ France entière, Paris 1 039 M€, communes 3,1 Md€. — SA-8.
8. **S-54 — Ministère de l'Économie, communiqué du 15/07/2026 (Livret A 1,7 % au 01/08/2026)** — https://presse.economie.gouv.fr/?p=181486 (ou https://www.info.gouv.fr/actualite/augmentation-du-taux-du-livret-a-a-compter-du-1er-aout-2026). — SA-10.
9. *(optionnel)* Anah, « La MOI, un dispositif à vocation sociale » (10/03/2023) — https://www.anah.gouv.fr/actualites/la-maitrise-d-ouvrage-d-insertion-un-dispositif-vocation-sociale — SA-12 ; Fédération Soliha / Koreis, étude IML (02/12/2025) — https://soliha.fr/core/wp-content/uploads/2025/12/20251202-cp-etude-iml-soliha-v2.pdf — SA-13 ; Fapil, Panorama MOI (07/2026) — https://www.fapil.fr/wp-content/uploads/2026/07/panorama-MOI-web.pdf — SA-12.
10. *(à trouver avant de citer 290 M€)* rendement officiel TLV/THLV 2024 : évaluation préalable de l'art. 108 du PLF 2026 ou tome I « Voies et moyens » — SA-7.

## Verdict global

Les huit sources nouvelles sont figées, checksummées et citées avec exactitude sur le fond (toutes les citations textuelles ont été retrouvées ; six références de page sont fausses, deux chiffres — le « 3 % » de H-14 et le décompte « 96 » de S-39 — sont mal lus, et deux bornes de H-16 ne sont dans aucun fichier figé).
Une objection majeure : M-D est calibré sur le produit DMTO 2024 (9,9 Md€, point bas) alors que l'OFGL a publié le millésime 2025 (11,9 Md€, + 20,4 %, même périmètre) en juin-juillet 2026 — R-17, I-17 et P-01 doivent être recalculés ou publier ce millésime en sensibilité (charge 343 vs 286 €/logement/an ; 27 ans d'équivalence au lieu de 33).
Les conclusions I-15/I-16 ne sont pas renversées par les sources trouvées (les corrections SA-2, SA-4, SA-5 vont respectivement dans le sens conservateur, contre M-B de +7 %, et en faveur de M-C) ; mais le CPO 2023, la TVLH 2027 et l'exonération de TFPB du bail à réhabilitation sont des sources officielles absentes de la chaîne qu'un lecteur informé opposera immédiatement.
