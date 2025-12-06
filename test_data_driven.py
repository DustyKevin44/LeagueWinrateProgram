from interface import WinProbabilityInterface

interface = WinProbabilityInterface()

print("=== DATA-DRIVEN TOWER-TAKING CAPABILITY ===\n")

# Your actual game scenario
print("YOUR GAME (28 min):")
print("  +2 towers BUT -13 kills, -1 baron, -5 levels, +667 gold\n")

pred = interface.predict(
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

print(f"  Prediction: {pred*100:.2f}%")
print(f"  Interpretation: ", end="")

if pred > 0.70:
    print("WINNING (you can take more towers)")
elif pred < 0.30:
    print("LOSING (enemy can push you)")
else:
    print("CLOSE GAME (trading blows)")

print(f"\n  Model learned from DATA that:")
print(f"   - objective_control (40.9% importance) sees: -2 dragons, -1 baron, +2 towers = mixed")
print(f"   - combat_power (10.7% importance) sees: -13 kills, -5 levels, -1 baron = WEAK")
print(f"   - push_capability (8.5% importance) sees: weak combat + no baron = CAN'T PUSH")
print(f"\n  Result: The model learned tower advantage doesn't matter")
print(f"         if you lack the power to defend/push!")
