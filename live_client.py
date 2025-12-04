import requests
import urllib3

# Disable SSL warnings for local API
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class LiveClientAPI:
    """Interface to League of Legends Live Client Data API"""
    
    BASE_URL = "https://127.0.0.1:2999/liveclientdata"
    
    def __init__(self):
        self.session = requests.Session()
        self.session.verify = False  # Local API uses self-signed cert
    
    def is_game_running(self):
        """Check if a game is currently running"""
        try:
            response = self.session.get(f"{self.BASE_URL}/activeplayername", timeout=2)
            return response.status_code == 200
        except:
            return False
    
    def get_all_game_data(self):
        """Fetch complete game state"""
        try:
            response = self.session.get(f"{self.BASE_URL}/allgamedata", timeout=2)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to fetch game data: {e}")
    
    def extract_features(self, game_data):
        """
        Extract features for win prediction from live game data.
        
        Returns dict with keys matching the trained model:
        - kill_diff, assist_diff, gold_diff, cs_diff,
          dragon_diff, baron_diff, tower_diff, game_duration
        """
        try:
            # Get all players
            all_players = game_data.get('allPlayers', [])
            
            # Separate by team
            blue_team = [p for p in all_players if p.get('team') == 'ORDER']
            red_team = [p for p in all_players if p.get('team') == 'CHAOS']
            
            # Aggregate player stats from scores
            blue_kills = sum(p.get('scores', {}).get('kills', 0) for p in blue_team)
            red_kills = sum(p.get('scores', {}).get('kills', 0) for p in red_team)
            
            blue_assists = sum(p.get('scores', {}).get('assists', 0) for p in blue_team)
            red_assists = sum(p.get('scores', {}).get('assists', 0) for p in red_team)
            
            blue_cs = sum(p.get('scores', {}).get('creepScore', 0) for p in blue_team)
            red_cs = sum(p.get('scores', {}).get('creepScore', 0) for p in red_team)
            
            # Calculate gold from item prices (more accurate than currentGold)
            def calculate_team_gold(team):
                total_gold = 0
                for player in team:
                    items = player.get('items', [])
                    for item in items:
                        total_gold += item.get('price', 0)
                return total_gold
            
            blue_gold = calculate_team_gold(blue_team)
            red_gold = calculate_team_gold(red_team)
            
            # Get events for objectives (towers, dragons, barons)
            events = game_data.get('events', {}).get('Events', [])
            
            # Get player names for team identification
            blue_names = [p.get('summonerName') for p in blue_team]
            red_names = [p.get('summonerName') for p in red_team]
            
            # Count objectives
            blue_towers = len([e for e in events if e.get('EventName') == 'TurretKilled' and e.get('KillerName') in blue_names])
            red_towers = len([e for e in events if e.get('EventName') == 'TurretKilled' and e.get('KillerName') in red_names])
            
            blue_dragons = len([e for e in events if e.get('EventName') == 'DragonKill' and e.get('KillerName') in blue_names])
            red_dragons = len([e for e in events if e.get('EventName') == 'DragonKill' and e.get('KillerName') in red_names])
            
            blue_barons = len([e for e in events if e.get('EventName') == 'BaronKill' and e.get('KillerName') in blue_names])
            red_barons = len([e for e in events if e.get('EventName') == 'BaronKill' and e.get('KillerName') in red_names])
            
            # Game time
            game_time = game_data.get('gameData', {}).get('gameTime', 0)
            
            # Calculate diffs (MUST match training features exactly)
            features = {
                'kill_diff': blue_kills - red_kills,
                'assist_diff': blue_assists - red_assists,
                'gold_diff': blue_gold - red_gold,
                'cs_diff': blue_cs - red_cs,
                'dragon_diff': blue_dragons - red_dragons,
                'baron_diff': blue_barons - red_barons,
                'tower_diff': blue_towers - red_towers,
                'game_duration': game_time
            }
            
            return features
            
        except Exception as e:
            raise Exception(f"Failed to extract features: {e}")


if __name__ == "__main__":
    # Test the API client
    client = LiveClientAPI()
    
    if client.is_game_running():
        print("Game is running!")
        try:
            data = client.get_all_game_data()
            features = client.extract_features(data)
            print("\nExtracted Features:")
            for key, value in features.items():
                print(f"  {key}: {value}")
        except Exception as e:
            print(f"Error: {e}")
    else:
        print("No game running. Start a League game and try again.")
