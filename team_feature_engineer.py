import pandas as pd
from data_loader import DataLoader

class TeamLevelFeatureEngineer:
    """
    Feature engineer using ONLY TeamMatchTbl data (complete and accurate).
    No player-level aggregation needed.
    """
    
    def fit_transform(self, team_stats, match_tbl):
        """
        Extract features directly from TeamMatchTbl.
        
        Args:
            team_stats: TeamMatchTbl DataFrame
            match_tbl: MatchTbl DataFrame (for game duration)
        
        Returns:
            X: Features DataFrame
            y: Target Series (BlueWin)
        """
        # Merge with match_tbl to get GameDuration
        df = team_stats.merge(
            match_tbl[['MatchId', 'GameDuration']],
            left_on='MatchFk',
            right_on='MatchId',
            how='left'
        )
        
        # Calculate diffs (Blue - Red)
        features_df = pd.DataFrame()
        features_df['kill_diff'] = df['BlueKills'] - df['RedKills']
        features_df['tower_diff'] = df['BlueTowerKills'] - df['RedTowerKills']
        features_df['dragon_diff'] = df['BlueDragonKills'] - df['RedDragonKills']
        features_df['baron_diff'] = df['BlueBaronKills'] - df['RedBaronKills']
        features_df['game_duration'] = df['GameDuration']
        
        # Target
        y = df['BlueWin']
        
        # Drop NaNs
        features_df = features_df.fillna(0)
        
        return features_df, y


if __name__ == "__main__":
    # Test the new feature engineer
    loader = DataLoader("data")
    _, team_stats, match_tbl, _ = loader.load_match_stats()
    
    engineer = TeamLevelFeatureEngineer()
    X, y = engineer.fit_transform(team_stats, match_tbl)
    
    print("Features shape:", X.shape)
    print("\nFeature correlations with BlueWin:")
    for col in X.columns:
        corr = X[col].corr(y)
        print(f"  {col}: {corr:.4f}")
    
    print(f"\nBlue win rate: {y.mean():.4f}")
    print("\nSample features:")
    print(X.head())
