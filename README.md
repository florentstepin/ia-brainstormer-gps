# 🧭 IA-BrainStormer GPS

Application Streamlit implémentant le système GPS complet de la méthodologie IA-BrainStormer par Florent.

**Mode BYOK (Bring Your Own Key)** : L'application fonctionne avec votre propre clé API OpenAI pour une sécurité et un contrôle des coûts optimaux.

## 🎯 Fonctionnalités

### Phase 0 : Crash Test D.U.R.
- Validation de l'idée selon les critères **Douloureux, Urgent, Reconnu**
- Identification automatique du **maillon faible**
- Conseil spécifique de l'Architecte pour renforcer le point faible
- **Veto de l'Architecte** : zone éditable pour reformuler l'idée

### Phase G : Génération
- Génération de **10 angles stratégiques** avec l'Explorateur de Perspective
- Chaque angle contient :
  - Titre accrocheur
  - Cible précise (niche ultra-spécifique)
  - Opportunité (mécanisme de différenciation et monopole)
- Sélection interactive de 3 angles favoris

### Phase P : Priorisation
- Évaluation selon la **Matrice de Conviction** avec pondération stricte :
  - Douleur Client : 40%
  - Unicité de l'Angle : 30%
  - Alignement/Passion : 30%
- Tableau comparatif avec scores pondérés
- Recommandation automatique de l'angle optimal
- **Veto de l'Architecte** : zone éditable pour modifier l'angle

### Phase S : Séquençage
- Plan d'action de **7 jours** en **backcasting**
- Méthode : partir du résultat J+7 et remonter jusqu'à J+1
- Actions concrètes et réalisables pour une personne seule
- Export du plan complet en JSON

## 🚀 Installation

### Prérequis
- Python 3.8 ou supérieur
- Une clé API OpenAI (obtenue sur [platform.openai.com/api-keys](https://platform.openai.com/api-keys))

### Installation des dépendances

```bash
pip install -r requirements.txt
```

## 🎮 Utilisation

### Lancer l'application

```bash
streamlit run app.py
```

L'application s'ouvrira automatiquement dans votre navigateur à l'adresse `http://localhost:8501`

### Configuration (Mode BYOK)

1. **Obtenir votre clé API OpenAI** :
   - Allez sur [platform.openai.com/api-keys](https://platform.openai.com/api-keys)
   - Connectez-vous ou créez un compte
   - Cliquez sur "Create new secret key"
   - Copiez la clé (elle commence par `sk-...`)

2. **Configurer l'application** :
   - Dans la barre latérale gauche, collez votre clé API
   - Choisissez le modèle (recommandé : **gpt-4o**)

3. **Sécurité** :
   - 🔒 Votre clé n'est **jamais enregistrée** sur un serveur
   - Elle reste dans votre navigateur pendant la session
   - Elle est utilisée uniquement pour vos appels API

### Workflow

1. **Crash Test** : Décrivez votre idée et lancez le test D.U.R.
2. **Génération** : Explorez les 10 angles générés et sélectionnez-en 3
3. **Priorisation** : Analysez la matrice de conviction et choisissez votre angle
4. **Séquençage** : Obtenez votre plan d'action de 7 jours
5. **Export** : Téléchargez votre plan complet en JSON

## 💰 Estimation des Coûts

**Coût approximatif par session complète :**
- **gpt-4o** : ~0.05$ (Recommandé pour la meilleure qualité)
- **gpt-4-turbo** : ~0.10$
- **gpt-3.5-turbo** : ~0.01$ (Moins précis)

Une session complète = Crash Test + 10 angles + Priorisation + Plan de 7 jours

## 📁 Structure du projet

```
ia-brainstormer-gps/
├── app.py                      # Application Streamlit principale (Mode BYOK)
├── requirements.txt            # Dépendances Python
├── README.md                   # Documentation
├── prompts/
│   └── system_prompts.py      # Prompts système pour chaque phase
└── utils/
    ├── openai_helper.py       # Gestion des appels API OpenAI
    └── gps_system.py          # Logique métier du système GPS
```

## 🔑 Spécificités de la Méthodologie

### 1. Crash Test D.U.R. Intelligent
- Identification automatique du critère le plus faible (D, U ou R)
- Conseil spécifique pour transformer le point faible en force

### 2. Matrice de Conviction (Phase P)
- Pondération stricte : Douleur (40%) + Unicité (30%) + Alignement (30%)
- Interdiction de prioriser uniquement sur la facilité financière

### 3. Veto de l'Architecte
- Entre chaque phase, l'utilisateur peut modifier le résultat de l'IA
- L'IA prend ensuite la version modifiée pour l'étape suivante
- Principe : l'IA propose, l'Architecte dispose

### 4. Séquençage Backcasting
- Le plan part de J+7 (résultat obtenu) et remonte jusqu'à J+1
- Méthode inverse pour garantir la cohérence du plan

## 🛠️ Technologies

- **Streamlit** : Interface utilisateur interactive
- **OpenAI API** : Génération des analyses et recommandations (Mode BYOK)
- **Python 3.8+** : Langage de programmation

## 🌐 Déploiement Public

L'application est conçue pour être déployée publiquement sur :
- **Streamlit Cloud** (gratuit)
- **Heroku**
- **AWS / GCP / Azure**

Le mode BYOK garantit que :
- Aucune clé API n'est stockée côté serveur
- Chaque utilisateur utilise sa propre clé
- Les coûts sont directement facturés à l'utilisateur par OpenAI

## 📝 Notes Techniques

- L'application utilise `st.session_state` pour la persistance des données
- Workflow en étapes conditionnelles pour une navigation fluide
- Design responsive avec CSS personnalisé
- Export des résultats en JSON pour archivage
- Tutoriel intégré "Zéro Friction" pour les débutants

## 🎓 Méthodologie

Basée sur la formation **IA-BrainStormer** par Florent, cette application implémente le système GPS (Génération • Priorisation • Séquençage) avec le Crash Test D.U.R. en amont.

## 📄 Licence

Méthodologie IA-BrainStormer © Florent  
Application développée par Manus AI
