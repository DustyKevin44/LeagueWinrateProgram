from interface import WinProbabilityInterface

interface = WinProbabilityInterface()

print("=== TOWER-TAKING CAPABILITY TEST ===\n")

# Your actual game scenario (first update)
print("1. YOUR ACTUAL GAME (28 min):")
print("   Situation: +2 towers BUT -13 kills, -1 baron, -5 levels")
pred_your_game = interface.predict(
    kill_diff=-13,
    assist_diff=-21,
    gold_diff=667,
    cs_diff=100,
    ward_score_diff=22.9,
    level_diff=-5,
    dragon_diff=-2,
    baron_diff=-1,
    tower_diff=2,
    herald_diff=-1,
    inhib_diff=0,
    game_duration=1685
)
print(f"   OLD would say: ~58% (overvalues towers)")
print(f"   NEW prediction: {pred_your_game*100:.2f}%")
print(f"   → Should be LOWER because you can't defend those towers!\n")

# Opposite scenario: Strong but behind in towers
print("2. OPPOSITE SCENARIO:")
print("   Situation: -2 towers BUT +10 kills, +1 baron, +3000 gold")
pred_opposite = interface.predict(
    kill_diff=10,
    assist_diff=15,
    gold_diff=3000,
    cs_diff=80,
    ward_score_diff=10,
    level_diff=5,
    dragon_diff=0,
    baron_diff=1,
    tower_diff=-2,
    herald_diff=0,
    inhib_diff=0,
    game_duration=1500
)
print(f"   Prediction: {pred_opposite*100:.2f}%")
print(f"   → Should be HIGH because you can take towers back!\n")

# Matched scenario: Towers AND power
print("3. TOWERS + POWER (aligned):")
print("   Situation: +2 towers AND +8 kills, +2000 gold")
pred_aligned = interface.predict(
    kill_diff=8,
    assist_diff=12,
    gold_diff=2000,
    cs_diff=60,
    ward_score_diff=15,
    level_diff=3,
    dragon_diff=1,
    baron_diff=0,
    tower_diff=2,
    herald_diff=0,
    inhib_diff=0,
    game_duration=1400
)
print(f"   Prediction: {pred_aligned*100:.2f}%")
print(f"   → Should be VERY HIGH (have towers AND can defend/push)\n")

print("=== SUMMARY ===")
print("Tower-taking capability adjustment:")
print(f"  Towers without power: {pred_your_game*100:.2f}% (penalized)")
print(f"  Power without towers: {pred_opposite*100:.2f}% (boosted)")
print(f"  Towers WITH power:    {pred_aligned*100:.2f}% (no penalty)")
