import os
from data_loader import DataLoader
from team_feature_engineer import TeamLevelFeatureEngineer
from model import RandomForestWinModel, MODEL_PATH

def train_team_model():
    """Train model using complete team-level data from TeamMatchTbl"""
    print("Loading data...")
    loader = DataLoader("data")
    _, team_stats, match_tbl, _ = loader.load_match_stats()
    
    print("Engineering features from TeamMatchTbl...")
    engineer = TeamLevelFeatureEngineer()
    X, y = engineer.fit_transform(team_stats, match_tbl)
    
    print(f"Dataset: {len(X)} matches")
    print(f"Blue win rate: {y.mean():.1%}\n")
    
    print("Training and Evaluating Model...")
    model = RandomForestWinModel(MODEL_PATH)
    model.train(X, y)
    model.save()
    
    print("\n✅ Model trained and saved successfully!")
    print(f"Model saved to: {MODEL_PATH}")

if __name__ == "__main__":
    train_team_model()
