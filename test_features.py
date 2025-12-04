import pandas as pd
from data_loader import DataLoader
from feature_engineer import DefaultFeatureEngineer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score

def test_no_objectives():
    print("Loading data...")
    loader = DataLoader("data")
    match_stats, team_stats, match_tbl, summoner_match = loader.load_match_stats()
    
    engineer = DefaultFeatureEngineer()
    X, y = engineer.fit_transform(match_stats, team_stats, summoner_match, match_tbl)
    
    # Drop objective features
    drop_cols = ['tower_diff', 'dragon_diff', 'baron_diff']
    X_reduced = X.drop(columns=drop_cols)
    
    # Handle NaNs
    X_reduced = X_reduced.fillna(0)
    
    X_train, X_val, y_train, y_val = train_test_split(X_reduced, y, test_size=0.2, random_state=42)
    
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_val_scaled = scaler.transform(X_val)
    
    model = LogisticRegression(max_iter=1000, random_state=42, class_weight='balanced')
    model.fit(X_train_scaled, y_train)
    
    print(f"Accuracy without objectives: {model.score(X_val_scaled, y_val):.4f}")
    
    # Check Gold Coefficient
    gold_idx = list(X_reduced.columns).index('gold_diff')
    print(f"Gold Diff Coef: {model.coef_[0][gold_idx]:.4f}")
    
    # Predict +1000 gold (others 0)
    # We need to scale the input
    input_data = [0] * len(X_reduced.columns)
    input_data[gold_idx] = 1000
    # game_duration default
    if 'game_duration' in X_reduced.columns:
        dur_idx = list(X_reduced.columns).index('game_duration')
        input_data[dur_idx] = 1500
        
    input_scaled = scaler.transform([input_data])
    prob = model.predict_proba(input_scaled)[0][1]
    print(f"Win Prob for +1000 Gold: {prob*100:.2f}%")

if __name__ == "__main__":
    test_no_objectives()
