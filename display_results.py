"""
Script pour afficher les recommandations de champions avec un formatage visuel riche.
"""
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.markdown import Markdown
from rich.text import Text
from rich import box
from rich.layout import Layout
from rich.align import Align


def display_champion_recommendations():
    """
    Affiche les recommandations de champions de manière visuellement attractive.
    """
    console = Console()

    # Bannière d'en-tête
    console.print("\n")
    header = Text("🎮 COACH LOL - RECOMMANDATIONS DE CHAMPIONS 🎮", style="bold white on blue", justify="center")
    console.print(Panel(header, box=box.DOUBLE, border_style="bright_blue"))

    # Introduction
    intro = """
    **Analyse pour JUNGLE** avec **Yasuo** et **Lulu** face à **Teemo** et **Sylas**
    
    Objectif: Maximiser les synergies et contrer les picks ennemis
    """
    console.print(Panel(Markdown(intro), title="[bold cyan]📋 Contexte[/bold cyan]", border_style="cyan"))

    # Données des champions
    champions = [
        {
            "name": "Pantheon",
            "emoji": "🛡️",
            "id": 80,
            "winrate": "50.15%",
            "kda": "7.13/6.05/7.73",
            "matchups": "Excellent contre Sylas (3-0)",
            "synergie_yasuo": "Stun ciblé pour setup ultime",
            "synergie_lulu": "Buffs pour plonger agressivement",
            "forces": "Excellent early-game, snowball, présence globale",
            "conseils": "Abusez de l'early-game, priorisez les ganks avec Yasuo"
        },
        {
            "name": "Talon",
            "emoji": "🗡️",
            "id": 91,
            "winrate": "51.3%",
            "kda": "8.68/5.72/6.53",
            "matchups": "Excellent contre Sylas (4-1)",
            "synergie_yasuo": "Nettoyage de la backline",
            "synergie_lulu": "Buffs pour augmenter le burst",
            "forces": "Mobilité exceptionnelle, burst dévastateur",
            "conseils": "Cherchez les ganks early, visez Teemo et Sylas"
        },
        {
            "name": "Jarvan IV",
            "emoji": "🦅",
            "id": 59,
            "winrate": "51.44%",
            "kda": "5.71/5.16/12.02",
            "matchups": "Mitigé contre Sylas (5-7)",
            "synergie_yasuo": "Combo E+Q = knock-up parfait",
            "synergie_lulu": "Boucliers pour survivre aux engages",
            "forces": "Excellent engageur, tanky, contrôle de foule",
            "conseils": "Gank avec combo E+Q, priorisez les teamfights avec Yasuo"
        },
        {
            "name": "Master Yi",
            "emoji": "🥷",
            "id": 11,
            "winrate": "52.16%",
            "kda": "8.62/6.11/5.34",
            "matchups": "Équilibré contre Sylas (3-3)",
            "synergie_yasuo": "Double carry potentiel",
            "synergie_lulu": "Combo hyper-carry imparable",
            "forces": "Excellent scaling, potentiel carry incroyable",
            "conseils": "Farm efficacement, évitez les combats inutiles en early"
        },
        {
            "name": "Qiyana",
            "emoji": "🌬️",
            "id": 246,
            "winrate": "51.0%",
            "kda": "7.85/5.91/6.33",
            "matchups": "Excellent contre Sylas (6-2)",
            "synergie_yasuo": "Ultime contre mur = knock-up",
            "synergie_lulu": "Bouclier + vitesse pour dive",
            "forces": "Burst élevé, grande mobilité, contrôle de zone",
            "conseils": "Maîtrisez les éléments, isolez les cibles prioritaires"
        }
    ]

    # Afficher chaque champion
    for i, champ in enumerate(champions, 1):
        console.print("\n")

        # Créer un tableau pour les statistiques
        stats_table = Table(show_header=False, box=box.SIMPLE, padding=(0, 1))
        stats_table.add_column("Stat", style="cyan", width=15)
        stats_table.add_column("Value", style="white")

        stats_table.add_row("📊 WinRate", f"[green bold]{champ['winrate']}[/green bold]")
        stats_table.add_row("⚔️ KDA", f"[yellow]{champ['kda']}[/yellow]")
        stats_table.add_row("🎯 Matchups", f"[magenta]{champ['matchups']}[/magenta]")

        # Créer un tableau pour les synergies
        synergie_table = Table(show_header=False, box=box.SIMPLE, padding=(0, 1))
        synergie_table.add_column("Type", style="cyan", width=15)
        synergie_table.add_column("Description", style="white")

        synergie_table.add_row("🤝 Yasuo", champ['synergie_yasuo'])
        synergie_table.add_row("✨ Lulu", champ['synergie_lulu'])
        synergie_table.add_row("💪 Forces", champ['forces'])
        synergie_table.add_row("💡 Conseils", f"[italic]{champ['conseils']}[/italic]")

        # Créer le layout pour ce champion
        champion_content = Table.grid(padding=1)
        champion_content.add_column()
        champion_content.add_row(stats_table)
        champion_content.add_row(synergie_table)

        # Afficher le panel du champion
        title = f"[bold white]{i}. {champ['emoji']} {champ['name']}[/bold white] [dim](ID: {champ['id']})[/dim]"
        console.print(Panel(
            champion_content,
            title=title,
            border_style="bright_yellow" if i <= 3 else "yellow",
            box=box.ROUNDED
        ))

    # Footer avec résumé
    console.print("\n")
    footer_text = Text.from_markup(
        "Ces champions offrent une excellente combinaison de synergies et de matchups favorables.\n"
        "La clé sera la coordination et l'exécution en jeu ! 🏆",
        justify="center"
    )
    console.print(Panel(
        Align.center(footer_text),
        title="[bold green]✅ Conclusion[/bold green]",
        border_style="green",
        box=box.DOUBLE
    ))
    console.print("\n")


def display_from_file(filepath="data/results.txt"):
    """
    Affiche le contenu du fichier results.txt avec un formatage riche en Markdown.
    """
    console = Console()

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Afficher avec le rendu Markdown de Rich
        console.print("\n")
        md = Markdown(content)
        console.print(md)

    except FileNotFoundError:
        console.print(f"[bold red]❌ Erreur:[/bold red] Le fichier {filepath} n'a pas été trouvé.")
    except Exception as e:
        console.print(f"[bold red]❌ Erreur:[/bold red] {str(e)}")


if __name__ == "__main__":
    import sys

    console = Console()

    # Menu de sélection
    console.print("\n[bold cyan]Choisissez le mode d'affichage:[/bold cyan]")
    console.print("1. Affichage structuré avec tableaux")
    console.print("2. Affichage Markdown depuis results.txt")

    if len(sys.argv) > 1:
        choice = sys.argv[1]
    else:
        choice = input("\nVotre choix (1 ou 2): ").strip()

    if choice == "1":
        display_champion_recommendations()
    elif choice == "2":
        display_from_file()
    else:
        console.print("[yellow]⚠️ Affichage par défaut (Markdown)[/yellow]\n")
        display_from_file()

