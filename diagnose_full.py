import pandas as pd
from data_loader import DataLoader

def diagnose_data():
    loader = DataLoader("data")
    match_stats, team_stats, match_tbl, summoner_match = loader.load_match_stats()
    
    print("=== DATA STRUCTURE ===")
    print(f"MatchStats rows: {len(match_stats)}")
    print(f"TeamStats rows: {len(team_stats)}")
    print(f"SummonerMatch rows: {len(summoner_match)}")
    print(f"MatchTbl rows: {len(match_tbl)}")
    
    # Check one match
    match_id = team_stats['MatchFk'].iloc[0]
    print(f"\n=== MATCH {match_id} ===")
    
    # How many summoner_match entries for this match?
    sm_for_match = summoner_match[summoner_match['MatchFk'] == match_id]
    print(f"SummonerMatch entries: {len(sm_for_match)}")
    
    # How many match_stats entries?
    # match_stats has SummonerMatchFk, need to join to get MatchFk
    ms_ids = sm_for_match['SummonerMatchId'].values
    ms_for_match = match_stats[match_stats['SummonerMatchFk'].isin(ms_ids)]
    print(f"MatchStats entries: {len(ms_for_match)}")
    
    # Check team_stats
    ts_for_match = team_stats[team_stats['MatchFk'] == match_id]
    print(f"TeamStats entries: {len(ts_for_match)}")
    
    if len(ts_for_match) > 0:
        print("\nTeam Stats columns:", ts_for_match.columns.tolist())
        print("\nBlue Champs:", ts_for_match.iloc[0][['B1Champ','B2Champ','B3Champ','B4Champ','B5Champ']].values)
        print("Red Champs:", ts_for_match.iloc[0][['R1Champ','R2Champ','R3Champ','R4Champ','R5Champ']].values)
    
    if len(sm_for_match) > 0:
        print("\nChampions in SummonerMatch for this match:")
        print(sm_for_match[['SummonerMatchId', 'ChampionFk']].values)
    
    # Check if merge is causing duplicates
    print("\n=== MERGE TEST ===")
    merged = match_stats.merge(
        summoner_match[['SummonerMatchId','MatchFk','ChampionFk']],
        left_on='SummonerMatchFk', right_on='SummonerMatchId',
        how='left'
    )
    print(f"After first merge: {len(merged)} rows (was {len(match_stats)})")
    
    merged2 = merged.merge(
        team_stats[['TeamID','MatchFk','B1Champ','B2Champ','B3Champ','B4Champ','B5Champ',
                    'R1Champ','R2Champ','R3Champ','R4Champ','R5Champ']],
        left_on='MatchFk', right_on='MatchFk', how='left'
    )
    print(f"After second merge: {len(merged2)} rows")
    
    # Check for one match
    merged_one = merged2[merged2['MatchFk'] == match_id]
    print(f"Rows for match {match_id}: {len(merged_one)}")

if __name__ == "__main__":
    diagnose_data()
