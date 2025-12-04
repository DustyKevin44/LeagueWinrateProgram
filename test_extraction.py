import json
from live_client import LiveClientAPI

# Simplified example data focusing on key fields
example_data = {
	"allPlayers": [
		# Blue team (ORDER)
		{
			"championName": "Cho'Gath",
			"items": [
				{"itemID": 1056, "price": 400},  # Doran's Ring
				{"itemID": 2003, "price": 50},   # Health Potion x2
				{"itemID": 1028, "price": 400},  # Ruby Crystal
				{"itemID": 2055, "price": 75},   # Control Ward
				{"itemID": 3340, "price": 0}     # Stealth Ward
			],
			"scores": {"assists": 0, "creepScore": 20, "deaths": 1, "kills": 0},
			"summonerName": "DustyKevin#5978",
			"team": "ORDER"
		},
		{
			"championName": "Lee Sin",
			"items": [{"itemID": 1102, "price": 450}, {"itemID": 3340, "price": 0}],
			"scores": {"assists": 0, "creepScore": 20, "deaths": 0, "kills": 0},
			"summonerName": "Lee Sin Bot",
			"team": "ORDER"
		},
		{
			"championName": "Tryndamere",
			"items": [{"itemID": 1055, "price": 450}, {"itemID": 1042, "price": 250}, {"itemID": 3340, "price": 0}],
			"scores": {"assists": 0, "creepScore": 0, "deaths": 1, "kills": 0},
			"summonerName": "Tryndamere Bot",
			"team": "ORDER"
		},
		{
			"championName": "Sona",
			"items": [{"itemID": 3865, "price": 400}, {"itemID": 3340, "price": 0}],
			"scores": {"assists": 0, "creepScore": 0, "deaths": 0, "kills": 0},
			"summonerName": "Sona Bot",
			"team": "ORDER"
		},
		{
			"championName": "Lucian",
			"items": [{"itemID": 1055, "price": 450}, {"itemID": 3340, "price": 0}],
			"scores": {"assists": 0, "creepScore": 10, "deaths": 0, "kills": 1},
			"summonerName": "Lucian Bot",
			"team": "ORDER"
		},
		# Red team (CHAOS)
		{
			"championName": "Vi",
			"items": [],
			"scores": {"assists": 0, "creepScore": 0, "deaths": 0, "kills": 0},
			"summonerName": "Vi Bot",
			"team": "CHAOS"
		},
		{
			"championName": "Brand",
			"items": [{"itemID": 3070, "price": 400}, {"itemID": 2003, "price": 50}, {"itemID": 3340, "price": 0}],
			"scores": {"assists": 0, "creepScore": 20, "deaths": 0, "kills": 1},
			"summonerName": "Brand Bot",
			"team": "CHAOS"
		},
		{
			"championName": "Udyr",
			"items": [{"itemID": 1054, "price": 450}, {"itemID": 3340, "price": 0}],
			"scores": {"assists": 0, "creepScore": 20, "deaths": 0, "kills": 1},
			"summonerName": "Udyr Bot",
			"team": "CHAOS"
		},
		{
			"championName": "Rakan",
			"items": [{"itemID": 3865, "price": 400}, {"itemID": 2055, "price": 75}, {"itemID": 3340, "price": 0}],
			"scores": {"assists": 0, "creepScore": 0, "deaths": 1, "kills": 0},
			"summonerName": "Rakan Bot",
			"team": "CHAOS"
		},
		{
			"championName": "Jinx",
			"items": [{"itemID": 1055, "price": 450}, {"itemID": 2055, "price": 75}, {"itemID": 1042, "price": 250}, {"itemID": 3340, "price": 0}],
			"scores": {"assists": 0, "creepScore": 0, "deaths": 0, "kills": 0},
			"summonerName": "Jinx Bot",
			"team": "CHAOS"
		}
	],
	"events": {
		"Events": [
			{"EventID": 2, "EventName": "ChampionKill", "KillerName": "Lucian Bot", "VictimName": "Rakan Bot"},
			{"EventID": 4, "EventName": "ChampionKill", "KillerName": "Udyr Bot", "VictimName": "Tryndamere Bot"},
			{"EventID": 5, "EventName": "ChampionKill", "KillerName": "Brand Bot", "VictimName": "DustyKevin"}
		]
	},
	"gameData": {
		"gameTime": 216.91
	}
}

print("Testing feature extraction with updated 8-feature model...")
print("=" * 70)

client = LiveClientAPI()
features = client.extract_features(example_data)

print("\nExtracted Features:")
print("-" * 70)
for key, value in features.items():
    print(f"{key:20s}: {value}")

# Calculate expected values
blue_gold = 400 + 50 + 400 + 75 + 450 + 450 + 250 + 400 + 450  # 2925
red_gold = 400 + 50 + 450 + 400 + 75 + 450 + 75 + 250  # 2150
expected_gold_diff = blue_gold - red_gold

print("\n" + "=" * 70)
print("Expected values:")
print("-" * 70)
print(f"{'kill_diff':20s}: 1 - 2 = -1 (Blue: 1 kill, Red: 2 kills)")
print(f"{'assist_diff':20s}: 0 - 0 = 0")
print(f"{'gold_diff':20s}: {blue_gold} - {red_gold} = {expected_gold_diff}")
print(f"{'cs_diff':20s}: 50 - 40 = 10 (Blue: 50 CS, Red: 40 CS)")
print(f"{'dragon_diff':20s}: 0")
print(f"{'baron_diff':20s}: 0")
print(f"{'tower_diff':20s}: 0")
print(f"{'game_duration':20s}: ~217 seconds")

print("\n" + "=" * 70)
print("Testing prediction interface...")
print("-" * 70)

from interface import WinProbabilityInterface

interface = WinProbabilityInterface()
try:
    win_prob = interface.predict(**features)
    print(f"\nWin Probability: {win_prob*100:.2f}%")
    print("SUCCESS - Prediction works with 8-feature model!")
except Exception as e:
    print(f"\nERROR during prediction: {e}")
