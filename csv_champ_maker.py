import csv
import pandas as pd

dataset = pd.read_csv('data/matchData.csv')

df = pd.DataFrame(dataset, columns=dataset.columns)

champs = {}

for row in df.itertuples():
    for i in range(10):
        champ_name = getattr(row, f'participant{i}ChampionName')
        if champ_name not in champs:
            champs[champ_name] = {
                'games_played': 0,
                'wins': 0,
                'kills': 0,
                'deaths': 0,
                'assists': 0,
                'gold_earned': 0,
                'damage_dealt': 0
            }
        champs[champ_name]['games_played'] += 1
        if getattr(row, f'participant{i}Win'):
            champs[champ_name]['wins'] += 1
        champs[champ_name]['kills'] += getattr(row, f'participant{i}Kills')
        champs[champ_name]['deaths'] += getattr(row, f'participant{i}Deaths')
        champs[champ_name]['assists'] += getattr(row, f'participant{i}Assists')
        champs[champ_name]['gold_earned'] += getattr(row, f'participant{i}GoldEarned')
        champs[champ_name]['damage_dealt'] += getattr(row, f'participant{i}TotalDamageDealtToChampions')

with open('data/champStats.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['ChampionName', 'GamesPlayed', 'Wins', 'Kills', 'Deaths', 'Assists', 'GoldEarned', 'DamageDealt'])
    for champ_name, stats in champs.items():
        writer.writerow([
            champ_name,
            stats['games_played'],
            stats['wins'],
            stats['kills'],
            stats['deaths'],
            stats['assists'],
            stats['gold_earned'],
            stats['damage_dealt']
        ])