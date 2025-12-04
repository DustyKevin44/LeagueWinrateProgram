import pandas as pd

class FeatureEngineerBase:
    """Abstract base class for feature engineering"""
    def fit_transform(self, match_stats: pd.DataFrame, team_stats: pd.DataFrame, summoner_match: pd.DataFrame):
        raise NotImplementedError

class DefaultFeatureEngineer(FeatureEngineerBase):
    """Aggregates player stats per team and computes differences for blue vs red"""
    def fit_transform(self, match_stats, team_stats, summoner_match):
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
            'DmgDealt':'sum',
            'DmgTaken':'sum',
            'visionScore':'sum',
            'DragonKills':'sum',
            'BaronKills':'sum'
        }).reset_index()

        # Pivot BLUE vs RED
        blue = player_features[player_features.Team=='BLUE'].set_index('MatchFk')
        red  = player_features[player_features.Team=='RED'].set_index('MatchFk')

        df = pd.DataFrame()
        df['kill_diff'] = blue['kills'] - red['kills']
        df['death_diff'] = blue['deaths'] - red['deaths']
        df['assist_diff'] = blue['assists'] - red['assists']
        df['gold_diff'] = blue['TotalGold'] - red['TotalGold']
        df['cs_diff'] = blue['MinionsKilled'] - red['MinionsKilled']
        df['dmg_dealt_diff'] = blue['DmgDealt'] - red['DmgDealt']
        df['dmg_taken_diff'] = blue['DmgTaken'] - red['DmgTaken']
        df['dragon_diff'] = blue['DragonKills'] - red['DragonKills']
        df['baron_diff'] = blue['BaronKills'] - red['BaronKills']
        df['tower_diff'] = team_stats.set_index('MatchFk')['BlueTowerKills'] - team_stats.set_index('MatchFk')['RedTowerKills']
        df['game_duration'] = match_stats.set_index('MatchFk')['GameDuration'] if 'GameDuration' in match_stats.columns else 0
        df['blue_win'] = team_stats.set_index('MatchFk')['BlueWin']

        # Drop rows with missing target/features
        df = df.dropna(subset=['blue_win'])
        features = ['kill_diff','death_diff','assist_diff','gold_diff','cs_diff',
                    'dmg_dealt_diff','dmg_taken_diff','dragon_diff','baron_diff',
                    'tower_diff','game_duration']
        X = df[features]
        y = df['blue_win']
        return X, y
