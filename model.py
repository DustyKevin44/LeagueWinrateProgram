import os
import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

MODEL_PATH = "data/winprob_model.joblib"

class ModelBase:
    """Abstract base class for models"""
    def train(self, X, y):
        raise NotImplementedError
    def predict(self, X):
        raise NotImplementedError

class RandomForestWinModel(ModelBase):
    """Random Forest model - naturally handles feature interactions and game state"""
    
    def __init__(self, model_path):
        self.model_path = model_path
        self.model = None

    def train(self, X, y):
        # Split data
        X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

        # Train Random Forest
        # Random Forest naturally handles:
        # - Feature interactions (e.g., tower_diff importance changes based on game time)
        # - Non-linear relationships
        # - Different feature importance at different game states
        # - Automatically ignores features when they're not informative (e.g., tower_diff=0 early game)
        self.model = RandomForestClassifier(
            n_estimators=50,
            max_depth=10,
            min_samples_split=20,
            min_samples_leaf=10,
            random_state=42,
            class_weight='balanced',
            n_jobs=-1
        )
        self.model.fit(X_train, y_train)
        
        # Evaluate
        self.evaluate(X_val, y_val)
        
        # Print feature importances
        feature_names = X.columns if hasattr(X, 'columns') else [f'feature_{i}' for i in range(X.shape[1])]
        importances = pd.DataFrame({
            'feature': feature_names,
            'importance': self.model.feature_importances_
        }).sort_values('importance', ascending=False)
        
        print("\nFeature Importances:")
        for _, row in importances.iterrows():
            print(f"  {row['feature']:20s}: {row['importance']:.4f}")

    def evaluate(self, X, y):
        if self.model is None:
            print("Model not trained.")
            return
        
        y_pred = self.model.predict(X)
        acc = accuracy_score(y, y_pred)
        print(f"Model Accuracy: {acc:.4f}")
        print("Classification Report:")
        print(classification_report(y, y_pred))
        
        return acc

    def predict(self, X):
        if self.model is None:
            raise ValueError("Model not loaded or trained.")
        
        # No scaling needed for Random Forest
        return self.model.predict_proba(X)[:, 1]

    def save(self):
        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
        joblib.dump(self.model, self.model_path)

    def load(self):
        if os.path.exists(self.model_path):
            self.model = joblib.load(self.model_path)
            return True
        return False
