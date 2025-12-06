# League Win Predictor

Real-time win probability predictions for League of Legends using machine learning.

## 🎮 Features

- **Live predictions** during your League games
- **Real-time overlay** showing win probability
- **Machine learning** powered by Random Forest model
- **Optimized builds** to minimize antivirus false positives
- **Free and open source**

## 📥 For Users (Download)

See **[DOWNLOAD_INSTRUCTIONS.md](DOWNLOAD_INSTRUCTIONS.md)** for installation guide.

## 🛠️ For Developers (Build from Source)

### Quick Start
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Train model
python main.py

# 3. Run live predictor
python live_predictor.py
```

### Build Executable
```bash
# Build optimized .exe (antivirus-friendly)
python build_exe.py

# Generate distribution info
python post_build.py
```

## 📚 Documentation

- **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** - File usage guide
- **[PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md)** - Detailed architecture
- **[ANTIVIRUS_GUIDE.md](ANTIVIRUS_GUIDE.md)** - Build optimization & distribution tips
- **[DOWNLOAD_INSTRUCTIONS.md](DOWNLOAD_INSTRUCTIONS.md)** - End-user installation guide

## 🔒 Privacy

- Runs entirely on your local machine
- No data collection or external requests
- Uses official League Client API (`127.0.0.1:2999`)
- Open source - verify the code yourself

## ⚖️ Legal

DustyKevin is not endorsed by Riot Games and does not reflect the views or opinions of Riot Games or anyone officially involved in producing or managing Riot Games properties. Riot Games and all associated properties are trademarks or registered trademarks of Riot Games, Inc.
