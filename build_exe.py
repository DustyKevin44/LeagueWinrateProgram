"""
Build script to create standalone .exe for League Win Rate Predictor
Uses PyInstaller to package the application with all dependencies
"""

import os
import shutil
import subprocess
import sys
from data_loader import DataLoader
from feature_engineer import DefaultFeatureEngineer
from model import RandomForestWinModel, MODEL_PATH

RANK_MAP = {
    'iron': 1,
    'bronze': 2,
    'silver': 3,
    'gold': 4,
    'platinum': 5,
    'emerald': 6,
    'diamond': 7,
    'master': 8,
    'grandmaster': 9,
    'challenger': 10
}

def retrain_model(target_rank):
    """Retrain model on specific rank range (+/- 1)"""
    rank_id = RANK_MAP.get(target_rank.lower())
    if not rank_id:
        print(f"Invalid rank: {target_rank}")
        return False
        
    # Calculate range (+/- 1)
    min_rank = max(1, rank_id - 1)
    max_rank = min(10, rank_id + 1)
    rank_ids = list(range(min_rank, max_rank + 1))
    
    print(f"\nRetraining model for {target_rank.capitalize()} (+/- 1 rank)...")
    print(f"Including Rank IDs: {rank_ids}")
    
    try:
        # Load data with filter
        print("Loading filtered data...")
        loader = DataLoader("data")
        match_stats, team_stats, match_tbl, summoner_match = loader.load_match_stats(rank_ids=rank_ids)
        
        if len(match_stats) < 100:
            print("Error: Not enough data for this rank range!")
            return False
            
        # Engineer features
        print("Engineering features...")
        engineer = DefaultFeatureEngineer()
        X, y = engineer.fit_transform(match_stats, team_stats, summoner_match, match_tbl)
        
        # Train model
        print("Training model...")
        model = RandomForestWinModel(MODEL_PATH)
        model.train(X, y)
        model.save()
        print("[OK] Model retrained and saved!")
        return True
        
    except Exception as e:
        print(f"Error during training: {e}")
        return False

def build_exe():
    """Build the executable using PyInstaller"""
    
    print("=" * 80)
    print("Building League Win Rate Predictor Executable")
    print("=" * 80)
    
    # Ask for rank
    print("\nDo you want to build for a specific rank? (Leave empty for ALL ranks)")
    print("Options: Iron, Bronze, Silver, Gold, Platinum, Emerald, Diamond, Master, Grandmaster, Challenger")
    rank_input = input("Enter rank: ").strip()
    
    if rank_input:
        if not retrain_model(rank_input):
            print("Failed to retrain model. Aborting build.")
            return
    else:
        print("Using existing model (trained on all ranks).")
    
    # Check if PyInstaller is installed
    try:
        import PyInstaller
        print("[OK] PyInstaller found")
    except ImportError:
        print("[X] PyInstaller not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("[OK] PyInstaller installed")
    
    # Clean previous builds
    if os.path.exists("build"):
        try:
            shutil.rmtree("build")
            print("[OK] Cleaned build directory")
        except Exception as e:
            print(f"Warning: Could not clean build directory: {e}")
            
    if os.path.exists("dist"):
        try:
            shutil.rmtree("dist")
            print("[OK] Cleaned dist directory")
        except Exception as e:
            print(f"Warning: Could not clean dist directory: {e}")
    
    # PyInstaller command - optimized to reduce antivirus false positives
    cmd = [
        "pyinstaller",
        "--onefile",  # Single executable file
        "--console",  # Show console window for debugging
        "--name=LeagueWinPredictor",
        "--clean",  # Clean PyInstaller cache before building (important!)
        "--noupx",  # Don't use UPX compression (MAJOR antivirus trigger!)
        
        # Add version info to make exe look legitimate
        "--version-file=version_info.txt",  # We'll create this file
        
        # Include the model
        "--add-data=data/winprob_model.joblib;data",
        
        # Exclude unused modules to reduce size
        "--exclude-module=matplotlib",
        # "--exclude-module=scipy",  # Required by sklearn!
        "--exclude-module=IPython",
        "--exclude-module=jupyter",
        "--exclude-module=notebook",
        "--exclude-module=distutils",
        
        "--hidden-import=sklearn.ensemble",
        "--hidden-import=sklearn.tree",
        "--hidden-import=sklearn.utils._weight_vector",
        "--hidden-import=tkinter",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=joblib",
        "live_predictor.py"
    ]
    
    print("\nRunning PyInstaller...")
    print(" ".join(cmd))
    print()
    
    try:
        subprocess.check_call(cmd)
        print("\n" + "=" * 80)
        print("[OK] Build successful!")
        print("=" * 80)
        print(f"\nExecutable location: {os.path.abspath('dist/LeagueWinPredictor.exe')}")
        print("\nTo distribute to your friend:")
        print("1. Send them the .exe file from the 'dist' folder")
        print("2. They just need to double-click it to run")
        print("3. Make sure they have a League game running!")
        
        if rank_input:
            print(f"\nNOTE: This version is optimized for {rank_input.capitalize()} (+/- 1 rank)!")
            
        print("\nNote: The .exe is ~70MB due to bundled Python libraries")
        
    except subprocess.CalledProcessError as e:
        print(f"\n[X] Build failed: {e}")
        print("\nTry checking the build log for errors")
        return False
    
    return True

if __name__ == "__main__":
    build_exe()
