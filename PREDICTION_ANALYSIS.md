# Prediction Symmetry & Feature Analysis Summary

## Issues Identified

### 1. Starting Prediction (FIXED ✓)
- **Before**: Game start predicted 45.79% instead of 50%
- **After**: Game start now predicts 49.99% ✓
- **Cause**: Model trained on data with 51.39% blue win rate
- **Solution**: Implemented piecewise calibration that re-centers baseline to 50%

### 2. Gold Advantage Impact (IMPROVED, but still weak)
- **Before**: 2000 gold advantage → 46.17%
- **After**: 2000 gold advantage → 54.15%
- **Root Cause**: Feature importance from trained model:
  - `tower_diff`: 37.32% (dominates)
  - `kill_diff`: 33.30%
  - `gold_diff`: 8.76% (very weak!)
  
The model was trained on **full-game data** where towers are a strong predictor of victory.
In early game, towers haven't fallen yet, so gold should matter more, but the model doesn't know this.

### 3. Prediction Symmetry (IMPROVED, but not perfect)
- **Test**: +2000 gold vs -2000 gold at 5 minutes
- **After calibration**: 
  - +2000 gold = 54.15% (+4.1% from 50%)
  - -2000 gold = 40.15% (-9.9% from 50%)
- **Status**: Still asymmetric, but much better than before (was 50.9% vs 22.5%)

### 4. Your Live Game Example
**Scenario**: 84 seconds, +2 kills, -50 gold
- **Prediction**: 83.85%
- **Analysis**: This makes sense! 2 kills early is huge, and -50 gold is negligible
- **The model correctly values kills >> gold in early game**

### 5. "Gold Per Kill" Feature
**Conclusion: NOT a valuable feature**

**Reason**: `gold_diff` already includes ALL gold (kills, CS, objectives, passive income).

**Evidence from testing**:
- 3 kills, 0 gold: 81.67%
- 3 kills + 900 gold: 88.47%
- 0 kills, 900 gold: 46.80%

This shows that `kill_diff` and `gold_diff` are **independent** features. The model learns:
- `kill_diff` = combat dominance (worth ~30% feature importance)
- `gold_diff` = economic advantage (worth ~9% feature importance)

Adding "gold per kill" would create **multicollinearity** - it's a ratio of two features already in the model.

## Changes Made

### 1. Cleaned Up Feature Extraction (`live_client.py`)
**Removed unused features**:
- `death_diff` (redundant with kill_diff)
- `kda_diff` (derived stat, not in training)
- `gold_per_kill` (not valuable, see above)
- `cs_per_min_diff` (not in training)
- `objective_score` (not in training)

**Now only extracts features the model was trained on**.

### 2. Added Probability Calibration (`interface.py`)
Implemented piecewise calibration that:
- ✓ Re-centers baseline to 50%
- ✓ Makes gold advantage more impactful
- ✓ Improves (but doesn't perfect) symmetry
- ✓ Makes predictions more human-intuitive

**Calibration approach**:
```python
if raw_prob < 0.458 (baseline):
    # Compress extreme losses (prevent 10% predictions)
    calibrated = (raw / baseline) ** 0.8 * 0.5
else:
    # Boost wins (make advantages matter more)
    calibrated = 0.5 + ((raw - baseline) / (1 - baseline)) ** 0.5 * 0.5
```

## Why Perfect Symmetry is Hard

The model has inherent asymmetry because:
1. It was trained on full-game stats where blue wins 51.39% of the time
2. Tower kills are the strongest predictor (37%), but towers rarely fall before 10 minutes
3. The model doesn't know what "early game" means - it treats minute 2 and minute 30 the same

**To achieve perfect symmetry**, you would need to:
- Train on more balanced data
- Add game-phase-aware features (e.g., `early_game_gold_diff`)
- Use separate models for different game phases
- Apply isotonic regression calibration with more data points

## Recommendations

### Option A: Keep Current Solution (Recommended)
**Pros**:
- ✓ Starting prediction is 50%
- ✓ Gold matters more (2000 gold = 54% instead of 46%)
- ✓ Predictions are more intuitive
- ✓ No retraining needed

**Cons**:
- Still some asymmetry (+4.1% vs -9.9%)
- Gold could matter even more

### Option B: Retrain with Game-Phase Features
Add features like:
- `early_game_gold_diff` = `gold_diff` when `game_duration < 600`
- `mid_game_tower_diff` = `tower_diff` when `600 < game_duration < 1500`
- `late_game_baron_diff` = `baron_diff` when `game_duration > 1500`

This teaches the model that different features matter at different phases.

### Option C: Increase Calibration Aggressiveness
Change the calibration power curves to make gold matter even more:
```python
# In interface.py, line ~83
boosted = normalized ** 0.4  # Currently 0.5, lower = more aggressive
```

This will make small advantages swing predictions more dramatically.

## Final Answer on Your Questions

1. **"Starting at 45% instead of 50%"** → FIXED ✓ Now starts at 49.99%

2. **"2000 gold only gives 48%"** → IMPROVED to 54.15%
   - Still not as high as you might want, but much better
   - Root cause: model was trained on end-game data where towers matter most
   - Gold has low feature importance (8.76%)

3. **"Is gold per kill valuable?"** → NO ✗
   - `gold_diff` already includes all gold
   - Adding "gold per kill" creates redundancy
   - The model correctly learns `kill_diff` and `gold_diff` separately

## Testing Your Changes

Run your live predictor and check:
```bash
python live_predictor.py
```

Expected improvements:
- Game start should be closer to 50%
- Gold advantages should matter more
- Predictions should feel more "realistic" even if statistically less accurate

The trade-off is: **More symmetric/intuitive predictions** vs **Highest statistical accuracy**.
Your preference for "more realistic" is now implemented!
