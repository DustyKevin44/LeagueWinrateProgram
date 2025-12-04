import os
import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

FEATURE_MEANS_PATH = "data/feature_means.joblib"

class ModelBase:
    """Abstract base class for models"""
    def train(self, X, y):
        raise NotImplementedError
    def predict(self, X):
        raise NotImplementedError

class RandomForestWinModel(ModelBase):
    def __init__(self, model_path):
        self.model_path = model_path
        self.model = None
        self.feature_means = None

    def train(self, X, y):
        # Train model
        self.model = RandomForestClassifier(n_estimators=300, random_state=42)
        self.model.fit(X, y)

        # Save feature means for defaults
        self.feature_means = X.mean().to_dict()
        os.makedirs(os.path.dirname(FEATURE_MEANS_PATH), exist_ok=True)
        joblib.dump(self.feature_means, FEATURE_MEANS_PATH)

    def predict(self, X):
        return self.model.predict_proba(X)[:, 1]

    def save(self):
        joblib.dump(self.model, self.model_path)
        if self.feature_means is not None:
            joblib.dump(self.feature_means, FEATURE_MEANS_PATH)

    def load(self):
        loaded = False
        if os.path.exists(self.model_path):
            self.model = joblib.load(self.model_path)
            loaded = True
        # Load feature means if exists
        if os.path.exists(FEATURE_MEANS_PATH):
            self.feature_means = joblib.load(FEATURE_MEANS_PATH)
        return loaded
