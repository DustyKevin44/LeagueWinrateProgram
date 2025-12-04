import sys
import os
import pandas as pd
from model import RandomForestWinModel

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

MODEL_PATH = resource_path(os.path.join("data", "winprob_model.joblib"))
FEATURES = [
    # Core stats
    'kill_diff', 'death_diff', 'assist_diff', 'gold_diff', 'cs_diff',
    'ward_score_diff', 'level_diff',
    # Objectives
    'dragon_diff', 'baron_diff', 'tower_diff', 'herald_diff', 'inhib_diff',
    # Derived features
    'kda_diff', 'gold_per_kill', 'cs_per_min_diff', 'objective_score',
    # Time context
    'game_duration'
]

class WinProbabilityInterface:
    def __init__(self):
        self.model = RandomForestWinModel(MODEL_PATH)
        if not self.model.load():
            print("Warning: Model not found at", MODEL_PATH)

    def predict(self, **kwargs):
        """
        Predict win probability using the trained Random Forest model.
        """
        data = {}
        
        # Fill in all features with failsafe defaults
        for f in FEATURES:
            data[f] = kwargs.get(f, 0)
            
        # Create DataFrame for prediction
        df = pd.DataFrame([data])
        df = df[FEATURES]
        
        try:
            # Use the full Random Forest model
            prob = self.model.predict(df)[0]
            
            # Sanity check: clamp to valid probability range
            prob = max(0.0, min(1.0, prob))
            
            return prob
            
        except Exception as e:
            print(f"Error predicting: {e}")
            # Failsafe: return 50% if model fails
            return 0.5
