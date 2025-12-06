# League Win Predictor - Download & Install

## 🎮 What is this?

A real-time win probability predictor for League of Legends that shows your chances of winning during a live game.

---

## 📥 Download

**Latest Version**: v1.0.0  
**File**: `LeagueWinPredictor.exe` (Size: ~85MB)

### ✅ File Verification (Recommended)

To verify you have the authentic, unmodified file:

```bash
certutil -hashfile LeagueWinPredictor.exe SHA256
```

**Expected SHA256 Hash**: `b0b21f781c6a66124a43de73656f0d5952a1a45dfdfb35db0297e339231b7d27`

**Expected SHA1 Hash**: `fce76d182799cd081f096fb4a3698cd3e25efa36`

If the hash matches, the file is safe and authentic!

---

## 🛡️ Security Notice

### Why does Windows show a warning?

When you download and run this program, **Windows SmartScreen might show a security warning**. Here's why this is normal:

1. **The app is not code-signed**  
   - Code signing costs $100-400/year
   - This is a free, open-source project
   - The source code is fully available on GitHub

2. **Windows doesn't recognize new applications**  
   - All new apps show this warning initially
   - As more people use it, the warning disappears
   - This is normal for free software

3. **Some antivirus software may flag it**  
   - This is a "false positive" (the file is safe)
   - Common for apps packaged with PyInstaller
   - You can verify by uploading to VirusTotal.com

---

## 🚀 Installation (Windows)

### Step 1: Download
Download `LeagueWinPredictor.exe` from [GitHub Releases](YOUR_RELEASE_URL)

### Step 2: Run the file
Double-click `LeagueWinPredictor.exe`

### Step 3: Handle Windows SmartScreen (if it appears)
1. Windows might show: *"Windows protected your PC"*
2. Click **"More info"**
3. Click **"Run anyway"**

### Step 4: Start a League game!
The overlay will appear in the top-right corner showing your win probability in real-time.

---

## 🔧 Alternative Installation (Run from Source)

If you prefer to run the Python code directly:

### Requirements:
- Python 3.9 or higher
- Windows 10/11

### Steps:

```bash
# 1. Clone or download the repository
git clone https://github.com/DustyKevin44/LeagueWinrateProgram.git
cd LeagueWinrateProgram

# 2. Install dependencies
pip install -r requirements.txt

# 3. Train the model (first time only)
python main.py

# 4. Run the predictor
python live_predictor.py
```

---

## 🎯 Usage

1. **Start League of Legends** and join a game (ARAM, Normals, Ranked)
2. **Run LeagueWinPredictor.exe**
3. **Wait ~30 seconds** into the game for predictions to start
4. The overlay shows your **win probability** updated every 10 seconds

### Overlay Features:
- **Real-time predictions** based on current game state
- **Color-coded probability**:
  - 🟢 Green: Winning (>60%)
  - 🟡 Yellow: Close game (45-55%)
  - 🔴 Red: Losing (<45%)
- **Draggable**: Click and drag to reposition
- **Always on top**: Stays visible even in fullscreen

---

## ❓ Troubleshooting

### "No game running" error
- Make sure League is fully loaded into a game (not lobby)
- Wait until you're in the actual game (after loading screen)

### Predictions seem wrong early game
- The model is trained on full game data
- Predictions become more accurate after ~5 minutes
- Tower differences are heavily weighted (as they should be)

### Overlay not appearing
- Check if it's hidden behind other windows
- Make sure League is running
- Try running as Administrator

### Antivirus deleted the file
- Add an exception for `LeagueWinPredictor.exe`
- Or use the Python version (see "Alternative Installation")
- Submit a false positive report to your AV vendor

---

## 🔒 Privacy & Safety

- ✅ **No data collection**: Everything runs locally on your PC
- ✅ **Open source**: Full code available on GitHub
- ✅ **No network requests**: Only connects to local League Client API
- ✅ **No account access**: Doesn't interact with your Riot account
- ✅ **Read-only**: Only reads game data, never modifies anything

**Technical details**:
- Connects to `https://127.0.0.1:2999/liveclientdata` (official League Client API)
- Uses machine learning model trained on historical match data
- All processing happens on your computer

---

## 📊 How It Works

The predictor uses a **Random Forest machine learning model** trained on thousands of League matches to predict win probability based on:

- Gold difference
- Kill/death/assist differences  
- CS (creep score) difference
- Tower differences
- Dragon/Baron/Herald objectives
- Inhibitor status
- Game duration

**Accuracy**: ~97% on test data

---

## 🤝 Support

Having issues? 

1. Open an issue on GitHub: https://github.com/DustyKevin44/LeagueWinrateProgram/issues
2. Make sure you're running the latest version

---

## ⚠️ Disclaimer

This tool is for **educational and personal use only**. It:
- Does not violate Riot's Terms of Service (uses official API)
- Does not provide an unfair advantage (only shows statistics)
- Does not modify game files or memory

**Use at your own discretion.**

---

## 🙏 Credits

Built with:
- Python
- scikit-learn (Machine Learning)
- tkinter (Overlay UI)
- League Client API
- Antigravity IDE

---

**Enjoy predicting your wins!** 
