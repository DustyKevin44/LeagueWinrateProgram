from interface import WinProbabilityInterface
import pandas as pd

def test_predictions():
    interface = WinProbabilityInterface()
    
    print("=" * 60)
    print("SYMMETRY AND STARTING PREDICTION TESTS")
    print("=" * 60)
    
    # Test 1: Game start (all zeros)
    print("\n1. GAME START (all zeros):")
    pred_start = interface.predict(
        kill_diff=0, assist_diff=0, gold_diff=0, cs_diff=0,
        ward_score_diff=0, level_diff=0,
        dragon_diff=0, baron_diff=0, tower_diff=0, herald_diff=0, inhib_diff=0,
        game_duration=60
    )
    print(f"   Win Probability: {pred_start*100:.2f}%")
    print(f"   >>> EXPECTED: ~50%, ACTUAL: {pred_start*100:.2f}%")
    
    # Test 2: Early game with 2000 gold advantage
    print("\n2. EARLY GAME - 2000 Gold Advantage (no other differences):")
    pred_gold_only = interface.predict(
        kill_diff=0, assist_diff=0, gold_diff=2000, cs_diff=0,
        ward_score_diff=0, level_diff=0,
        dragon_diff=0, baron_diff=0, tower_diff=0, herald_diff=0, inhib_diff=0,
        game_duration=300
    )
    print(f"   Win Probability: {pred_gold_only*100:.2f}%")
    print(f"   >>> EXPECTED: >55%, ACTUAL: {pred_gold_only*100:.2f}%")
    
    # Test 3: Symmetric test - positive vs negative gold
    print("\n3. SYMMETRY TEST - Gold Advantage vs Disadvantage:")
    
    gold_values = [-3000, -2000, -1000, 0, 1000, 2000, 3000]
    print(f"   {'Gold Diff':>10} | {'Win%':>8} | Balance")
    print(f"   {'-'*10}-+-{'-'*8}-+--------")
    
    for gold in gold_values:
        pred = interface.predict(
            kill_diff=0, assist_diff=0, gold_diff=gold, cs_diff=0,
            ward_score_diff=0, level_diff=0,
            dragon_diff=0, baron_diff=0, tower_diff=0, herald_diff=0, inhib_diff=0,
            game_duration=600
        )
        balance = "BALANCED" if abs(pred - 0.5) < 0.02 else ("FAVORED" if pred > 0.5 else "BEHIND")
        print(f"   {gold:>10} | {pred*100:>7.2f}% | {balance}")
    
    # Test 4: Feature importance - Gold per kill value
    print("\n4. GOLD PER KILL - Is it captured indirectly?")
    
    # Scenario A: 3 kills = ~900 gold (300 per kill)
    pred_kills_only = interface.predict(
        kill_diff=3, assist_diff=0, gold_diff=0, cs_diff=0,
        ward_score_diff=0, level_diff=0,
        dragon_diff=0, baron_diff=0, tower_diff=0, herald_diff=0, inhib_diff=0,
        game_duration=600
    )
    
    # Scenario B: 3 kills + ~900 gold
    pred_kills_and_gold = interface.predict(
        kill_diff=3, assist_diff=0, gold_diff=900, cs_diff=0,
        ward_score_diff=0, level_diff=0,
        dragon_diff=0, baron_diff=0, tower_diff=0, herald_diff=0, inhib_diff=0,
        game_duration=600
    )
    
    # Scenario C: Just 900 gold (no kills)
    pred_gold_no_kills = interface.predict(
        kill_diff=0, assist_diff=0, gold_diff=900, cs_diff=0,
        ward_score_diff=0, level_diff=0,
        dragon_diff=0, baron_diff=0, tower_diff=0, herald_diff=0, inhib_diff=0,
        game_duration=600
    )
    
    print(f"   A. 3 kills, 0 gold:         {pred_kills_only*100:.2f}%")
    print(f"   B. 3 kills + 900 gold:      {pred_kills_and_gold*100:.2f}%")
    print(f"   C. 0 kills, 900 gold:       {pred_gold_no_kills*100:.2f}%")
    print(f"   >>> If gold_diff already includes kill gold, A~=B")
    print(f"   >>> If gold_diff is NET gold after kills, A<B")
    
    # Test 5: Model bias - checking base prediction
    print("\n5. MODEL BIAS CHECK:")
    print(f"   Game start prediction: {pred_start*100:.2f}%")
    if abs(pred_start - 0.5) > 0.05:
        print(f"   WARNING: Model has significant bias ({abs(pred_start-0.5)*100:.1f}% from 50%)")
        print(f"   This suggests class imbalance or feature leakage in training data")
    else:
        print(f"   Model is reasonably balanced")
    
    # Test 6: Check data for potential class imbalance
    print("\n6. CHECKING TRAINED MODEL STATISTICS:")
    from data_loader import DataLoader
    from feature_engineer import DefaultFeatureEngineer
    
    loader = DataLoader("data")
    match_stats, team_stats, match_tbl, summoner_match = loader.load_match_stats()
    engineer = DefaultFeatureEngineer()
    X, y = engineer.fit_transform(match_stats, team_stats, summoner_match, match_tbl)
    
    blue_wins = y.sum()
    total_games = len(y)
    blue_win_rate = blue_wins / total_games
    
    print(f"   Total games in training: {total_games}")
    print(f"   Blue wins: {blue_wins} ({blue_win_rate*100:.2f}%)")
    print(f"   Red wins: {total_games - blue_wins} ({(1-blue_win_rate)*100:.2f}%)")
    
    if abs(blue_win_rate - 0.5) > 0.02:
        print(f"   Class imbalance detected: Blue wins {abs(blue_win_rate-0.5)*100:.1f}% more often")
    else:
        print(f"   Classes are balanced")
    
    print("\n" + "=" * 60)
    print("RECOMMENDATIONS:")
    print("=" * 60)
    
    if abs(pred_start - 0.5) > 0.05:
        print("1. FIX STARTING PREDICTION:")
        print("   - Model predicts {:.1f}% at game start instead of 50%".format(pred_start*100))
        print("   - Consider adding calibration or balanced sampling")
    
    if pred_gold_only < 0.55:
        print("2. GOLD ADVANTAGE TOO WEAK:")
        print("   - 2000 gold advantage only gives {:.1f}%".format(pred_gold_only*100))
        print("   - Feature importance: gold_diff is only 8.76%")
        print("   - tower_diff (37%) and kill_diff (33%) dominate")
        print("   - Consider removing 'tower_diff' from early game or weighting gold more")
    
    print("\n3. ABOUT 'GOLD PER KILL':")
    print("   - gold_diff already includes all gold (kills, CS, objectives)")
    print("   - 'gold per kill' is NOT a direct feature")
    print("   - The model learns kill_diff AND gold_diff separately")
    print("   - If gold_diff correlates with kills, it's redundant")
    print("   - Recommendation: gold_diff is valuable, but not 'gold per kill'")

if __name__ == "__main__":
    test_predictions()
