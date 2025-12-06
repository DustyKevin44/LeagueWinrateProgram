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
        # We also need to know the COUNT of players per team per match to scale correctly
        player_features = match_stats.groupby(['MatchFk','Team']).agg({
            'kills':'sum', # We use TeamStats for kills, so this is just for aux check
            'deaths':'sum',
            'assists':'sum',
            'TotalGold':'sum',
            'MinionsKilled':'sum',
            'DragonKills':'sum',
            'BaronKills':'sum',
            'visionScore':'sum',
            'SummonerMatchFk': 'count' # Count number of observed data points
        }).reset_index()

        # Pivot BLUE vs RED
        blue = player_features[player_features.Team=='BLUE'].set_index('MatchFk')
        red  = player_features[player_features.Team=='RED'].set_index('MatchFk')

        df = pd.DataFrame()
        
        # --- Reliability Fix ---
        # Player data is incomplete. We use TeamStats for exact totals where possible.
        # For player-specific stats (Gold, CS, Assists), we must SCALE the partial data 
        # to estimate the full 5-player team total.
        # Scaling Factor = 5 / observed_player_count
        
        # Avoid division by zero by replacing 0 with 1 (though count should > 0)
        blue_scale = 5.0 / blue['SummonerMatchFk'].replace(0, 1)
        red_scale  = 5.0 / red['SummonerMatchFk'].replace(0, 1)
        
        # Kills/Deaths from TeamStats (Exact)
        ts_indexed = team_stats.set_index('MatchFk')
        
        # Validating overlap - only process matches present in ALL three (Blue players, Red players, TeamStats)
        common_indices = blue.index.intersection(red.index).intersection(ts_indexed.index)
        
        blue = blue.loc[common_indices]
        red = red.loc[common_indices]
        ts_indexed = ts_indexed.loc[common_indices]
        blue_scale = blue_scale.loc[common_indices]
        red_scale = red_scale.loc[common_indices]
        
        df['kill_diff'] = ts_indexed['BlueKills'] - ts_indexed['RedKills']
        # death_diff is redundant (it's just -kill_diff)
        
        # Scaled Estimates for Partial Data
        # We estimate what the total would be if we had all 5 players
        blue_gold_est = blue['TotalGold'] * blue_scale
        red_gold_est  = red['TotalGold'] * red_scale
        
        blue_assists_est = blue['assists'] * blue_scale
        red_assists_est  = red['assists'] * red_scale
        
        blue_cs_est = blue['MinionsKilled'] * blue_scale
        red_cs_est  = red['MinionsKilled'] * red_scale
        
        blue_ward_est = blue['visionScore'] * blue_scale
        red_ward_est  = red['visionScore'] * red_scale
        
        # Calculate Diffs using Scaled Estimates
        df['assist_diff'] = blue_assists_est - red_assists_est
        df['gold_diff'] = blue_gold_est - red_gold_est
        df['cs_diff'] = blue_cs_est - red_cs_est
        df['ward_score_diff'] = blue_ward_est - red_ward_est
        
        # Note: Level data not available in historical data, will use 0 as placeholder
        df['level_diff'] = 0
        
        # Objectives (Reliable from TeamStats)
        df['dragon_diff'] = ts_indexed['BlueDragonKills'] - ts_indexed['RedDragonKills']
        df['baron_diff'] = ts_indexed['BlueBaronKills'] - ts_indexed['RedBaronKills']
        df['tower_diff'] = ts_indexed['BlueTowerKills'] - ts_indexed['RedTowerKills']
        df['herald_diff'] = ts_indexed['BlueRiftHeraldKills'] - ts_indexed['RedRiftHeraldKills']
        
        # Inhibitors not in TeamMatchTbl, use 0 as placeholder
        df['inhib_diff'] = 0
        
        # Game Duration
        df['game_duration'] = match_tbl.set_index('MatchId').loc[common_indices]['GameDuration']
        game_minutes = (df['game_duration'] / 60).clip(lower=1)
        
        df['blue_win'] = ts_indexed['BlueWin']

        # Drop rows with missing target/features
        df = df.dropna(subset=['blue_win'])
        
        # Fill other NaNs with 0
        df = df.fillna(0)
        
        # ============ DERIVED INTERACTION FEATURES ============
        # These capture the concept of "tower-taking capability"
        # Instead of heuristics, let the model LEARN these relationships from data!
        
        # 1. Combat Power: Overall fighting strength
        # Normalized to similar scales so model can weight them
        df['combat_power'] = (
            df['kill_diff'] / 10.0 +           # Kills normalized
            df['gold_diff'] / 3000.0 +         # Gold normalized  
            df['level_diff'] / 10.0 +          # Levels normalized
            df['baron_diff'] * 3.0 +           # Baron is huge
            df['dragon_diff'] * 0.5            # Dragons help
        )
        
        # 2. Tower-Combat Mismatch: Do towers match combat strength?
        # Positive = have towers but weak (bad)
        # Negative = strong but lack towers (can recover)
        df['tower_combat_mismatch'] = df['tower_diff'] - df['combat_power']
        
        # 3. Push Capability: Can you actually take objectives?
        # Combines combat power with objective control
        df['push_capability'] = (
            df['combat_power'] + 
            df['baron_diff'] * 2.0 +           # Baron enables pushing
            df['herald_diff'] * 1.0            # Herald helps early
        )
        
        # 4. Economic Advantage: Gold/CS combined (scales better)
        df['economic_advantage'] = (
            df['gold_diff'] / 1000.0 +         # Gold per 1k
            df['cs_diff'] / 50.0               # CS per 50
        )
        
        # 5. Objective Control: Overall map control
        df['objective_control'] = (
            df['dragon_diff'] * 1.0 +
            df['baron_diff'] * 3.0 +
            df['tower_diff'] * 2.0 +
            df['herald_diff'] * 1.5 +
            df['inhib_diff'] * 4.0
        )
        
        features = [
            # Core stats
            'kill_diff', 'assist_diff', 'gold_diff', 'cs_diff',
            'ward_score_diff', 'level_diff',
            # Objectives
            'dragon_diff', 'baron_diff', 'tower_diff', 'herald_diff', 'inhib_diff',
            # Time context
            'game_duration',
            # NEW: Derived interaction features (data-driven, not heuristic!)
            'combat_power', 'tower_combat_mismatch', 'push_capability',
            'economic_advantage', 'objective_control'
        ]
        X = df[features]
        y = df['blue_win']
        return X, y
