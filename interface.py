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
    'kill_diff', 'assist_diff', 'gold_diff', 'cs_diff',
    'ward_score_diff', 'level_diff',
    # Objectives
    'dragon_diff', 'baron_diff', 'tower_diff', 'herald_diff', 'inhib_diff',
    # Time context
    'game_duration',
    # Derived interaction features (model learns these!)
    'combat_power', 'tower_combat_mismatch', 'push_capability',
    'economic_advantage', 'objective_control'
]

class WinProbabilityInterface:
    def __init__(self):
        self.model = RandomForestWinModel(MODEL_PATH)
        if not self.model.load():
            print("Warning: Model not found at", MODEL_PATH)
        
        # Calibration parameters to fix symmetry
        # The model has asymmetric predictions because it was trained on full-game data
        # where towers/objectives matter most. We need to:
        #   1. Center the baseline at 50%
        #   2. Make it more symmetric
        #   3. Increase sensitivity to early-game features like gold
        
        # Empirically measured baseline (all zeros with small game_duration)
        self.baseline_raw = 0.458
        
        # Use a two-stage calibration:
        # Stage 1: Re-center around 0.5
        # Stage 2: Apply non-linear mapping to fix asymmetry and boost sensitivity
        
    def _calibrate(self, raw_prob):
        """
        Apply piecewise calibration to fix symmetry and sensitivity.
        
        The model's raw predictions have these issues:
        - Baseline (~0.458) should be 0.50
        - Asymmetric: advantage predictions are compressed, disadvantage predictions are too extreme
        - Insensitive: 2000 gold advantage barely moves the needle
        
        We apply a piecewise mapping with different curves for each side:
        - Map 0 → 0 (total loss)
        - Map baseline (0.458) → 0.50 (even game)
        - Map extremes with power curves to boost middle range and improve symmetry
        - Map 1 → 1 (total win)
        """
        
        if raw_prob <= 0.01:
            return 0.0
        elif raw_prob >= 0.99:
            return 1.0
        
        # Piecewise calibration with different handling for each side
        
        if raw_prob < self.baseline_raw:
            # Below baseline: map [0, 0.458] → [0, 0.5]
            # The model tends to be too extreme on the low end
            normalized = raw_prob / self.baseline_raw  # 0 to 1
            
            # Use power curve to compress extreme values human: 0.8 makes it less extreme)
            compressed = normalized ** 0.8
            
            return compressed * 0.5
        else:
            # Above baseline: map [0.458, 1.0] → [0.5, 1.0]
            # The model tends to be too conservative on the high end
            normalized = (raw_prob - self.baseline_raw) / (1.0 - self.baseline_raw)  # 0 to 1
            
            # Use power curve to boost sensitivity (< 1.0 boosts middle range)
            boosted = normalized ** 0.5
            
            return 0.5 + (boosted * 0.5)

    def _calculate_derived_features(self, **kwargs):
        """
        Calculate derived interaction features from base features.
        These are the SAME formulas used in training!
        """
        # Extract base features
        kill_diff = kwargs.get('kill_diff', 0)
        gold_diff = kwargs.get('gold_diff', 0)
        level_diff = kwargs.get('level_diff', 0)
        baron_diff = kwargs.get('baron_diff', 0)
        dragon_diff = kwargs.get('dragon_diff', 0)
        tower_diff = kwargs.get('tower_diff', 0)
        herald_diff = kwargs.get('herald_diff', 0)
        inhib_diff = kwargs.get('inhib_diff', 0)
        cs_diff = kwargs.get('cs_diff', 0)
        
        # Calculate derived features (must match feature_engineer.py!)
        combat_power = (
            kill_diff / 10.0 +
            gold_diff / 3000.0 +
            level_diff / 10.0 +
            baron_diff * 3.0 +
            dragon_diff * 0.5
        )
        
        tower_combat_mismatch = tower_diff - combat_power
        
        push_capability = (
            combat_power +
            baron_diff * 2.0 +
            herald_diff * 1.0
        )
        
        economic_advantage = (
            gold_diff / 1000.0 +
            cs_diff / 50.0
        )
        
        objective_control = (
            dragon_diff * 1.0 +
            baron_diff * 3.0 +
            tower_diff * 2.0 +
            herald_diff * 1.5 +
            inhib_diff * 4.0
        )
        
        return {
            'combat_power': combat_power,
            'tower_combat_mismatch': tower_combat_mismatch,
            'push_capability': push_capability,
            'economic_advantage': economic_advantage,
            'objective_control': objective_control
        }

    def predict(self, **kwargs):
        """
        Predict win probability using the trained Random Forest model with calibration.
        
        Calibration ensures:
        - Game start (all zeros) → 50% prediction
        - Better symmetry: +X and -X are symmetric around 50%
        - More responsive to gold/stats differences in early game
        
        Model now learns tower-taking capability from DATA instead of heuristics!
        """
        data = {}
        
        # Fill in base features
        for f in FEATURES:
            if f not in ['combat_power', 'tower_combat_mismatch', 'push_capability', 
                         'economic_advantage', 'objective_control']:
                data[f] = kwargs.get(f, 0)
        
        # Calculate derived features
        derived = self._calculate_derived_features(**kwargs)
        data.update(derived)
            
        # Create DataFrame for prediction
        df = pd.DataFrame([data])
        df = df[FEATURES]  # Ensure correct order
        
        try:
            # Use the full Random Forest model
            # Model will use the derived features to understand tower-taking capability!
            raw_prob = self.model.predict(df)[0]
            
            # Apply calibration for symmetry
            calibrated_prob = self._calibrate(raw_prob)
            
            # Clamp to valid probability range
            final_prob = max(0.0, min(1.0, calibrated_prob))
            
            return final_prob
            
        except Exception as e:
            print(f"Error predicting: {e}")
            # Failsafe: return 50% if model fails
            return 0.5
