# 🎮 LOL Coach - Guide d'utilisation

## 📋 Description

Ce projet fournit un système de recommandation de champions League of Legends basé sur l'IA (Gemini) qui analyse les statistiques et les matchups pour suggérer les meilleurs choix.

## 🚀 Installation

1. Installez les dépendances :
```powershell
pip install -r requirements.txt
```

2. Ajoutez les bibliothèques pour l'affichage visuel :
```powershell
pip install rich
```

3. Configurez votre clé API Gemini :
   - Créez un fichier `.env` à la racine du projet
   - Ajoutez : `GEMINI_API_KEY=votre_cle_api`

## 🎯 Utilisation

### 1. Chatbot avec recommandations IA

```powershell
python chatbot.py
```

Le chatbot analyse les données et recommande 5 champions en fonction :
- Du rôle demandé (TOP, JUNGLE, MID, BOT, SUP)
- Des champions alliés (synergies)
- Des champions ennemis (counter-picks)

**Personnaliser les paramètres :**

Éditez la fonction `main()` dans `chatbot.py` :

```python
result = get_champion_recommendations(
    role="MID",                                    # Changez le rôle
    allied_champions=["Jinx", "Leona"],           # Champions alliés
    enemy_champions=["Zed", "Lee Sin"]            # Champions ennemis
)
```

### 2. Affichage des résultats formatés

```powershell
# Mode 1 : Affichage structuré avec tableaux
python display_results.py 1

# Mode 2 : Affichage Markdown depuis results.txt
python display_results.py 2
```

**Mode 1** : Affiche les données dans des tableaux colorés et structurés
**Mode 2** : Affiche le contenu du fichier `results.txt` avec formatage Markdown enrichi

## 📊 Fichiers de données

- `data/champStats.csv` : Statistiques globales des champions (winrate, KDA, etc.)
- `data/matchUp.csv` : Données des matchups 1v1 par lane (~47 MB, 500+ matchups filtrés par rôle)
- `data/results.txt` : Exemple de résultats générés par le chatbot

## 🔧 Fonctionnalités

### ✨ Chatbot (`chatbot.py`)

- ✅ Filtrage intelligent des données (limite à 500 matchups par rôle)
- ✅ Analyse par IA avec contexte complet
- ✅ Recommandations avec justifications détaillées
- ✅ Affichage console enrichi avec Rich
- ✅ Support des champions alliés et ennemis

### 🎨 Affichage formaté (`display_results.py`)

- ✅ Deux modes d'affichage au choix
- ✅ Rendu Markdown avec coloration syntaxique
- ✅ Tableaux structurés avec émojis
- ✅ Panneaux colorés et bordures stylisées
- ✅ Support UTF-8 complet

## 📝 Exemples de sortie

### Statistiques de champion

```
📊 WinRate        52.16%
⚔️ KDA            8.62/6.11/5.34
🎯 Matchups       Équilibré contre Sylas (3-3)
```

### Synergies

```
🤝 Yasuo          Combo E+Q = knock-up parfait
✨ Lulu           Boucliers pour survivre aux engages
💪 Forces         Excellent engageur, tanky, contrôle de foule
💡 Conseils       Gank avec combo E+Q, priorisez les teamfights
```

## 🎯 Cas d'usage

### Scénario 1 : Draft en partie classée

```python
# Votre équipe a déjà pick Yasuo (MID) et Lulu (SUP)
# L'ennemi a pick Teemo (TOP) et Sylas (JUNGLE)
# Vous cherchez un bon JUNGLE

result = get_champion_recommendations(
    role="JUNGLE",
    allied_champions=["Yasuo", "Lulu"],
    enemy_champions=["Teemo", "Sylas"]
)
```

### Scénario 2 : Découvrir les meilleurs champions d'un rôle

```python
# Sans contrainte, trouvez les 5 meilleurs SUP
result = get_champion_recommendations(role="SUP")
```

### Scénario 3 : Counter-pick spécifique

```python
# L'ennemi a pick Zed en MID, trouvez des counters
result = get_champion_recommendations(
    role="MID",
    enemy_champions=["Zed"]
)
```

## 🔍 Détails techniques

### Filtrage des données

Pour éviter de dépasser les limites de tokens de l'API Gemini :
- Les matchups sont filtrés par rôle spécifique
- Maximum 500 matchups les plus récents par requête
- Si des champions ennemis sont spécifiés, seuls les matchups pertinents sont inclus

### Modèle IA

- Utilise `gemini-1.5-flash-latest` pour l'analyse
- Temperature : 0.7 (bon équilibre créativité/précision)
- Context window optimisé avec données filtrées

## 🛠️ Dépannage

### Erreur : "Missing API key"

Créez un fichier `.env` avec :
```
GEMINI_API_KEY=votre_cle_api_ici
```

### Erreur : "Quota exceeded"

Vous avez atteint la limite gratuite de l'API. Attendez ou passez à un plan payant.

### Caractères mal affichés dans la console

Assurez-vous que votre console supporte UTF-8 :
```powershell
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
```

## 📚 Librairies utilisées

- `google-genai` : API Gemini pour l'IA
- `pandas` : Manipulation des données CSV
- `rich` : Affichage console enrichi
- `python-dotenv` : Gestion des variables d'environnement

## 🎓 Améliorations futures

- [ ] Interface web avec Flask/Streamlit
- [ ] Cache des résultats pour éviter les appels API répétés
- [ ] Analyse de compositions d'équipe complètes
- [ ] Graphiques de statistiques avec matplotlib
- [ ] Export PDF des recommandations

## 📄 Licence

Projet éducatif - Libre d'utilisation

---

**Bon coaching ! 🏆**

