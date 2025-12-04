import joblib
import pandas as pd
from model import RandomForestWinModel, MODEL_PATH, SCALER_PATH

# Load model and scaler
model_obj = RandomForestWinModel(MODEL_PATH)
model_obj.load()

# Test predictions
test_cases = [
    {'kill_diff': 0, 'assist_diff': 0, 'gold_diff': 1000, 'cs_diff': 0, 'dragon_diff': 0, 'baron_diff': 0, 'tower_diff': 0, 'game_duration': 1200},
    {'kill_diff': 0, 'assist_diff': 0, 'gold_diff': -1000, 'cs_diff': 0, 'dragon_diff': 0, 'baron_diff': 0, 'tower_diff': 0, 'game_duration': 1200},
    {'kill_diff': 5, 'assist_diff': 0, 'gold_diff': 2000, 'cs_diff': 20, 'dragon_diff': 1, 'baron_diff': 0, 'tower_diff': 2, 'game_duration': 1500},
    {'kill_diff': -5, 'assist_diff': 0, 'gold_diff': -2000, 'cs_diff': -20, 'dragon_diff': -1, 'baron_diff': 0, 'tower_diff': -2, 'game_duration': 1500},
]

print("Testing model predictions:")
print("=" * 70)

for i, case in enumerate(test_cases, 1):
    df = pd.DataFrame([case])
    prob = model_obj.predict(df)[0]
    print(f"\nTest {i}:")
    print(f"  Features: gold_diff={case['gold_diff']}, kill_diff={case['kill_diff']}, tower_diff={case['tower_diff']}")
    print(f"  Win Probability: {prob*100:.2f}%")

# Check scaler and model details
scaler = joblib.load(SCALER_PATH)
print("\n" + "=" * 70)
print("Scaler details:")
print(f"  Mean: {scaler.mean_}")
print(f"  Scale: {scaler.scale_}")

print("\nModel coefficients:")
print(f"  {model_obj.model.coef_[0]}")
print(f"  Intercept: {model_obj.model.intercept_[0]}")
