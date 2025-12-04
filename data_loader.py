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
        return match_stats, team_stats, match_tbl, summoner_match
