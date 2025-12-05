# League Win Rate Predictor - Quick Reference

## 📋 File Usage Summary

### 🎯 Main Applications (What to Run)

| File                | Usage           | Description                              |
| ------------------- | --------------- | ---------------------------------------- |
| `main.py`           | Training        | Train the model on historical match data |
| `live_predictor.py` | Live Prediction | Run the overlay during League games      |
| `build_exe.py`      | Build           | Create standalone .exe for distribution  |

**Quick Start:**
```bash
# 1. Train model
python main.py

# 2. Run live predictor (during a League game)
python live_predictor.py

# 3. Build executable
python build_exe.py
```

---

## 🔧 Core Modules (Library Files)

| File                  | Purpose              | Key Classes/Functions                    |
| --------------------- | -------------------- | ---------------------------------------- |
| `model.py`            | ML Model             | `RandomForestWinModel`                   |
| `data_loader.py`      | Data Loading         | `DataLoader.load_match_stats()`          |
| `feature_engineer.py` | Feature Engineering  | `DefaultFeatureEngineer.fit_transform()` |
| `live_client.py`      | League API Client    | `LiveClientAPI.extract_features()`       |
| `interface.py`        | Prediction Interface | `WinProbabilityInterface.predict()`      |
| `overlay.py`          | GUI Overlay          | `WinRateOverlay`                         |

**Note**: These are imported by the main applications. Don't run directly.

---

## 📊 Analysis Tools (Optional)

| File                            | Purpose                    | When to Use                            |
| ------------------------------- | -------------------------- | -------------------------------------- |
| `analyze_rank_importance.py`    | Feature importance by rank | To understand rank-specific patterns   |
| `analyze_feature_importance.py` | Feature importance         | To understand feature importance       |
| `hyperparameter_tuning.py`      | Optimize model params      | To improve model accuracy              |
| `hyperparameter_summary.py`     | View tuning results        | After running hyperparameter_tuning.py |

**Usage:**
```bash
# Analyze feature importance across all ranks
python analyze_rank_importance.py

# Analyze feature importance
python analyze_feature_importance.py

# Find best hyperparameters (takes ~10 minutes)
python hyperparameter_tuning.py

# View results
python hyperparameter_summary.py
```

---

## 🐛 Debug/Test Files (Development)

### Debug Scripts
| File                | Purpose                   |
| ------------------- | ------------------------- |
| `debug_live_api.py` | Test live API extraction  |
| `debug_data.py`     | Check data quality        |
| `debug_teams.py`    | Validate team assignments |
| `diagnose_full.py`  | Full data structure check |
| `check_features.py` | Feature statistics        |

### Test Scripts
| File                 | Purpose                                |
| -------------------- | -------------------------------------- |
| `test_extraction.py` | Test feature extraction with mock data |
| `test_features.py`   | Test model without objectives          |
| `test_logreg.py`     | Compare RF vs Logistic Regression      |
| `test_model.py`      | Validate model predictions             |

**Usage:**
```bash
# Test live API (requires active game)
python debug_live_api.py

# Test predictions
python test_model.py
```

---

## ⚠️ Legacy Files (Not Used)

| File                       | Status           | Replacement                    |
| -------------------------- | ---------------- | ------------------------------ |
| `model_logistic_OLD.py`    | Deprecated       | Use `model.py` (Random Forest) |
| `team_feature_engineer.py` | Alternative impl | Use `feature_engineer.py`      |
| `train_team_model.py`      | Not integrated   | Use `main.py`                  |

**Recommendation**: Move to `_legacy/` folder or delete.

---

## 📂 Data Files

| Location                    | Contents                      |
| --------------------------- | ----------------------------- |
| `data/MatchStatsTbl.csv`    | Player-level match statistics |
| `data/TeamMatchTbl.csv`     | Team-level aggregated stats   |
| `data/MatchTbl.csv`         | Match metadata                |
| `data/SummonerMatchTbl.csv` | Summoner-match linking table  |
| `data/winprob_model.joblib` | Trained model (generated)     |

---

## 🎮 Typical Workflows

### Workflow 1: First Time Setup
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Train the model
python main.py

# 3. Test it works
python test_model.py
```

### Workflow 2: Using Live Predictor
```bash
# 1. Ensure model is trained
python main.py

# 2. Start a League game

# 3. Run the live predictor
python live_predictor.py
```

### Workflow 3: Building for Distribution
```bash
# 1. Train model (optionally for specific rank)
python main.py

# 2. Build executable
python build_exe.py

# 3. Distribute dist/LeagueWinPredictor.exe
```

### Workflow 4: Improving Model Accuracy
```bash
# 1. Analyze current feature importance
python analyze_rank_importance.py

# 2. Analyze feature importance
python analyze_feature_importance.py

# 3. Find optimal hyperparameters
python hyperparameter_tuning.py

# 4. Update model.py with recommended params

# 5. Retrain
python main.py
```

### Workflow 5: Debugging Issues
```bash
# If predictions seem wrong:
python debug_data.py          # Check data quality
python check_features.py      # Check feature distributions

# If live API not working:
python debug_live_api.py      # Test API extraction

# If objectives not tracking:
python debug_live_api.py      # Check event parsing
```

---

## 📝 Key Features Overview

### Model Features (17 total)
1. **Core Stats** (7): kill_diff, death_diff, assist_diff, gold_diff, cs_diff, ward_score_diff, level_diff
2. **Objectives** (5): dragon_diff, baron_diff, tower_diff, herald_diff, inhib_diff
3. **Derived** (4): kda_diff, gold_per_kill, cs_per_min_diff, objective_score
4. **Context** (1): game_duration

All features are **differences** (Blue team - Red team).

---

## 🔑 Important Paths

```python
# Model Location
MODEL_PATH = "data/winprob_model.joblib"

# League Client API
LIVE_CLIENT_URL = "https://127.0.0.1:2999/liveclientdata"

# Data Directory
DATA_DIR = "data/"

# Build Output
EXE_OUTPUT = "dist/LeagueWinPredictor.exe"
```

---

## 💡 Common Issues & Solutions

### Issue: "Model not found"
**Solution**: Run `python main.py` to train the model first.

### Issue: "No game running"
**Solution**: Start a League of Legends game before running `live_predictor.py`.

### Issue: "Test file crashes"
**Solution**: Files have been fixed in this cleanup. Pull latest changes.

### Issue: "Predictions unreliable early game"
**Explanation**: Model trained on end-game data. Predictions improve after 5 minutes.

### Issue: "Executable too large (~70MB)"
**Explanation**: Normal. Includes Python + scikit-learn + pandas. Optimization possible but complex.

---

## 📚 Documentation Files

| File                  | Content                     |
| --------------------- | --------------------------- |
| `README.md`           | Basic project info          |
| `PROJECT_OVERVIEW.md` | Detailed file-by-file guide |
| `CLEANUP_SUMMARY.md`  | Cleanup changes log         |
| `QUICK_REFERENCE.md`  | This file!                  |

---

## 🎯 Remember

1. **Always train before predicting**: Run `main.py` before `live_predictor.py`
2. **Test scripts are safe**: They won't modify your model or data
3. **Debug scripts require active game**: Only for `debug_live_api.py`
4. **Legacy files can be deleted**: They're not used anywhere
5. **Hyperparameter tuning is slow**: Takes ~10 minutes but improves accuracy

---

## 🚀 Next Steps After Cleanup

1. ✅ Review `PROJECT_OVERVIEW.md` for detailed explanations
2. ✅ Run `python main.py` to ensure model training works
3. ✅ Run `python test_model.py` to verify predictions work
4. ✅ Optionally reorganize files into folders (see `CLEANUP_SUMMARY.md`)
5. ✅ Delete or archive legacy files
6. ✅ Start using `live_predictor.py` during games!

---

*Last Updated: 2025-12-05*
*After comprehensive cleanup and documentation*
