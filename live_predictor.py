import time
import threading
import pandas as pd
from live_client import LiveClientAPI
from overlay import WinRateOverlay
from interface import WinProbabilityInterface

class LiveWinRatePredictor:
    """Main application coordinating API polling, prediction, and UI updates"""
    
    def __init__(self, update_interval=30):
        self.update_interval = update_interval
        self.api_client = LiveClientAPI()
        self.predictor = WinProbabilityInterface()
        self.overlay = WinRateOverlay()
        self.running = False
        
    def predict_from_live_data(self):
        """Fetch live data and make prediction"""
        try:
            # Check if game is running
            if not self.api_client.is_game_running():
                return None, "No game running"
            
            # Fetch and extract features
            game_data = self.api_client.get_all_game_data()
            features = self.api_client.extract_features(game_data)
            
            # Make prediction
            win_prob = self.predictor.predict(**features)
            
            return win_prob, "Updated just now"
            
        except Exception as e:
            return None, f"Error: {str(e)[:30]}"
    
    def update_loop(self):
        """Background thread that polls API and updates overlay"""
        while self.running:
            win_prob, status = self.predict_from_live_data()
            
            if win_prob is not None:
                self.overlay.update_win_rate(win_prob)
                self.overlay.update_status(status)
            else:
                self.overlay.update_status(status)
            
            # Wait for next update
            time.sleep(self.update_interval)
    
    def start(self):
        """Start the predictor and overlay"""
        self.running = True
        
        # Start update thread
        self.update_thread = threading.Thread(target=self.update_loop, daemon=True)
        self.update_thread.start()
        
        # Run overlay (blocking)
        self.overlay.run()
        
    def stop(self):
        """Stop the predictor"""
        self.running = False
        self.overlay.destroy()


if __name__ == "__main__":
    print("Starting Live Win Rate Predictor...")
    print("Make sure you have a League game running!")
    print("The overlay will appear in the top-right corner.")
    print("Press Ctrl+C to exit.\n")
    
    predictor = LiveWinRatePredictor(update_interval=30)
    
    try:
        predictor.start()
    except KeyboardInterrupt:
        print("\nShutting down...")
        predictor.stop()
