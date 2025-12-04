"""
Test script to debug live API feature extraction
Prints all events and extracted features to help diagnose issues
"""

from live_client import LiveClientAPI
import json

client = LiveClientAPI()

if client.is_game_running():
    print("=" * 80)
    print("GAME DETECTED - Fetching data...")
    print("=" * 80)
    
    try:
        data = client.get_all_game_data()
        
        # Print all events
        events = data.get('events', {}).get('Events', [])
        print(f"\nTotal events: {len(events)}")
        print("\nEvent types found:")
        event_types = {}
        for e in events:
            event_name = e.get('EventName', 'Unknown')
            event_types[event_name] = event_types.get(event_name, 0) + 1
        
        for event_name, count in sorted(event_types.items()):
            print(f"  {event_name}: {count}")
        
        # Print sample events
        print("\nSample events:")
        for e in events[:10]:
            print(f"  {e}")
        
        # Extract features
        print("\n" + "=" * 80)
        print("EXTRACTED FEATURES:")
        print("=" * 80)
        features = client.extract_features(data)
        for key, value in sorted(features.items()):
            print(f"  {key:20s}: {value}")
        
        # Check for issues
        print("\n" + "=" * 80)
        print("DIAGNOSTICS:")
        print("=" * 80)
        
        if features['herald_diff'] == 0 and any(e.get('EventName') == 'HeraldKill' for e in events):
            print("  [WARNING] Herald events found but herald_diff is 0!")
            herald_events = [e for e in events if e.get('EventName') == 'HeraldKill']
            print(f"  Herald events: {herald_events}")
        
        if features['dragon_diff'] == 0 and any(e.get('EventName') == 'DragonKill' for e in events):
            print("  [WARNING] Dragon events found but dragon_diff is 0!")
            dragon_events = [e for e in events if e.get('EventName') == 'DragonKill']
            print(f"  Dragon events: {dragon_events}")
        
        if features['inhib_diff'] == 0 and any(e.get('EventName') == 'InhibKilled' for e in events):
            print("  [WARNING] Inhibitor events found but inhib_diff is 0!")
        
        print("\n[OK] Feature extraction completed successfully")
        
    except Exception as e:
        print(f"\n[ERROR] {e}")
        import traceback
        traceback.print_exc()
else:
    print("No game running. Start a League game and try again.")
