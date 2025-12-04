import pandas as pd

# Load results
df = pd.read_csv("data/hyperparameter_tuning_results.csv")

# Sort by accuracy
df = df.sort_values('mean_test_score', ascending=False)

print("=" * 80)
print("HYPERPARAMETER TUNING RESULTS SUMMARY")
print("=" * 80)

print("\nTOP 5 CONFIGURATIONS:")
print("-" * 80)
for idx, row in df.head(5).iterrows():
    depth = row['param_max_depth'] if pd.notna(row['param_max_depth']) else 'None'
    print(f"\nRank {idx}:")
    print(f"  n_estimators: {int(row['param_n_estimators'])}")
    print(f"  max_depth: {depth}")
    print(f"  CV Accuracy: {row['mean_test_score']:.4f} (+/- {row['std_test_score']:.4f})")
    print(f"  Train Accuracy: {row['mean_train_score']:.4f}")
    print(f"  Fit Time: {row['mean_fit_time']:.2f}s")

# Best configuration
best = df.iloc[0]
best_depth = best['param_max_depth'] if pd.notna(best['param_max_depth']) else 'None'

print("\n" + "=" * 80)
print("BEST CONFIGURATION")
print("=" * 80)
print(f"n_estimators: {int(best['param_n_estimators'])}")
print(f"max_depth: {best_depth}")
print(f"CV Accuracy: {best['mean_test_score']:.4f}")

# Current configuration
current_n_est = 100
current_depth = 10
current_row = df[(df['param_n_estimators'] == current_n_est) & 
                 (df['param_max_depth'] == current_depth)]

if not current_row.empty:
    current_acc = current_row.iloc[0]['mean_test_score']
    improvement = (best['mean_test_score'] - current_acc) * 100
    
    print("\n" + "=" * 80)
    print("COMPARISON WITH CURRENT MODEL")
    print("=" * 80)
    print(f"Current (n_estimators={current_n_est}, max_depth={current_depth}):")
    print(f"  CV Accuracy: {current_acc:.4f}")
    print(f"\nBest configuration:")
    print(f"  CV Accuracy: {best['mean_test_score']:.4f}")
    print(f"  Improvement: {improvement:.2f}%")

print("\n" + "=" * 80)
print("RECOMMENDATION")
print("=" * 80)
print(f"\nUpdate model.py lines 35-36 to:")
print(f"  n_estimators={int(best['param_n_estimators'])},")
print(f"  max_depth={best_depth},")
