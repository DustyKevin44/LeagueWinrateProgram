import pandas as pd
from data_loader import DataLoader
from feature_engineer import DefaultFeatureEngineer

# Load and process data
print("Loading data...")
loader = DataLoader("data")
match_stats, team_stats, match_tbl, summoner_match = loader.load_match_stats()

print("Engineering features...")
engineer = DefaultFeatureEngineer()
X, y = engineer.fit_transform(match_stats, team_stats, summoner_match, match_tbl)

# Check class distribution
print(f"\nClass Distribution:")
print(f"Blue wins (1): {y.sum()} ({y.sum()/len(y)*100:.2f}%)")
print(f"Red wins (0): {(1-y).sum()} ({(1-y).sum()/len(y)*100:.2f}%)")

# Check if there are any rows with all zeros
all_zeros = (X == 0).all(axis=1)
print(f"\nRows with all zeros: {all_zeros.sum()}")

# Check distribution of target for rows close to zero
near_zero = (X.abs() < 100).all(axis=1)
print(f"\nRows with all features near zero (<100): {near_zero.sum()}")
if near_zero.sum() > 0:
    print(f"  Blue win rate for near-zero rows: {y[near_zero].mean()*100:.2f}%")

# Check basic statistics
print(f"\nFeature Statistics:")
print(X.describe())
