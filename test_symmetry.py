import pandas as pd
from interface import WinProbabilityInterface

interface = WinProbabilityInterface()

print("Testing Symmetry:")
print("=" * 70)

# Test case 1: +1000 gold advantage (from main.py)
pred_plus = interface.predict(
    kill_diff=2, assist_diff=3, gold_diff=1000, cs_diff=15,
    ward_score_diff=5, level_diff=0, dragon_diff=0, baron_diff=0,
    tower_diff=1, herald_diff=0, inhib_diff=0, game_duration=1200
)
print(f"\nBlue team with advantage:")
print(f"  +2 kills, +3 assists, +1000 gold, +15 CS, +1 tower")
print(f"  Blue win probability: {pred_plus*100:.2f}%")
print(f"  Red win probability: {(1-pred_plus)*100:.2f}%")

# Test case 2: -1000 gold disadvantage (exact opposite)
pred_minus = interface.predict(
    kill_diff=-2, assist_diff=-3, gold_diff=-1000, cs_diff=-15,
    ward_score_diff=-5, level_diff=0, dragon_diff=0, baron_diff=0,
    tower_diff=-1, herald_diff=0, inhib_diff=0, game_duration=1200
)
print(f"\nBlue team with disadvantage:")
print(f"  -2 kills, -3 assists, -1000 gold, -15 CS, -1 tower")
print(f"  Blue win probability: {pred_minus*100:.2f}%")
print(f"  Red win probability: {(1-pred_minus)*100:.2f}%")

print("\n" + "=" * 70)
print("Symmetry Analysis:")
print(f"  Blue advantage → Blue wins: {pred_plus*100:.2f}%")
print(f"  Blue disadvantage → Red wins: {(1-pred_minus)*100:.2f}%")
print(f"  Difference: {abs(pred_plus - (1-pred_minus))*100:.2f}%")

if abs(pred_plus - (1-pred_minus)) < 0.05:
    print("  ✓ Model is SYMMETRIC (difference < 5%)")
else:
    print("  ✗ Model is ASYMMETRIC (difference >= 5%)")
    print(f"    This means Blue and Red teams have different win patterns")
