import os
import pandas as pd
from model import RandomForestWinModel

MODEL_PATH = os.path.join("data", "winprob_model.joblib")
FEATURES = [
    'kill_diff','assist_diff','gold_diff','cs_diff',
    'dragon_diff','baron_diff','tower_diff','game_duration'
]

class WinProbabilityInterface:
    def __init__(self):
        self.model = RandomForestWinModel(MODEL_PATH)
        if not self.model.load():
            print("Warning: Model not found at", MODEL_PATH)

    def predict(self, **kwargs):
        data = {}
        
        for f in FEATURES:
            data[f] = kwargs.get(f, 0)

        # Hybrid approach: Use heuristic for early game, model for mid/late game
        tower_diff = data.get('tower_diff', 0)
        game_time = data.get('game_duration', 0)
        
        # Early game (no towers down yet): Use simple heuristic
        if tower_diff == 0 and game_time < 600:  # Before 10 minutes and no towers
            return self._early_game_heuristic(data)
        
        # Mid/Late game: Use Random Forest model
        df = pd.DataFrame([data])
        df = df[FEATURES]
        
        try:
            prob = self.model.predict(df)[0]
        except Exception as e:
            print(f"Error predicting: {e}")
            return 0.5

        return prob
    
    def _early_game_heuristic(self, data):
        """
        Simple heuristic for early game before first tower falls.
        Focuses on gold, kills, and CS since towers haven't become important yet.
        """
        # Base probability
        base_prob = 0.5
        
        # Gold advantage (most important early)
        gold_diff = data.get('gold_diff', 0)
        gold_impact = gold_diff / 10000  # +1000 gold = +0.1 (10%)
        
        # Kill advantage
        kill_diff = data.get('kill_diff', 0)
        kill_impact = kill_diff * 0.03  # Each kill = 3%
        
        # CS advantage
        cs_diff = data.get('cs_diff', 0)
        cs_impact = cs_diff / 100  # +10 CS = +0.1 (10%)
        
        # Dragon advantage (minor early)
        dragon_diff = data.get('dragon_diff', 0)
        dragon_impact = dragon_diff * 0.05  # Each dragon = 5%
        
        # Combine impacts
        total_impact = gold_impact + kill_impact + cs_impact + dragon_impact
        
        # Clamp to reasonable range [0.1, 0.9]
        prob = base_prob + total_impact
        prob = max(0.1, min(0.9, prob))
        
        return prob
