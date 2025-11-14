import csv
import pandas as pd

dataset = pd.read_csv('data/matchData.csv')

df = pd.DataFrame(dataset, columns=dataset.columns)

# determine matchup between champions

champs = {}

for row in df.itertuples():
    for i in range(10):
        champ_name = getattr(row, f'participant{i}ChampionName')
        if champ_name not in champs:
            champs[champ_name] = {
                'champion_id': getattr(row, f'participant{i}ChampionId')
            }