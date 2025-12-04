import os
from interface import WinProbabilityInterface
from data_loader import DataLoader
from feature_engineer import DefaultFeatureEngineer
from model import RandomForestWinModel, MODEL_PATH

def main():
    # 1. Train Model
    print("Loading data...")
    loader = DataLoader("data")
    match_stats, team_stats, match_tbl, summoner_match = loader.load_match_stats()
    
    print("Engineering features...")
    engineer = DefaultFeatureEngineer()
    X, y = engineer.fit_transform(match_stats, team_stats, summoner_match, match_tbl)
    
    print("Training and Evaluating Model...")
    model = RandomForestWinModel(MODEL_PATH)
    model.train(X, y)
    model.save()
    
    # 2. Test Predictions
    print("\n--- Prediction Examples ---")
    interface_instance = WinProbabilityInterface()
    
    # Realistic mid-game scenario: +1000 gold advantage
    # Typically means: slight kill lead, small CS lead, maybe 1 tower
    pred_plus = interface_instance.predict(
        kill_diff=2, assist_diff=3, gold_diff=1000, cs_diff=15,
        dragon_diff=0, baron_diff=0, tower_diff=1, game_duration=1200
    )
    print(f"Mid-game +1000 gold advantage: {pred_plus*100:.2f}%")
    
    # Realistic mid-game scenario: -1000 gold disadvantage  
    pred_minus = interface_instance.predict(
        kill_diff=-2, assist_diff=-3, gold_diff=-1000, cs_diff=-15,
        dragon_diff=0, baron_diff=0, tower_diff=-1, game_duration=1200
    )
    print(f"Mid-game -1000 gold disadvantage: {pred_minus*100:.2f}%")
    
    # Even game
    pred_even = interface_instance.predict(
        kill_diff=0, assist_diff=0, gold_diff=0, cs_diff=0,
        dragon_diff=0, baron_diff=0, tower_diff=0, game_duration=1200
    )
    print(f"Even game: {pred_even*100:.2f}%")

if __name__ == "__main__":
    main()
