import os
import joblib
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import StandardScaler

FEATURE_MEANS_PATH = "data/feature_means.joblib"
MODEL_PATH = "data/winprob_model.joblib"
SCALER_PATH = "data/scaler.joblib"

class ModelBase:
    """Abstract base class for models"""
    def train(self, X, y):
        raise NotImplementedError
    def predict(self, X):
        raise NotImplementedError

class RandomForestWinModel(ModelBase):
    # Keeping the name 'RandomForestWinModel' to avoid breaking interface.py imports immediately,
    # but implementation is now Logistic Regression (or we can rename it).
    # Let's rename it to 'WinModel' or keep it and update interface.py.
    # User asked to "rework interface.py", so I can change the name.
    # But to minimize changes, I'll keep the class name but change the implementation.
    # Actually, let's rename it to 'WinProbabilityModel' to be more generic.
    
    def __init__(self, model_path):
        self.model_path = model_path
        self.model = None
        self.scaler = None

    def train(self, X, y):
        # Split data
        X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

        # Scale data (important for LR)
        self.scaler = StandardScaler()
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_val_scaled = self.scaler.transform(X_val)

        # Train model (Logistic Regression)
        self.model = LogisticRegression(max_iter=1000, random_state=42, class_weight='balanced')
        self.model.fit(X_train_scaled, y_train)

        # Save scaler
        os.makedirs(os.path.dirname(SCALER_PATH), exist_ok=True)
        joblib.dump(self.scaler, SCALER_PATH)
        
        # Evaluate
        self.evaluate(X_val_scaled, y_val)

    def evaluate(self, X, y):
        if self.model is None:
            print("Model not trained.")
            return
        
        y_pred = self.model.predict(X)
        acc = accuracy_score(y, y_pred)
        print(f"Model Accuracy: {acc:.4f}")
        print("Classification Report:")
        print(classification_report(y, y_pred))
        
        # Print coefficients
        if hasattr(self.model, 'coef_'):
            print("\nCoefficients:")
            # We don't have feature names here easily unless we pass them or store them
            # But we can print the array
            print(self.model.coef_)
            print("Intercept:", self.model.intercept_)
            
        return acc

    def predict(self, X):
        if self.model is None:
            raise ValueError("Model not loaded or trained.")
        
        # Scale input
        if self.scaler:
            X = self.scaler.transform(X)
            
        return self.model.predict_proba(X)[:, 1]

    def save(self):
        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
        joblib.dump(self.model, self.model_path)
        if self.scaler:
            joblib.dump(self.scaler, SCALER_PATH)

    def load(self):
        loaded = False
        if os.path.exists(self.model_path):
            self.model = joblib.load(self.model_path)
            loaded = True
        if os.path.exists(SCALER_PATH):
            self.scaler = joblib.load(SCALER_PATH)
        return loaded
