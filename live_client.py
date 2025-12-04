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
            
            blue_deaths = sum(p.get('scores', {}).get('deaths', 0) for p in blue_team)
            red_deaths = sum(p.get('scores', {}).get('deaths', 0) for p in red_team)
            
            blue_assists = sum(p.get('scores', {}).get('assists', 0) for p in blue_team)
            red_assists = sum(p.get('scores', {}).get('assists', 0) for p in red_team)
            
            blue_cs = sum(p.get('scores', {}).get('creepScore', 0) for p in blue_team)
            red_cs = sum(p.get('scores', {}).get('creepScore', 0) for p in red_team)
            
            blue_ward = sum(p.get('scores', {}).get('wardScore', 0.0) for p in blue_team)
            red_ward = sum(p.get('scores', {}).get('wardScore', 0.0) for p in red_team)
            
            blue_levels = sum(p.get('level', 1) for p in blue_team)
            red_levels = sum(p.get('level', 1) for p in red_team)
            
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
            
            # IMPORTANT: Events use player names as KillerName
            # We need to check if the killer is on blue or red team
            
            # Count objectives by team
            blue_towers = 0
            red_towers = 0
            blue_dragons = 0
            red_dragons = 0
            blue_barons = 0
            red_barons = 0
            blue_heralds = 0
            red_heralds = 0
            blue_inhibs = 0
            red_inhibs = 0
            blue_grubs = 0
            red_grubs = 0
            blue_first_blood = 0  # 0 or 1
            red_first_blood = 0   # 0 or 1
            
            for event in events:
                event_name = event.get('EventName', '')
                killer_name = event.get('KillerName', '')
                
                # Determine which team got the objective
                # Check if killer is on blue or red team
                is_blue_kill = killer_name in blue_names
                is_red_kill = killer_name in red_names
                
                # Count objectives
                if event_name == 'TurretKilled':
                    if is_blue_kill:
                        blue_towers += 1
                    elif is_red_kill:
                        red_towers += 1
                
                elif event_name == 'DragonKill':
                    if is_blue_kill:
                        blue_dragons += 1
                    elif is_red_kill:
                        red_dragons += 1
                
                elif event_name == 'BaronKill':
                    if is_blue_kill:
                        blue_barons += 1
                    elif is_red_kill:
                        red_barons += 1
                
                elif event_name == 'HeraldKill':
                    if is_blue_kill:
                        blue_heralds += 1
                    elif is_red_kill:
                        red_heralds += 1
                        
                elif event_name == 'HordeKill':  # Void Grubs
                    if is_blue_kill:
                        blue_grubs += 1
                    elif is_red_kill:
                        red_grubs += 1
                
                elif event_name == 'InhibKilled':
                    if is_blue_kill:
                        blue_inhibs += 1
                    elif is_red_kill:
                        red_inhibs += 1
                        
                elif event_name == 'FirstBlood':
                    recipient = event.get('Recipient', '')
                    if recipient in blue_names:
                        blue_first_blood = 1
                    elif recipient in red_names:
                        red_first_blood = 1
            
            # Game time
            game_time = game_data.get('gameData', {}).get('gameTime', 0)
            game_minutes = max(game_time / 60, 1)  # Avoid division by zero
            
            # Calculate diffs (MUST match training features exactly)
            kill_diff = blue_kills - red_kills
            death_diff = blue_deaths - red_deaths
            assist_diff = blue_assists - red_assists
            gold_diff = blue_gold - red_gold
            cs_diff = blue_cs - red_cs
            ward_diff = blue_ward - red_ward
            level_diff = blue_levels - red_levels
            dragon_diff = blue_dragons - red_dragons
            baron_diff = blue_barons - red_barons
            tower_diff = blue_towers - red_towers
            herald_diff = blue_heralds - red_heralds
            inhib_diff = blue_inhibs - red_inhibs
            grub_diff = blue_grubs - red_grubs
            first_blood_diff = blue_first_blood - red_first_blood
            
            # Derived features for better prediction
            # KDA differential (more stable than kills alone)
            blue_kda = (blue_kills + blue_assists) / max(blue_deaths, 1)
            red_kda = (red_kills + red_assists) / max(red_deaths, 1)
            kda_diff = blue_kda - red_kda
            
            # Gold efficiency (gold per kill)
            gold_per_kill = gold_diff / max(abs(kill_diff), 1)
            
            # CS efficiency (CS per minute)
            cs_per_min_diff = cs_diff / game_minutes
            
            # Objective score (weighted by importance)
            objective_score = (
                tower_diff * 1.0 +
                dragon_diff * 1.5 +
                herald_diff * 1.2 +
                baron_diff * 3.0 +
                inhib_diff * 2.5
            )
            
            features = {
                # Core stats
                'kill_diff': kill_diff,
                'death_diff': death_diff,
                'assist_diff': assist_diff,
                'gold_diff': gold_diff,
                'cs_diff': cs_diff,
                'ward_score_diff': ward_diff,
                'level_diff': level_diff,
                
                # Objectives
                'dragon_diff': dragon_diff,
                'baron_diff': baron_diff,
                'tower_diff': tower_diff,
                'herald_diff': herald_diff,
                'inhib_diff': inhib_diff,
                
                # Derived features
                'kda_diff': kda_diff,
                'gold_per_kill': gold_per_kill,
                'cs_per_min_diff': cs_per_min_diff,
                'objective_score': objective_score,
                
                # Time context
                'game_duration': game_time
            }
            
            return features
            
        except KeyError as e:
            raise Exception(f"Missing required data field: {e}")
        except ValueError as e:
            raise Exception(f"Invalid data value: {e}")
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
