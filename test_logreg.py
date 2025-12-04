import pandas as pd
from data_loader import DataLoader
from feature_engineer import DefaultFeatureEngineer
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

def test_models():
    print("Loading data...")
    loader = DataLoader("data")
    match_stats, team_stats, match_tbl, summoner_match = loader.load_match_stats()
    
    engineer = DefaultFeatureEngineer()
    X, y = engineer.fit_transform(match_stats, team_stats, summoner_match)
    
    # Handle NaNs
    X = X.fillna(0)
    
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Random Forest
    rf = RandomForestClassifier(n_estimators=100, random_state=42)
    rf.fit(X_train, y_train)
    print(f"RF Accuracy: {rf.score(X_val, y_val):.4f}")
    
    # Logistic Regression
    lr = LogisticRegression(max_iter=1000)
    lr.fit(X_train, y_train)
    print(f"LR Accuracy: {lr.score(X_val, y_val):.4f}")
    
    # Test Prediction
    features = X.columns
    data_plus = {f: 0 for f in features}
    data_plus['gold_diff'] = 1000
    # game_duration default?
    if 'game_duration' in features:
        data_plus['game_duration'] = 1500
        
    df_plus = pd.DataFrame([data_plus])
    
    rf_pred = rf.predict_proba(df_plus)[0][1]
    lr_pred = lr.predict_proba(df_plus)[0][1]
    
    print(f"\nPrediction for Gold +1000 (others 0):")
    print(f"RF: {rf_pred*100:.2f}%")
    print(f"LR: {lr_pred*100:.2f}%")

if __name__ == "__main__":
    test_models()
