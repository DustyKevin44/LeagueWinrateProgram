import pandas as pd
from data_loader import DataLoader

def check_teams():
    loader = DataLoader("data")
    match_stats, team_stats, match_tbl, summoner_match = loader.load_match_stats()
    
    # Merge like in feature_engineer
    match_stats = match_stats.merge(
        summoner_match[['SummonerMatchId','MatchFk','ChampionFk']],
        left_on='SummonerMatchFk', right_on='SummonerMatchId',
        how='left'
    )

    match_stats = match_stats.merge(
        team_stats[['TeamID','MatchFk','B1Champ','B2Champ','B3Champ','B4Champ','B5Champ',
                    'R1Champ','R2Champ','R3Champ','R4Champ','R5Champ']],
        left_on='MatchFk', right_on='MatchFk', how='left'
    )
    
    # Pick one match
    match_id = match_stats['MatchFk'].iloc[0]
    one_match = match_stats[match_stats['MatchFk'] == match_id]
    
    print(f"Checking Match {match_id}")
    print("Blue Champs:", one_match.iloc[0][['B1Champ','B2Champ','B3Champ','B4Champ','B5Champ']].values)
    print("Red Champs:", one_match.iloc[0][['R1Champ','R2Champ','R3Champ','R4Champ','R5Champ']].values)
    
    for idx, row in one_match.iterrows():
        champ = row['ChampionFk']
        # Logic from feature_engineer
        if champ in [row['B1Champ'], row['B2Champ'], row['B3Champ'], row['B4Champ'], row['B5Champ']]:
            team = 'BLUE'
        else:
            team = 'RED'
        print(f"Champ {champ} -> {team}")

if __name__ == "__main__":
    check_teams()
