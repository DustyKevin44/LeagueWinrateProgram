# League Win Rate Predictor - Project Overview

## Project Purpose
A real-time League of Legends win probability predictor using machine learning. The application connects to the League client during live games, extracts game statistics, and predicts the win probability for the Blue team using a Random Forest model.

---

## Core Application Files

### **main.py**
- **Purpose**: Training entry point for the model
- **Usage**: Trains the Random Forest model on historical data and tests predictions
- **Key Functions**:
  - `main()`: Loads data, trains model, saves to disk, and runs sample predictions

### **model.py**
- **Purpose**: Machine learning model implementation
- **Classes**:
  - `ModelBase`: Abstract base class for models
  - `RandomForestWinModel`: Random Forest classifier for win prediction
- **Key Features**:
  - Model training with cross-validation
  - Feature importance analysis
  - Model persistence (save/load)
- **Configuration**: 50 estimators, max depth 10, balanced class weights

### **data_loader.py**
- **Purpose**: Loads and filters historical match data from CSV files
- **Classes**:
  - `DataLoader`: Loads match statistics from data directory
- **Key Features**:
  - Filters for CLASSIC game mode (Summoner's Rift 5v5)
  - Supports rank-based filtering
  - Loads 4 data tables: MatchStatsTbl, TeamMatchTbl, MatchTbl, SummonerMatchTbl

### **feature_engineer.py**
- **Purpose**: Transforms raw match data into ML features
- **Classes**:
  - `FeatureEngineerBase`: Abstract base class
  - `DefaultFeatureEngineer`: Aggregates player stats per team and calculates differences
- **Features Generated** (17 total):
  - **Core Stats**: kill_diff, death_diff, assist_diff, gold_diff, cs_diff, ward_score_diff, level_diff
  - **Objectives**: dragon_diff, baron_diff, tower_diff, herald_diff, inhib_diff
  - **Derived**: kda_diff, gold_per_kill, cs_per_min_diff, objective_score
  - **Context**: game_duration

### **live_client.py**
- **Purpose**: Interface to League of Legends Live Client Data API
- **Classes**:
  - `LiveClientAPI`: Fetches and processes live game data
- **Key Features**:
  - Connects to local League client API (https://127.0.0.1:2999)
  - Extracts real-time game features matching training data
  - Handles team detection and player matching
  - Processes game events (kills, objectives, etc.)
  - Calculates gold from items when direct gold unavailable

### **live_predictor.py**
- **Purpose**: Main application for live game prediction
- **Classes**:
  - `LiveWinRatePredictor`: Coordinates API polling, prediction, and UI updates
- **Key Features**:
  - Background thread polling every 10 seconds
  - Real-time prediction updates
  - Integration with overlay window
- **Usage**: Run this file to start the live predictor

### **interface.py**
- **Purpose**: Prediction interface layer
- **Classes**:
  - `WinProbabilityInterface`: User-facing prediction API
- **Key Features**:
  - Loads trained model from disk
  - Handles feature defaults and missing values
  - PyInstaller compatibility (resource path handling)
  - Returns probability clamped to [0, 1]

### **overlay.py**
- **Purpose**: GUI overlay window for displaying win probability
- **Classes**:
  - `WinRateOverlay`: Tkinter-based transparent overlay
- **Key Features**:
  - Transparent, always-on-top window
  - Tool window mode (visible over fullscreen games)
  - Draggable interface
  - Color-coded win probability (red to green gradient)
  - Displays status messages
- **Default Position**: Top-right corner

### **build_exe.py**
- **Purpose**: Build script for creating standalone executable
- **Key Features**:
  - Optional rank-specific model training
  - PyInstaller configuration
  - Dependency bundling
  - Automatic module exclusion to reduce size
  - Creates single .exe file (~70MB)
- **Usage**: Run to build `LeagueWinPredictor.exe` in dist folder

---

## Analysis & Optimization Files

### **analyze_rank_importance.py**
- **Purpose**: Analyzes feature importance across different ranks
- **Key Functions**:
  - `analyze_ranks()`: Trains models for each rank tier
  - `main()`: Generates feature importance comparison tables
- **Output**: feature_importances_per_rank.csv
- **Ranks Analyzed**: Iron to Challenger + All ranks combined

### **analyze_feature_importance.py**
- **Purpose**: Analyzes feature importance across different ranks
- **Key Functions**:
  - `analyze_ranks()`: Trains models for each rank tier
  - `main()`: Generates feature importance comparison tables
- **Output**: feature_importances_per_rank.csv
- **Ranks Analyzed**: Iron to Challenger + All ranks combined

### **hyperparameter_tuning.py**
- **Purpose**: Grid search for optimal Random Forest hyperparameters
- **Key Features**:
  - 5-fold cross-validation
  - Tests combinations of n_estimators (50-300) and max_depth (5-None)
  - Compares against current model
  - Generates detailed performance reports
- **Output**: hyperparameter_tuning_results.csv

### **hyperparameter_summary.py**
- **Purpose**: Quick summary of hyperparameter tuning results
- **Key Features**:
  - Displays top 5 configurations
  - Compares with current model settings
  - Provides code recommendations for model.py updates

---

## Debug & Testing Files

### **debug_live_api.py**
- **Purpose**: Debug script for live API feature extraction
- **Key Features**:
  - Prints all game events
  - Shows event type counts
  - Validates feature extraction
  - Diagnoses objective tracking issues

### **debug_data.py**
- **Purpose**: Data quality checks and correlation analysis
- **Key Features**:
  - Feature correlation with target
  - Analyzes gold difference relationships
  - Estimates feature slopes using linear regression

### **debug_teams.py**
- **Purpose**: Validates team assignment logic
- **Key Features**:
  - Checks champion-to-team mapping
  - Verifies merge operations
  - Tests sample matches

### **diagnose_full.py**
- **Purpose**: Comprehensive data structure diagnostics
- **Key Features**:
  - Validates data table relationships
  - Checks for merge duplicates
  - Analyzes single match structure

### **check_features.py**
- **Purpose**: Feature statistics for wins vs losses
- **Key Features**:
  - Average feature values by outcome
  - Sample data inspection
  - Quick sanity checks

### **test_extraction.py**
- **Purpose**: Unit test for live API feature extraction
- **Key Features**:
  - Mock game data
  - Validates feature calculation
  - Tests prediction interface

### **test_features.py**
- **Purpose**: Tests model without objective features
- **Key Features**:
  - Trains on reduced feature set
  - Evaluates gold coefficient
  - Tests partial feature predictions

### **test_logreg.py**
- **Purpose**: Compares Random Forest vs Logistic Regression
- **Key Features**:
  - Side-by-side accuracy comparison
  - Prediction behavior analysis

### **test_model.py**
- **Purpose**: Model prediction validation
- **Key Features**:
  - Tests various game scenarios
  - Validates scaler and model details
  **Note**: Contains outdated SCALER_PATH reference (models no longer use scaling)

---

## Unused/Legacy Files

### **team_feature_engineer.py**
- **Status**: Unused alternative implementation
- **Purpose**: Feature engineering using only TeamMatchTbl (no player aggregation)
- **Note**: Not integrated into main pipeline

### **train_team_model.py**
- **Status**: Unused training script
- **Purpose**: Trains model using team_feature_engineer
- **Note**: Main pipeline uses DefaultFeatureEngineer instead

### **model_logistic_OLD.py**
- **Status**: Deprecated
- **Purpose**: Old Logistic Regression implementation
- **Note**: Replaced by Random Forest in model.py

---

## Data Files (in /data directory)

- **MatchStatsTbl.csv**: Player-level match statistics
- **TeamMatchTbl.csv**: Team-level aggregated stats and objectives
- **MatchTbl.csv**: Match metadata (duration, queue type, rank)
- **SummonerMatchTbl.csv**: Links summoners to matches
- **winprob_model.joblib**: Trained Random Forest model
- **hyperparameter_tuning_results.csv**: Tuning experiment results

---

## Configuration Files

### **requirements.txt**
- **Dependencies**:
  - pandas
  - scikit-learn
  - joblib
  - requests
  - urllib3

### **LeagueWinPredictor.spec**
- **Purpose**: PyInstaller specification file
- **Generated**: Automatically by build_exe.py

---

## How to Use This Project

### **Training a Model**
```bash
python main.py
```

### **Running Live Predictor**
```bash
python live_predictor.py
```
- Start a League game
- Overlay appears in top-right corner
- Updates every 10 seconds

### **Building Executable**
```bash
python build_exe.py
```
- Follow prompts for rank-specific build
- Output: `dist/LeagueWinPredictor.exe`

### **Analyzing Performance**
```bash
# Feature importance by rank
python analyze_rank_importance.py

# Hyperparameter optimization
python hyperparameter_tuning.py

# View tuning results
python hyperparameter_summary.py
```

### **Debugging**
```bash
# Test live API extraction
python debug_live_api.py

# Check data quality
python debug_data.py

# Test predictions
python test_extraction.py
```

---

## Architecture Flow

```
Historical Data (CSV files)
    ↓
DataLoader → loads and filters matches
    ↓
FeatureEngineer → transforms to ML features
    ↓
RandomForestWinModel → trains classifier
    ↓
Model saved to disk (winprob_model.joblib)
    ↓
────────────────────────────────────────
    ↓
Live Game API (League Client)
    ↓
LiveClientAPI → extracts game features
    ↓
WinProbabilityInterface → loads model + predicts
    ↓
WinRateOverlay → displays probability
```

---

## Feature Importance (Typical Rankings)

1. **gold_diff** - Most important predictor
2. **tower_diff** - Critical objective advantage
3. **kill_diff** - Combat advantage
4. **objective_score** - Combined objective value
5. **dragon_diff** - Long-term scaling
6. **kda_diff** - Team fight efficiency
7. **baron_diff** - Late game power
8. **cs_per_min_diff** - Farm efficiency
9. **game_duration** - Context for other features

---

## Model Performance

- **Accuracy**: ~90-95% (varies by rank)
- **Model Type**: Random Forest (50 trees, depth 10)
- **Features**: 17 calculated features
- **Training Data**: Filtered for CLASSIC mode only
- **Update Frequency**: 10 seconds during live games

---

## Known Limitations

1. **Early Game**: Predictions less reliable before 5 minutes (tower_diff dominates in training data)
2. **Level Diff**: Not available in historical data (set to 0)
3. **Inhibitors**: Not tracked in TeamMatchTbl (set to 0)
4. **Void Grubs**: Not in dataset (future feature)
5. **First Blood**: Not explicitly tracked

---

## Future Enhancements

- Add Void Grubs tracking when data available
- Improve early-game predictions
- Add champion composition analysis
- Multi-rank ensemble models
- Real-time player performance metrics
