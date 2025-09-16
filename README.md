# 🌱 Dashboard Éco-Évaluation des Expositions Culturelles

Application Streamlit pour l'évaluation environnementale et éco-sociale des expositions culturelles et musées selon les normes internationales.

## 🎯 Objectif

Fournir un outil d'évaluation complet permettant aux institutions culturelles de :
- Mesurer leur impact environnemental selon les standards ADEME et ISO
- Évaluer leur performance éco-sociale selon ISO 26000
- Générer des rapports détaillés et des recommandations
- Comparer leurs résultats avec des benchmarks sectoriels

## 🏗️ Architecture

```
eco_evaluation_dashboard/
├── app.py                    # Point d'entrée Streamlit
├── requirements.txt          # Dépendances Python
├── src/                      # Code source
│   ├── config/              # Configuration et critères
│   ├── data/                # Modèles et stockage
│   ├── questionnaire/       # Module questionnaire
│   ├── dashboard/           # Module dashboard
│   └── utils/               # Utilitaires
├── data/                    # Données persistantes
└── tests/                   # Tests unitaires
```

## 🚀 Installation et lancement

### Prérequis
- Python 3.8+
- pip

### Installation
```bash
# Cloner le projet
git clone <url-du-repo>
cd eco_evaluation_dashboard

# Créer un environnement virtuel
python -m venv eco_eval_env
source eco_eval_env/bin/activate  # Linux/Mac
# eco_eval_env\Scripts\activate   # Windows

# Installer les dépendances
pip install -r requirements.txt
```

### Lancement
```bash
streamlit run app.py
```

L'application sera accessible à l'adresse : http://localhost:8501

## 📋 Fonctionnalités

### Phase 1 - Foundation (Actuelle)
- ✅ Structure modulaire du projet
- ✅ Configuration des critères d'évaluation
- ✅ Interface de base avec navigation
- ✅ Dashboard dummy avec graphiques de test
- ✅ Placeholder pour le questionnaire

### Phases suivantes (En développement)
- 📝 **Questionnaire complet** avec validation des données
- 📊 **Dashboard interactif** avec calculs selon les normes
- 💾 **Sauvegarde** et gestion des évaluations
- 📈 **Comparaisons** et analyses temporelles
- 📑 **Export** PDF et Excel des rapports

## 🔧 Configuration

### Critères d'évaluation
Les critères sont définis dans `src/config/criteria.py` et couvrent :
1. **Impacts Environnementaux Directs** (30%)
2. **Impacts Environnementaux Indirects** (15%)
3. **Impacts Éco-Sociaux** (30%)
4. **Impacts Temporels et Contextuels** (15%)
5. **Critères Transversaux** (10%)

### Normes de référence
- **ADEME** : Bilan carbone et méthodes de calcul
- **ISO 14001** : Management environnemental
- **ISO 26000** : Responsabilité sociétale
- **Loi française 2005** : Accessibilité universelle

## 📊 Types de questions

Le questionnaire supporte plusieurs types de questions :
- **Numériques** : Valeurs avec unités (kg CO₂eq, kWh, litres)
- **Pourcentages** : 0-100%
- **Échelles** : Notations 1-10 ou 1-5
- **Choix multiples** : Sélection parmi options prédéfinies
- **Booléennes** : Oui/Non
- **Texte libre** : Descriptions qualitatives

## 🎨 Interface utilisateur

### Thème et couleurs
- **Couleur principale** : #2E7D32 (Vert foncé)
- **Couleur secondaire** : #1976D2 (Bleu)
- **Design** : Material Design avec Streamlit

### Navigation
- **Sidebar** : Navigation principale et actions rapides
- **Onglets** : Dashboard, Questionnaire, À propos
- **Responsive** : Adaptatif aux différentes tailles d'écran

## 📈 Métriques et calculs

### Indicateurs principaux
- **Empreinte carbone** : kg CO₂eq (méthode ADEME)
- **Score éco-social** : 0-10 (basé sur ISO 26000)
- **Taux de matériaux recyclés** : 0-100%
- **Part d'énergies renouvelables** : 0-100%

### Formules officielles
```python
# Bilan carbone ADEME
emissions = quantity * emission_factor

# Criticité ISO 14001
criticality = (frequency * severity) / control

# Performance par catégorie
score = weighted_average(subcategory_scores)
```

## 🔍 Validation des données

- **Champs obligatoires** : Contrôle strict
- **Bornes numériques** : Validation des plages de valeurs
- **Cohérence** : Vérification des relations entre réponses
- **Formats** : Validation des dates, pourcentages, etc.

## 📁 Stockage des données

### Format actuel : JSON
```json
{
  "evaluation_id": "uuid",
  "metadata": {
    "name": "Nom exposition",
    "date": "2024-01-15",
    "type": "temporary_exhibition"
  },
  "responses": {
    "category": {
      "subcategory": {
        "question_id": "value"
      }
    }
  },
  "calculated_scores": {
    "carbon_footprint": 2.4,
    "eco_social_score": 7.8
  }
}
```

## 🧪 Tests

```bash
# Lancer les tests (quand implémentés)
python -m pytest tests/

# Avec couverture
python -m pytest tests/ --cov=src/
```

## 🚀 Déploiement

### Streamlit Cloud
1. Pousser le code sur GitHub
2. Connecter à Streamlit Cloud
3. Configuration automatique

### Serveur local
```bash
streamlit run app.py --server.port 8501
```

## 🤝 Contribution

### Structure de développement
1. **Phase 1** : Foundation et structure
2. **Phase 2** : Modèles de données
3. **Phase 3** : Module questionnaire
4. **Phase 4** : Calculs et métriques
5. **Phase 5** : Dashboard et visualisations
6. **Phase 6** : Features avancées
7. **Phase 7** : Tests et documentation

### Standards de code
- **Format** : Black (future implémentation)
- **Linting** : Flake8 (future implémentation)
- **Documentation** : Docstrings Google style

## 📝 Changelog

### Version 1.0.0 (Phase 1)
- ✅ Structure de base du projet
- ✅ Configuration des critères d'évaluation (93 questions)
- ✅ Interface Streamlit avec navigation
- ✅ Dashboard dummy avec graphiques Plotly
- ✅ Système de configuration modulaire

## 📞 Support

- **Documentation** : Voir le dossier `docs/`
- **Issues** : Créer une issue sur GitHub
- **Contact** : [Insérer contact]

## 📄 Licence

MIT License - Voir le fichier LICENSE pour les détails.

---

**Version actuelle** : 1.0.0 (Phase 1 - Foundation)
**Dernière mise à jour** : Janvier 2024
