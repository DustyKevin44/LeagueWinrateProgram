import os
import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

MODEL_PATH = "data/winprob_model.joblib"
FEATURE_MEANS_PATH = "data/feature_means.joblib"
FEATURES = [
    'kill_diff','death_diff','assist_diff','gold_diff','cs_diff',
    'dmg_dealt_diff','dmg_taken_diff','dragon_diff','baron_diff',
    'tower_diff','game_duration'
]

class ModelManager:
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.features = FEATURES

    def train(self, X: pd.DataFrame, y: pd.Series):
        """Trains model and saves it with feature means."""
        # Split data
        X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

        # Train model
        self.model.fit(X_train, y_train)

        # Save model
        os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
        joblib.dump(self.model, MODEL_PATH)

        # Save feature means
        feature_means = X_train.mean().to_dict()
        joblib.dump(feature_means, FEATURE_MEANS_PATH)
        print(f"Model and feature means saved. Validation score: {self.model.score(X_val, y_val):.4f}")

    def load(self):
        """Loads the model from disk."""
        if os.path.exists(MODEL_PATH):
            self.model = joblib.load(MODEL_PATH)
            return True
        return False
