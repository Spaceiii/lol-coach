from google import genai
from google.genai import types
import os
from dotenv import load_dotenv
import pandas as pd
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich import box


def get_champion_recommendations(role, allied_champions=None, enemy_champions=None):
    """
    Recommande 5 champions pour un rôle donné en tenant compte des alliés et ennemis.

    Args:
        role: Le rôle/lane (TOP, JUNGLE, MID, BOT, SUP)
        allied_champions: Liste des champions alliés déjà choisis (optionnel)
        enemy_champions: Liste des champions ennemis (optionnel)

    Returns:
        La réponse du modèle avec les 5 champions recommandés et leurs justifications
    """
    # Récupérer la clé API depuis les variables d'environnement
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError(
            "La clé API GEMINI n'est pas définie. "
            "Veuillez définir la variable d'environnement GEMINI_API_KEY"
        )

    client = genai.Client(api_key=api_key)

    print("📊 Chargement et filtrage des données...")

    # Charger les statistiques des champions
    champ_stats = pd.read_csv("data/champStats.csv")

    # Charger et filtrer les matchups pour le rôle spécifique
    matchups = pd.read_csv("data/matchUp.csv")
    role_matchups = matchups[matchups['lane'] == role.upper()].copy()

    # Si des champions ennemis sont spécifiés, filtrer les matchups pertinents
    if enemy_champions:
        role_matchups = role_matchups[
            role_matchups['champB'].isin(enemy_champions)
        ]

    # Limiter à un échantillon raisonnable pour éviter de dépasser les limites de tokens
    if len(role_matchups) > 500:
        role_matchups = role_matchups.tail(500)

    print(f"✓ Données préparées: {len(champ_stats)} champions, {len(role_matchups)} matchups pour {role.upper()}")

    # Convertir les dataframes en format texte CSV compact
    stats_csv = champ_stats.to_csv(index=False)
    matchups_csv = role_matchups.to_csv(index=False)

    # Définir le contexte système
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

    # Construire la requête avec les données intégrées
    query_parts = []

    query_parts.append("=== STATISTIQUES GLOBALES DES CHAMPIONS ===")
    query_parts.append(stats_csv)
    query_parts.append("\n=== MATCHUPS POUR " + role.upper() + " ===")
    query_parts.append(matchups_csv)
    query_parts.append("\n=== VOTRE MISSION ===")
    query_parts.append(f"Rôle demandé : {role.upper()}")

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

    # Générer une réponse
    print("\n🔍 Analyse en cours...\n")
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=query,
        config=types.GenerateContentConfig(
            system_instruction=context,
            temperature=0.7
        )
    )

    return response.text


def main():
    """
    Exemple d'utilisation avec des paramètres de test.
    Modifiez les valeurs ci-dessous ou appelez get_champion_recommendations() directement.
    """
    console = Console()

    # Afficher l'en-tête
    console.print("\n")
    header = Panel(
        "[bold white on blue]🎮 LOL COACH - RECOMMANDATIONS DE CHAMPIONS 🎮[/bold white on blue]",
        box=box.DOUBLE,
        border_style="bright_blue"
    )
    console.print(header)

    # Obtenir les recommandations
    result = get_champion_recommendations(
        role="JUNGLE",
        allied_champions=["Yasuo", "Lulu"],
        enemy_champions=["Teemo", "Sylas"]
    )

    # Afficher les résultats avec formatage Markdown
    console.print("\n")
    md = Markdown(result)
    console.print(Panel(
        md,
        title="[bold cyan]📋 Analyse Détaillée[/bold cyan]",
        border_style="cyan",
        box=box.ROUNDED,
        padding=(1, 2)
    ))
    console.print("\n")


if __name__ == "__main__":
    main()

