import csv
import pandas as pd

dataset = pd.read_csv('data/matchData.csv')

df = pd.DataFrame(dataset, columns=dataset.columns)

print("Dataframe chargé !")

champs = {}

for row in df.itertuples():
    for i in range(10):
        champ_name = getattr(row, f'participant{i}ChampionName')
        if champ_name not in champs:
            champs[champ_name] = {
                'champion_id': getattr(row, f'participant{i}ChampionId'),
                'games_played': 0,
                'wins': 0,
                'kills': 0,
                'deaths': 0,
                'assists': 0,
                'gold_earned': 0,
                'damage_dealt': 0,
                'total_heal': 0,
                'total_heals_on_teammates': 0,
            }
        champs[champ_name]['games_played'] += 1
        if getattr(row, f'participant{i}Win'):
            champs[champ_name]['wins'] += 1
        champs[champ_name]['kills'] += getattr(row, f'participant{i}Kills')
        champs[champ_name]['deaths'] += getattr(row, f'participant{i}Deaths')
        champs[champ_name]['assists'] += getattr(row, f'participant{i}Assists')
        champs[champ_name]['gold_earned'] += getattr(row, f'participant{i}GoldEarned')
        champs[champ_name]['damage_dealt'] += getattr(row, f'participant{i}TotalDamageDealtToChampions')
        champs[champ_name]['total_heal'] += getattr(row, f'participant{i}TotalHeal')
        champs[champ_name]['total_heals_on_teammates'] += getattr(row, f'participant{i}TotalHealsOnTeammates')

with open('data/champStats.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['ChampionId', 'ChampionName', 'GamesPlayed', 'ChampionWinRate', 'AvgKills', 'AvgDeaths', 'AvgAssists', 'AvgGoldEarned', 'AvgDamageDealt', 'AvgHeal', 'AvgHealsOnTeammates', 'Wins', 'Kills', 'Deaths', 'Assists', 'GoldEarned', 'DamageDealt', 'TotalHeal', 'TotalHealsOnTeammates'])
    for champ_name, stats in champs.items():
        writer.writerow([
            stats['champion_id'],
            champ_name,
            stats['games_played'],
            str(round(stats['wins']/stats['games_played']*100, 2))+'%',
            round(stats['kills'] / stats['games_played'], 2),
            round(stats['deaths'] / stats['games_played'], 2),
            round(stats['assists'] / stats['games_played'], 2),
            round(stats['gold_earned'] / stats['games_played'], 2),
            round(stats['damage_dealt'] / stats['games_played'], 2),
            round(stats['total_heal'] / stats['games_played'], 2),
            round(stats['total_heals_on_teammates'] / stats['games_played'], 2),
            stats['wins'],
            stats['kills'],
            stats['deaths'],
            stats['assists'],
            stats['gold_earned'],
            stats['damage_dealt'],
            stats['total_heal'],
            stats['total_heals_on_teammates'],
        ])


print("Les stats sont là !")