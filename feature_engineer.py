import pandas as pd

class FeatureEngineerBase:
    """Abstract base class for feature engineering"""
    def fit_transform(self, match_stats: pd.DataFrame, team_stats: pd.DataFrame, summoner_match: pd.DataFrame, match_tbl: pd.DataFrame):
        raise NotImplementedError

class DefaultFeatureEngineer(FeatureEngineerBase):
    """Aggregates player stats per team and computes differences for blue vs red"""
    def fit_transform(self, match_stats, team_stats, summoner_match, match_tbl):
        # Merge match stats with summoner_match to get MatchID
        match_stats = match_stats.merge(
            summoner_match[['SummonerMatchId','MatchFk','ChampionFk']],
            left_on='SummonerMatchFk', right_on='SummonerMatchId',
            how='left'
        )

        # Merge with team_stats to get champions per side
        match_stats = match_stats.merge(
            team_stats[['TeamID','MatchFk','B1Champ','B2Champ','B3Champ','B4Champ','B5Champ',
                        'R1Champ','R2Champ','R3Champ','R4Champ','R5Champ',
                        'BlueBaronKills','BlueDragonKills','BlueTowerKills','BlueKills',
                        'RedBaronKills','RedDragonKills','RedTowerKills','RedKills',
                        'BlueWin','RedWin']],
            left_on='MatchFk', right_on='MatchFk', how='left'
        )
        
        # Merge with match_tbl to get GameDuration
        match_stats = match_stats.merge(
            match_tbl[['MatchId', 'GameDuration']],
            left_on='MatchFk', right_on='MatchId',
            how='left'
        )

        # Assign team BLUE or RED
        def assign_team(row):
            if row['ChampionFk'] in [row['B1Champ'], row['B2Champ'], row['B3Champ'], row['B4Champ'], row['B5Champ']]:
                return 'BLUE'
            else:
                return 'RED'

        match_stats['Team'] = match_stats.apply(assign_team, axis=1)

        # Aggregate stats per team
        player_features = match_stats.groupby(['MatchFk','Team']).agg({
            'kills':'sum',
            'deaths':'sum',
            'assists':'sum',
            'TotalGold':'sum',
            'MinionsKilled':'sum',
            'DragonKills':'sum',
            'BaronKills':'sum',
            'visionScore':'sum'
        }).reset_index()

        # Pivot BLUE vs RED
        blue = player_features[player_features.Team=='BLUE'].set_index('MatchFk')
        red  = player_features[player_features.Team=='RED'].set_index('MatchFk')

        df = pd.DataFrame()
        # Core stats
        df['kill_diff'] = blue['kills'] - red['kills']
        df['death_diff'] = blue['deaths'] - red['deaths']
        df['assist_diff'] = blue['assists'] - red['assists']
        df['gold_diff'] = blue['TotalGold'] - red['TotalGold']
        df['cs_diff'] = blue['MinionsKilled'] - red['MinionsKilled']
        df['ward_score_diff'] = blue['visionScore'] - red['visionScore']
        
        # Note: Level data not available in historical data, will use 0 as placeholder
        df['level_diff'] = 0
        
        # Objectives
        df['dragon_diff'] = blue['DragonKills'] - red['DragonKills']
        df['baron_diff'] = blue['BaronKills'] - red['BaronKills']
        df['tower_diff'] = team_stats.set_index('MatchFk')['BlueTowerKills'] - team_stats.set_index('MatchFk')['RedTowerKills']
        df['herald_diff'] = team_stats.set_index('MatchFk')['BlueRiftHeraldKills'] - team_stats.set_index('MatchFk')['RedRiftHeraldKills']
        
        # Inhibitors not in TeamMatchTbl, use 0 as placeholder
        df['inhib_diff'] = 0
        
        # Game Duration
        df['game_duration'] = match_tbl.set_index('MatchId')['GameDuration']
        game_minutes = (df['game_duration'] / 60).clip(lower=1)
        
        # Derived features (matching live_client.py)
        blue_kda = (blue['kills'] + blue['assists']) / blue['deaths'].clip(lower=1)
        red_kda = (red['kills'] + red['assists']) / red['deaths'].clip(lower=1)
        df['kda_diff'] = blue_kda - red_kda
        
        df['gold_per_kill'] = df['gold_diff'] / df['kill_diff'].abs().clip(lower=1)
        df['cs_per_min_diff'] = df['cs_diff'] / game_minutes
        
        df['objective_score'] = (
            df['tower_diff'] * 1.0 +
            df['dragon_diff'] * 1.5 +
            df['herald_diff'] * 1.2 +
            df['baron_diff'] * 3.0 +
            df['inhib_diff'] * 2.5
        )
        
        df['blue_win'] = team_stats.set_index('MatchFk')['BlueWin']

        # Drop rows with missing target/features
        df = df.dropna(subset=['blue_win'])
        
        # Fill other NaNs with 0
        df = df.fillna(0)
        
        features = [
            # Core stats
            'kill_diff', 'death_diff', 'assist_diff', 'gold_diff', 'cs_diff',
            'ward_score_diff', 'level_diff',
            # Objectives
            'dragon_diff', 'baron_diff', 'tower_diff', 'herald_diff', 'inhib_diff',
            # Derived features
            'kda_diff', 'gold_per_kill', 'cs_per_min_diff', 'objective_score',
            # Time context
            'game_duration'
        ]
        X = df[features]
        y = df['blue_win']
        return X, y
