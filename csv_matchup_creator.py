import pandas as pd

df = pd.read_csv("data/matchData.csv")

def extract_participants(df):
    participants = []

    for i in range(10):
        prefix = f"participant{i}"
        participant = {
            "matchId": df["matchId"],
            "participantId": df[f"{prefix}ParticipantId"],
            "teamId": df[f"{prefix}TeamId"],
            "championId": df[f"{prefix}ChampionId"],
            "championName": df[f"{prefix}ChampionName"],
            "position": df[f"{prefix}IndividualPosition"],
            "role": df[f"{prefix}Role"],
            "win": df[f"{prefix}Win"],

            # Early game (si tu as des stats par minute tu les mets ici)
            "kills": df[f"{prefix}Kills"],
            "deaths": df[f"{prefix}Deaths"],
            "assists": df[f"{prefix}Assists"],
            "gold": df[f"{prefix}GoldEarned"],
            "cs": df[f"{prefix}TotalMinionsKilled"],
            "damage": df[f"{prefix}TotalDamageDealtToChampions"],

            "firstBloodKill": df[f"{prefix}FirstBloodKill"],
            "firstBloodAssist": df[f"{prefix}FirstBloodAssist"],
            "firstTowerKill": df[f"{prefix}FirstTowerKill"],
            "firstTowerAssist": df[f"{prefix}FirstTowerAssist"],

            "totalDamageDealtToChampions": df[f"{prefix}TotalDamageDealtToChampions"],
            "visionScore": df[f"{prefix}VisionScore"],
        }
        participants.append(pd.DataFrame(participant))

    return pd.concat(participants, ignore_index=True)

participants = extract_participants(df)

# Nettoyage simple
participants["position"] = participants["position"].replace({
    "TOP": "TOP", "JUNGLE": "JUNGLE", "MIDDLE": "MID",
    "BOTTOM": "BOT", "UTILITY": "SUP"
})


team_list = []
for t in [0, 1]:
    prefix = f"team{t}"
    team_list.append(pd.DataFrame({
        "matchId": df["matchId"],
        "teamId": df[f"{prefix}TeamId"],
        "teamWin": df[f"{prefix}Win"],
        "teamKills": df[f"{prefix}ChampionKills"],
        "teamFirstBlood": df[f"{prefix}FeatsFIRST_BLOODFeatState"],
        "teamFirstTower": df[f"{prefix}FeatsFIRST_TURRETFeatState"],
    }))

teams = pd.concat(team_list, ignore_index=True)

team_damage = participants.groupby(["matchId", "teamId"])["totalDamageDealtToChampions"].sum().reset_index()
team_damage.rename(columns={"totalDamageDealtToChampions": "teamTotalDamage"}, inplace=True)

teams = teams.merge(team_damage, on=["matchId", "teamId"], how="left")
teams["teamTotalDamage"] = teams["teamTotalDamage"].fillna(0)


matchups = []

for match_id, part in participants.groupby("matchId"):
    match_duration = df.set_index("matchId")["gameDuration"]

    # Un matchup se calcule lane par lane
    for lane, lane_part in part.groupby("position"):

        if lane not in ["TOP", "JUNGLE", "MID", "BOT", "SUP"]:
            continue

        # Doit y avoir EXACTEMENT 2 joueurs sur la lane (un par équipe)
        if len(lane_part) != 2:
            continue

        pA, pB = lane_part.iloc[0], lane_part.iloc[1]

        teamA = teams[(teams.matchId == match_id) & (teams.teamId == pA["teamId"])].iloc[0]
        teamB = teams[(teams.matchId == match_id) & (teams.teamId == pB["teamId"])].iloc[0]

        # Construction du matchup 1 ligne
        matchups.append({
            "matchId": match_id,
            "lane": lane,

            "champA": pA["championName"],
            "champB": pB["championName"],
            "champA_id": pA["championId"],
            "champB_id": pB["championId"],

            "winA": int(pA["win"]),
            "winB": int(pB["win"]),

            # Différences importantes
            "goldDiff": pA["gold"] - pB["gold"],
            "csDiff": pA["cs"] - pB["cs"],
            "damageDiff": pA["damage"] - pB["damage"],

            # Stats absolues (A)
            "killsA": pA["kills"],
            "deathsA": pA["deaths"],
            "assistsA": pA["assists"],
            "visionA": pA["visionScore"],

            # Stats absolues (B)
            "killsB": pB["kills"],
            "deathsB": pB["deaths"],
            "assistsB": pB["assists"],
            "visionB": pB["visionScore"],

            # Infos équipes
            "teamA_win": int(teamA["teamWin"]),
            "teamB_win": int(teamB["teamWin"]),

            "teamA_firstBlood": int(teamA["teamFirstBlood"]),
            "teamB_firstBlood": int(teamB["teamFirstBlood"]),

            "teamA_firstTower": int(teamA["teamFirstTower"]),
            "teamB_firstTower": int(teamB["teamFirstTower"]),

            "teamA_kills": teamA["teamKills"],
            "teamB_kills": teamB["teamKills"],

            "teamA_totalDamage": teamA["teamTotalDamage"],
            "teamB_totalDamage": teamB["teamTotalDamage"],

            # Kill participation
            "kpA": (pA["kills"] + pA["assists"]) / teamA["teamKills"] if teamA["teamKills"] > 0 else 0,
            "kpB": (pB["kills"] + pB["assists"]) / teamB["teamKills"] if teamB["teamKills"] > 0 else 0,

            # Damage share
            "damageShareA": pA["damage"] / teamA["teamTotalDamage"] if teamA["teamTotalDamage"] > 0 else 0,
            "damageShareB": pB["damage"] / teamB["teamTotalDamage"] if teamB["teamTotalDamage"] > 0 else 0,

            # Vision diff
            "visionDiff": pA["visionScore"] - pB["visionScore"],

            # First blood participation
            "firstBloodPartA": int(pA["firstBloodKill"] or pA["firstBloodAssist"]),
            "firstBloodPartB": int(pB["firstBloodKill"] or pB["firstBloodAssist"]),

            # First tower participation
            "firstTowerPartA": int(pA["firstTowerKill"] or pA["firstTowerAssist"]),
            "firstTowerPartB": int(pB["firstTowerKill"] or pB["firstTowerAssist"]),

            "gameDuration": match_duration.loc[match_id],
        })


matchups_df = pd.DataFrame(matchups)

# --- 3. Ajouter des features utiles pour IA ---
matchups_df["kdaA"] = (matchups_df["killsA"] + matchups_df["assistsA"]) / matchups_df["deathsA"].replace(0, 1)
matchups_df["kdaB"] = (matchups_df["killsB"] + matchups_df["assistsB"]) / matchups_df["deathsB"].replace(0, 1)

# --- 4. Sauvegarde ---
matchups_df.to_csv("data/matchUp.csv", index=False)

print("✓ Matchups générés :", len(matchups_df))

