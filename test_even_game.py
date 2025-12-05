import pandas as pd
from model import RandomForestWinModel, MODEL_PATH

# Load model
model_obj = RandomForestWinModel(MODEL_PATH)
model_obj.load()

# Create test case with all zeros
even_game = {
    'kill_diff': 0, 'assist_diff': 0, 'gold_diff': 0, 'cs_diff': 0,
    'ward_score_diff': 0, 'level_diff': 0, 'dragon_diff': 0, 'baron_diff': 0,
    'tower_diff': 0, 'herald_diff': 0, 'inhib_diff': 0, 'game_duration': 1200
}

df = pd.DataFrame([even_game])
prob = model_obj.predict(df)[0]

print(f"Even game prediction: {prob*100:.2f}%")
print(f"\nThis means the model predicts Blue team has {prob*100:.2f}% chance to win")
print(f"and Red team has {(1-prob)*100:.2f}% chance to win")

# Try different game durations
print("\n" + "="*70)
print("Testing different game durations (all other features = 0):")
for duration in [600, 900, 1200, 1500, 1800, 2100, 2400]:
    even_game['game_duration'] = duration
    df = pd.DataFrame([even_game])
    prob = model_obj.predict(df)[0]
    print(f"  {duration:4d}s ({duration//60:2d}min): Blue win prob = {prob*100:.2f}%")
