import pandas as pd
from data_loader import DataLoader

# Load data
print("Loading data...")
loader = DataLoader("data")
match_stats, team_stats, match_tbl, summoner_match = loader.load_match_stats()

# Check blue vs red win rate
print(f"\nBlue vs Red Win Rates:")
print(f"Blue wins: {team_stats['BlueWin'].sum()}")
print(f"Red wins: {team_stats['RedWin'].sum()}")
print(f"Total games: {len(team_stats)}")
print(f"Blue win rate: {team_stats['BlueWin'].mean()*100:.2f}%")
print(f"Red win rate: {team_stats['RedWin'].mean()*100:.2f}%")
