"""
LOL Coach - Chatbot IA avec Streamlit
Application de recommandation de champions League of Legends
"""

import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Configuration de la page
st.set_page_config(
    page_title="LOL Coach - Assistant IA",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Charger les variables d'environnement
load_dotenv()

# CSS personnalisé
st.markdown("""
<style>
    /* Style principal */
    .main {
        background: linear-gradient(135deg, #0F1419 0%, #1A202C 100%);
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1A202C 0%, #2D3748 100%);
    }

    /* Titres */
    h1 {
        background: linear-gradient(135deg, #0BC5EA 0%, #805AD5 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700;
    }

    /* Boutons */
    .stButton > button {
        background: linear-gradient(135deg, #0BC5EA 0%, #805AD5 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        transition: transform 0.2s ease;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(11, 197, 234, 0.3);
    }

    /* Messages de chat */
    [data-testid="stChatMessage"] {
        background: rgba(26, 32, 44, 0.8);
        border-radius: 12px;
        border: 1px solid rgba(45, 55, 72, 0.5);
        padding: 1rem;
    }

    /* Selectbox et inputs */
    .stSelectbox > div > div {
        background: #2D3748;
        border-radius: 8px;
    }

    .stTextInput > div > div {
        background: #2D3748;
        border-radius: 8px;
    }

    /* Info boxes */
    .stAlert {
        background: rgba(11, 197, 234, 0.1);
        border: 1px solid rgba(11, 197, 234, 0.3);
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

# Initialiser l'état de session
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": """👋 **Bienvenue sur LOL Coach !**

Je suis votre assistant IA pour vous aider à choisir les meilleurs champions en fonction de votre rôle, de vos alliés et de vos ennemis.

**Pour commencer :**
1. Sélectionnez votre rôle dans le menu à gauche
2. Optionnel : Ajoutez vos champions alliés et ennemis
3. Cliquez sur "🎯 Obtenir des recommandations"

Je vous donnerai 5 recommandations personnalisées avec des analyses détaillées ! 🎮
"""
        }
    ]

if "api_key" not in st.session_state:
    st.session_state.api_key = os.getenv("GEMINI_API_KEY")


def get_champion_recommendations(role: str, allied_champions: list = None, enemy_champions: list = None) -> str:
    """
    Recommande 5 champions pour un rôle donné en tenant compte des alliés et ennemis.
    """
    # Vérifier la clé API
    if not st.session_state.api_key:
        return "❌ **Erreur**: La clé API GEMINI n'est pas définie. Veuillez la configurer dans le fichier `.env` ou dans la barre latérale."

    try:
        client = genai.Client(api_key=st.session_state.api_key)

        # Charger les statistiques des champions
        with st.spinner("📊 Chargement des données..."):
            champ_stats = pd.read_csv("data/champStats.csv")
            matchups = pd.read_csv("data/matchUp.csv")

        # Filtrer les matchups pour le rôle spécifique
        role_matchups = matchups[matchups['lane'] == role.upper()].copy()

        # Si des champions ennemis sont spécifiés, filtrer les matchups pertinents
        if enemy_champions:
            role_matchups = role_matchups[role_matchups['champB'].isin(enemy_champions)]

        # Limiter à 500 matchups
        if len(role_matchups) > 500:
            role_matchups = role_matchups.tail(500)

        # Convertir en CSV
        stats_csv = champ_stats.to_csv(index=False)
        matchups_csv = role_matchups.to_csv(index=False)

        # Contexte système
        context = """
        Vous êtes le coach professionnel d'une équipe de League of Legends. 
        Votre tâche est d'analyser les différents matchups entre les champions en fonction de leurs statistiques de jeu.

        Vous devez recommander 5 champions en tenant compte de :
        1. Les statistiques globales du champion (winrate, KDA, dégâts)
        2. Les matchups favorables contre les champions ennemis spécifiés
        3. Les synergies potentielles avec les champions alliés
        4. La performance du champion dans le rôle demandé

        Pour chaque champion recommandé, expliquez clairement POURQUOI le choisir en vous basant sur les données fournies.
        """

        # Construire la requête
        query_parts = [
            "=== STATISTIQUES GLOBALES DES CHAMPIONS ===",
            stats_csv,
            f"\n=== MATCHUPS POUR {role.upper()} ===",
            matchups_csv,
            "\n=== VOTRE MISSION ===",
            f"Rôle demandé : {role.upper()}"
        ]

        if allied_champions:
            query_parts.append(f"Champions alliés : {', '.join(allied_champions)}")

        if enemy_champions:
            query_parts.append(f"Champions ennemis : {', '.join(enemy_champions)}")

        query_parts.append("""
Veuillez recommander 5 champions pour ce rôle en analysant les données ci-dessus.

Pour chaque champion, fournissez :
1. Le nom du champion
2. Ses statistiques clés (winrate, KDA moyen)
3. Les raisons de le choisir (matchups favorables, synergies, forces)
4. Des conseils stratégiques spécifiques

Formatez la réponse de manière claire et structurée avec des émojis pour la rendre plus lisible.
        """)

        query = "\n".join(query_parts)

        # Générer la réponse
        with st.spinner("🤖 Analyse en cours..."):
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=query,
                config=types.GenerateContentConfig(
                    system_instruction=context,
                    temperature=0.7
                )
            )

        return response.text

    except FileNotFoundError as e:
        return f"❌ **Erreur**: Fichier de données manquant - {str(e)}"
    except Exception as e:
        return f"❌ **Erreur**: {str(e)}"


# Sidebar - Configuration
with st.sidebar:
    st.title("🎮 LOL Coach")
    st.markdown("### 📋 Configuration")

    # Sélection du rôle
    role = st.selectbox(
        "Rôle *",
        options=["", "TOP", "JUNGLE", "MID", "BOT", "SUP"],
        help="Sélectionnez votre rôle"
    )

    # Champions alliés
    allied_input = st.text_input(
        "Champions Alliés (optionnel)",
        placeholder="Ex: Yasuo, Lulu, Jinx",
        help="Séparez les champions par des virgules"
    )

    # Champions ennemis
    enemy_input = st.text_input(
        "Champions Ennemis (optionnel)",
        placeholder="Ex: Teemo, Sylas, Zed",
        help="Séparez les champions par des virgules"
    )

    # Bouton de soumission
    if st.button("🎯 Obtenir des recommandations", use_container_width=True):
        if not role:
            st.error("⚠️ Veuillez sélectionner un rôle")
        else:
            # Préparer les données
            allied_champions = [c.strip() for c in allied_input.split(",") if c.strip()] if allied_input else None
            enemy_champions = [c.strip() for c in enemy_input.split(",") if c.strip()] if enemy_input else None

            # Créer le message utilisateur
            user_message = f"Je cherche un champion pour le rôle **{role}**"
            if allied_champions:
                user_message += f"\n\n**Champions alliés :** {', '.join(allied_champions)}"
            if enemy_champions:
                user_message += f"\n\n**Champions ennemis :** {', '.join(enemy_champions)}"

            # Ajouter le message utilisateur
            st.session_state.messages.append({
                "role": "user",
                "content": user_message
            })

            # Obtenir les recommandations
            recommendations = get_champion_recommendations(role, allied_champions, enemy_champions)

            # Ajouter la réponse du bot
            st.session_state.messages.append({
                "role": "assistant",
                "content": recommendations
            })

            # Rerun pour afficher les nouveaux messages
            st.rerun()

    st.markdown("---")

    # Bouton pour effacer la conversation
    if st.button("🗑️ Effacer la conversation", use_container_width=True):
        st.session_state.messages = [st.session_state.messages[0]]  # Garder le message de bienvenue
        st.rerun()

    st.markdown("---")

    # Configuration de la clé API (optionnel)
    with st.expander("⚙️ Configuration API"):
        api_key_input = st.text_input(
            "Clé API Gemini",
            value=st.session_state.api_key if st.session_state.api_key else "",
            type="password",
            help="Votre clé API Gemini"
        )
        if st.button("Sauvegarder", key="save_api_key"):
            st.session_state.api_key = api_key_input
            st.success("✅ Clé API sauvegardée")

    st.markdown("---")

    # Informations
    st.markdown("""
    ### 💡 Comment ça marche ?

    1. Sélectionnez votre rôle
    2. Ajoutez vos alliés (optionnel)
    3. Ajoutez les ennemis (optionnel)
    4. Recevez 5 recommandations personnalisées

    ---

    ### 📊 Données

    - **100k+ matchs** analysés
    - **180+ champions** répertoriés
    - **Stats en temps réel** par rôle

    ---

    Propulsé par **Gemini AI** 🤖
    """)

# Main - Zone de chat
st.title("💬 Conversation")

# Afficher les messages
for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar="🤖" if message["role"] == "assistant" else "👤"):
        st.markdown(message["content"])

# Zone de saisie (désactivée car on utilise le formulaire dans la sidebar)
st.info("👈 Utilisez le formulaire dans la barre latérale pour obtenir des recommandations")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #718096; padding: 1rem;'>
        <p>Propulsé par Gemini AI • Données basées sur 100k+ matchs • v1.0.0</p>
    </div>
    """,
    unsafe_allow_html=True
)