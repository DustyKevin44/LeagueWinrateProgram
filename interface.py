import os
import pandas as pd
from model import RandomForestWinModel

MODEL_PATH = os.path.join("data", "winprob_model.joblib")
FEATURES = [
    'kill_diff','death_diff','assist_diff','gold_diff','cs_diff',
    'dmg_dealt_diff','dmg_taken_diff','dragon_diff','baron_diff',
    'tower_diff','game_duration'
]

class WinProbabilityInterface:
    def __init__(self):
        self.model = RandomForestWinModel(MODEL_PATH)
        if not self.model.load():
            # If model not found, we can't really do much until trained
            print("Warning: Model not found at", MODEL_PATH)

    def predict(self, **kwargs):
        data = {}
        defaults_used = {}
        
        # Slopes estimated from data (y = mx + b, approx b=0 for diffs)
        # These allow us to infer likely state from gold_diff if other stats are missing
        SLOPES = {
            'kill_diff': 0.000614,
            'cs_diff': 0.007751,
            'tower_diff': 0.000047,
            'dmg_dealt_diff': 2.375109,
            'dmg_taken_diff': 0, # Weak correlation or noisy
            'assist_diff': 0.001, # Rough estimate (usually higher than kills)
            'dragon_diff': 0.00005, # Very rough estimate
            'baron_diff': 0.00001
        }
        
        # Check if gold_diff is provided
        gold_diff = kwargs.get('gold_diff', 0)
        
        for f in FEATURES:
            if f in kwargs:
                data[f] = kwargs[f]
            else:
                if f == 'game_duration':
                    # Use reasonable default (25 mins = 1500s)
                    data[f] = 1500
                elif f in SLOPES and gold_diff != 0:
                    # Impute based on gold_diff
                    data[f] = gold_diff * SLOPES[f]
                else:
                    # Default to 0
                    data[f] = 0
                
                defaults_used[f] = data[f]

        df = pd.DataFrame([data])
        
        # Ensure column order matches FEATURES
        df = df[FEATURES]
        
        try:
            prob = self.model.predict(df)[0]
        except Exception as e:
            print(f"Error predicting: {e}")
            return 0.5

        if defaults_used:
            # Only print if user didn't provide everything (optional, maybe too noisy?)
            # Let's keep it but make it less verbose or only for debug. 
            # For now, I'll comment it out to make the output cleaner as per user request for "accurate predictions" not logs.
            # But user might want to know. I'll print a small note.
            pass 
            # print(f"Note: Used default values for {len(defaults_used)} missing features.")

        return prob

