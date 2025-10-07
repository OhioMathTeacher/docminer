# Research Buddy 3.1 - Professional Positionality Analysis Interface

**Simple, professional software for analyzing academic papers and detecting positionality statements.**

Perfect for graduate assistants, researchers, and academic institutions conducting qualitative research analysis.

---

## 📥 **DOWNLOAD EXECUTABLES - Just Click and Run!**

**No Python, no setup, no terminal commands - just download and double-click!**

### **macOS**
🍎 [**ResearchBuddy-5.1.1.app.zip**](https://github.com/OhioMathTeacher/research-buddy/releases/download/v5.1.1/ResearchBuddy-5.1.1-macos.zip) 
- Download → Extract → Double-click `ResearchBuddy.app`
- If Mac says "unidentified developer": Right-click app → Open → Open

### **Windows**  
🪟 [**ResearchBuddy-5.1.1.exe**](https://github.com/OhioMathTeacher/research-buddy/releases/download/v5.1.1/ResearchBuddy-5.1.1-windows.zip)
- Download → Extract → Double-click `ResearchBuddy.exe`
- If Windows Defender blocks: Click "More info" → "Run anyway"

### **Linux**
🐧 [**ResearchBuddy-5.1.1.AppImage**](https://github.com/OhioMathTeacher/research-buddy/releases/download/v5.1.1/ResearchBuddy-5.1.1-linux.tar.gz)
- Download → Extract → Run `./ResearchBuddy`
- Or: `chmod +x ResearchBuddy && ./ResearchBuddy`

---

## 🚀 **Alternative: GitHub Codespaces (Zero Installation!)**

**Works on ANY computer with a web browser - perfect if downloads don't work:**

1. Go to https://github.com/OhioMathTeacher/research-buddy
2. Click green **"Code"** button → **"Codespaces"** tab → **"Create codespace"**
3. When VS Code opens in browser, run: `python run_research_buddy.py`
4. **That's it! No installation needed!**

---

## �️ **For Developers: Clone and Run**

If you want to modify the code or have Python installed:

```bash
git clone https://github.com/OhioMathTeacher/research-buddy.git
cd research-buddy
python3 run_research_buddy.py
```

*On Windows, use `python` instead of `python3`*

**⚠️ Note:** We're working on Windows executable and improved cross-platform naming. Check [releases page](https://github.com/OhioMathTeacher/research-buddy/releases) for updates.

---

## Quick Start

### Step 1: Download the Latest Release

**Production Ready (Recommended):**  
Use the direct download links above, or visit [Research Buddy Releases](https://github.com/OhioMathTeacher/research-buddy/releases/latest) for more options.

**For Developers:**
```bash
git clone https://github.com/OhioMathTeacher/research-buddy.git
cd research-buddy
python run_research_buddy.py
```

### Step 2: Start Using

1. **Extract** the downloaded zip file
2. **Double-click** the executable to launch
3. **Select** your PDF folder to analyze
4. **Start analyzing!** (Works immediately for manual analysis)

### Step 3: Optional Setup (for AI features)

1. Go to **Configuration → Settings**
2. Enter your **OpenAI API key** (for AI analysis)
3. Enter your **GitHub token** (for uploading results)
4. Click **Save Configuration**

---

## What It Does

* **PDF Viewer** – Professional navigation for academic papers
* **Text Selection** – Highlight and extract quotes for evidence
* **AI Assistant** – Optional AI pre-screening (requires OpenAI API key)
* **Training Data** – Export reviewer decisions for analysis
* **Smart Buttons** – Color-coded status indicators for easy setup
* **Secure Configuration** – Password-protected API key entry

---

## Project Structure

```
research-buddy/
├── run_research_buddy.py          # Main entry point for developers
├── enhanced_training_interface.py # Core application
├── configuration_dialog.py        # Settings interface  
├── github_report_uploader.py      # Upload functionality
├── launch_research_buddy.py       # Legacy launcher
├── requirements.txt               # Python dependencies
├── docs/                          # Documentation
│   ├── QUICK_START_FOR_GAS.md    # Quick start guide
│   ├── RELEASE_v5.0.md           # Latest release notes
│   └── about_EVIDENCE.txt        # Evidence export info
├── legal/                         # License files
│   ├── LICENSE                   # Main MIT license
│   ├── LICENSE-ACADEMIC          # Academic use terms
│   └── LICENSE-NONCOMMERCIAL     # Non-commercial terms
├── build_files/                   # Build and packaging
│   ├── build.py                  # Build script
│   └── *.spec                    # PyInstaller configs
├── tests/                         # Test files
├── utils/                         # Utility modules
├── scripts/                       # Helper scripts
├── cli/                          # Command-line tools
└── sample_pdfs/                  # Example documents
```

---

## Need Help?

* **Getting Started**: See `docs/QUICK_START_FOR_GAS.md`
* **Questions**: Open an [issue](https://github.com/OhioMathTeacher/research-buddy/issues)
* **Technical Support**: Contact your research supervisor or IT team

---

## For Developers

### Running from Source

1. **Clone the repository:**
   ```bash
   git clone https://github.com/OhioMathTeacher/research-buddy.git
   cd research-buddy
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   python run_research_buddy.py
   ```

### Building Executables

```bash
python build_files/build.py
```

Built executables will be in the `dist/` directory.

### Running Tests

```bash
python -m pytest tests/
```

---

## License

**Academic and Educational Use Only**
This project is licensed under **Creative Commons Attribution-NonCommercial 4.0**:

* Free for academic research and education
* Share and modify for research purposes
* Commercial use requires separate licensing

See `legal/` directory for full license terms.

---

**Research Buddy** – Making contextual analysis accessible to everyone in academia.