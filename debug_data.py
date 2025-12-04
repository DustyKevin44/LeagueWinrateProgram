import pandas as pd
from data_loader import DataLoader
from feature_engineer import DefaultFeatureEngineer

def check_data():
    loader = DataLoader("data")
    match_stats, team_stats, match_tbl, summoner_match = loader.load_match_stats()
    
    engineer = DefaultFeatureEngineer()
    X, y = engineer.fit_transform(match_stats, team_stats, summoner_match, match_tbl)
    
    # Check correlation
    df = X.copy()
    df['target'] = y
    
    corr = df.corr()['target'].sort_values(ascending=False)
    print("Correlations with Target (BlueWin):")
    print(corr)
    
    # Check what +1000 gold looks like in real data
    print("\nStats for games with Gold Diff between 500 and 1500:")
    subset = df[(df['gold_diff'] > 500) & (df['gold_diff'] < 1500)]
    print(subset.describe())
    print(f"Win rate in this subset: {subset['target'].mean()}")
    
    # Calculate slope for key features vs gold_diff
    from sklearn.linear_model import LinearRegression
    
    features_to_check = ['kill_diff', 'cs_diff', 'tower_diff', 'dmg_dealt_diff']
    
    print("\nEstimating relationships with Gold Diff:")
    for feat in features_to_check:
        lr = LinearRegression()
        # Drop NaNs
        df_clean = df.dropna(subset=['gold_diff', feat])
        lr.fit(df_clean[['gold_diff']], df_clean[feat])
        print(f"{feat}: Slope={lr.coef_[0]:.6f}, Intercept={lr.intercept_:.4f}")

if __name__ == "__main__":
    check_data()
