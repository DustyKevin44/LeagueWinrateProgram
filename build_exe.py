"""
Build script to create standalone .exe for League Win Rate Predictor
Uses PyInstaller to package the application with all dependencies
"""

import os
import shutil
import subprocess
import sys

def build_exe():
    """Build the executable using PyInstaller"""
    
    print("=" * 80)
    print("Building League Win Rate Predictor Executable")
    print("=" * 80)
    
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
        shutil.rmtree("build")
        print("[OK] Cleaned build directory")
    if os.path.exists("dist"):
        shutil.rmtree("dist")
        print("[OK] Cleaned dist directory")
    
    # PyInstaller command
    cmd = [
        "pyinstaller",
        "--onefile",  # Single executable file
        "--console",  # Show console window for debugging
        "--name=LeagueWinPredictor",
        "--add-data=data/winprob_model.joblib;data",  # Include the model
        
        # Exclude unused modules to reduce size
        "--exclude-module=matplotlib",
        "--exclude-module=scipy",
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
        print("\nNote: The .exe is ~50-100MB due to bundled Python libraries")
        
    except subprocess.CalledProcessError as e:
        print(f"\n[X] Build failed: {e}")
        print("\nTry checking the build log for errors")
        return False
    
    return True

if __name__ == "__main__":
    build_exe()
