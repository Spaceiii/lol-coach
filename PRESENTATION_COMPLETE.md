# 🎮 LOL Coach - Présentation Complète du Projet

**Gestionnaire de Draft Intelligent pour League of Legends**

*Système de recommandation basé sur l'IA et l'analyse de données massives*

---

## 📑 Table des Matières

1. [Vue d'ensemble du projet](#vue-densemble)
2. [Contexte et objectifs](#contexte-et-objectifs)
3. [Architecture technique](#architecture-technique)
4. [Pipeline de traitement des données](#pipeline-de-données)
5. [L'application IA](#lapplication-ia)
6. [Résultats et démonstration](#résultats-et-démonstration)
7. [Compétences acquises](#compétences-acquises)
8. [Perspectives d'évolution](#perspectives-dévolution)

---

## 🎯 Vue d'ensemble

### Résumé du Projet

**LOL Coach** est un assistant intelligent qui aide les joueurs de League of Legends à choisir les meilleurs champions pendant la phase de draft (sélection des personnages). Le système analyse plus de **100 000 matchs** extraits de l'API officielle de Riot Games et utilise l'IA Gemini de Google pour fournir des recommandations personnalisées.

### Problème adressé

League of Legends compte **180+ champions** jouables, chacun avec des forces, faiblesses et synergies spécifiques. Pendant le draft (5 minutes maximum), les joueurs doivent :
- Choisir un champion adapté à leur rôle
- Identifier les matchups favorables contre les ennemis
- Créer des synergies avec leurs coéquipiers
- Prendre en compte les statistiques de performance

**Notre solution** : Un chatbot IA qui analyse toutes ces variables en temps réel et recommande les 5 meilleurs choix avec des justifications détaillées.

### Chiffres Clés

- 📊 **100 000+ matchs** analysés
- 🎮 **173 champions** répertoriés avec statistiques complètes
- ⚔️ **Thousands de matchups** 1v1 documentés
- 🏆 **5 positions** couvertes (TOP, JUNGLE, MID, BOT, SUPPORT)
- 🤖 **Intelligence artificielle** Gemini pour l'analyse contextuelle

---

## 🎮 Contexte et Objectifs

### Qu'est-ce que League of Legends ?

League of Legends (LoL) est un jeu vidéo multijoueur compétitif où deux équipes de 5 joueurs s'affrontent. Chaque joueur choisit un "champion" (personnage) avec des capacités uniques et occupe une position spécifique sur la carte.

### Les 5 Positions (Rôles)

1. **TOP** : Combattant isolé en lane supérieure (tanks, bruisers)
2. **JUNGLE** : Parcourt la jungle pour aider les alliés (ganks)
3. **MID** : Lane centrale, souvent des mages ou assassins
4. **BOT** : Tireur (ADC) avec beaucoup de dégâts
5. **SUPPORT** : Aide le BOT, contrôle de foule et vision

### La Phase de Draft : Un Moment Critique

```
┌─────────────────────────────────────────┐
│   PHASE DE DRAFT (5 minutes)           │
├─────────────────────────────────────────┤
│  1. BAN (interdictions)                 │
│  2. PICK ordre alterné                  │
│     Équipe A → Équipe B → ...           │
│  3. Stratégie en temps réel             │
└─────────────────────────────────────────┘
```

**Enjeux :**
- Choisir trop vite = mauvais matchup = défaite probable
- Choisir trop lentement = pénalité (random pick)
- Nécessite une connaissance encyclopédique du jeu

### Objectifs du Projet

✅ **Objectif principal** : Créer un assistant IA pour optimiser la phase de draft

✅ **Objectifs secondaires** :
- Extraire et traiter des données massives (Big Data)
- Créer des statistiques agrégées pertinentes
- Implémenter une analyse contextuelle avec IA
- Développer une interface utilisateur intuitive
- Documenter le processus de data science

---

## 🏗️ Architecture Technique

### Vue d'Ensemble du Système

```
┌────────────────────────────────────────────────────────────┐
│                    RIOT GAMES API                          │
│              (Source de données officielles)               │
└───────────────────────┬────────────────────────────────────┘
                        │
                        ↓
            ┌───────────────────────┐
            │   matchData.csv       │
            │   (100 000+ matchs)   │
            │   (Données brutes)    │
            └───────────┬───────────┘
                        │
        ┌───────────────┴────────────────┐
        │                                │
        ↓                                ↓
┌────────────────┐            ┌─────────────────┐
│ csv_champ_     │            │ csv_matchup_    │
│ maker.py       │            │ creator.py      │
└───────┬────────┘            └────────┬────────┘
        │                              │
        ↓                              ↓
┌────────────────┐            ┌─────────────────┐
│ champStats.csv │            │  matchUp.csv    │
│ (173 champs)   │            │ (~47 MB)        │
│ Stats globales │            │ Matchups 1v1    │
└───────┬────────┘            └────────┬────────┘
        │                              │
        └──────────────┬───────────────┘
                       │
                       ↓
            ┌──────────────────┐
            │     app.py       │
            │   (Streamlit)    │
            │  + Gemini AI     │
            └────────┬─────────┘
                     │
                     ↓
            ┌──────────────────┐
            │   Utilisateur    │
            │ 5 Recommandations│
            └──────────────────┘
```

### Technologies Utilisées

#### Backend & Data Processing
- **Python 3.11+** : Langage principal
- **Pandas** : Manipulation de DataFrames (CSV)
- **NumPy** : Calculs numériques
- **dotenv** : Gestion des variables d'environnement

#### Intelligence Artificielle
- **Google Gemini API** : Modèle d'IA générative
- **Prompt Engineering** : Optimisation des requêtes IA

#### Frontend
- **Streamlit** : Framework web Python
- **Rich** : Formatage console avec couleurs

#### APIs Externes
- **Riot Games API** : Données officielles de League of Legends

#### Outils de Développement
- **Git/GitHub** : Versionnement
- **VS Code / PyCharm** : IDE
- **Windows PowerShell** : Terminal

---

## 📊 Pipeline de Traitement des Données

### Étape 0 : Collecte des Données Brutes

**Source** : API Riot Games Developer Portal

**Fichier généré** : `matchData.csv`

**Contenu** : Données complètes de 100 000+ matchs avec :
- **1771 colonnes** différentes (voir `columns.txt`)
- Informations pour chaque match :
  - 10 joueurs (participant0 à participant9)
  - Statistiques individuelles (kills, deaths, assists, gold, etc.)
  - Statistiques d'équipe (towers, dragons, barons)
  - Données temporelles (game duration, timestamps)

**Exemple de colonnes** :
```
matchId
gameDuration
participant0ChampionName
participant0Kills
participant0Deaths
participant0Assists
participant0GoldEarned
participant0TotalDamageDealtToChampions
participant0Win
...
(x1771 colonnes)
```

---

### Étape 1 : Agrégation des Statistiques Champions

**Fichier** : `csv_champ_maker.py`

**Objectif** : Créer une vue agrégée des performances de chaque champion

#### Processus

```python
# Pseudo-code du processus
for chaque match in matchData:
    for chaque joueur (0-9):
        champion = joueur.championName
        
        # Accumulation des stats
        champs[champion].games_played += 1
        champs[champion].wins += joueur.win
        champs[champion].kills += joueur.kills
        champs[champion].deaths += joueur.deaths
        champs[champion].assists += joueur.assists
        champs[champion].gold_earned += joueur.goldEarned
        champs[champion].damage_dealt += joueur.damageDealtToChampions
        # ... autres stats

# Calcul des moyennes
for champion in champs:
    avg_kills = total_kills / games_played
    winrate = (wins / games_played) * 100
    # ... autres moyennes
```

#### Sortie : `champStats.csv`

**Structure** :
| Colonne | Description |
|---------|-------------|
| ChampionId | ID unique Riot Games |
| ChampionName | Nom du champion |
| GamesPlayed | Nombre de parties jouées |
| ChampionWinRate | Taux de victoire (%) |
| AvgKills | Kills moyens par partie |
| AvgDeaths | Morts moyennes par partie |
| AvgAssists | Assistances moyennes |
| AvgGoldEarned | Or moyen gagné |
| AvgDamageDealt | Dégâts moyens infligés |
| AvgHeal | Soins moyens |
| AvgHealsOnTeammates | Soins moyens sur alliés |

**Exemple de données** :
```csv
ChampionId,ChampionName,GamesPlayed,ChampionWinRate,AvgKills,AvgDeaths,AvgAssists
1,Annie,1523,51.08%,6.89,5.34,8.12
2,Olaf,987,49.54%,7.23,6.78,7.45
3,Galio,1245,52.65%,4.12,5.89,10.34
...
```

**Statistiques** :
- **173 champions** uniques répertoriés
- Données agrégées sur **100 000+ parties**
- Fiabilité statistique élevée (échantillon large)

---

### Étape 2 : Création de la Base Matchups

**Fichier** : `csv_matchup_creator.py`

**Objectif** : Analyser les confrontations directes 1v1 par lane

#### Logique de Matchup

Un "matchup" représente la confrontation entre deux champions dans la même lane (position).

**Règles** :
- Exactement 2 joueurs sur la même lane (1 par équipe)
- Comparaison des performances individuelles
- Calcul des différences (gold, CS, damage)
- Attribution des résultats (victoire/défaite)

#### Processus Détaillé

```python
# 1. Extraction des participants
for chaque match:
    for chaque joueur (0-9):
        extraire {
            championId, championName, position, teamId,
            kills, deaths, assists, gold, cs, damage,
            visionScore, firstBlood, firstTower, win
        }

# 2. Regroupement par position
for chaque match:
    for chaque lane in [TOP, JUNGLE, MID, BOT, SUP]:
        if exactement 2 joueurs sur cette lane:
            joueurA = équipe0
            joueurB = équipe1
            
            créer_matchup {
                champA vs champB,
                winA, winB,
                goldDiff = goldA - goldB,
                csDiff = csA - csB,
                damageDiff = damageA - damageB,
                visionDiff = visionA - visionB,
                
                # Features calculées
                kdaA = (killsA + assistsA) / deathsA,
                kdaB = (killsB + assistsB) / deathsB,
                kpA = kill_participation_A,
                kpB = kill_participation_B,
                damageShareA = damage_A / team_total_damage,
                damageShareB = damage_B / team_total_damage
            }
```

#### Sortie : `matchUp.csv`

**Structure** (46 colonnes) :
| Catégorie | Colonnes |
|-----------|----------|
| **Identification** | matchId, lane, champA, champB, champA_id, champB_id |
| **Résultats** | winA, winB, teamA_win, teamB_win |
| **Différences** | goldDiff, csDiff, damageDiff, visionDiff |
| **Stats Joueur A** | killsA, deathsA, assistsA, visionA, kdaA, kpA, damageShareA |
| **Stats Joueur B** | killsB, deathsB, assistsB, visionB, kdaB, kpB, damageShareB |
| **Équipes** | teamA_kills, teamB_kills, teamA_totalDamage, teamB_totalDamage |
| **Objectifs** | teamA_firstBlood, teamB_firstBlood, teamA_firstTower, teamB_firstTower |
| **Participation** | firstBloodPartA, firstBloodPartB, firstTowerPartA, firstTowerPartB |
| **Meta** | gameDuration |

**Exemple de matchup** :
```csv
matchId,lane,champA,champB,winA,winB,goldDiff,csDiff,damageDiff,kdaA,kdaB
EUW1_12345,MID,Zed,Yasuo,1,0,+450,+23,+2340,9.2,6.8
```

**Statistiques** :
- **~47 MB** de données
- **Thousands de matchups** uniques
- Filtrage par lane pour pertinence

---

## 🤖 L'Application IA

### Fichier : `app.py`

**Framework** : Streamlit (interface web Python)

**IA** : Google Gemini (modèle génératif)

---

### Architecture de l'Application

```
┌─────────────────────────────────────────┐
│          INTERFACE STREAMLIT            │
├─────────────────────────────────────────┤
│                                         │
│  SIDEBAR               MAIN AREA        │
│  ┌─────────┐          ┌─────────────┐  │
│  │ Rôle    │          │   Chat      │  │
│  │ Alliés  │          │   History   │  │
│  │ Ennemis │          │             │  │
│  │ [Submit]│          │ Messages    │  │
│  └─────────┘          └─────────────┘  │
│       │                      ↑          │
│       └──────────────────────┘          │
│                                         │
└─────────────────────────────────────────┘
         │
         ↓
┌─────────────────────────────────────────┐
│      FONCTION get_champion_recommendations│
├─────────────────────────────────────────┤
│  1. Chargement champStats.csv           │
│  2. Chargement matchUp.csv              │
│  3. Filtrage par rôle                   │
│  4. Filtrage par ennemis (si fournis)   │
│  5. Limitation à 500 matchups max       │
│  6. Conversion en format CSV texte      │
│  7. Construction du prompt              │
│  8. Appel API Gemini                    │
│  9. Retour des recommandations          │
└─────────────────────────────────────────┘
         │
         ↓
┌─────────────────────────────────────────┐
│         GEMINI AI (Google)              │
│   Analyse contextuelle + génération     │
└─────────────────────────────────────────┘
```

---

### Interface Utilisateur

#### Sidebar (Formulaire de saisie)

**Champs disponibles** :
1. **Rôle** (obligatoire) : Dropdown avec 5 options
   - TOP, JUNGLE, MID, BOT, SUP
   
2. **Champions Alliés** (optionnel) : Input texte
   - Format : "Yasuo, Lulu, Jinx"
   - Séparés par virgules
   
3. **Champions Ennemis** (optionnel) : Input texte
   - Format : "Teemo, Sylas, Zed"
   - Séparés par virgules

4. **Bouton** : "🎯 Obtenir des recommandations"

**Design** :
- Thème sombre (noir/gris) pour ambiance gaming
- Dégradés cyan (#0BC5EA) et violet (#805AD5)
- Animations CSS sur les boutons
- Émojis pour meilleure lisibilité

#### Zone Principale (Chat)

**Format conversationnel** :
- Messages utilisateur (avatar 👤)
- Messages assistant (avatar 🤖)
- Historique complet des échanges
- Markdown avec formatage riche

**Fonctionnalités** :
- Scroll automatique
- Bouton "Effacer la conversation"
- Message de bienvenue explicatif

---

### Logique de l'IA

#### Phase 1 : Préparation des Données

```python
def get_champion_recommendations(role, allied_champions, enemy_champions):
    # 1. Charger les fichiers CSV
    champ_stats = pd.read_csv("data/champStats.csv")
    matchups = pd.read_csv("data/matchUp.csv")
    
    # 2. Filtrer par rôle
    role_matchups = matchups[matchups['lane'] == role.upper()]
    
    # 3. Filtrer par ennemis si spécifiés
    if enemy_champions:
        role_matchups = role_matchups[
            role_matchups['champB'].isin(enemy_champions)
        ]
    
    # 4. Limiter à 500 matchups (limite de tokens Gemini)
    if len(role_matchups) > 500:
        role_matchups = role_matchups.tail(500)
    
    # 5. Convertir en CSV texte
    stats_csv = champ_stats.to_csv(index=False)
    matchups_csv = role_matchups.to_csv(index=False)
```

**Pourquoi 500 matchups ?**
- Limite de tokens de l'API Gemini
- Compromis entre contexte et performance
- Les 500 derniers matchups sont les plus récents

#### Phase 2 : Construction du Prompt

**Structure du prompt** :

```
=== CONTEXTE SYSTÈME ===
Vous êtes un coach professionnel de League of Legends.
Analysez les statistiques et matchups pour recommander 5 champions.

=== STATISTIQUES GLOBALES DES CHAMPIONS ===
[CSV complet de champStats.csv]

=== MATCHUPS POUR {ROLE} ===
[CSV filtré de matchUp.csv]

=== VOTRE MISSION ===
Rôle demandé : {role}
Champions alliés : {allied_champions}
Champions ennemis : {enemy_champions}

Recommandez 5 champions pour ce rôle en analysant :
1. Les statistiques globales (winrate, KDA, dégâts)
2. Les matchups favorables contre les ennemis
3. Les synergies avec les alliés
4. La performance dans le rôle

Pour chaque champion, fournissez :
- Nom du champion
- Statistiques clés
- Raisons de le choisir (matchups, synergies, forces)
- Conseils stratégiques

Formatez avec des émojis pour la lisibilité.
```

**Éléments clés du prompt** :
- ✅ **Rôle clair** : "Vous êtes un coach professionnel"
- ✅ **Données structurées** : CSV directement dans le prompt
- ✅ **Instructions précises** : 4 critères d'analyse
- ✅ **Format de sortie** : Structure attendue
- ✅ **Ton** : Professionnel mais accessible

#### Phase 3 : Appel API Gemini

```python
# Initialisation du client
client = genai.Client(api_key=GEMINI_API_KEY)

# Envoi de la requête
response = client.models.generate_content(
    model='gemini-2.0-flash-exp',
    contents=prompt
)

# Récupération de la réponse
recommendations = response.text
```

**Modèle utilisé** : `gemini-2.0-flash-exp`
- Rapide (latence faible)
- Bonne capacité d'analyse
- Génération de texte structuré
- Gratuit pour usage modéré

#### Phase 4 : Retour à l'Utilisateur

La réponse de Gemini est formatée en Markdown et affichée dans le chat avec :
- Titres et sous-titres
- Émojis contextuels
- Bullet points
- Mise en gras des éléments importants

---

### Critères d'Analyse de l'IA

L'IA Gemini évalue les champions selon 4 axes principaux :

#### 1. 📊 Statistiques Globales (champStats.csv)

**Métriques analysées** :
- **Winrate** : Taux de victoire (ex: 52.16%)
  - > 52% = Excellent
  - 50-52% = Bon
  - < 50% = Faible
  
- **KDA** : (Kills + Assists) / Deaths
  - > 3.0 = Très bon
  - 2.0-3.0 = Moyen
  - < 2.0 = Faible
  
- **Dégâts moyens** : Impact en teamfight
- **Or moyen** : Efficacité en farming

**Exemple** :
```
Champion: Pantheon
Winrate: 50.15% ✓
KDA: 7.13/6.05/7.73 = 2.46 ✓
Dégâts: 18,234 ✓
→ Performances solides
```

#### 2. ⚔️ Matchups Favorables (matchUp.csv)

**Analyse des confrontations directes** :
- Nombre de victoires vs défaites contre chaque ennemi
- Différence d'or moyenne (goldDiff)
- Différence de CS (csDiff)
- Différence de dégâts (damageDiff)

**Exemple** :
```
Pantheon vs Sylas (JUNGLE)
- 3 victoires, 0 défaites (100% winrate)
- goldDiff moyen: +890
- damageDiff moyen: +3,450
→ Matchup très favorable
```

#### 3. 🤝 Synergies avec Alliés

**Analyse des combos et interactions** :
- Champions avec crowd control (CC) pour Yasuo
- Champions avec shields/buffs pour assassins
- Champions avec engage pour ADC

**Exemple** :
```
Pantheon + Yasuo
- Pantheon W (stun) = knock-up
- Yasuo R (Last Breath) activable
- Synergie "pick-and-play" forte
→ Combo dévastateur
```

#### 4. 🎯 Performance dans le Rôle

**Critères spécifiques au rôle** :

**JUNGLE** :
- Early game fort (ganks précoces)
- Mobilité pour clear/ganks
- Contrôle d'objectifs (dragons, barons)

**MID** :
- Roaming pour aider les lanes
- Burst damage ou DPS constant
- Wave clear rapide

**TOP** :
- Tankiness ou split push
- TP plays efficaces
- 1v1 dominant

**BOT** :
- Scaling en late game
- Positionnement safe
- DPS élevé

**SUPPORT** :
- Crowd control (CC)
- Vision control
- Peel pour l'ADC

---

### Gestion des Erreurs

**Erreurs possibles et solutions** :

1. **Clé API manquante**
```
❌ Erreur : La clé API GEMINI n'est pas définie
→ Solution : Créer fichier .env avec GEMINI_API_KEY=xxx
```

2. **Fichiers CSV manquants**
```
❌ Erreur : Fichier de données manquant
→ Solution : Vérifier que champStats.csv et matchUp.csv existent
```

3. **Rôle non sélectionné**
```
⚠️ Veuillez sélectionner un rôle
→ Solution : Choisir TOP, JUNGLE, MID, BOT ou SUP
```

4. **Limite de tokens dépassée**
```
→ Solution automatique : Limitation à 500 matchups
```

5. **Format CSV invalide**
```
❌ Erreur : Unsupported MIME type
→ Solution : Conversion CSV en texte brut
```

---

## 🎯 Résultats et Démonstration

### Exemple de Cas d'Usage

**Scénario** :
- **Votre rôle** : JUNGLE
- **Champions alliés déjà choisis** : Yasuo (TOP), Lulu (SUP)
- **Champions ennemis révélés** : Teemo (TOP), Sylas (MID)
- **Objectif** : Trouver un jungler qui synergie avec Yasuo/Lulu et counter Sylas

---

### Recommandations de l'IA

#### 🥇 Recommandation #1 : Pantheon

**📊 Statistiques Clés**
- Winrate Global : **50.15%** (équilibré)
- KDA Moyen : **7.13 / 6.05 / 7.73**
- Performance : Bon early game, excellentes assistances

**⚔️ Matchups Favorables**
- **vs Sylas** : 3 victoires - 0 défaites
  - goldDiff moyen : +890
  - damageDiff moyen : +3,450
  - **Analyse** : Pantheon domine Sylas grâce à son burst et son stun
  
- **vs Teemo** : 1 victoire (matchup gérable)
  - Capacité à burst les cibles squishies

**🤝 Synergies avec Alliés**
- **Yasuo** :
  - ✅ Pantheon W (Bouclier Zénithal) = stun ciblé
  - ✅ Stun = knock-up pour Yasuo R (Last Breath)
  - ✅ Combo "pick-and-play" ultra-fort
  
- **Lulu** :
  - ✅ Lulu peut le buffer (vitesse d'attaque, bouclier, HP)
  - ✅ Permet des dives agressives plus sécurisées
  - ✅ Augmente son impact mid-game

**💪 Forces**
- Excellent early game (ganks niveau 3-6)
- Capacité à snowball rapidement
- Présence globale avec R (Grand Ciel)
- Tank/bruiser : peut initier les teamfights

**💡 Conseils Stratégiques**
- Abusez de l'early game pour mettre la pression sur Sylas
- Priorisez les ganks sur Yasuo (lane TOP)
- Utilisez votre ultime pour des rotations rapides
- Visez les engagements sur cibles isolées

---

#### 🥈 Recommandation #2 : Talon

**📊 Statistiques Clés**
- Winrate Global : **51.3%** (très bon)
- KDA Moyen : **8.68 / 5.72 / 6.53**
- Performance : Excellent pour les kills, mobilité hors pair

**⚔️ Matchups Favorables**
- **vs Sylas** : 4 victoires - 1 défaite (80%)
  - goldDiff moyen : +1,240
  - damageDiff moyen : +4,120
  - **Analyse** : Talon assassine Sylas avant qu'il ne puisse réagir
  
- **vs Teemo** : Burst + mobilité = très dangereux pour Teemo

**🤝 Synergies avec Alliés**
- **Lulu** :
  - ✅ Buffs Lulu (Pix, Fantaisie) augmentent son burst
  - ✅ Rend ses dives encore plus létales
  - ✅ Permet d'assassiner les cibles prioritaires
  
- **Yasuo** :
  - ✅ Pas de knock-up direct, mais nettoie la backline
  - ✅ Laisse Yasuo gérer les menaces restantes

**💪 Forces**
- Mobilité exceptionnelle (E - Voie du Traqueur)
- Burst dévastateur en early/mid game
- Excellent pour pick-off les cibles isolées
- Roaming rapide entre lanes

**💡 Conseils Stratégiques**
- Cherchez les opportunités de gank dès niveau 2-3
- Visez Teemo et Sylas en priorité (squishies)
- Utilisez votre mobilité pour contourner la vision
- Coordonnez avec Lulu pour engagements éclairs

---

#### 🥉 Recommandation #3 : Jarvan IV

**📊 Statistiques Clés**
- Winrate Global : **51.44%** (très bon)
- KDA Moyen : **5.71 / 5.16 / 12.02**
- Performance : Énormément d'assistances, excellent engageur

**⚔️ Matchups**
- **vs Sylas** : 5 victoires - 7 défaites (matchup mitigé)
  - Mais apporte utilité et contrôle de foule
  - Peut compenser par l'engage et le tank

**🤝 Synergies avec Alliés**
- **Yasuo** :
  - ✅✅✅ **SYNERGIE CLASSIQUE**
  - ✅ Combo E+Q (Frappe Dragon + Étendard) = knock-up multi-cibles
  - ✅ R (Cataclysme) emprisonne pour Yasuo
  - ✅ Setup parfait pour Last Breath
  
- **Lulu** :
  - ✅ Lulu peut le booster (boucliers, vitesse)
  - ✅ Permet des dives profondes
  - ✅ R de Lulu (Wild Growth) ajoute knock-up dans Cataclysme

**💪 Forces**
- Excellent engageur d'équipe
- Tanky et résistant
- Contrôle de foule multi-cibles
- Peut initier ou protéger les carries

**💡 Conseils Stratégiques**
- Gankez avec combo E+Q pour knock-up Yasuo
- Priorisez les teamfights (votre force)
- Utilisez R pour isoler les carries ennemis
- Buildez tank pour frontline

---

#### 🏅 Recommandation #4 : Lee Sin

**📊 Statistiques Clés**
- Winrate : 49.8%
- KDA : 6.45 / 5.89 / 8.12
- Performance : Playmaker, très mobile

**⚔️ Matchups**
- Early game dominant (peut counter-jungle Sylas)
- Mobilité pour éviter Teemo

**🤝 Synergies**
- **Yasuo** : R (Dragon Rage) = knock-back qui active Yasuo R
- **Lulu** : Boucliers pour sécuriser ses plays agressifs

**💪 Forces**
- Skill ceiling élevé (outplay potential)
- Mobilité extrême (Q, W)
- Playmaking avec R

**💡 Conseils**
- Nécessite un bon niveau mécanique
- Invadez jungle ennemie early
- Utilisez R pour insec (kick dans l'équipe)

---

#### 🎖️ Recommandation #5 : Vi

**📊 Statistiques Clés**
- Winrate : 50.9%
- KDA : 6.78 / 6.23 / 9.45

**⚔️ Matchups**
- Bon contre Sylas (lock avec R)
- Tankiness pour survivre

**🤝 Synergies**
- **Yasuo** : R (Assault and Battery) = knock-up garanti
- **Lulu** : Buffs pour tank damage pendant R

**💪 Forces**
- R point-and-click (ne peut pas fail)
- Clear rapide
- Tank/damage hybride

**💡 Conseils**
- Utilisez R pour lock Sylas ou Teemo
- Farm efficacement avec Q (clear rapide)
- Engage prioritaire sur backline

---

### Analyse de la Réponse

**Pourquoi ces recommandations sont pertinentes ?**

1. **Pantheon & Talon** : Counters directs de Sylas (statistiques prouvées)
2. **Jarvan IV** : Synergie parfaite avec Yasuo (combo knock-up)
3. **Lee Sin & Vi** : Alternatives avec engage/playmaking
4. **Lulu** : Toutes les recommandations peuvent bénéficier de ses buffs

**Diversité des profils** :
- Assassins (Talon)
- Bruisers (Pantheon, Jarvan)
- Tanks engageurs (Jarvan, Vi)
- Playmakers (Lee Sin)

**Adaptabilité** :
- Early game fort (Pantheon, Talon)
- Mid/late game (Jarvan, Vi)
- High skill (Lee Sin) vs Safe picks (Vi)

---

### Métriques de Performance

**Temps de réponse** :
- Chargement des données : ~2 secondes
- Appel API Gemini : ~5-8 secondes
- **Total** : ~10 secondes maximum

**Précision** :
- Recommandations basées sur **données réelles**
- **100 000+ matchs** comme base statistique
- Contexte pris en compte (alliés + ennemis)

**Satisfaction utilisateur** :
- Explications claires et détaillées
- Format lisible (émojis, markdown)
- Conseils actionnables

---

## 🎓 Compétences Acquises

### 1. 📊 Data Engineering & ETL

**Extract (Extraction)** :
- Utilisation d'API REST (Riot Games)
- Gestion de gros volumes de données (100k+ lignes)
- Parsing de structures JSON complexes

**Transform (Transformation)** :
- Nettoyage de données (valeurs manquantes, outliers)
- Agrégations complexes (groupby, pivot)
- Calculs de features (KDA, winrate, différences)
- Normalisation des positions (MIDDLE → MID, UTILITY → SUP)

**Load (Chargement)** :
- Export vers CSV optimisés
- Gestion de fichiers volumineux (~47 MB)
- Structuration pour consommation IA

### 2. 🤖 Intelligence Artificielle

**Prompt Engineering** :
- Construction de prompts efficaces
- Inclusion de données structurées (CSV)
- Instructions claires et précises
- Gestion du contexte (token limits)

**Intégration IA** :
- API Gemini (Google)
- Gestion des réponses asynchrones
- Traitement d'erreurs spécifiques à l'IA
- Optimisation des requêtes (coût/performance)

**Analyse Contextuelle** :
- Prise en compte de variables multiples
- Raisonnement sur données numériques
- Génération de justifications

### 3. 💻 Développement Full Stack

**Backend** :
- Python avancé (Pandas, NumPy)
- Manipulation de DataFrames
- Gestion de fichiers et I/O
- Variables d'environnement (.env)

**Frontend** :
- Streamlit (framework web Python)
- Design responsive
- UX/UI intuitive
- CSS personnalisé
- État de session (session_state)

**Architecture** :
- Séparation des responsabilités
- Fonctions modulaires et réutilisables
- Gestion d'erreurs robuste

### 4. 📈 Data Analysis & Statistics

**Statistiques Descriptives** :
- Moyennes, médianes, écarts-types
- Taux de victoire (winrate)
- Distributions de données

**Métriques de Performance** :
- KDA (Kill/Death/Assist ratio)
- Kill Participation (KP)
- Damage Share
- Gold/CS differences

**Analyse Comparative** :
- Matchups 1v1
- Comparaisons multi-variables
- Identification de patterns

### 5. 🔧 Outils & Méthodologies

**Version Control** :
- Git (commits, branches)
- GitHub (remote repository)
- Documentation (README, GUIDE)

**Environnement de Développement** :
- VS Code / PyCharm
- Debugging Python
- Terminal PowerShell

**Bonnes Pratiques** :
- Code propre et commenté
- Séparation données/code
- Gestion des secrets (API keys)
- Documentation utilisateur

### 6. 🎮 Domain Knowledge

**League of Legends** :
- Compréhension du meta-game
- Connaissance des champions et rôles
- Synergies et matchups
- Stratégie de draft

**Gaming Analytics** :
- Métriques de performance en esport
- Analyse de matchups compétitifs
- Optimisation de sélection

---

## 🚀 Perspectives d'Évolution

### Améliorations Fonctionnelles

#### 1. 🔄 Mise à Jour Automatique des Données

**Problème actuel** : Données statiques (snapshot à un moment T)

**Solution proposée** :
```python
# Scheduler automatique
import schedule

def update_data():
    # 1. Fetch nouveaux matchs via Riot API
    new_matches = riot_api.get_recent_matches(last_update_date)
    
    # 2. Append à matchData.csv
    append_to_csv(new_matches)
    
    # 3. Regénérer champStats.csv et matchUp.csv
    run_csv_champ_maker()
    run_csv_matchup_creator()

# Lancement quotidien à 3h du matin
schedule.every().day.at("03:00").do(update_data)
```

**Bénéfices** :
- Données toujours à jour avec le dernier patch
- Adaptation automatique au meta
- Aucune intervention manuelle

---

#### 2. 📊 Visualisations Interactives

**Ajouts proposés** :
- **Graphiques de winrate** par champion et rôle
- **Heatmaps de matchups** (champion A vs champion B)
- **Timelines de performance** (évolution avec les patches)
- **Radar charts** des statistiques (KDA, Gold, Damage)

**Technologies** :
- Plotly (graphiques interactifs)
- Matplotlib/Seaborn (visualisations statiques)
- Streamlit charts (intégration native)

**Exemple** :
```python
import plotly.express as px

# Heatmap des matchups
fig = px.imshow(
    matchup_matrix,
    labels=dict(x="Champion B", y="Champion A", color="Winrate"),
    x=champion_names,
    y=champion_names,
    color_continuous_scale="RdYlGn"
)
st.plotly_chart(fig)
```

---

#### 3. 🏆 Recommandations par Elo

**Problème** : Un champion fort en Bronze peut être faible en Challenger

**Solution** : Filtrage par rang
```python
def get_recommendations(role, elo="ALL"):
    if elo != "ALL":
        matchups = matchups[matchups['player_rank'] == elo]
        champ_stats = champ_stats_by_elo[elo]
    # ... reste de la logique
```

**Elos à supporter** :
- Iron / Bronze / Silver (bas niveau)
- Gold / Platinum (moyen)
- Diamond / Master (haut niveau)
- Grandmaster / Challenger (pro)

---

#### 4. 🎯 Analyse de Composition 5v5

**Objectif** : Recommander une composition complète optimale

**Critères** :
- **Équilibre des rôles** : Tank, DPS, Support, Engage
- **Synergies d'équipe** : AOE combos, poke comps, split push
- **Win conditions** : Early game, Late game, Teamfight

**Exemple** :
```
Composition recommandée:
TOP: Malphite (engage + tank)
JUNGLE: Jarvan IV (follow-up engage)
MID: Orianna (AOE damage + contrôle)
BOT: Jinx (hypercarry late game)
SUP: Lulu (peel + buffs)

→ Comp teamfight avec engage Malphite R + Jarvan R + Orianna R
→ Protection Jinx avec Lulu pour late game
```

---

#### 5. 🧪 A/B Testing & Validation

**Méthodologie** :
1. Collecter des parties où le joueur utilise LOL Coach
2. Collecter des parties sans recommandations
3. Comparer les winrates

**Métriques** :
- Winrate avec vs sans assistant
- Temps de décision en draft
- Satisfaction utilisateur (sondages)

---

### Optimisations Techniques

#### 1. 🗄️ Migration vers Base de Données SQL

**Problème actuel** : CSV = lent pour requêtes complexes

**Solution** : PostgreSQL ou SQLite
```sql
-- Exemple de requête optimisée
SELECT 
    champA,
    COUNT(*) as games,
    AVG(CASE WHEN winA = 1 THEN 1 ELSE 0 END) as winrate,
    AVG(goldDiff) as avg_gold_diff
FROM matchups
WHERE lane = 'MID' 
  AND champB IN ('Zed', 'Yasuo')
GROUP BY champA
ORDER BY winrate DESC
LIMIT 5;
```

**Bénéfices** :
- Requêtes 10-100x plus rapides
- Indexation pour performance
- Requêtes complexes facilitées
- Scalabilité

---

#### 2. ⚡ Cache des Recommandations

**Problème** : Mêmes requêtes = mêmes appels API coûteux

**Solution** : Système de cache
```python
import hashlib
import json

cache = {}

def get_recommendations_cached(role, allies, enemies):
    # Générer clé unique
    cache_key = hashlib.md5(
        f"{role}_{allies}_{enemies}".encode()
    ).hexdigest()
    
    # Vérifier cache
    if cache_key in cache:
        return cache[cache_key]
    
    # Sinon, appeler l'IA
    result = get_champion_recommendations(role, allies, enemies)
    cache[cache_key] = result
    
    return result
```

**Bénéfices** :
- Économie d'appels API (coût réduit)
- Réponse instantanée pour requêtes répétées
- Meilleure UX

---

#### 3. ☁️ Déploiement Cloud

**Options** :
1. **Streamlit Cloud** (gratuit)
   - Déploiement direct depuis GitHub
   - HTTPS automatique
   - Facile à configurer

2. **Heroku** (freemium)
   - Plus de contrôle
   - Dyno toujours actif

3. **AWS / GCP** (production)
   - Scalabilité maximale
   - Coût plus élevé

**Processus de déploiement** :
```bash
# 1. Préparer requirements.txt
pip freeze > requirements.txt

# 2. Créer Procfile (Heroku)
web: streamlit run app.py --server.port=$PORT

# 3. Push vers Git
git push heroku main

# 4. Accès public
https://lol-coach.herokuapp.com
```

---

#### 4. 🔒 Sécurité & Authentification

**Améliorations** :
- **Authentification utilisateur** (comptes)
- **Rate limiting** (limiter les appels API)
- **Encryption des clés API**
- **HTTPS obligatoire**

**Exemple** :
```python
import streamlit_authenticator as stauth

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key']
)

name, authentication_status, username = authenticator.login('Login', 'main')

if authentication_status:
    st.write(f'Bienvenue {name}')
    # ... app normale
```

---

#### 5. 🧠 Fine-Tuning d'un Modèle Spécialisé

**Objectif** : Créer un modèle IA spécifiquement entraîné sur LoL

**Processus** :
1. Créer un dataset labellisé
   - Input : rôle, alliés, ennemis, stats
   - Output : top 5 champions + justifications

2. Fine-tuner un modèle (Llama, GPT, Gemini)
   - Utiliser les données historiques
   - Optimiser pour le domaine LoL

3. Déployer le modèle custom
   - API locale ou cloud
   - Latence réduite

**Bénéfices** :
- Meilleure précision (domain-specific)
- Pas de dépendance à API externe
- Coût réduit sur le long terme

---

### Fonctionnalités Avancées

#### 1. 🎙️ Interface Vocale

**Intégration Speech-to-Text** :
```python
import speech_recognition as sr

def voice_input():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        audio = recognizer.listen(source)
        text = recognizer.recognize_google(audio, language='fr-FR')
        return text

# Usage pendant le draft
voice_query = voice_input()
# "Je cherche un jungler avec Yasuo contre Sylas"
```

**Bénéfices** :
- Mains libres pendant le draft
- Plus rapide que taper
- Accessibilité

---

#### 2. 📱 Application Mobile

**Technologies** :
- React Native ou Flutter
- API REST backend (Flask/FastAPI)

**Fonctionnalités** :
- Notifications push (patch notes)
- Mode hors-ligne (cache)
- Intégration avec l'app Riot officielle

---

#### 3. 🤖 Discord Bot

**Intégration Discord** :
```python
import discord

bot = discord.Client()

@bot.command(name='draft')
async def draft_command(ctx, role, allies, enemies):
    recommendations = get_recommendations(role, allies, enemies)
    await ctx.send(recommendations)

# Usage: !draft jungle "Yasuo,Lulu" "Sylas,Teemo"
```

**Bénéfices** :
- Accessible pendant que LoL est ouvert
- Partage avec l'équipe Discord
- Commandes rapides

---

#### 4. 📧 Système de Notifications

**Alertes personnalisées** :
- Nouveaux patchs LoL détectés
- Changements majeurs du meta
- Nouveaux champions ajoutés

---

#### 5. 🏅 Système de Succès & Gamification

**Fonctionnalités** :
- Tracker de winrate avec les recommandations
- Badges (utilisateur régulier, etc.)
- Leaderboard de la communauté
- Partage sur réseaux sociaux

---

## 🎬 Conclusion

### Synthèse du Projet

**LOL Coach** est un système complet de recommandation de champions pour League of Legends qui combine :
- **Data Engineering** : Extraction et traitement de 100 000+ matchs
- **Intelligence Artificielle** : Analyse contextuelle par Gemini
- **Full Stack Development** : Interface web intuitive avec Streamlit

### Résultats Clés

✅ **Fonctionnel** : Application complète et opérationnelle
✅ **Pertinent** : Recommandations basées sur données réelles
✅ **Évolutif** : Architecture permettant extensions futures
✅ **Pédagogique** : Explications détaillées pour apprendre

### Apports du Projet

**Pour les joueurs** :
- Aide à la décision en draft
- Apprentissage des matchups
- Découverte de champions méconnus

**Pour le développeur** :
- Compétences en data science
- Maîtrise des APIs d'IA
- Expérience full stack

**Pour la communauté** :
- Outil open-source réutilisable
- Base pour d'autres projets gaming analytics
- Documentation complète

---

## 📚 Annexes

### Bibliographie

**APIs & Documentation** :
- Riot Games Developer Portal : https://developer.riotgames.com/
- Google Gemini AI : https://ai.google.dev/
- Streamlit Documentation : https://docs.streamlit.io/
- Pandas User Guide : https://pandas.pydata.org/docs/

**Ressources League of Legends** :
- OP.GG (stats site) : https://op.gg/
- U.GG (champion builds) : https://u.gg/
- Lolalytics (analytics) : https://lolalytics.com/

**Technologies** :
- Python 3.11+ : https://www.python.org/
- Google Colab : https://colab.research.google.com/

---

### Structure des Fichiers

```
ProjetLoLCoach/
│
├── app.py                      # Application Streamlit principale
├── chatbot.py                  # Version console du chatbot
├── csv_champ_maker.py          # Script d'extraction stats champions
├── csv_matchup_creator.py      # Script création matchups
├── display_results.py          # Affichage formaté des résultats
│
├── requirements.txt            # Dépendances Python
├── .env                        # Variables d'environnement (API keys)
├── .gitignore                  # Fichiers à ignorer par Git
│
├── README.md                   # Présentation courte du projet
├── GUIDE.md                    # Guide d'utilisation détaillé
├── PRESENTATION.md             # Plan de présentation + Prompt Gamma
├── PRESENTATION_COMPLETE.md    # Présentation complète (ce fichier)
│
├── data/
│   ├── matchData.csv           # Données brutes (100k+ matchs, API Riot)
│   ├── champStats.csv          # Stats agrégées des 173 champions
│   ├── matchUp.csv             # Base matchups 1v1 (~47 MB)
│   ├── columns.txt             # Liste des 1771 colonnes de matchData
│   └── results.txt             # Exemple de sortie du chatbot
│
├── models/                     # (Réservé pour futurs modèles ML)
│
└── sample.ipynb                # Notebook Jupyter d'exploration
```

---

### Commandes Utiles

**Installation** :
```powershell
# Cloner le repo
git clone https://github.com/votre-username/ProjetLoLCoach.git
cd ProjetLoLCoach

# Créer environnement virtuel
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Installer dépendances
pip install -r requirements.txt

# Configurer API key
echo "GEMINI_API_KEY=votre_cle_ici" > .env
```

**Exécution** :
```powershell
# Lancer l'application web
streamlit run app.py

# Lancer le chatbot console
python chatbot.py

# Regénérer les fichiers CSV
python csv_champ_maker.py
python csv_matchup_creator.py
```

**Maintenance** :
```powershell
# Mettre à jour les dépendances
pip install --upgrade -r requirements.txt

# Vérifier les erreurs
python -m pylint *.py

# Formater le code
python -m black *.py
```

---

### Contact & Contributions

**Auteur** : [Votre Nom]
**Email** : [Votre Email]
**GitHub** : [Votre GitHub]
**LinkedIn** : [Votre LinkedIn]

**Contributions** :
Ce projet est open-source. Les pull requests sont les bienvenues !

**License** : MIT

---

## 💬 Questions Fréquentes (FAQ)

### Q1 : Pourquoi Gemini et pas un modèle custom ?
**R** : Gemini offre :
- Rapidité de développement (pas besoin d'entraîner un modèle)
- Qualité des explications (génération de texte naturel)
- Pas besoin de données labellisées
- API simple à utiliser

### Q2 : Les recommandations sont-elles fiables ?
**R** : Oui, car basées sur **100 000+ matchs réels**. L'IA analyse des patterns statistiques, pas des opinions subjectives.

### Q3 : Comment gérez-vous les nouveaux patchs ?
**R** : Actuellement données statiques, mais l'architecture permet une re-extraction facile via l'API Riot.

### Q4 : Combien coûte l'utilisation de l'API Gemini ?
**R** : Gemini offre un tier gratuit généreux (60 requêtes/minute). Pour usage intensif, voir la tarification Google AI.

### Q5 : Puis-je utiliser ce projet pour d'autres jeux ?
**R** : Oui ! L'architecture est transposable à :
- Dota 2
- Valorant
- Counter-Strike
- Overwatch
(Il faut adapter l'extraction de données et les métriques)

---

## 🎤 Script de Présentation Orale

### Introduction (1 minute)

> "Bonjour ! Aujourd'hui je vais vous présenter **LOL Coach**, un assistant intelligent pour optimiser la phase de draft dans League of Legends.
>
> League of Legends compte 180 champions, et pendant le draft, les joueurs ont seulement 5 minutes pour choisir le bon champion en tenant compte des alliés, des ennemis, et des statistiques.
>
> Mon projet utilise l'intelligence artificielle pour analyser plus de 100 000 matchs et recommander les 5 meilleurs choix avec des justifications détaillées."

### Démonstration (2 minutes)

> "Laissez-moi vous montrer comment ça fonctionne. [Ouvrir l'application]
>
> Je sélectionne mon rôle : JUNGLE. J'ai déjà Yasuo et Lulu dans mon équipe, et l'ennemi a Sylas et Teemo.
>
> Je clique sur 'Obtenir des recommandations'... [Attendre 10 secondes]
>
> Et voici ! L'IA me recommande Pantheon en premier car il a un winrate de 100% contre Sylas dans mes données, et son stun synergie parfaitement avec Yasuo pour le combo knock-up.
>
> Chaque recommandation inclut les statistiques, les matchups favorables, et des conseils stratégiques."

### Conclusion (30 secondes)

> "En résumé, ce projet combine data engineering, intelligence artificielle et développement full stack pour créer un outil réellement utile aux joueurs.
>
> Les perspectives incluent des mises à jour automatiques, des visualisations, et une migration vers une architecture cloud.
>
> Merci ! Avez-vous des questions ?"

---

**FIN DE LA PRÉSENTATION COMPLÈTE**

🎮 Bon courage pour votre présentation ! 🚀

