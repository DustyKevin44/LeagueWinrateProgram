import os
import pandas as pd

class DataLoader:
    def __init__(self, data_dir: str):
        self.data_dir = data_dir

    def load_match_stats(self):
        match_stats = pd.read_csv(os.path.join(self.data_dir, 'MatchStatsTbl.csv'))
        team_stats  = pd.read_csv(os.path.join(self.data_dir, 'TeamMatchTbl.csv'))
        match_tbl   = pd.read_csv(os.path.join(self.data_dir, 'MatchTbl.csv'))
        summoner_match = pd.read_csv(os.path.join(self.data_dir, 'SummonerMatchTbl.csv'))
        
        # Filter for Classic games only (Summoner's Rift 5v5)
        if 'QueueType' in match_tbl.columns:
            print(f"Total matches before filtering: {len(match_tbl)}")
            match_tbl = match_tbl[match_tbl['QueueType'] == 'CLASSIC']
            print(f"Classic matches after filtering: {len(match_tbl)}")
            
            # Filter other tables to only include matches in match_tbl
            valid_match_ids = match_tbl['MatchId'].unique()
            team_stats = team_stats[team_stats['MatchFk'].isin(valid_match_ids)]
            summoner_match = summoner_match[summoner_match['MatchFk'].isin(valid_match_ids)]
            match_stats = match_stats[match_stats['SummonerMatchFk'].isin(summoner_match['SummonerMatchId'])]
        
        return match_stats, team_stats, match_tbl, summoner_match
