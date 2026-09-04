<!--
MATÉRIAU EXPLORATOIRE (méthode Métabolisme, INTRO §2.1) — archivé tel quel.

Note de travail de Rémy Loubradou, septembre 2026, à l'origine de l'étude
`monopoles/`. Elle relève du régime exploratoire : ses chiffres ne sont pas
sourcés (l'auteur le signale lui-même en fin de texte pour tous les secteurs
hors logement) et RIEN de ce qui suit ne doit être cité comme établi. Le
cadrage qui en est tiré est `../INTRO.md`.

Divergences relevées le 2026-09-04 en confrontant le texte aux sources déjà
figées dans le dépôt (étude `logement/` et note privée « Le parc social,
fonction régulatrice ou logique volumétrique ? ») :

- « 60 % des habitants de Vienne en loyer plafonné » — la Ville de Vienne
  dit « environ 50 % » (socialhousing.wien) ;
- « au moins 80 % des logements loués au plafond en zone tendue, Ancols » —
  Panorama du logement social 2025, p. 40 : 17 % au plafond et 50 % à 98 %
  ou plus du plafond en France ; 62 % en zone A, 45 % en Abis, 38 % en C ;
- « 27,8 €/m² à Paris » — OLAP, rapport Paris 2024 : 25,5 €/m² en moyenne,
  27,2 €/m² pour les emménagés récents (parc privé non meublé, hors charges) ;
- « entre un tiers et 40 % du parc locatif » — Ancols : un tiers ; enquête
  Logement 2020 (Insee) : 43 % par calcul ;
- prix de l'ancien ×2,3 / ×2,6 (2001-2020), « 3,5 % des ménages détiennent
  50 % du locatif », « 58 % de propriétaires » — aucune source figée dans le
  dépôt à cette date ;
- §6.1 (« le coût de construction hors terrain a suivi les prix à la
  consommation ») contredit §7 (« l'indice du coût de la construction
  diverge sensiblement de l'inflation à la consommation »).

Le tableau de synthèse conclut pour le logement « allocation administrée
nécessaire » alors que la proposition (§3.9, §6.3) conserve un marché privé
et vise un parc faiseur de prix : la tension est tranchée dans le cadrage
(`../INTRO.md` §8.1).
-->

# La grille des deux questions

## Collectiviser la rente là où le marché n'existe pas

*Note de travail — méthode d'identification des monopoles naturels et doctrine de captation de la rente*

---

## Résumé

Ce texte propose un critère de décision simple, applicable secteur par secteur, pour déterminer ce qui doit revenir à la collectivité et ce qui peut légitimement rester au marché.

Il ne s'agit pas d'un plaidoyer contre le marché. Il s'agit de constater que dans une série de secteurs qui représentent environ la moitié du budget des ménages — logement, énergie, eau, transport, télécommunications — le marché n'existe pas réellement, et que le prix payé par l'usager rémunère une position plutôt qu'une production.

La thèse tient en une phrase : **là où la ressource est non substituable, il n'y a pas de concurrence possible, donc la rente est structurelle et doit revenir à l'usager sous forme de prix, pas à un propriétaire sous forme de profit.**

---

## 1. Deux rentes qu'il ne faut pas confondre

Toute rente n'est pas illégitime. La distinction est décisive politiquement, parce qu'elle protège l'argument contre l'accusation d'anticapitalisme indifférencié.

**La rente d'innovation** rémunère une découverte et un risque. Elle est temporaire : elle se dissipe par imitation dès que d'autres acteurs reproduisent l'avancée. C'est le mécanisme schumpétérien classique, et c'est précisément ce qui rend le marché utile. Dans un secteur réellement concurrentiel, les prix convergent vers les coûts de fonctionnement augmentés de ce qui est nécessaire pour financer l'innovation suivante. Cette rente-là a une fonction.

**La rente de position** ne rémunère rien. Elle provient du contrôle d'une ressource que personne ne peut reproduire ni contourner. Elle ne se dissipe jamais, parce qu'aucune imitation n'est possible. Elle ne finance aucune innovation : elle prélève.

Le critère qui sépare les deux est la **non-substituabilité** de la ressource mobilisée. Une innovation est substituable par définition — quelqu'un peut faire aussi bien autrement. Un réseau d'eau, un sillon ferroviaire, une position urbaine ne le sont pas.

**Deux zones grises à assumer.** Le brevet crée une rente juridiquement protégée et durable, donc pas si temporaire que cela : c'est un choix de politique publique, révisable. Et les plateformes numériques fabriquent des monopoles naturels par effets de réseau, sans aucune rareté physique. Le critère de non-substituabilité les attrape correctement, ce qui est un bon indice de sa robustesse.

---

## 2. La grille

Deux questions, posées dans l'ordre.

### Question 1 — L'infrastructure est-elle substituable ?

Peut-on raisonnablement en construire une seconde qui concurrence la première ? Si la réponse est non, on est devant un monopole naturel, et la rente qu'il produit doit revenir à la collectivité. Ce n'est pas une opinion politique, c'est un constat technique : il n'existe aucun mécanisme de marché capable de discipliner ce prix.

### Question 2 — Le réseau est-il partageable entre plusieurs opérateurs de service ?

Une fois l'infrastructure collectivisée, il reste à savoir si plusieurs acteurs peuvent y servir des clients **simultanément** de manière utile, ou si la nature du réseau impose un opérateur unique.

- **Réseau partageable** → la concurrence a un sens sur la couche de service, à condition que l'infrastructure reste collective et l'accès régulé.
- **Réseau non partageable** → un opérateur unique, et l'accès à la capacité est nécessairement administré.

Deux propriétés physiques déterminent la réponse.

**La rivalité de la capacité.** Une unité de capacité est rivale lorsque, une fois consommée, elle n'est plus disponible pour un autre. Un sillon ferroviaire est rival : un train occupe le créneau, aucun autre ne peut l'emprunter. Un lien de fibre ne l'est presque pas, le coût marginal d'un utilisateur supplémentaire étant proche de zéro. Plus la capacité est rivale, moins la coexistence d'opérateurs apporte, et plus l'allocation doit être arbitrée par un gestionnaire.

**La différenciabilité du bien livré.** Certains biens sont physiquement indistinguables une fois arrivés chez l'usager. Un électron sur le réseau n'a pas d'origine identifiable, un mètre cube d'eau au robinet non plus. Dans ce cas, une concurrence entre fournisseurs est purement comptable : elle porte sur la facturation, pas sur le produit.

### Une question distincte, à ne pas confondre : qui exploite le réseau ?

L'entretien et l'exploitation d'une infrastructure peuvent **toujours** être délégués, quel que soit le résultat des deux questions précédentes. Une régie publique peut le faire, ou un ou plusieurs prestataires privés sélectionnés par appel d'offres. Un réseau autoroutier ou ferroviaire peut parfaitement être entretenu par plusieurs entreprises attributaires de lots distincts.

Mais cela n'est pas une concurrence *sur* le réseau : c'est une concurrence *pour* le réseau, une mise en compétition de prestataires rémunérés au forfait, sans transfert de la recette d'usage. C'est un **choix de mode de gestion**, pas un choix de structure de marché.

La confusion entre les deux est précisément ce qui a permis de justifier la cession des concessions autoroutières : on a présenté comme une ouverture à la concurrence ce qui n'était qu'un transfert de la rente à un exploitant unique en situation de monopole local.

**Les trois niveaux à tenir séparés :**

| Niveau | Question | Réponse déterminée par |
|---|---|---|
| Propriété de l'infrastructure | Qui possède le réseau et encaisse la rente ? | Q1 — substituabilité |
| Opérateurs de service | Combien d'acteurs peuvent servir des clients dessus ? | Q2 — partageabilité (rivalité + différenciabilité) |
| Exploitation et entretien | Qui fait le travail sur le réseau ? | Choix de gestion : régie ou délégation au forfait |

### Tableau de synthèse

| Secteur | Infrastructure substituable ? | Capacité rivale ? | Bien différenciable ? | Réseau partageable ? | Conclusion |
|---|---|---|---|---|---|
| Fibre / boucle locale | Non | Non | Oui (services) | Oui | Réseau collectif, opérateurs de service en concurrence |
| Rail | Non | Oui (sillons) | Partiellement | Partiellement | Réseau collectif, sillons administrés, concurrence marginale |
| Électricité | Non | Oui (+ contrainte temporelle) | Non | Non | Réseau et production de base collectifs, prix administré |
| Hydroélectricité | Non (sites finis) | Oui | Non | Non | Concessions non renouvelées, exploitation publique |
| Eau | Non | Oui | Non | Non | Régie publique intégrale |
| Réseaux de chaleur | Non | Oui | Non | Non | Maîtrise publique, usager captif à protéger |
| Autoroutes | Non | Faiblement | Non | Non | Recette publique, entretien délégable au forfait |
| Stationnement | Non (le sol) | Totalement | Non | Non | Domaine public déjà collectif : ne pas reconcéder |
| Logement | Non (le sol) | Totalement | Oui (le bâti) | Non | Cas extrême : allocation administrée nécessaire |
| Satellite | Non (spectre, orbite) | Oui | Oui (services) | Oui, sous quota | Ressource commune à tarifer, service concurrentiel |

---

## 3. Ce que la grille donne, secteur par secteur

### 3.1 Télécommunications — le cas où la doctrine a déjà fonctionné

La boucle locale n'est pas duplicable à coût raisonnable. Mais la capacité n'est pas rivale et le service est différenciable : le réseau est donc partageable, et plusieurs opérateurs peuvent y servir des clients différents simultanément.

C'est exactement ce que la régulation a fait, avec le dégroupage puis la mutualisation de la fibre sous supervision de l'ARCEP. Le résultat est connu : la France a parmi les prix fixes et mobiles les plus bas d'Europe.

**Ce cas est capital pour l'argumentation, parce qu'il prouve que la grille n'est pas une théorie.** Elle décrit un dispositif existant, qui fonctionne, et que personne ne songe sérieusement à démanteler. Toute la discussion consiste à l'appliquer ailleurs.

### 3.2 Rail — la rivalité de la capacité impose l'administration

Le réseau n'est pas duplicable, et sa capacité est strictement rivale : un sillon consommé n'existe plus. Deux opérateurs ne peuvent pas partir à la même heure sur la même voie. Le réseau n'est donc que partiellement partageable.

La conséquence est que l'allocation des sillons ne peut pas être marchande. Elle est attribuée par un gestionnaire, selon des priorités décidées politiquement. La concurrence entre opérateurs reste possible à la marge, mais elle porte sur l'exploitation d'un créneau attribué, jamais sur l'accès lui-même.

### 3.3 Électricité — la dimension temporelle

L'électricité ajoute une variable que les autres cas n'ont pas : **elle n'existe qu'au moment où elle est consommée.** Elle est rivale, non stockable à grande échelle, et indifférenciable.

Cela a une conséquence qu'il faut concéder : le prix instantané a une vraie fonction informationnelle, il signale quand consommer et quand s'abstenir. Un signal temporel sur la marge d'ajustement est utile.

Mais cela ne justifie en rien l'architecture actuelle. Le réseau est un monopole naturel évident. La production nucléaire est un actif largement amorti, à coûts massivement fixes, dont le coût de production n'a aucun rapport avec le prix de marché européen. L'ARENH en est l'illustration : un dispositif obligeant l'opérateur historique à céder son électricité amortie à des fournisseurs alternatifs qui la revendaient sans rien produire. Une rente transférée à des intermédiaires, sans gain d'efficacité correspondant.

Le renouvelable complique le tableau, mais pas dans le sens qu'on croit. Le coût difficile n'est pas celui de la production, qui a beaucoup baissé : c'est le **coût système** — le back-up pilotable, le stockage, le renforcement du réseau, la gestion de l'intermittence. Or c'est typiquement un coût qu'un opérateur intégré optimise et qu'un marché fragmenté externalise.

**Conclusion de la grille :** réseau et production de base collectivisés, prix administré couvrant le coût complet, signal temporel conservé sur la seule marge.

### 3.4 Concessions hydroélectriques — la rente la plus visible

Un site de barrage est le cas de non-substituabilité le plus littéral qui soit : il n'existe qu'un nombre fini de vallées équipables, elles sont déjà équipées, et on n'en fabrique pas de nouvelles. La capacité est rivale — un mètre cube turbiné ne l'est qu'une fois — et l'électricité produite est indifférenciable.

La rente est ici particulièrement nette. Les ouvrages sont anciens et largement amortis, souvent construits sur fonds publics ; leur coût de production est très bas et sans rapport avec le prix de marché de l'électricité. L'écart entre les deux n'est pas une rémunération du risque, c'est une rente d'antériorité.

Le contentieux européen sur la mise en concurrence des concessions échues éclaire précisément la limite de l'approche marchande : **mettre une rente aux enchères ne la supprime pas, elle change simplement de bénéficiaire.** Un appel d'offres capture au mieux une fraction de la rente à l'instant de l'attribution ; toutes les hausses de prix ultérieures reviennent au concessionnaire, sans qu'il ait rien produit de plus.

Un argument spécifique renforce le cas : un barrage n'est jamais un pur outil de production électrique. Il arbitre en permanence entre soutien d'étiage, irrigation, alimentation en eau potable, écrêtement des crues, tourisme et production. Ces arbitrages sont politiques et non marchands, et un concessionnaire rémunéré au mégawattheure n'a aucune raison de les rendre dans le sens de l'intérêt général.

### 3.5 Eau — le cas le plus pur

Réseau non duplicable, capacité rivale, bien totalement indifférenciable. Le réseau n'est pas partageable, et il n'existe aucun espace pour une concurrence entre opérateurs de service.

La France ne l'a d'ailleurs jamais organisée : la compétence est communale, et ce qui existe n'est pas une concurrence *sur* le service mais une concurrence *pour* le service, par délégation. L'écart de coût entre gestion déléguée et régie publique est documenté et va généralement de dix à vingt pour cent, à qualité comparable. C'est ce qui a motivé le retour en régie de plusieurs grandes villes, dont Paris en 2010.

L'eau fournit en outre un précédent directement transposable : le débat sur la gratuité des premiers mètres cubes est exactement une logique de **plancher et de plafond** appliquée à un monopole naturel. Un socle vital tarifé au coût, une progressivité au-delà.

### 3.6 Réseaux de chaleur urbains — le monopole le plus absolu

C'est probablement le cas où la captivité de l'usager est la plus totale, et paradoxalement le moins discuté.

Personne ne pose un second réseau de canalisations dans la même rue : l'infrastructure n'est pas duplicable. La capacité est rivale, la chaleur livrée est indifférenciable, et le réseau n'est donc partageable entre aucun opérateur de service.

Mais s'y ajoute une caractéristique que les autres réseaux n'ont pas au même degré : **une fois raccordé, l'usager ne peut plus sortir.** Changer de source de chauffage suppose de refaire l'installation complète de l'immeuble, pour un coût prohibitif, et la décision relève de la copropriété et non de l'occupant. Le consommateur n'a donc ni concurrence, ni arbitrage possible, ni même la capacité de refuser une hausse. Il est captif au sens strict, et les concessions courent sur vingt à trente ans.

Le sujet est de surcroît appelé à grossir, puisque les réseaux de chaleur sont un des principaux leviers de décarbonation du chauffage — géothermie, biomasse, récupération de chaleur industrielle fatale. D'où l'argument politique, qui est simple à porter : **on ne peut pas demander aux habitants de se raccorder massivement à un réseau décarboné tout en les livrant à un monopole non régulé pour trente ans.** L'exigence de maîtrise publique est ici la condition de l'acceptabilité de la transition.

Comme pour l'eau, la compétence est communale, ce qui rend le sujet immédiatement actionnable.

### 3.7 Autoroutes — la distinction décisive

L'infrastructure n'est pas duplicable. La capacité n'est que faiblement rivale, sauf en situation de congestion, mais le service est indifférenciable : rouler sur une voie n'est pas un produit qu'un opérateur pourrait distinguer de celui d'un autre. Le réseau n'est donc pas partageable entre opérateurs de service.

C'est ici que le **troisième niveau** de la grille devient décisif. Qu'aucune concurrence de service ne soit possible n'empêche nullement de mettre en compétition l'entretien et l'exploitation, éventuellement par lots et entre plusieurs entreprises. Simplement, l'attributaire est sélectionné sur sa performance et rémunéré au forfait ; le péage remonte à la collectivité, qui porte le risque de trafic et encaisse le produit. C'est la différence entre **concurrence pour le réseau** et **concurrence sur le réseau**.

Le rail relève exactement de la même logique : plusieurs entreprises peuvent entretenir des sections différentes du réseau sans que cela crée le moindre marché du transport ferroviaire.

Le modèle français a fait l'inverse. Les concessionnaires encaissent les péages jusqu'aux échéances de 2031 à 2036, avec des marges nettes élevées sur des infrastructures déjà amorties par le contribuable.

Et comme pour l'eau, la coexistence de régies publiques et d'opérateurs privés fournirait un **étalon d'efficacité** : chacun devant s'aligner sur la performance de l'autre, sans que ni l'un ni l'autre ne capte la rente.

### 3.8 Stationnement et parkings — le cas le plus immédiatement actionnable

La grille donne ici le même profil que le logement : le sol est non substituable et purement positionnel, la capacité est totalement rivale — une place occupée ne l'est par personne d'autre — et le service est indifférenciable. Réseau non partageable, allocation nécessairement administrée.

Mais ce cas présente une particularité qui le rend plus simple que tous les autres : **l'actif sous-jacent appartient déjà à la collectivité.** La voirie et le sous-sol relèvent du domaine public. Il n'y a donc aucune question d'expropriation ni d'indemnisation d'un propriétaire : la collectivité a seulement cédé l'exploitation par concession, souvent pour plusieurs décennies, à un petit nombre d'acteurs — largement les mêmes groupes que sur les autoroutes. Récupérer la rente ne demande rien de plus que de ne pas renouveler.

Deux atouts tactiques en découlent.

**La compétence est municipale.** Le sujet ne se heurte ni au droit européen ni à un blocage électoral national. Il est actionnable ville par ville, immédiatement, et produit une démonstration vérifiable à petite échelle — ce qui manque cruellement au reste du programme.

**Le précédent existe.** La décentralisation du stationnement payant de surface, effective depuis 2018, a déjà transféré aux communes la fixation du tarif et le produit de la redevance. Le raisonnement est donc déjà admis en droit pour la surface ; il s'agit de l'étendre aux ouvrages concédés.

Le stationnement est en outre un levier de politique de mobilité à part entière : les arbitrages entre résidents, visiteurs, livraisons, transports collectifs et réaffectation de l'espace public sont des décisions politiques, qu'un concessionnaire rémunéré à la rotation n'a aucune raison de rendre correctement.

**Point de vigilance rhétorique.** Toute intervention publique sur le stationnement est spontanément lue comme une hausse de tarif, ce qui est impopulaire. Or l'argument ne porte pas sur le prix mais sur le destinataire de la recette. Il faut le formuler comme une récupération de ressource municipale, jamais comme une politique tarifaire.

### 3.9 Logement — le cas extrême

Le logement est l'application la plus radicale de la grille, et c'est ce qui explique qu'il soit le secteur le plus dysfonctionnel.

Le sol est non substituable, non par rareté physique mais par **rareté positionnelle** : la valeur d'usage d'un logement dépend entièrement de sa localisation, et une position ne se reproduit pas. Et la capacité est totalement rivale : un logement occupé ne l'est par personne d'autre.

Les deux réponses de la grille sont donc au maximum, ce qui exclut toute régulation par le marché.

Les données le confirment. La hausse des prix depuis 2000 n'est pas une hausse de coût de production : le coût de construction hors terrain a suivi les prix à la consommation, tandis que les prix de l'ancien ont été multipliés par 2,3 en métropole et 2,6 en Île-de-France entre 2001 et 2020, contre 1,3 à 1,4 pour l'inflation, les loyers et le revenu par ménage. **Ce qui a doublé n'est pas le bâti, c'est la position.**

Et le parc social français, pourtant massif — 5,4 millions de logements, entre un tiers et 40 % du parc locatif — ne régule pas les prix. Les loyers y sont 31 % moins chers que dans le privé, mais l'écart de taux d'effort n'est que de trois points : 29,6 % contre 26,6 %. La raison est que ce parc est **résiduel** et non universel : réservé aux ménages sous plafonds, il n'est jamais une option de sortie pour un locataire du privé, donc il ne concurrence personne. En zone tendue, il suit même le marché plutôt qu'il ne le discipline, avec au moins 80 % des logements loués au plafond réglementaire.

Vienne fournit le contre-exemple : 60 % des habitants en loyer plafonné, un parc universel, inaliénable, financé par une cotisation employeurs et salariés, et un loyer moyen **tous statuts confondus** de 9,8 €/m² contre 27,8 € à Paris.

La conclusion est que la taille du parc ne suffit pas. Ce qui compte, c'est qu'il soit **assez large et assez ouvert pour devenir faiseur de prix** plutôt que preneur de prix. Au-delà de ce seuil, la propriété lucrative subsiste mais devient économiquement banale : elle ne rapporte plus que l'entretien et l'inflation, et cesse d'attirer les capitaux d'elle-même.

C'est l'atout politique majeur de cette approche : **on ne prohibe rien, on rend la spéculation inintéressante.** La liberté de posséder est intacte ; c'est son rendement anormal qui disparaît.

---

## 4. La frontière non régulée : l'orbite et le spectre

L'espace est le seul cas où la grille s'applique intégralement à un domaine où **aucune autorité n'existe pour la mettre en œuvre.** C'est ce qui en fait un objet d'étude précieux : on y observe la formation d'une rente en temps réel.

### Le service est concurrentiel, la ressource ne l'est pas

Pour un utilisateur situé en zone couverte, l'internet par satellite concurrence la fibre et la 4G. Le service est donc substituable, et la concurrence y est légitime.

Mais les deux ressources sous-jacentes ne le sont pas :

- **Le spectre radio** est fini. Il est coordonné par l'Union internationale des télécommunications selon un principe qui revient en pratique à un droit de priorité pour le premier déclarant. Des dizaines de milliers de satellites déposés, et des bandes de fréquences verrouillées pour des décennies.
- **L'orbite basse** est finie. Le nombre de couloirs utilisables est limité, et chaque satellite y crée un risque de collision et de débris qu'il ne paie pas.

### Une rente créée par pure antériorité d'occupation

Le mécanisme est exactement celui du foncier urbain, transposé à l'orbite : une ressource rare, distribuée gratuitement à celui qui est arrivé le premier, et dont l'occupation ne se dissipe pas par la concurrence une fois acquise.

Il faut concéder ce qui relève de la rente légitime : la réutilisabilité des lanceurs est une innovation réelle, qui a fait chuter le coût de mise en orbite. C'est une rente schumpétérienne, et le raisonnement de ce texte ne la conteste pas. Ce qu'il conteste, c'est le fait que cette innovation ait servi de véhicule à l'appropriation gratuite d'une ressource commune.

### Un régime de commun faiblement gouverné

Il n'y a pas de propriété, mais il n'y a pas non plus de Far West.

- Le traité de l'espace de 1967 interdit l'appropriation par les États, mais reste largement muet sur les entreprises.
- L'État de lancement est responsable des dommages causés par ses objets. C'est ce qui tient l'ensemble : ce sont les États qui répondent, pas les opérateurs. Détruire délibérément un satellite serait imputé à un État.
- La coordination des fréquences produit une **priorité d'usage opposable**, qui n'est pas un droit de propriété mais produit un effet d'exclusion comparable.

Ce qui manque, c'est l'exécution. Aucune autorité ne peut imposer une manœuvre d'évitement ni sanctionner un refus. La coordination repose sur la bonne volonté des opérateurs.

Le vrai risque n'est donc pas l'agression, c'est l'accident — et surtout l'impossibilité de distinguer les deux. Une manœuvre de proximité mal calculée, un débris laissé sur une trajectoire : la structure est idéale pour l'action hybride, sur le modèle de l'attribution impossible dans le domaine cyber.

Un frein existe, mais il est physique et non juridique. Un débris en orbite basse menace tout le monde, y compris son auteur, pour des décennies — c'est le syndrome de Kessler, et c'est ce qui a valu une condamnation internationale unanime au tir antisatellite russe de 2021. Contrairement au nucléaire, aucun bouclier ne protège d'un objet à sept kilomètres par seconde. Il n'existe pas de défense, seulement de l'évitement, ce qui pousse structurellement vers la coopération plutôt que vers la course.

### Ce que la grille recommande

**Tarifer l'occupation orbitale et l'usage du spectre à leur valeur de rareté, et affecter le produit à la désorbitation et au nettoyage.** Le pollueur finance le commun qu'il dégrade. Cela ne bloque aucune innovation : cela fait payer la rareté au lieu de la céder gratuitement.

Le précédent existe et fonctionne : la coordination internationale du spectre terrestre tient depuis un siècle. Le modèle n'est pas utopique, il est simplement sous-appliqué à l'orbite.

Ce qui manque n'est pas l'idée, c'est l'autorité et le financement.

---

## 5. Méthode de mise en œuvre

Identifier la rente est une chose. La récupérer en est une autre, et la méthode compte autant que le diagnostic.

### 5.1 Comprimer le rendement plutôt que rompre le contrat

Sur les concessions en cours, la résiliation unilatérale est un piège : politiquement populaire, juridiquement perdue. Les contrats prévoient l'indemnisation du manque à gagner, et les tribunaux l'accordent. On paie alors la rente d'un coup, sans même percevoir le péage.

Le levier efficace est la **compression du rendement régulé** : taxation de la rente exceptionnelle, refus des hausses tarifaires, obligations d'investissement. Le flux futur se réduit, la valeur actualisée de la concession s'effondre mécaniquement, et le rachat négocié devient abordable. On ne rompt pas : on rend la concession moins rentable que sa vente.

### 5.2 Chaque brique doit tenir seule

C'est la contrainte juridique décisive. Si un juge établit qu'un ensemble de mesures n'avait d'autre objet que de vider un contrat de sa valeur, il requalifie en expropriation déguisée, et tout tombe.

Donc chaque mesure doit être défendable isolément, avec sa propre justification d'intérêt général. Une taxe sur les rentes qui frappe toutes les rentes est légitime. Une taxe calibrée pour ne frapper qu'un acteur ne l'est pas.

### 5.3 Transparence sur les fins, rigueur sur les moyens

La question s'est posée de savoir s'il fallait dissimuler l'intention. La réponse est non, et pas seulement pour des raisons morales : un programme politique est public et archivé, et le mensonge serait produit au dossier par la partie adverse au pire moment.

Il n'y a d'ailleurs rien à dissimuler. « Nous considérons que cette rente est indue et nous voulons la ramener à la collectivité » est une position parfaitement assumable devant un juge. La ligne de partage juridique ne sépare pas le transparent du caché : elle sépare la poursuite d'un but d'intérêt général du détournement d'un instrument.

### 5.4 Séquencer par ordre de faisabilité

Commencer par ce qui arrive à échéance naturellement et où l'opinion est massivement acquise — les concessions autoroutières — plutôt que par ce qui suppose une renégociation européenne ou une confrontation avec un blocage électoral diffus.

Et surtout, ne pas négliger l'**échelon municipal**, qui est le seul immédiatement disponible. Le stationnement, les réseaux de chaleur et l'eau relèvent de compétences communales : ils ne demandent ni majorité nationale ni renégociation des traités, ils peuvent être engagés dès la première mandature obtenue, et ils fournissent la chose qui manque le plus à ce type de programme — une démonstration réelle et vérifiable plutôt qu'une promesse.

### 5.5 Nommer les oppositions réelles

- **Le droit européen** est l'obstacle le plus structurel : la libéralisation de l'énergie, du rail et des télécommunications y est inscrite, pas seulement dans la loi française.
- **Les concessionnaires** se battront devant les tribunaux, pas dans l'opinion. Le combat est financier et technique.
- **Sur le logement, l'opposition n'est pas un lobby mais une majorité.** Les organisations de propriétaires existent et sont actives, mais le vrai poids est diffus : environ 58 % des ménages sont propriétaires de leur résidence principale et ont un intérêt objectif à la hausse des prix, sans percevoir un seul loyer. C'est cette configuration qui rend le sujet intouchable, et c'est pourquoi la distinction entre propriété d'usage et propriété lucrative est stratégiquement centrale : elle sépare le propriétaire occupant du multipropriétaire, et défait l'alliance qui bloque.

---

## 6. Objections attendues

### 6.1 Sur le diagnostic

**« Il y a bien une concurrence entre logements : dans un quartier, des milliers de biens sont en concurrence. »**

C'est l'objection la plus sérieuse, et elle appelle trois réponses.

*La concurrence existe, mais elle est bornée.* Mille appartements d'un même quartier se concurrencent sur le bâti — la surface, l'étage, l'état. Ils ne se concurrencent jamais sur la localisation, qui leur est commune et que rien ne reproduit. C'est de la concurrence *à l'intérieur* d'une rente, pas contre elle : elle peut redistribuer entre biens, elle ne peut pas faire descendre le prix en dessous de la valeur de la position.

*Le test empirique tranche.* Dans un marché concurrentiel, le prix converge vers le coût de production. Or le coût de construction hors terrain a suivi les prix à la consommation pendant que les prix de l'ancien doublaient. Si la concurrence fonctionnait, cet écart serait impossible. C'est l'argument le plus fort, parce qu'il est factuel.

*L'offre est inélastique.* Un producteur normal augmente sa production quand le prix monte. On ne fabrique pas de sol au centre de Lyon. La hausse ne déclenche donc aucune réponse d'offre, seulement de la valorisation.

**Le retournement à opérer :** s'il y a bien concurrence libre et non faussée, pourquoi ne produit-elle aucun des quatre effets qu'on en attend ?

| Effet attendu d'un marché concurrentiel | Ce qu'on observe |
|---|---|
| Le prix converge vers le coût de production | Coût du bâti ×1,3, prix ×2,3 à ×2,6 |
| Les marges s'érodent avec l'entrée de nouveaux acteurs | Rendements en hausse, concentration renforcée (3,5 % des ménages détiennent 50 % du locatif privé) |
| Une hausse de prix déclenche une hausse d'offre | La construction en zone tendue n'a pas suivi, elle a reculé |
| Les prix convergent entre zones comparables | Divergence massive, maximale là où la contrainte de position est la plus forte |

Un marché où le prix se décorrèle du coût, où les marges montent, où l'offre ne répond pas et où les écarts se creusent n'est pas un marché concurrentiel. C'est la signature d'une rente.

**« Si la construction recule, c'est parce que le foncier est devenu trop cher pour qu'elle soit rentable. »**

Cette objection concède l'essentiel. Si le foncier absorbe toute la valeur disponible au point de rendre la construction non rentable, alors le prix du logement n'est pas déterminé par son coût de production : il est déterminé par le prix du sol. C'est la définition même de la rente foncière, formulée par le contradicteur.

Il faut y ajouter l'inversion causale. Le prix du foncier n'est pas un coût qui pousse les prix vers le haut : c'est un **résidu**. Le promoteur part de ce que l'acheteur final peut payer, retire son coût de construction et sa marge, et ce qui reste devient le prix qu'il peut offrir pour le terrain — c'est le compte à rebours, méthode standard de la promotion immobilière. Le foncier ne cause pas le prix, il le capte.

La conséquence est directe : tant que le sol reste marchand, tout gain de pouvoir d'achat et toute aide publique finissent absorbés dans le prix du terrain. D'où l'intérêt du foncier public et du bail réel solidaire, qui permettent de construire à coût réel en sortant le sol du marché.

### 6.2 Sur le principe

**« C'est de l'étatisme, vous supprimez le marché. »**
Non : on le restitue là où il n'existe pas. La grille conserve explicitement la concurrence partout où le réseau est partageable, et reconnaît la légitimité de la rente d'innovation. C'est un critère d'application, pas une doctrine d'extension.

**« La gestion publique est moins efficace. »**
C'est une hypothèse testable, et elle a été testée. Sur l'eau, l'écart documenté entre régie et délégation joue en faveur de la régie. Sur les télécoms, la régulation de l'infrastructure a produit les prix les plus bas d'Europe. Et le maintien d'opérateurs privés en concurrence *pour* le marché conserve l'aiguillon d'efficacité sans céder la rente.

**« Cela coûte trop cher. »**
La question est mal posée. Il ne s'agit pas d'une dépense de fonctionnement mais d'une acquisition d'actifs générant des recettes. La structure de financement existe : le fonds d'épargne de la Caisse des dépôts prête au logement social sur des maturités de quarante à soixante ans. Ce qui garantit l'emprunt n'est pas la revente — les actifs sont précisément inaliénables — mais le flux de recettes d'usage, qui est plus prévisible qu'une valeur de marché.

**« Vous spoliez les propriétaires. »**
La grille ne porte pas sur la propriété d'usage mais sur la propriété lucrative. Personne n'est expulsé, personne ne perd son logement. Et sur les acquisitions, la décote n'est justifiée que par un comportement — la rétention d'un bien hors d'usage — et non par le statut du propriétaire.

**« La baisse des prix ruine les héritiers. »**
En grande partie non : le patrimoine immobilier est une réserve de valeur *relative*. Si les prix baissent, l'héritage vaut moins mais achète autant. Ce que perd réellement l'héritier n'est pas du pouvoir d'achat immobilier, c'est sa position relative face à ceux qui n'héritent de rien — ce qui est précisément l'effet recherché. Il faut en revanche assumer un risque réel : les primo-accédants récents endettés à prix élevé se retrouveraient avec une dette supérieure à la valeur du bien. C'est ce qui plaide pour une transition longue visant une **stagnation nominale** plutôt qu'une chute, le taux d'effort se réduisant alors par la progression des revenus.

### 6.3 Sur l'attribution

C'est le terrain sur lequel la discussion se déplace dès que le diagnostic est admis, et il faut l'aborder de front plutôt que de le laisser venir.

**« Les gens ne pourront plus choisir où ils vivent. Il faudra un tri. »**

Oui, il y aura un tri — comme aujourd'hui. La différence est que le critère actuel est la fortune, et que personne ne l'appelle un tri parce qu'il passe par le prix et reste donc invisible. **La question n'est pas de savoir s'il faut trier, mais qui décide du critère.** Rendre le critère explicite, c'est le rendre discutable démocratiquement.

Le mécanisme proposé combine deux étages. D'abord un **appariement par adéquation** entre la composition du foyer et la capacité du logement, qui est un critère d'allocation efficace des ressources et non un jugement sur les personnes. Ensuite, entre candidats équivalents et donc indistinguables, un **arbitre neutre**. Le tirage au sort en est un ; l'ancienneté d'inscription, retenue à Vienne, en est un autre, moins heurtant pour l'opinion.

Le point à formuler avec soin : le hasard n'est pas le principe d'attribution, c'est l'arbitre de dernier recours. Présenté à l'envers, l'argument est perdu d'avance.

Deux éléments désamorcent l'angoisse qui sous-tend l'objection. La **mobilité** d'abord : avec un parc massif et un système d'échange organisé, ne pas obtenir son quartier préféré au premier tour n'est pas une assignation à vie. La **coexistence du privé** ensuite : le dispositif ne vise pas la totalité du parc, la propriété privée subsiste, et avec elle la possibilité d'acheter où l'on veut. C'est la soupape du système, et il faut l'assumer explicitement plutôt que la glisser en fin de phrase.

Enfin, il faut relativiser la liberté que l'on est accusé de retirer. Aujourd'hui, l'argent n'achète pas un quartier : il achète une place dans une file d'attente pour les rares biens mis en vente. Personne ne choisit son quartier, on choisit parmi ce qui se libère. On ne supprime pas une liberté existante.

**« Ce sera le règne du copinage et du clientélisme. »**

La réponse est procédurale, pas rhétorique. Le tirage au sort est précisément l'antidote au clientélisme : un tirage public et auditable ne se négocie pas, alors qu'une commission d'attribution discrétionnaire, elle, se négocie. L'accusation vise donc le mécanisme qui la rend impossible.

Ce qui rend l'attribution corruptible, ce n'est pas l'absence de marché, c'est l'absence de règle publique et vérifiable. La charge de la preuve porte sur la transparence du dispositif, et elle est tenable.

---

## 7. Ce qui reste à consolider

Deux points sont, à ce stade, des hypothèses de travail et non des résultats établis. Il vaut mieux les signaler ici que les voir surgir en contradiction.

**Le seuil de bascule.** L'ensemble du raisonnement sur le logement repose sur l'idée qu'il existe un seuil — situé autour de 30 à 40 % du parc locatif — au-delà duquel un parc régulé cesse d'être preneur de prix pour devenir faiseur de prix. Cette intuition est cohérente avec le cas viennois, mais elle n'est pas adossée à une estimation économétrique de l'élasticité des loyers privés à la part du parc régulé. C'est le point d'attaque le plus probable, et il mérite un travail de sourçage dédié.

**Le calibrage tarifaire.** Le mécanisme plancher-plafond suppose que le plancher couvre l'entretien courant et que l'écart entre plancher et plafond finance l'extension et la rénovation du parc. Trois questions restent ouvertes : l'indice de référence du plancher — l'indice du coût de la construction diverge sensiblement de l'inflation à la consommation ; l'indexation du plafond, qui perd sa référence externe dès que le parc devient dominant et doit alors basculer sur un indice interne, ce qui change sa nature de mécanisme concurrentiel en tarification publique ; et le fait qu'une pondération à la hausse entre plusieurs indices produirait un effet de cliquet à éviter, une pondération fixe étant préférable.

**Une contrainte technique à ne pas sous-estimer.** Le classement comptable de la structure porteuse dépend de son taux de couverture par les recettes d'usage. Tant que celles-ci couvrent les coûts de production et le service de la dette, la structure reste hors du périmètre des administrations publiques. Cela implique deux choses : que les ressources proviennent des seuls usagers, et que le parc capte suffisamment de ménages aisés pour que la mutualisation par le haut fonctionne. Un parc exclusivement pauvre est un parc subventionné, donc un parc dont la dette compte.

---

## Sources principales

| Donnée | Source |
|---|---|
| Parc social : 5,4 M de logements, 15,9 % des résidences principales | SDES, RPLS 2025 |
| Loyers : 418 € social / 607 € privé ; 6,5 vs 10,5 €/m² | SDES |
| Taux d'effort net des aides 2023 : 29,6 % privé / 26,6 % social | INSEE |
| Part du parc social dans le parc locatif : un tiers à 40 % | ANCOLS |
| 80 % des logements sociaux au plafond en zone tendue | ANCOLS |
| Prix de l'ancien ×2,3 métropole, ×2,6 IdF (2001-2020) vs ×1,3-1,4 inflation | INSEE / Friggit |
| Concentration : 3,5 % des ménages détiennent 50 % des logements loués par des particuliers | INSEE, portrait social 2021 |
| Vienne : 220 000 logements municipaux, 60 % en loyer plafonné, 9,8 €/m² moyen | Ville de Vienne / comparaisons européennes |

Les données relatives à l'eau, aux autoroutes, à l'électricité, à l'hydroélectricité, aux réseaux de chaleur, au stationnement et au domaine spatial sont mobilisées ici à titre d'ordres de grandeur et demandent un sourçage précis avant toute diffusion publique. Les développements sur ces secteurs reposent sur des raisonnements structurels, non sur des données chiffrées vérifiées.
