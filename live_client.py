import requests
import urllib3
import re

# Disable SSL warnings for local API
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# GLOBAL REGEX — removes everything except letters and numbers
_non_alnum = re.compile(r"[^a-z0-9]+")

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


    # ----------------------------
    # NORMALIZATION
    # ----------------------------

    def _normalize(self, name):
        if not name:
            return ""
        n = str(name).lower().strip()
        # Remove spaces, punctuation, symbols
        n = _non_alnum.sub("", n)
        return n
    

    # ----------------------------
    # NAME COLLECTION
    # ----------------------------

    def collect_player_names(self, player):
        """
        Build a *complete* set of possible identifiers for matching.
        """
        names = set()

        fields = [
            "summonerName", "riotIdGameName", "riotId",
            "championName", "rawChampionName"
        ]

        for f in fields:
            v = player.get(f)
            if v:
                names.add(self._normalize(v))

        # Combine gamename + tagline
        rg = player.get("riotIdGameName")
        rt = player.get("riotIdTagLine")
        if rg and rt:
            names.add(self._normalize(f"{rg}{rt}"))
            names.add(self._normalize(f"{rg}-{rt}"))
            names.add(self._normalize(f"{rg}#{rt}"))

        return names


    def belongs_to_team(self, raw_name, team_set):
        """Return True if the given raw_name matches known normalized names."""
        if not raw_name:
            return False
        return self._normalize(raw_name) in team_set


    # ----------------------------
    # GOLD EXTRACTION
    # ----------------------------

    def get_player_gold(self, player):
        """
        Returns the best available gold value.
        """
        gold_fields = [
            ("totalGold",),
            ("currentGold",),
            ("scores.goldEarned",),
            ("scores.totalGold",)
        ]

        for f in gold_fields:
            key = f[0]
            if "." in key:
                top, sub = key.split(".", 1)
                tv = player.get(top, {})
                if isinstance(tv, dict) and sub in tv:
                    try:
                        return float(tv[sub])
                    except:
                        pass
            else:
                if key in player:
                    try:
                        return float(player[key])
                    except:
                        pass

        # Fallback: sum item prices
        total = 0
        for it in player.get("items", []) or []:
            try:
                total += float(it.get("price", 0)) * int(it.get("count", 1))
            except:
                pass
        return total


    # ----------------------------
    # MAIN FEATURE EXTRACTION
    # ----------------------------

    def extract_features(self, game_data):
        try:
            all_players = game_data.get("allPlayers", [])

            blue_team = [p for p in all_players if p.get("team") == "ORDER"]
            red_team  = [p for p in all_players if p.get("team") == "CHAOS"]

            # Build robust name lookup tables
            blue_names = set()
            red_names = set()

            for p in blue_team:
                blue_names |= self.collect_player_names(p)

            for p in red_team:
                red_names |= self.collect_player_names(p)

            # ------------ DETECT ACTIVE PLAYER'S TEAM ------------
            # CRITICAL: Model always predicts from Blue's perspective
            # If active player is Red, we need to invert features!
            
            active_player_name = game_data.get("activePlayer", {}).get("summonerName", "")
            player_is_blue = self.belongs_to_team(active_player_name, blue_names)
            player_is_red = self.belongs_to_team(active_player_name, red_names)
            
            # Default to blue if we can't determine (shouldn't happen)
            if not player_is_blue and not player_is_red:
                player_is_blue = True

            # ------------ TEAM STAT TOTALS ------------

            def sum_scores(team, key):
                return sum(p.get("scores", {}).get(key, 0) for p in team)

            blue_kills = sum_scores(blue_team, "kills")
            red_kills  = sum_scores(red_team, "kills")

            blue_deaths = sum_scores(blue_team, "deaths")
            red_deaths  = sum_scores(red_team, "deaths")

            blue_assists = sum_scores(blue_team, "assists")
            red_assists  = sum_scores(red_team, "assists")

            blue_cs = sum_scores(blue_team, "creepScore")
            red_cs  = sum_scores(red_team, "creepScore")

            blue_ward = sum_scores(blue_team, "wardScore")
            red_ward  = sum_scores(red_team, "wardScore")

            blue_levels = sum(p.get("level", 0) for p in blue_team)
            red_levels  = sum(p.get("level", 0) for p in red_team)

            blue_gold = sum(self.get_player_gold(p) for p in blue_team)
            red_gold  = sum(self.get_player_gold(p) for p in red_team)


            # ------------ OBJECTIVES via EVENTS ------------

            blue_towers = red_towers = 0
            blue_dragons = red_dragons = 0
            blue_barons = red_barons = 0
            blue_heralds = red_heralds = 0
            blue_inhibs = red_inhibs = 0
            blue_grubs = red_grubs = 0
            blue_first_blood = red_first_blood = 0

            events = game_data.get("events", {}) or {}
            event_list = events.get("Events") or events.get("events") or []

            for e in event_list:
                name = e.get("EventName", "")
                killer = e.get("KillerName") or e.get("Killer") or ""
                recipient = e.get("Recipient") or ""

                is_blue = self.belongs_to_team(killer, blue_names)
                is_red  = self.belongs_to_team(killer, red_names)

                if name == "TurretKilled":
                    if is_blue: blue_towers += 1
                    if is_red:  red_towers += 1

                elif name == "DragonKill":
                    if is_blue: blue_dragons += 1
                    if is_red:  red_dragons += 1

                elif name == "BaronKill":
                    if is_blue: blue_barons += 1
                    if is_red:  red_barons += 1

                elif name == "HeraldKill":
                    if is_blue: blue_heralds += 1
                    if is_red:  red_heralds += 1

                elif name == "HordeKill":
                    if is_blue: blue_grubs += 1
                    if is_red:  red_grubs += 1

                elif name == "InhibKilled":
                    if is_blue: blue_inhibs += 1
                    if is_red:  red_inhibs += 1

                elif name == "FirstBlood":
                    if self.belongs_to_team(recipient, blue_names):
                        blue_first_blood = 1
                    elif self.belongs_to_team(recipient, red_names):
                        red_first_blood = 1


            # ------------ GAME TIME ------------

            game_time = game_data.get("gameData", {}).get("gameTime", 0)

            # ------------ FEATURE DIFFS (from active player's perspective) ------------
            
            # Calculate differences (Blue - Red)
            kill_diff    = blue_kills - red_kills
            assist_diff  = blue_assists - red_assists
            gold_diff    = blue_gold - red_gold
            cs_diff      = blue_cs - red_cs
            ward_diff    = blue_ward - red_ward
            level_diff   = blue_levels - red_levels

            dragon_diff  = blue_dragons - red_dragons
            baron_diff   = blue_barons - red_barons
            tower_diff   = blue_towers - red_towers
            herald_diff  = blue_heralds - red_heralds
            inhib_diff   = blue_inhibs - red_inhibs
            
            # CRITICAL FIX: If player is on RED team, invert all differentials!
            # The model was trained to predict Blue's win probability
            # So if player is Red, we need to flip the perspective
            if player_is_red:
                kill_diff = -kill_diff
                assist_diff = -assist_diff
                gold_diff = -gold_diff
                cs_diff = -cs_diff
                ward_diff = -ward_diff
                level_diff = -level_diff
                dragon_diff = -dragon_diff
                baron_diff = -baron_diff
                tower_diff = -tower_diff
                herald_diff = -herald_diff
                inhib_diff = -inhib_diff

            # Return ONLY features that the model was trained on
            # Plus diagnostic info
            features = {
                # Core stats
                "kill_diff": kill_diff,
                "assist_diff": assist_diff,
                "gold_diff": gold_diff,
                "cs_diff": cs_diff,
                "ward_score_diff": ward_diff,
                "level_diff": level_diff,
                
                # Objectives
                "dragon_diff": dragon_diff,
                "baron_diff": baron_diff,
                "tower_diff": tower_diff,
                "herald_diff": herald_diff,
                "inhib_diff": inhib_diff,
                
                # Time context
                "game_duration": game_time,
                
                # Diagnostic (not used by model, just for debugging)
                "player_team": "BLUE" if player_is_blue else "RED"
            }
            
            return features

        except Exception as e:
            raise Exception(f"Failed to extract features: {e}")


if __name__ == "__main__":
    client = LiveClientAPI()
    
    if client.is_game_running():
        print("Game is running!")
        try:
            data = client.get_all_game_data()
            features = client.extract_features(data)
            print("\nExtracted Features:")
            for key, value in features.items():
                print(f"{key}: {value}")
        except Exception as e:
            print(f"Error: {e}")
    else:
        print("No game running. Start a League game and try again.")
