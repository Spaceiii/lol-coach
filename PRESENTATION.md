# 🎮 LOL Coach - Gestionnaire de Draft IA pour League of Legends

## 📋 Plan Détaillé de Présentation

---

## 🎯 **SLIDE 1 : Page de Titre**
**LOL Coach - Assistant IA pour le Draft**
- Sous-titre : "Système de recommandation intelligent basé sur l'analyse de 100 000+ matchs"
- Votre nom + Date
- Logo/Image : Interface de League of Legends ou du projet

---

## 💡 **SLIDE 2 : Contexte & Problématique**

### Le Problème
- **180+ champions** à choisir dans League of Legends
- Phase de draft complexe : choix stratégiques en temps limité
- Nécessité de connaître :
  - Les matchups favorables/défavorables
  - Les synergies entre champions alliés
  - Les statistiques de performance (winrate, KDA, etc.)

### La Solution
Un assistant IA qui analyse les données historiques pour recommander les 5 meilleurs picks en fonction de la situation

---

## 🏗️ **SLIDE 3 : Architecture du Projet**

### Pipeline de Données
```
matchData.csv (API Riot Games)
        ↓
┌───────────────────────────┐
│  EXTRACTION & TRAITEMENT  │
├───────────────────────────┤
│ csv_champ_maker.py        │ → champStats.csv (173 champions)
│ csv_matchup_creator.py    │ → matchUp.csv (matchups 1v1)
└───────────────────────────┘
        ↓
┌───────────────────────────┐
│   APPLICATION IA          │
├───────────────────────────┤
│ app.py (Streamlit)        │
│ + Gemini AI               │
└───────────────────────────┘
```

### Technologies Utilisées
- **Python** : Pandas, Streamlit
- **IA** : Google Gemini API
- **API** : Riot Games API
- **Données** : 100 000+ matchs analysés

---

## 📊 **SLIDE 4 : Étape 1 - Extraction des Données**

### Fichier : `csv_champ_maker.py`

**Objectif** : Agréger les statistiques globales de chaque champion

**Données extraites :**
- **173 champions** répertoriés
- Pour chaque champion :
  - Winrate global (% de victoires)
  - KDA moyen (Kills/Deaths/Assists)
  - Or moyen gagné par partie
  - Dégâts moyens infligés
  - Soins moyens

**Sortie** : `champStats.csv`

### Exemple de données
| ChampionName | GamesPlayed | WinRate | AvgKills | AvgDeaths | AvgAssists |
|--------------|-------------|---------|----------|-----------|------------|
| Aatrox       | 1234        | 52.16%  | 8.62     | 6.11      | 5.34       |
| Ahri         | 1589        | 51.30%  | 7.43     | 5.89      | 7.21       |

---

## ⚔️ **SLIDE 5 : Étape 2 - Analyse des Matchups**

### Fichier : `csv_matchup_creator.py`

**Objectif** : Créer une base de données des confrontations 1v1 par lane

**Données calculées :**
- Matchups par position (TOP, JUNGLE, MID, BOT, SUP)
- Pour chaque matchup :
  - Champion A vs Champion B
  - Résultat (victoire/défaite)
  - Différences d'or, CS, dégâts
  - KDA individuel
  - Kill Participation (KP)
  - Damage Share (% des dégâts de l'équipe)
  - Vision score

**Sortie** : `matchUp.csv` (~47 MB)

### Exemple de matchup
```
Lane: MID
Zed vs Yasuo
Gold Diff: +450 (avantage Zed)
Win: Zed (60% des matchs)
KDA Zed: 9.2 | KDA Yasuo: 6.8
```

---

## 🤖 **SLIDE 6 : Étape 3 - L'Assistant IA**

### Fichier : `app.py` (Streamlit + Gemini AI)

**Fonctionnalités :**
1. **Interface intuitive** avec Streamlit
2. **Formulaire de sélection** :
   - Rôle (TOP, JUNGLE, MID, BOT, SUP)
   - Champions alliés (optionnel)
   - Champions ennemis (optionnel)
3. **Analyse par IA** : Gemini traite les données
4. **Recommandations personnalisées** : 5 champions avec justifications

### Workflow
```
Utilisateur → [Rôle + Alliés + Ennemis]
     ↓
Chargement champStats.csv + matchUp.csv
     ↓
Filtrage des données (500 matchups max)
     ↓
Prompt envoyé à Gemini AI
     ↓
5 Recommandations avec analyses détaillées
```

---

## 🎯 **SLIDE 7 : Logique de l'IA**

### Contexte donné à Gemini

L'IA reçoit :
1. **Statistiques globales** (champStats.csv)
2. **Matchups filtrés** pour le rôle demandé
3. **Instructions** :
   - Analyser les winrates
   - Identifier les matchups favorables
   - Calculer les synergies avec alliés
   - Évaluer les contre-picks

### Critères d'analyse
- ✅ **Winrate** : Performance globale du champion
- ⚔️ **Matchups** : Avantages contre les ennemis
- 🤝 **Synergies** : Combos avec les alliés (ex: Yasuo + knock-ups)
- 📊 **KDA & Dégâts** : Impact en partie

---

## 💬 **SLIDE 8 : Exemple de Recommandation**

### Requête
- **Rôle** : JUNGLE
- **Alliés** : Yasuo, Lulu
- **Ennemis** : Teemo, Sylas

### Réponse de l'IA

**1. 🛡️ Pantheon**
- **Winrate** : 50.15%
- **KDA** : 7.13 / 6.05 / 7.73
- **Pourquoi ?**
  - ✅ Excellent contre Sylas (3-0 dans les matchups)
  - ✅ Stun pour combo avec Yasuo (synergie knock-up)
  - ✅ Early game fort pour snowball
  - ✅ Ultime global pour rotations rapides

**2. 🗡️ Talon**
- **Winrate** : 51.3%
- **KDA** : 8.68 / 5.72 / 6.53
- **Pourquoi ?**
  - ✅ Counter Sylas (4-1 matchups)
  - ✅ Mobilité exceptionnelle (E - murs)
  - ✅ Burst dévastateur
  - ✅ Synergie avec Lulu (buffs pour assassiner)

*[... 3 autres champions]*

---

## 📈 **SLIDE 9 : Résultats & Performance**

### Métriques du Projet
- **100 000+ matchs** analysés
- **173 champions** avec statistiques complètes
- **Thousands de matchups** 1v1 répertoriés
- **5 positions** couvertes (TOP, JUNGLE, MID, BOT, SUP)

### Avantages
- ⚡ **Rapidité** : Recommandations en secondes
- 🎯 **Précision** : Basé sur données réelles
- 🧠 **Contexte** : Analyse situationnelle (alliés/ennemis)
- 📚 **Pédagogique** : Explications détaillées

### Limites actuelles
- Dépend de la qualité des données d'entraînement
- Nécessite une clé API Gemini
- Pas de prédiction en temps réel (patches)

---

## 🛠️ **SLIDE 10 : Aspects Techniques**

### Stack Technique
```python
# Librairies principales
pandas          # Manipulation de données
streamlit       # Interface web
google-genai    # IA Gemini
python-dotenv   # Variables d'environnement
```

### Fichiers du Projet
```
ProjetLoLCoach/
├── app.py                      # Application Streamlit
├── csv_champ_maker.py          # Extraction stats champions
├── csv_matchup_creator.py      # Création matchups
├── data/
│   ├── matchData.csv           # Données brutes (API Riot)
│   ├── champStats.csv          # Stats agrégées champions
│   ├── matchUp.csv             # Base matchups 1v1
│   └── columns.txt             # Documentation colonnes
└── requirements.txt            # Dépendances
```

### Défis rencontrés
- **Volume de données** : ~100k matchs → filtrage nécessaire
- **Limites de tokens** : Gemini limité à 500 matchups par requête
- **Format CSV** : Problème MIME type (résolu avec conversion texte)

---

## 🚀 **SLIDE 11 : Démonstration Live**

### Interface Utilisateur
- **Sidebar** :
  - Sélection du rôle (dropdown)
  - Input champions alliés
  - Input champions ennemis
  - Bouton "Obtenir des recommandations"

- **Zone principale** :
  - Chat conversationnel
  - Affichage des recommandations formatées
  - Historique des requêtes

### Design
- Thème sombre (gaming aesthetic)
- Dégradés cyan/violet
- Emojis pour la lisibilité
- Animations CSS

---

## 🎓 **SLIDE 12 : Apprentissages & Compétences**

### Compétences développées
- ✅ **Data Engineering** : ETL (Extract, Transform, Load)
- ✅ **Machine Learning** : Intégration d'IA générative
- ✅ **Full Stack** : Frontend (Streamlit) + Backend (Python)
- ✅ **API REST** : Utilisation Riot Games API + Gemini API
- ✅ **Data Analysis** : Pandas, statistiques, agrégations
- ✅ **UX/UI** : Design d'interface utilisateur

### Méthodologie
1. **Collecte de données** (API Riot)
2. **Nettoyage & transformation** (Pandas)
3. **Modélisation** (création de features)
4. **Intégration IA** (prompt engineering)
5. **Déploiement** (Streamlit)

---

## 🔮 **SLIDE 13 : Améliorations Futures**

### Fonctionnalités à venir
- 🔄 **Mise à jour automatique** des données (via API Riot en temps réel)
- 📊 **Visualisations** : Graphiques de winrates, heatmaps de matchups
- 🏆 **Tiers personnalisés** : Recommandations par elo (Bronze → Challenger)
- 🎯 **Analyse d'équipe complète** : Composition 5v5 optimale
- 🧪 **A/B Testing** : Comparaison de performances avec/sans assistant

### Optimisations techniques
- Cache des requêtes IA (éviter les appels répétés)
- Base de données SQL (PostgreSQL) au lieu de CSV
- Déploiement cloud (Streamlit Cloud, Heroku)
- Fine-tuning d'un modèle spécialisé LoL

---

## 📚 **SLIDE 14 : Bibliographie & Ressources**

### APIs & Documentation
- **Riot Games API** : https://developer.riotgames.com/
- **Google Gemini** : https://ai.google.dev/
- **Streamlit** : https://docs.streamlit.io/

### Datasets
- **League of Legends Match Data** : Collecté via Riot API
- **Champion Statistics** : Agrégé depuis 100k+ matchs

### Outils
- Python 3.11+
- Pandas, NumPy
- VS Code / PyCharm
- Git / GitHub

---

## 🎬 **SLIDE 15 : Conclusion**

### Points clés
- ✅ Projet **complet** : extraction → traitement → IA → interface
- ✅ **Impact réel** : aide les joueurs à prendre de meilleures décisions
- ✅ **Scalable** : architecture extensible pour d'autres jeux
- ✅ **Innovant** : combinaison data science + IA générative

### Merci !
**Questions ?** 🙋‍♂️

---
---

## 🎨 **PROMPT POUR GAMMA.APP**

Copier-coller ce prompt dans Gamma.app pour générer automatiquement les slides :

---

**Titre : LOL Coach - Assistant IA pour le Draft de League of Legends**

Crée une présentation professionnelle et visuelle pour un projet de data science et intelligence artificielle. Le projet est un système de recommandation de champions pour League of Legends basé sur l'analyse de 100 000+ matchs.

**Structure de la présentation :**

**Slide 1 - Titre**
- Titre principal : "LOL Coach - Assistant IA pour le Draft"
- Sous-titre : "Système de recommandation intelligent basé sur 100 000+ matchs"
- Image : Interface gaming avec des éléments de League of Legends
- Style : Dark theme avec accents cyan et violet

**Slide 2 - Contexte & Problématique**
- Section problème : Draft complexe avec 180+ champions, nécessité de connaître matchups et synergies
- Section solution : Assistant IA qui recommande les 5 meilleurs picks
- Icônes : 🎮 pour gaming, 🤔 pour problème, 💡 pour solution
- Style : Split layout 50/50

**Slide 3 - Architecture du Projet**
- Diagramme de flux : matchData.csv → Scripts Python → Fichiers CSV → Application IA
- 3 composants principaux en colonnes :
  1. Extraction (csv_champ_maker.py)
  2. Traitement (csv_matchup_creator.py)
  3. Application (app.py + Gemini)
- Technologies : Python, Pandas, Streamlit, Gemini AI, Riot API
- Style : Schéma technique avec flèches

**Slide 4 - Extraction des Données**
- Titre : "Étape 1 : Agrégation des Statistiques Champions"
- Contenu : Explication de csv_champ_maker.py
- Tableau exemple avec 3-4 champions et leurs stats (WinRate, KDA, Gold)
- Métriques clés : 173 champions, 100k+ matchs
- Icône : 📊

**Slide 5 - Analyse des Matchups**
- Titre : "Étape 2 : Base de Données Matchups 1v1"
- Contenu : Explication de csv_matchup_creator.py
- Exemple visuel d'un matchup : Zed vs Yasuo avec statistiques
- Données calculées : Gold Diff, CS Diff, Damage Share, KP
- Icône : ⚔️

**Slide 6 - L'Assistant IA**
- Titre : "Étape 3 : Application Streamlit + Gemini"
- Workflow visuel en 4 étapes :
  1. Input utilisateur (rôle + alliés + ennemis)
  2. Chargement & filtrage données
  3. Analyse par Gemini AI
  4. 5 Recommandations personnalisées
- Screenshot ou mockup de l'interface
- Icône : 🤖

**Slide 7 - Logique de l'IA**
- Titre : "Comment l'IA analyse les données ?"
- 4 critères en colonnes :
  1. ✅ Winrate global
  2. ⚔️ Matchups favorables
  3. 🤝 Synergies alliés
  4. 📊 KDA & Dégâts
- Contexte donné à Gemini expliqué brièvement
- Style : Cards layout

**Slide 8 - Exemple de Recommandation**
- Titre : "Cas d'usage : JUNGLE avec Yasuo/Lulu vs Teemo/Sylas"
- 2 champions présentés en détail :
  - Pantheon : Stats + 3 raisons de le choisir
  - Talon : Stats + 3 raisons de le choisir
- Format : Cards avec émojis et bullet points
- Style : Visual et coloré

**Slide 9 - Résultats & Performance**
- Métriques en gros chiffres :
  - 100 000+ matchs
  - 173 champions
  - 5 positions
- Avantages en bullet points (rapidité, précision, contexte)
- Section "Limites" honnête (dépendance API, patches)
- Style : Dashboard layout

**Slide 10 - Aspects Techniques**
- Code snippet du stack (requirements.txt)
- Architecture fichiers en arborescence
- 3 défis techniques résolus avec solutions
- Style : Code-focused avec fond sombre

**Slide 11 - Démonstration Interface**
- Screenshot de l'interface Streamlit
- Annotations sur les fonctionnalités clés (sidebar, chat, boutons)
- Design mentionné : thème sombre gaming, dégradés cyan/violet
- Style : Product showcase

**Slide 12 - Compétences & Apprentissages**
- 6 compétences en grid layout :
  1. Data Engineering
  2. Machine Learning
  3. Full Stack
  4. API REST
  5. Data Analysis
  6. UX/UI Design
- Méthodologie en 5 étapes (flux linéaire)
- Icône : 🎓

**Slide 13 - Améliorations Futures**
- 2 sections :
  - Fonctionnalités futures (5 items avec émojis)
  - Optimisations techniques (4 items)
- Style : Roadmap visuelle avec timeline
- Icône : 🔮

**Slide 14 - Ressources & Bibliographie**
- 3 colonnes :
  1. APIs (Riot, Gemini, Streamlit)
  2. Datasets (sources de données)
  3. Outils (Python, IDE, Git)
- Liens inclus
- Icône : 📚

**Slide 15 - Conclusion**
- 4 points clés avec checkmarks
- Call to action : "Questions ?"
- Remerciements
- Style : Simple et impactant

**Style général pour toute la présentation :**
- Thème : Dark mode gaming (noir/gris foncé)
- Couleurs d'accent : Cyan (#0BC5EA) et Violet (#805AD5)
- Police : Moderne et lisible (Inter, SF Pro, ou équivalent)
- Beaucoup d'émojis pour la lisibilité
- Visuels : Diagrammes, tableaux, code snippets
- Animations : Subtiles et professionnelles
- Ton : Technique mais accessible, enthousiaste

---

**FIN DU PROMPT**

---

## 📝 Notes pour la Présentation Orale

### Timing recommandé (15-20 minutes)
1. Introduction (1 min) - Slides 1-2
2. Architecture (3 min) - Slide 3
3. Pipeline de données (4 min) - Slides 4-5
4. Application IA (4 min) - Slides 6-8
5. Résultats (2 min) - Slide 9
6. Aspects techniques (3 min) - Slides 10-11
7. Apprentissages & futur (2 min) - Slides 12-13
8. Conclusion (1 min) - Slide 15

### Conseils de présentation
- 🎬 **Commencer par une démo** : Montrez l'application en action
- 📊 **Insister sur les chiffres** : 100k matchs, 173 champions
- 🧠 **Expliquer la valeur ajoutée de l'IA** : Pas juste une recherche, mais une analyse contextuelle
- 💻 **Montrer du code** : 2-3 extraits pertinents (pas trop)
- 🎯 **Exemple concret** : Utilisez l'exemple Yasuo/Lulu pour illustrer
- 🚀 **Finir sur les perspectives** : Montrez que le projet est évolutif

### Questions probables du prof
1. **"Pourquoi Gemini et pas un modèle custom ?"**
   → Rapidité de dev, qualité des explications, pas besoin de training data labellisée

2. **"Comment gérez-vous les mises à jour de patchs ?"**
   → Actuellement données statiques, mais architecture permet re-extraction facile

3. **"Avez-vous validé la pertinence des recommandations ?"**
   → Basé sur données réelles (100k matchs), l'IA explique ses choix, validation qualitative faite

4. **"Quelles sont les limites ?"**
   → Dépend qualité données, pas de learning continu, coût API, patches LoL

5. **"Combien de temps le projet a pris ?"**
   → [Répondez honnêtement selon votre timeline]

Bonne présentation ! 🎉

