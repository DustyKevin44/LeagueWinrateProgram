from interface import WinProbabilityInterface

interface = WinProbabilityInterface()

print("=== QUICK CALIBRATION TEST ===\n")

# Test 1: Actual game start (84 seconds like your live game)
pred1 = interface.predict(
    kill_diff=0, assist_diff=0, gold_diff=0, cs_diff=0,
    ward_score_diff=0, level_diff=0,
    dragon_diff=0, baron_diff=0, tower_diff=0, herald_diff=0, inhib_diff=0,
    game_duration=84
)
print(f"1. Game start (84s, all zeros): {pred1*100:.2f}%")

# Test 2: Your actual live game scenario
pred2 = interface.predict(
    kill_diff=2, assist_diff=7, gold_diff=-50, cs_diff=0,
    ward_score_diff=0, level_diff=0,
    dragon_diff=0, baron_diff=0, tower_diff=0, herald_diff=0, inhib_diff=0,
    game_duration=84
)
print(f"2. Your live game (2 kills, -50 gold, 84s): {pred2*100:.2f}%")

# Test 3: Pure 2000 gold at 5 minutes
pred3 = interface.predict(
    kill_diff=0, assist_diff=0, gold_diff=2000, cs_diff=0,
    ward_score_diff=0, level_diff=0,
    dragon_diff=0, baron_diff=0, tower_diff=0, herald_diff=0, inhib_diff=0,
    game_duration=300
)
print(f"3. Pure 2000 gold advantage (5min): {pred3*100:.2f}%")

# Test 4: Symmetry test
pred4a = interface.predict(
    kill_diff=0, assist_diff=0, gold_diff=2000, cs_diff=0,
    ward_score_diff=0, level_diff=0,
    dragon_diff=0, baron_diff=0, tower_diff=0, herald_diff=0, inhib_diff=0,
    game_duration=300
)
pred4b = interface.predict(
    kill_diff=0, assist_diff=0, gold_diff=-2000, cs_diff=0,
    ward_score_diff=0, level_diff=0,
    dragon_diff=0, baron_diff=0, tower_diff=0, herald_diff=0, inhib_diff=0,
    game_duration=300
)
print(f"4. Symmetry: +2000 gold = {pred4a*100:.2f}%, -2000 gold = {pred4b*100:.2f}%")
print(f"   Difference from 50%: +{abs(pred4a-0.5)*100:.1f}% and -{abs(pred4b-0.5)*100:.1f}%")

if abs((pred4a - 0.5) + (pred4b - 0.5)) < 0.01:
    print("   OK - SYMMETRIC!")
else:
    print("   Still asymmetric")
