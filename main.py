import os
from interface import WinProbabilityInterface
from data_loader import DataLoader
from feature_engineer import DefaultFeatureEngineer
from model import RandomForestWinModel, MODEL_PATH

def main():
    # 1. Train Model if needed (or force retrain to ensure we have the latest logic)
    # Ideally we check if it exists, but user asked to "look over model training", so let's run it to be sure.
    print("Loading data...")
    loader = DataLoader("data")
    match_stats, team_stats, match_tbl, summoner_match = loader.load_match_stats()
    
    print("Engineering features...")
    engineer = DefaultFeatureEngineer()
    X, y = engineer.fit_transform(match_stats, team_stats, summoner_match, match_tbl)
    
    print("Training and Evaluating Model...")
    # We use the model class directly for training/evaluation
    model = RandomForestWinModel(MODEL_PATH)
    model.train(X, y)
    model.save()
    
    # 2. Use Interface for Predictions
    print("\n--- Prediction Examples ---")
    interface_instance = WinProbabilityInterface()
    
    # Predict with +1000 gold diff
    # We expect this to be > 50%
    pred_plus = interface_instance.predict(gold_diff=1000)
    print(f"Gold +1000 Win Probability: {pred_plus*100:.2f}%")
    
    # Predict with -1000 gold diff
    # We expect this to be < 50%
    pred_minus = interface_instance.predict(gold_diff=-1000)
    print(f"Gold -1000 Win Probability: {pred_minus*100:.2f}%")

if __name__ == "__main__":
    main()
