from data_loader import DataLoader
from feature_engineer import DefaultFeatureEngineer
import pandas as pd

loader = DataLoader('data')
match_stats, team_stats, match_tbl, summoner_match = loader.load_match_stats()

engineer = DefaultFeatureEngineer()
X, y = engineer.fit_transform(match_stats, team_stats, summoner_match, match_tbl)

df = pd.DataFrame(X)
df.columns = ['kill_diff','assist_diff','gold_diff','cs_diff','dragon_diff','baron_diff','tower_diff','game_duration']
df['blue_win'] = y

wins = df[df['blue_win'] == 1]
losses = df[df['blue_win'] == 0]

print('When Blue WINS:')
print(f'  Avg gold_diff: {wins["gold_diff"].mean():.2f}')
print(f'  Avg kill_diff: {wins["kill_diff"].mean():.2f}')
print(f'  Avg tower_diff: {wins["tower_diff"].mean():.2f}')

print('\nWhen Blue LOSES:')
print(f'  Avg gold_diff: {losses["gold_diff"].mean():.2f}')
print(f'  Avg kill_diff: {losses["kill_diff"].mean():.2f}')
print(f'  Avg tower_diff: {losses["tower_diff"].mean():.2f}')

print('\nSample rows where Blue wins:')
print(wins[wins['gold_diff'] != 0].head(10))

print('\nSample rows where Blue loses:')
print(losses[losses['gold_diff'] != 0].head(10))
