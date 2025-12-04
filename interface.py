import os
import pandas as pd
from model import RandomForestWinModel
import joblib
MODEL_PATH = os.path.join("data", "winprob_model.joblib")
FEATURES = [
    'kill_diff','death_diff','assist_diff','gold_diff','cs_diff',
    'dmg_dealt_diff','dmg_taken_diff','dragon_diff','baron_diff',
    'tower_diff','game_duration'
]

FEATURE_MEDIANS_PATH = os.path.join("data", "feature_medians.joblib")

class WinProbabilityInterface:
    def __init__(self):
        self.model = RandomForestWinModel(MODEL_PATH)
        if not self.model.load():
            raise FileNotFoundError("Model not found. Train the model first.")

        # Load median feature values
        if os.path.exists(FEATURE_MEDIANS_PATH):
            self.feature_defaults = joblib.load(FEATURE_MEDIANS_PATH)
        elif self.model.feature_means is not None:
            self.feature_defaults = self.model.feature_means
        else:
            self.feature_defaults = {f: 0 for f in FEATURES}

    def predict(self, **kwargs):
        data = {}
        defaults_used = {}
        for f in FEATURES:
            if f in kwargs:
                data[f] = kwargs[f]
            else:
                data[f] = self.feature_defaults.get(f, 0)
                defaults_used[f] = data[f]

        df = pd.DataFrame([data])
        prob = self.model.predict(df)[0]

        if defaults_used:
            print("Using default values for missing features:")
            for k, v in defaults_used.items():
                print(f"  {k}: {v}")

        return prob

