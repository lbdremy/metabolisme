# Chaîne de preuves exécutable

## Méthode de recherche et de conception de systèmes ancrés dans la réalité

Ce document définit la méthode de travail utilisée pour les recherches menées dans **Métabolisme**, ainsi que pour d’autres projets de conception institutionnelle, économique ou entrepreneuriale.

L’objectif n’est pas seulement de produire des textes convaincants, des chiffres plausibles ou des propositions cohérentes. Il est de construire des **chaînes de raisonnement inspectables**, reliées à leurs sources, dont les calculs peuvent être rejoués et dont les hypothèses peuvent être modifiées.

Une proposition publiée doit permettre à une autre personne de répondre à des questions simples :

* D’où vient ce chiffre ?
* Quelle définition a été retenue ?
* Quelles données ont été écartées ?
* Quels calculs ont été appliqués ?
* Quelles hypothèses ont été ajoutées ?
* Quelle partie du raisonnement relève d’un constat, d’une interprétation ou d’un choix de valeur ?
* Que devient la conclusion si une hypothèse change ?
* Le résultat peut-il être reproduit à partir des mêmes données ?

La méthode vise ainsi à produire un **système de publication à chaîne de preuves exécutable**.

> Une proposition politique, institutionnelle ou économique ne doit pas seulement être lisible. Elle doit être inspectable.

---

## 1. Pourquoi cette méthode existe

### 1.1 Concevoir à partir des conditions réelles

Les systèmes étudiés dans Métabolisme partent de contraintes matérielles :

* nombre de logements vacants ;
* coût de rénovation d’un bâtiment ;
* niveau des loyers et des revenus ;
* ressources humaines disponibles ;
* capacités de financement ;
* surfaces agricoles ;
* rendements ;
* consommation d’énergie ;
* temps de travail ;
* taux de conversion ;
* pertes économiques ou matérielles ;
* capacités actuellement inutilisées.

Ces éléments ne doivent pas être employés comme de simples illustrations ajoutées après coup. Ils doivent participer à la construction même du système.

La démarche générale est la suivante :

```text
Observer les conditions réelles
        ↓
Identifier les contraintes et les ressources
        ↓
Mesurer les pertes, les immobilisations et les capacités inutilisées
        ↓
Formuler des hypothèses explicites
        ↓
Construire un modèle
        ↓
Tester plusieurs configurations
        ↓
Proposer un système
        ↓
Rendre son raisonnement inspectable
```

Le système proposé n’est donc pas conçu dans l’abstrait, puis décoré de statistiques. Il résulte d’une tentative d’organisation des ressources, des contraintes et des besoins observés.

### 1.2 Concevoir comme une optimisation sous contraintes

Une grande partie des sujets étudiés peut être comprise comme une **optimisation sous contraintes**.

Il existe :

* des besoins à satisfaire ;
* des ressources limitées ;
* des institutions existantes ;
* des coûts de coordination ;
* des règles juridiques ;
* des pertes ;
* des ressources sorties de l’usage ;
* des effets redistributifs ;
* des arbitrages entre plusieurs objectifs.

Le travail consiste à comprendre comment un autre agencement pourrait produire de meilleurs résultats sans ignorer ces contraintes.

Les « pertes » ne sont pas toujours des destructions physiques. Elles peuvent prendre plusieurs formes :

* un logement vacant ;
* un bâtiment inhabitable mais récupérable ;
* une terre abandonnée ;
* une capacité de production inutilisée ;
* un temps de travail absorbé par une activité de coordination redondante ;
* un capital immobilisé ;
* une dépense orientée vers la concurrence plutôt que vers le service rendu ;
* une donnée publique disponible mais inexploitable ;
* une compétence absente d’un circuit productif ;
* un surplus détruit faute de débouché.

L’un des objets de la conception consiste à chercher comment ces éléments peuvent être **remis en mouvement**, réintégrés dans l’usage ou réorientés vers la satisfaction d’un besoin.

### 1.3 Distinguer le réel, le calcul et le choix politique

Une proposition institutionnelle mélange souvent plusieurs plans :

1. des faits observables ;
2. des définitions statistiques ;
3. des transformations de données ;
4. des hypothèses ;
5. des interprétations ;
6. des objectifs ;
7. des valeurs ;
8. des choix de conception.

Ces plans doivent rester reliés, mais ne doivent pas être confondus.

Par exemple :

* le nombre de logements déclarés vacants est une mesure statistique ;
* la part de ces logements réellement mobilisable est une estimation ;
* le coût moyen de leur remise en état dépend d’hypothèses ;
* la décision d’en faire un parc de propriété d’usage est un choix institutionnel ;
* la priorité donnée au droit au logement est un choix normatif.

Les données peuvent contraindre une proposition, invalider certains ordres de grandeur ou révéler des effets inattendus. Elles ne déterminent pas à elles seules les valeurs ni la forme finale de l’institution.

La méthode ne cherche donc pas à faire passer un choix politique pour une conséquence mécanique des données. Elle cherche à montrer précisément :

* ce que les données établissent ;
* ce qu’elles rendent plausible ;
* ce qu’elles ne permettent pas de conclure ;
* les hypothèses ajoutées au raisonnement ;
* les valeurs qui orientent la conception ;
* les arbitrages qui restent politiques.

---

## 2. Le principe central : explorer librement, stabiliser explicitement

La recherche assistée par IA est puissante parce qu’elle permet d’explorer rapidement :

* des sources ;
* des concepts ;
* des jeux de données ;
* des relations possibles ;
* des méthodes de calcul ;
* des objections ;
* des scénarios ;
* des architectures institutionnelles.

Cette phase est nécessairement ouverte et partiellement non déterministe. Deux explorations successives peuvent conduire à des sources différentes, à des formulations différentes ou à des hypothèses nouvelles.

Cette souplesse est une force pendant la découverte. Elle devient un problème lorsqu’un résultat doit être publié.

La méthode sépare donc deux régimes.

## 2.1 Le régime exploratoire

Le régime exploratoire sert à découvrir, essayer et comprendre.

Il peut inclure :

* des conversations avec une IA ;
* des recherches web ;
* des essais de calcul ;
* des notebooks temporaires ;
* des graphiques exploratoires ;
* des rapprochements entre plusieurs jeux de données ;
* des hypothèses encore fragiles ;
* des pistes abandonnées ;
* des approximations clairement signalées.

Il est :

* rapide ;
* souple ;
* incomplet ;
* révisable ;
* potentiellement non déterministe.

Aucun résultat important ne doit être publié directement depuis ce régime.

## 2.2 Le régime stabilisé

Lorsqu’un élément devient constitutif du raisonnement, il doit être transformé en artefact explicite :

```text
Intuition ou suggestion
        ↓
Source identifiée
        ↓
Donnée récupérée et figée
        ↓
Définition documentée
        ↓
Transformation codée
        ↓
Hypothèse nommée
        ↓
Calcul testé
        ↓
Résultat reproduit
        ↓
Intégration dans la chaîne de preuves
```

Le régime stabilisé doit être :

* versionné ;
* rejouable ;
* testable ;
* lisible ;
* documenté ;
* déterministe autant que possible ;
* rattaché à une version précise des données et du code.

Le passage du régime exploratoire au régime stabilisé est le cœur de la méthode.

> L’IA explore un espace non déterministe. Le dépôt transforme les résultats retenus en système déterministe, explicite et vérifiable.

---

## 3. Une chaîne de raisonnement, pas une chaîne de causalité

La méthode ne prétend pas toujours établir une causalité scientifique.

Elle reconstruit une **chaîne de raisonnement** reliant :

* des sources ;
* des définitions ;
* des observations ;
* des calculs ;
* des hypothèses ;
* des résultats ;
* des interprétations ;
* des choix de conception.

Le terme **chaîne de preuves** désigne ici l’ensemble des éléments qui soutiennent une proposition et permettent de l’examiner.

Une chaîne type peut prendre cette forme :

```text
Source publique
      ↓
Définition statistique
      ↓
Extraction
      ↓
Nettoyage
      ↓
Transformation
      ↓
Indicateur
      ↓
Hypothèses de modèle
      ↓
Scénarios
      ↓
Interprétation
      ↓
Choix normatif
      ↓
Proposition de système
```

Certains liens sont computationnels. D’autres sont conceptuels ou normatifs. Leur nature doit être rendue visible.

---

## 4. Les statuts épistémiques

Chaque élément important doit être classé selon son statut.

| Code | Statut         | Description                                           |
| ---- | -------------- | ----------------------------------------------------- |
| `S`  | Source         | Document, API, base ou fichier d’origine              |
| `D`  | Définition     | Définition statistique, juridique ou conceptuelle     |
| `O`  | Observation    | Fait directement observé dans une source              |
| `T`  | Transformation | Opération appliquée aux données                       |
| `M`  | Mesure         | Indicateur directement calculé                        |
| `H`  | Hypothèse      | Valeur ou relation introduite dans le modèle          |
| `R`  | Résultat       | Sortie produite par un calcul ou un scénario          |
| `I`  | Interprétation | Signification attribuée aux observations ou résultats |
| `V`  | Valeur         | Objectif normatif ou principe défendu                 |
| `C`  | Choix          | Décision de conception institutionnelle ou économique |
| `P`  | Proposition    | Système, mécanisme ou règle finalement proposé        |
| `L`  | Limite         | Incertitude, manque de données ou restriction connue  |

Exemple :

```text
S-01  Base INSEE sur les logements
D-01  Définition statistique du logement vacant
O-01  Nombre de logements classés vacants
T-01  Exclusion des vacances frictionnelles
H-01  Part estimée des logements techniquement récupérables
R-01  Fourchette de logements potentiellement mobilisables
I-01  Existence d’un parc important sorti de l’usage
V-01  Priorité donnée à l’accès durable au logement
C-01  Intégration progressive dans un parc collectif
P-01  Sécurité sociale du logement
L-01  Absence de données homogènes sur l’état détaillé des logements
```

Cette classification empêche de présenter une hypothèse comme une donnée ou un choix normatif comme une conclusion mathématique.

---

## 5. Architecture générale du dépôt

Le dépôt Git constitue la source de vérité du projet.

Une structure type peut être utilisée :

```text
project/
├── README.md
├── EVIDENCE.md
├── pyproject.toml
├── uv.lock
│
├── sources/
│   ├── sources.yaml
│   └── definitions.yaml
│
├── data/
│   ├── raw/
│   ├── intermediate/
│   ├── processed/
│   └── external/
│
├── src/
│   ├── acquisition/
│   ├── transformations/
│   ├── indicators/
│   ├── models/
│   ├── scenarios/
│   └── publication/
│
├── tests/
│   ├── unit/
│   ├── integration/
│   └── regression/
│
├── notebooks/
│   ├── exploration/
│   └── verification/
│
├── evidence/
│   ├── claims.yaml
│   ├── graphs/
│   └── reports/
│
├── articles/
│   └── ...
│
├── scripts/
│   ├── fetch_data.py
│   ├── reproduce.py
│   └── validate.py
│
└── .github/
    └── workflows/
        └── reproduce.yml
```

Cette structure peut être simplifiée pour un petit projet. La séparation logique doit néanmoins être conservée.

---

## 6. Rôle de chaque outil

## 6.1 Git : versionner le raisonnement

Git versionne :

* le code ;
* les documents ;
* les hypothèses ;
* les métadonnées des sources ;
* les tests ;
* les paramètres ;
* les résultats légers ;
* l’évolution du raisonnement.

Chaque publication doit pouvoir être rattachée à un commit ou à un tag.

Exemple :

```text
article-securite-sociale-logement-v1.0
commit: 82ca41f
```

Une modification d’hypothèse, de source ou de calcul devient ainsi visible dans l’historique.

Git ne sert pas seulement à conserver du code. Il conserve l’évolution de la chaîne de preuve.

## 6.2 Python : stabiliser les transformations

Python sert à implémenter les opérations qui doivent être :

* explicites ;
* répétables ;
* testées ;
* réutilisables ;
* indépendantes d’une interface graphique.

Les transformations importantes ne doivent pas rester enfermées dans une cellule de notebook.

Exemple :

```python
def estimate_mobilisable_housing(
    vacant_housing: int,
    frictional_vacancy_rate: float,
    unrecoverable_rate: float,
) -> int:
    excluded_rate = frictional_vacancy_rate + unrecoverable_rate

    if not 0 <= excluded_rate <= 1:
        raise ValueError("The combined exclusion rate must be between 0 and 1.")

    return round(vacant_housing * (1 - excluded_rate))
```

Cette fonction peut être :

* testée ;
* appelée depuis un notebook ;
* utilisée dans plusieurs scénarios ;
* intégrée à un rapport ;
* relue indépendamment de la narration.

## 6.3 JupyterLab : explorer et inspecter

JupyterLab est l’environnement privilégié pour :

* découvrir la structure d’un jeu de données ;
* afficher les valeurs intermédiaires ;
* tester une transformation ;
* comparer plusieurs méthodes ;
* produire des graphiques exploratoires ;
* documenter une séquence de calcul ;
* comprendre une anomalie ;
* examiner les sorties d’un modèle.

Il permet de réunir dans un même espace :

* du texte ;
* du code ;
* des résultats ;
* des tableaux ;
* des graphiques ;
* des formules.

Deux catégories de notebooks doivent être séparées.

### Notebooks d’exploration

Ils servent de laboratoire.

Ils peuvent contenir :

* des essais ;
* des détours ;
* des cellules temporaires ;
* des pistes abandonnées ;
* des commentaires provisoires.

Ils ne constituent pas une publication.

### Notebooks de vérification

Ils servent de visite guidée d’un calcul stabilisé.

Ils doivent :

* être exécutables de haut en bas ;
* importer le code depuis `src/` ;
* afficher les données utiles ;
* montrer les valeurs intermédiaires ;
* expliciter les hypothèses ;
* relier les résultats à leurs identifiants ;
* éviter toute étape manuelle invisible.

## 6.4 Jupytext : rendre les notebooks lisibles dans Git

Les fichiers `.ipynb` sont des documents JSON. Ils sont pratiques dans Jupyter, mais difficiles à relire dans un diff Git.

Jupytext permet d’associer un notebook à une représentation textuelle, généralement :

* un fichier Python ;
* un fichier Markdown ;
* un fichier MyST Markdown.

Le notebook peut continuer à être utilisé dans JupyterLab, tandis que sa version textuelle devient :

* lisible dans Git ;
* comparable entre deux commits ;
* facile à commenter ;
* simple à modifier par un agent.

Pour les notebooks importants, la version textuelle doit être considérée comme la représentation principale.

## 6.5 Quarto ou MyST : publier des documents exécutables

Quarto ou MyST Markdown servent à produire des documents de preuve lisibles et publiables.

Ils permettent de combiner :

* une narration ;
* du code ;
* des tableaux ;
* des formules ;
* des graphiques ;
* des références croisées ;
* des résultats calculés.

Un document peut ensuite être rendu en :

* HTML ;
* PDF ;
* page web ;
* livre ou documentation structurée.

Le document de preuve n’est pas seulement un export du notebook. Il constitue une présentation ordonnée du raisonnement.

Pour un usage général, l’organisation recommandée est :

```text
JupyterLab       → exploration
Python           → calculs stabilisés
Quarto ou MyST   → document de preuve publiable
Article Markdown → proposition destinée au lecteur
```

## 6.6 `uv` : figer l’environnement Python

La reproductibilité dépend aussi des versions de Python et des bibliothèques.

Le fichier `uv.lock` permet de verrouiller les dépendances nécessaires à l’exécution.

Le dépôt doit contenir :

* la version de Python attendue ;
* les dépendances directes ;
* les versions résolues ;
* les commandes d’installation ;
* les commandes de reproduction.

Un calcul ne doit pas dépendre implicitement de l’environnement local d’une personne.

## 6.7 Tests : vérifier les calculs

Les tests servent à vérifier plusieurs propriétés.

### Tests unitaires

Ils vérifient une transformation isolée.

```python
def test_estimate_mobilisable_housing():
    assert estimate_mobilisable_housing(
        vacant_housing=1_000,
        frictional_vacancy_rate=0.10,
        unrecoverable_rate=0.20,
    ) == 700
```

### Tests d’intégration

Ils vérifient qu’une chaîne complète fonctionne :

```text
donnée brute
→ nettoyage
→ transformation
→ indicateur
→ résultat
```

### Tests de régression

Ils signalent qu’un résultat publié a changé.

Un changement peut être légitime, mais il doit être expliqué :

* nouvelle source ;
* correction d’une erreur ;
* hypothèse modifiée ;
* amélioration du modèle ;
* changement de définition.

### Tests de propriétés

Ils vérifient des invariants :

* un taux reste compris entre 0 et 1 ;
* une quantité ne devient pas négative ;
* une somme de catégories correspond au total ;
* une augmentation de coût ne réduit pas artificiellement la dépense totale ;
* une population filtrée ne dépasse pas la population initiale.

## 6.8 Intégration continue : rejouer automatiquement

La CI doit exécuter le projet dans un environnement neuf.

Une pipeline type :

```text
1. Installer les dépendances verrouillées
2. Vérifier les données et leurs empreintes
3. Exécuter les tests
4. Reconstruire les données intermédiaires
5. Recalculer les indicateurs
6. Rejouer les scénarios
7. Exécuter les notebooks de vérification
8. Générer les documents de preuve
9. Signaler toute différence non documentée
```

L’objectif est de pouvoir exécuter une commande unique :

```bash
uv run reproduce
```

Cette commande doit reconstruire les résultats publiés à partir des données brutes disponibles.

## 6.9 DVC ou stockage externe : gérer les données volumineuses

Git suffit pour de petits fichiers.

Lorsque les données deviennent trop volumineuses, un outil comme DVC peut être ajouté pour :

* versionner les références aux données ;
* stocker les fichiers hors du dépôt Git ;
* décrire les étapes d’un pipeline ;
* reconstruire uniquement les étapes affectées ;
* partager des jeux de données entre plusieurs personnes.

DVC est optionnel. Il ne doit être introduit que lorsque la taille ou la complexité le justifie.

---

## 7. Le registre des sources

Chaque source utilisée doit être enregistrée dans un fichier structuré.

Exemple `sources/sources.yaml` :

```yaml
- id: S-01
  publisher: INSEE
  title: Parc de logements par catégorie
  dataset_id: identifiant-du-jeu
  source_url: https://...
  publication_date: 2025-06-12
  retrieved_at: 2026-08-01
  local_file: data/raw/insee-logements-2023.csv
  checksum: sha256:...
  license: Licence Ouverte 2.0
  geographic_scope: France
  temporal_scope: 2023
  notes: >
    La catégorie statistique « logement vacant » ne signifie pas
    que le logement est immédiatement mobilisable.
```

Les informations minimales sont :

* l’organisme ;
* le titre ;
* l’URL ;
* la date de publication ;
* la date de récupération ;
* la période couverte ;
* le périmètre géographique ;
* la licence ;
* le fichier local ;
* l’empreinte du fichier ;
* les limites connues.

Une URL seule n’est pas suffisante. Une ressource distante peut être modifiée, remplacée ou supprimée.

## 7.1 Données figées et données récupérables

Deux stratégies sont possibles.

### Conserver la donnée brute

À privilégier pour les petits fichiers publics.

Avantages :

* reproduction immédiate ;
* protection contre la disparition de la source ;
* identification exacte de la version utilisée.

### Conserver un script de récupération

À utiliser pour les API ou les fichiers volumineux.

Le script doit :

* identifier précisément la ressource ;
* enregistrer la date de récupération ;
* vérifier le schéma ;
* produire une empreinte ;
* échouer clairement si la source a changé.

Dans les deux cas, le projet doit permettre de savoir quelle version exacte de la donnée a servi au calcul publié.

---

## 8. Les définitions comme données de première classe

Une grande partie des erreurs vient moins des calculs que des définitions.

Exemples :

* qu’est-ce qu’un logement vacant ?
* qu’est-ce qu’un emploi ?
* qu’est-ce qu’un ménage pauvre ?
* comment une entreprise active est-elle comptée ?
* qu’est-ce qu’une exploitation agricole ?
* comment définit-on une passoire thermique ?
* qu’est-ce qu’un coût complet ?
* qu’est-ce qu’un utilisateur actif ?

Les définitions doivent être documentées et identifiées.

Exemple `definitions.yaml` :

```yaml
- id: D-01
  term: logement vacant
  source: S-01
  definition: >
    Logement inoccupé correspondant aux catégories retenues
    par la définition statistique de la source.
  caveats:
    - Peut inclure une vacance temporaire.
    - Ne renseigne pas toujours l’état du bâti.
    - Ne signifie pas une disponibilité juridique immédiate.
```

Lorsqu’une définition change, les résultats concernés doivent pouvoir être identifiés.

---

## 9. Les hypothèses comme paramètres explicites

Une hypothèse ne doit pas être enfouie dans une formule.

Elle doit posséder :

* un identifiant ;
* une description ;
* une valeur centrale ;
* une unité ;
* une justification ;
* une plage plausible ;
* un niveau de confiance ;
* les résultats qu’elle affecte.

Exemple :

```yaml
- id: H-03
  name: frictional_vacancy_rate
  description: Part de la vacance correspondant à une rotation normale
  central_value: 0.10
  plausible_range: [0.07, 0.15]
  unit: ratio
  confidence: medium
  justification:
    - S-04
    - I-02
  affects:
    - R-01
    - R-03
```

Les valeurs centrales ne doivent jamais masquer l’incertitude.

Lorsque c’est pertinent, le rapport doit afficher :

* un scénario bas ;
* un scénario central ;
* un scénario haut ;
* une analyse de sensibilité ;
* éventuellement une distribution de résultats.

---

## 10. Le graphe de preuves

La chaîne de preuves peut être représentée comme un graphe.

Chaque nœud possède un identifiant. Chaque relation indique comment un élément dépend d’un autre.

Exemple :

```text
S-01 ──► O-01 ──► T-01 ──► M-01
                               │
S-04 ──► H-03 ─────────────────┤
                               ▼
                             R-01
                               │
V-01 ──────────────────────────┤
                               ▼
                             C-01
                               │
                               ▼
                             P-01
```

Le graphe permet de répondre à plusieurs questions :

* Quelles sources soutiennent ce résultat ?
* Quels résultats dépendent d’une hypothèse donnée ?
* Quelles propositions seraient affectées par une correction de source ?
* Une conclusion repose-t-elle sur une seule donnée fragile ?
* Une valeur normative est-elle présentée à tort comme un résultat empirique ?
* Existe-t-il des étapes implicites dans le raisonnement ?

Une première version peut être gérée dans un simple fichier YAML.

Exemple `evidence/claims.yaml` :

```yaml
- id: R-01
  type: result
  title: Estimation du parc mobilisable
  depends_on:
    - O-01
    - T-01
    - H-03
    - H-04
  produced_by: src/models/housing.py
  output: data/processed/mobilisable_housing.json
  limitations:
    - L-01
    - L-03
```

Il n’est pas nécessaire de développer immédiatement une application de graphe. La priorité est de rendre les relations explicites et lisibles par une machine.

---

## 11. Structure d’un document de preuve

Chaque étude importante doit disposer d’un document de preuve distinct de l’article public.

Ce document peut suivre la structure suivante.

### 11.1 Question étudiée

* Quel problème cherche-t-on à comprendre ?
* Quelle décision ou proposition ce travail doit-il éclairer ?
* Quel est le périmètre ?

### 11.2 Définitions

* Quels termes sont utilisés ?
* Quelles définitions officielles sont retenues ?
* Quelles ambiguïtés persistent ?

### 11.3 Sources

* Quelles données sont utilisées ?
* Quelle est leur date ?
* Quel est leur périmètre ?
* Quelles sont leurs limites ?

### 11.4 Transformations

* Quels filtres sont appliqués ?
* Quelles catégories sont exclues ?
* Comment les données sont-elles agrégées ?
* Existe-t-il des opérations manuelles ?

### 11.5 Hypothèses

* Quelles valeurs sont introduites ?
* Pourquoi ?
* Quelle est leur plage plausible ?
* Quel est leur niveau de confiance ?

### 11.6 Résultats

* Quels résultats sont directement calculés ?
* Quels scénarios sont comparés ?
* Quels intervalles sont obtenus ?

### 11.7 Sensibilité

* Quelles hypothèses influencent le plus le résultat ?
* À partir de quel seuil la conclusion change-t-elle ?
* Quels paramètres sont secondaires ?

### 11.8 Interprétation

* Que montrent réellement les résultats ?
* Que ne montrent-ils pas ?
* Quelles inférences sont prudentes ?
* Quelles autres explications restent possibles ?

### 11.9 Implications de conception

* Quelles contraintes le système doit-il respecter ?
* Quelles ressources peut-il mobiliser ?
* Quels mécanismes deviennent plausibles ?
* Quels arbitrages restent politiques ?

### 11.10 Limites et objections

* Quelles données manquent ?
* Quelles hypothèses sont fragiles ?
* Quelles critiques ont été examinées ?
* Quelles validations supplémentaires sont nécessaires ?

### 11.11 Reproduction

* Quelle commande exécuter ?
* Quel commit correspond au rapport ?
* Quels fichiers sont produits ?
* Quel environnement est nécessaire ?

---

## 12. Relation entre le document de preuve et l’article

L’article et le document de preuve ont des fonctions différentes.

### L’article

Il doit :

* exposer le problème ;
* rendre le raisonnement accessible ;
* défendre une proposition ;
* expliquer les principaux mécanismes ;
* citer les résultats importants ;
* rendre visibles les incertitudes décisives.

Il ne doit pas devenir un journal exhaustif de calcul.

### Le document de preuve

Il doit :

* montrer les sources ;
* afficher les définitions ;
* décrire les transformations ;
* expliciter les hypothèses ;
* produire les résultats ;
* documenter les limites ;
* permettre la reproduction.

L’article doit pointer vers une version précise du document de preuve.

Exemple :

```markdown
L’estimation présentée ici repose sur le résultat
[R-01 — Parc de logements potentiellement mobilisable](...),
calculé à partir du document de preuve versionné avec l’article.
```

La publication doit idéalement fournir :

1. l’article ;
2. le document de preuve rendu en HTML ;
3. le dépôt Git ;
4. le commit ou tag correspondant ;
5. les données publiques redistribuables ;
6. les instructions de reproduction.

---

## 13. La place de l’IA

L’IA intervient dans presque toutes les phases, mais elle ne constitue jamais la source finale d’une affirmation factuelle.

## 13.1 Recherche

L’IA peut :

* proposer des organismes susceptibles de publier une donnée ;
* trouver des jeux de données ;
* comparer plusieurs sources ;
* suggérer des mots-clés ;
* repérer des définitions ;
* identifier des travaux contradictoires ;
* signaler des données manquantes.

Toute source retenue doit être enregistrée directement, sans dépendre de la mémoire de la conversation.

## 13.2 Exploration

L’IA peut :

* écrire des scripts temporaires ;
* inspecter un schéma ;
* proposer un nettoyage ;
* produire des graphiques ;
* détecter des anomalies ;
* rapprocher plusieurs fichiers ;
* suggérer des scénarios ;
* aider à interpréter les résultats.

Ces productions restent provisoires tant qu’elles n’ont pas été stabilisées.

## 13.3 Formalisation

L’IA peut :

* extraire les transformations d’un notebook ;
* les convertir en fonctions ;
* proposer des tests ;
* générer les métadonnées des hypothèses ;
* construire le graphe de dépendance ;
* documenter le code ;
* préparer un rapport Quarto.

Chaque élément doit être relu et exécuté.

## 13.4 Critique

L’IA doit également être employée comme contradicteur.

Elle peut chercher :

* une définition alternative ;
* un biais de sélection ;
* un double comptage ;
* une confusion entre stock et flux ;
* une hypothèse implicite ;
* une causalité non démontrée ;
* une donnée plus récente ;
* un ordre de grandeur incohérent ;
* une conséquence non prise en compte ;
* un scénario dans lequel la proposition échoue.

Une étude n’est pas considérée comme prête uniquement parce qu’une IA a réussi à produire un raisonnement cohérent. Elle doit aussi avoir été soumise à une tentative explicite de réfutation.

## 13.5 Publication

L’IA peut aider à rédiger l’article et le document de preuve, mais le texte publié doit être dérivé des artefacts stabilisés.

Elle ne doit pas :

* inventer un chiffre de transition ;
* résumer une source non enregistrée ;
* modifier silencieusement une hypothèse ;
* recalculer mentalement un résultat déjà présent dans le dépôt ;
* produire un ordre de grandeur non traçable ;
* transformer une corrélation en causalité ;
* présenter une valeur comme un fait.

## 13.6 Principe de confiance

Le principe général est le suivant :

> Ne pas demander au lecteur de faire confiance à l’IA. Lui donner les moyens d’inspecter ce que l’IA a contribué à construire.

---

## 14. Workflow complet

## Étape 1 — Formuler la question

Définir :

* le problème ;
* le périmètre ;
* la décision à éclairer ;
* les principales inconnues ;
* les unités pertinentes ;
* les premières hypothèses.

Sortie :

```text
research-question.md
```

## Étape 2 — Cartographier les besoins de preuve

Lister les affirmations nécessaires au raisonnement.

Exemple :

```text
Pour estimer la faisabilité d’un parc collectif de logements, il faut connaître :
- le nombre de logements vacants ;
- leur répartition ;
- leur état ;
- le coût de rénovation ;
- les capacités de financement ;
- la durée d’amortissement ;
- les revenus des ménages ;
- les coûts de gestion ;
- les effets sur le parc privé.
```

Chaque besoin devient une entrée provisoire du graphe.

## Étape 3 — Explorer avec l’IA

Rechercher :

* les sources publiques ;
* les définitions ;
* les études existantes ;
* les controverses ;
* les ordres de grandeur ;
* les données manquantes.

Conserver un journal succinct des pistes retenues et abandonnées.

## Étape 4 — Enregistrer les sources

Pour chaque source retenue :

* créer un identifiant ;
* enregistrer les métadonnées ;
* télécharger ou préparer la récupération ;
* calculer une empreinte ;
* documenter les limites.

## Étape 5 — Explorer les données

Utiliser JupyterLab pour :

* comprendre le schéma ;
* inspecter les valeurs ;
* tester les filtres ;
* repérer les ruptures ;
* produire les premiers indicateurs.

Le notebook d’exploration peut rester imparfait.

## Étape 6 — Stabiliser les transformations

Extraire du notebook :

* les règles de nettoyage ;
* les fonctions ;
* les agrégations ;
* les calculs ;
* les paramètres.

Les déplacer dans `src/`.

## Étape 7 — Ajouter les tests

Tester :

* les cas simples ;
* les valeurs limites ;
* les invariants ;
* les erreurs attendues ;
* les résultats déjà publiés.

## Étape 8 — Formaliser les hypothèses

Créer des paramètres identifiés.

Pour chaque hypothèse :

* valeur centrale ;
* plage plausible ;
* justification ;
* niveau de confiance ;
* résultats affectés.

## Étape 9 — Construire les scénarios

Au minimum :

* scénario prudent ;
* scénario central ;
* scénario favorable.

Lorsque cela est utile :

* analyse de sensibilité ;
* simulation ;
* propagation des incertitudes ;
* comparaison de politiques alternatives.

## Étape 10 — Produire le notebook de vérification

Le notebook doit :

* s’exécuter dans l’ordre ;
* importer le code stabilisé ;
* afficher les étapes utiles ;
* montrer les sorties ;
* référencer les identifiants ;
* signaler les limites.

## Étape 11 — Produire le document de preuve

Le rapport Quarto ou MyST présente :

* la question ;
* les sources ;
* les définitions ;
* les transformations ;
* les hypothèses ;
* les résultats ;
* la sensibilité ;
* les limites ;
* les implications.

## Étape 12 — Chercher les objections

Conduire une revue contradictoire :

* sources alternatives ;
* définitions concurrentes ;
* scénarios d’échec ;
* effets de bord ;
* biais ;
* hypothèses fragiles.

Les objections sérieuses doivent être intégrées au document.

## Étape 13 — Concevoir le système

À partir des résultats :

* identifier les contraintes incontournables ;
* comprendre les ressources mobilisables ;
* préciser les objectifs normatifs ;
* comparer plusieurs mécanismes ;
* expliciter les arbitrages ;
* proposer une architecture.

Le système proposé doit rester relié aux éléments qui justifient sa forme.

## Étape 14 — Rédiger l’article

L’article expose :

* le problème ;
* l’intuition centrale ;
* les ordres de grandeur ;
* les distinctions importantes ;
* le système proposé ;
* ses limites ;
* les liens vers la preuve.

## Étape 15 — Reproduire depuis zéro

Avant publication :

```bash
git clean -xfd
uv sync --locked
uv run reproduce
uv run test
uv run validate
```

La reconstruction doit aboutir aux résultats annoncés.

## Étape 16 — Publier une version identifiée

Créer un tag ou une release.

Exemple :

```text
housing-social-security-v1.0
```

La publication indique le commit correspondant.

---

## 15. Règles de publication

Une affirmation quantitative importante ne peut être publiée que si elle possède :

* une source ou un calcul identifié ;
* une unité ;
* un périmètre temporel ;
* un périmètre géographique ;
* une définition ;
* un statut épistémique ;
* une version reproductible ;
* une limite connue lorsque nécessaire.

Une proposition ne doit pas être présentée comme « prouvée » par les données lorsque les données ne font que :

* fixer un ordre de grandeur ;
* rendre un mécanisme plausible ;
* exclure certaines configurations ;
* révéler une contrainte ;
* soutenir une interprétation.

Toute estimation doit indiquer si elle est :

* observée ;
* calculée ;
* extrapolée ;
* simulée ;
* hypothétique.

Toute donnée sensible à une hypothèse importante doit être accompagnée d’une fourchette ou d’une analyse de sensibilité.

---

## 16. Critères de qualité

Une étude est considérée comme publiable lorsque les questions suivantes reçoivent une réponse satisfaisante.

### Sources

* Les sources originales sont-elles identifiées ?
* Les versions utilisées sont-elles conservées ou récupérables ?
* Les dates et périmètres sont-ils visibles ?
* Les limites des sources sont-elles documentées ?

### Calculs

* Les transformations sont-elles codées ?
* Les calculs peuvent-ils être rejoués ?
* Les unités sont-elles cohérentes ?
* Les cas limites sont-ils testés ?
* Les valeurs intermédiaires importantes sont-elles accessibles ?

### Hypothèses

* Les hypothèses sont-elles nommées ?
* Leur justification est-elle visible ?
* Leur plage plausible est-elle indiquée ?
* Leur influence sur le résultat est-elle connue ?

### Raisonnement

* Les faits sont-ils distingués des interprétations ?
* Les interprétations sont-elles distinguées des valeurs ?
* Les valeurs sont-elles distinguées des choix de conception ?
* Les étapes implicites ont-elles été rendues visibles ?
* Les objections sérieuses ont-elles été examinées ?

### Publication

* L’article pointe-t-il vers le document de preuve ?
* La version publiée est-elle rattachée à un commit ?
* Le projet peut-il être reproduit dans un environnement neuf ?
* Une modification future pourra-t-elle être comparée à cette version ?

---

## 17. Usage pour Métabolisme

Dans Métabolisme, cette méthode sert à concevoir des institutions à partir :

* des besoins matériels ;
* des ressources disponibles ;
* des flux existants ;
* des pertes ;
* des capacités inutilisées ;
* des effets de système ;
* des valeurs défendues.

Elle est particulièrement adaptée à des sujets comme :

* la Sécurité sociale du logement ;
* la propriété d’usage ;
* la rénovation thermique ;
* le financement collectif ;
* la Sécurité sociale de l’environnement ;
* les mécanismes d’assurance ;
* l’agriculture ;
* la gestion des communs ;
* les formes contributives d’entreprise ;
* la redistribution de la valeur ;
* l’organisation du travail.

Elle permet d’éviter deux écueils.

### L’invocation politique

Proposer un objectif sans décrire les attaches institutionnelles, les flux économiques et les mécanismes qui peuvent le faire durer.

### Le technicisme sans valeurs

Construire un modèle apparemment objectif qui dissimule les arbitrages normatifs ayant déterminé ses objectifs.

La chaîne de preuves doit rendre visibles à la fois :

* la contrainte du réel ;
* le travail de modélisation ;
* le choix politique.

---

## 18. Usage pour la recherche entrepreneuriale

La même méthode peut être appliquée à l’étude d’un marché ou à la conception d’un produit.

Une recherche business peut inclure :

* taille de marché ;
* nombre d’acteurs ;
* prix pratiqués ;
* coûts ;
* fréquences d’usage ;
* volumes ;
* taux de conversion ;
* comportements ;
* contraintes réglementaires ;
* temps perdu ;
* capacités inutilisées ;
* budget disponible ;
* solutions de substitution.

Le raisonnement peut suivre cette chaîne :

```text
Besoin observé
      ↓
Population concernée
      ↓
Solutions existantes
      ↓
Coûts et frictions
      ↓
Pertes ou capacités inutilisées
      ↓
Hypothèses de comportement
      ↓
Modèle économique
      ↓
Scénarios
      ↓
Proposition de produit
```

La chaîne de preuves aide à distinguer :

* une donnée de marché ;
* une estimation ;
* une hypothèse de conversion ;
* une préférence produit ;
* une décision stratégique.

Elle permet également de mettre à jour le modèle lorsqu’une hypothèse est invalidée, sans reconstruire tout le raisonnement depuis zéro.

---

## 19. Un principe de conception plus général

Cette méthode repose sur une intuition plus large :

> Concevoir un système consiste souvent à comprendre comment des ressources, des capacités ou des valeurs sorties de l’usage peuvent être réintroduites dans un mouvement utile, sous des contraintes explicites.

Le logement vacant est un exemple visible. Le principe peut s’appliquer à :

* du foncier ;
* du capital ;
* du temps ;
* des connaissances ;
* des infrastructures ;
* des surplus ;
* des capacités productives ;
* des flux financiers ;
* des données ;
* des compétences.

La chaîne de preuves ne sert pas seulement à justifier une proposition après sa conception. Elle aide à voir le système qui pourrait être conçu.

Elle transforme les données en matériau de raisonnement, sans réduire le raisonnement aux données.

---

## 20. Version minimale à mettre en œuvre

La première version ne doit pas chercher à construire une plateforme générale.

Pour une étude initiale, le socle minimal est :

```text
README.md
EVIDENCE.md
sources/sources.yaml
data/raw/
src/calculations.py
tests/test_calculations.py
notebooks/verification.md
evidence/report.qmd
articles/article.md
pyproject.toml
uv.lock
```

Commandes minimales :

```bash
uv sync --locked
uv run test
uv run reproduce
uv run validate
```

La première étude doit servir à éprouver la méthode.

Un sujet adapté serait une estimation liée à la Sécurité sociale du logement :

* parc vacant mobilisable ;
* coût de rénovation ;
* rythme d’acquisition ;
* financement ;
* cotisations ;
* amortissement ;
* scénarios de montée en charge.

Les abstractions supplémentaires ne doivent être introduites qu’après avoir rencontré un besoin réel dans plusieurs études.

---

## 21. Règles destinées aux agents

Tout agent travaillant dans ce dépôt doit respecter les règles suivantes.

1. Ne pas présenter une information trouvée par une IA comme une source.
2. Enregistrer la source originale de toute donnée retenue.
3. Ne pas modifier silencieusement une hypothèse.
4. Ne pas laisser un calcul important uniquement dans une conversation.
5. Ne pas laisser une transformation importante uniquement dans un notebook exploratoire.
6. Déplacer les calculs stabilisés dans du code testé.
7. Identifier clairement les estimations et extrapolations.
8. Distinguer faits, hypothèses, interprétations, valeurs et choix.
9. Documenter les données écartées et la raison de leur exclusion.
10. Conserver les unités et périmètres à chaque étape.
11. Produire des fourchettes lorsque l’incertitude est structurante.
12. Chercher activement les objections et données contradictoires.
13. Relier chaque résultat publié à ses dépendances.
14. Exécuter la chaîne complète avant publication.
15. Ne pas faire confiance à l’état mémoire d’un notebook.
16. Ne pas dépendre d’une opération manuelle non documentée.
17. Rattacher chaque publication à une version Git précise.
18. Préférer une limite explicite à une précision artificielle.
19. Préférer un raisonnement incomplet mais inspectable à un résultat complet impossible à vérifier.
20. Considérer la critique comme une fonction normale du système, non comme une attaque extérieure.

---

## 22. Définition finale

Une **chaîne de preuves exécutable** est un système de publication dans lequel :

* les sources sont identifiées ;
* les définitions sont explicites ;
* les données sont versionnées ou récupérables ;
* les transformations sont codées ;
* les hypothèses sont nommées ;
* les calculs sont testés ;
* les résultats sont reproductibles ;
* les incertitudes sont visibles ;
* les interprétations sont distinguées des faits ;
* les valeurs sont distinguées des mesures ;
* les choix de conception sont assumés ;
* l’article est relié à une version précise du raisonnement.

Son but n’est pas de supprimer le jugement humain ni le conflit politique.

Son but est de rendre visible l’endroit exact où commencent :

* l’incertitude ;
* l’interprétation ;
* le choix ;
* le désaccord.

La proposition devient alors critiquable sans devenir opaque, révisable sans perdre son histoire, et contestable sans que toute la discussion doive repartir de zéro.

> Le résultat attendu n’est pas une politique prétendument imposée par les chiffres. C’est une proposition dont les attaches au réel, les calculs, les hypothèses et les valeurs peuvent être examinés séparément — puis discutés ensemble.

