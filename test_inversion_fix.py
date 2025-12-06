from interface import WinProbabilityInterface

interface = WinProbabilityInterface()

print("=== TESTING INVERTED PROBABILITY BUG FIX ===\n")

# Simulate being behind in everything (-10 kills, -3000 gold, etc.)
# This is what you described: losing in everything
pred_losing = interface.predict(
    kill_diff=-10,
    assist_diff=-15,
    gold_diff=-3000,
    cs_diff=-50,
    ward_score_diff=-10,
    level_diff=-5,
    dragon_diff=-2,
    baron_diff=0,
    tower_diff=-3,
    herald_diff=-1,
    inhib_diff=0,
    game_duration=1200  # 20 minutes
)

print(f"1. Behind in EVERYTHING (-10 kills, -3000 gold, -3 towers, etc.)")
print(f"   Win Probability: {pred_losing*100:.2f}%")
print(f"   Expected: < 20% (you're losing badly)")

if pred_losing > 0.30:
    print(f"   [X] BUG STILL EXISTS! Should be low, but got {pred_losing*100:.1f}%")
else:
    print(f"   [OK] CORRECT! You're predicted to lose as expected")

print()

# Test winning scenario
pred_winning = interface.predict(
    kill_diff=10,
    assist_diff=15,
    gold_diff=3000,
    cs_diff=50,
    ward_score_diff=10,
    level_diff=5,
    dragon_diff=2,
    baron_diff=1,
    tower_diff=3,
    herald_diff=1,
    inhib_diff=1,
    game_duration=1200
)

print(f"2. Ahead in EVERYTHING (+10 kills, +3000 gold, +3 towers, +1 baron)")
print(f"   Win Probability: {pred_winning*100:.2f}%")
print(f"   Expected: > 80% (you're dominating)")

if pred_winning < 0.70:
    print(f"   [X] BUG! Should be high, but got {pred_winning*100:.1f}%")
else:
    print(f"   [OK] CORRECT! You're predicted to win as expected")

print()
print("=== SYMMETRY CHECK ===")
print(f"Losing badly: {pred_losing*100:.2f}%")
print(f"Winning big:  {pred_winning*100:.2f}%")
print(f"Should be symmetric around 50%")

difference = abs((pred_losing - 0.5) + (pred_winning - 0.5))
if difference < 0.20:
    print(f"[OK] Reasonably symmetric (difference: {difference:.3f})")
else:
    print(f"[!]  Still some asymmetry (difference: {difference:.3f})")
