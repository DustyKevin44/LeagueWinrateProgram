import pandas as pd
from model import RandomForestWinModel, MODEL_PATH

# Load model
model_obj = RandomForestWinModel(MODEL_PATH)
model_obj.load()

# Test predictions
test_cases = [
    # Mid-game +1000 gold advantage
    {'kill_diff': 2, 'assist_diff': 3, 'gold_diff': 1000, 'cs_diff': 15, 
     'ward_score_diff': 5, 'level_diff': 0, 'dragon_diff': 0, 'baron_diff': 0, 
     'tower_diff': 1, 'herald_diff': 0, 'inhib_diff': 0, 'game_duration': 1200},
    
    # Mid-game -1000 gold disadvantage
    {'kill_diff': -2, 'assist_diff': -3, 'gold_diff': -1000, 'cs_diff': -15,
     'ward_score_diff': -5, 'level_diff': 0, 'dragon_diff': 0, 'baron_diff': 0,
     'tower_diff': -1, 'herald_diff': 0, 'inhib_diff': 0, 'game_duration': 1200},
    
    # Strong advantage
    {'kill_diff': 5, 'assist_diff': 8, 'gold_diff': 2000, 'cs_diff': 20,
     'ward_score_diff': 10, 'level_diff': 0, 'dragon_diff': 1, 'baron_diff': 0,
     'tower_diff': 2, 'herald_diff': 1, 'inhib_diff': 0, 'game_duration': 1500},
    
    # Strong disadvantage
    {'kill_diff': -5, 'assist_diff': -8, 'gold_diff': -2000, 'cs_diff': -20,
     'ward_score_diff': -10, 'level_diff': 0, 'dragon_diff': -1, 'baron_diff': 0,
     'tower_diff': -2, 'herald_diff': -1, 'inhib_diff': 0, 'game_duration': 1500},
    
    # Even game
    {'kill_diff': 0, 'assist_diff': 0, 'gold_diff': 0, 'cs_diff': 0,
     'ward_score_diff': 0, 'level_diff': 0, 'dragon_diff': 0, 'baron_diff': 0,
     'tower_diff': 0, 'herald_diff': 0, 'inhib_diff': 0, 'game_duration': 1200},
]

print("Testing model predictions:")
print("=" * 70)

for i, case in enumerate(test_cases, 1):
    df = pd.DataFrame([case])
    prob = model_obj.predict(df)[0]
    print(f"\nTest {i}:")
    print(f"  Features: gold_diff={case['gold_diff']}, kill_diff={case['kill_diff']}, tower_diff={case['tower_diff']}")
    print(f"  Win Probability: {prob*100:.2f}%")

# Display model details
print("\n" + "=" * 70)
print("Model details:")
print(f"  Type: RandomForestClassifier")
print(f"  Number of estimators: {model_obj.model.n_estimators}")
print(f"  Max depth: {model_obj.model.max_depth}")
print(f"  Number of features: {model_obj.model.n_features_in_}")

# Feature importances
print("\nFeature importances:")
feature_names = [
    'kill_diff', 'assist_diff', 'gold_diff', 'cs_diff',
    'ward_score_diff', 'level_diff', 'dragon_diff', 'baron_diff',
    'tower_diff', 'herald_diff', 'inhib_diff', 'game_duration'
]
for name, importance in zip(feature_names, model_obj.model.feature_importances_):
    print(f"  {name:20s}: {importance:.4f}")
