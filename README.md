# Research Buddy 5.2 - Professional Positionality Analysis Interface

**Simple, professional software for analyzing academic papers and detecting positionality statements.**

Perfect for graduate assistants, researchers, and academic institutions conducting qualitative research analysis.

---

## 📥 **DOWNLOAD EXECUTABLES - Just Click and Run!**

**No Python, no setup, no terminal commands - just download and double-click!**

### **macOS**
🍎 [**Download ResearchBuddy-macos.dmg**](https://github.com/OhioMathTeacher/research-buddy/releases/download/v5.2/ResearchBuddy-macos.dmg) 
- Download → Double-click the DMG → Drag `ResearchBuddy5.2.app` to Applications
- **Works on both Intel and Apple Silicon Macs**

**First-time setup (security bypass):**
1. Try to open the app (it will show security warning)
2. Open Terminal and run: `xattr -cr /Applications/ResearchBuddy5.2.app`
3. Now double-click the app - it will open!

**Alternative (no Terminal):**
- Right-click the .app → Open → Open (may need to do this twice)

### **Windows**  
🪟 [**Download ResearchBuddy-windows.zip**](https://github.com/OhioMathTeacher/research-buddy/releases/download/v5.2/ResearchBuddy-windows.zip)
- Download → Extract → Double-click `ResearchBuddy5.2.exe`
- If Windows Defender blocks: Click "More info" → "Run anyway"

### **Linux**
🐧 [**Download ResearchBuddy-5.2-x86_64.AppImage**](https://github.com/OhioMathTeacher/research-buddy/releases/download/v5.2/ResearchBuddy-5.2-x86_64.AppImage) **(Recommended)**

**Easiest way - just 2 steps:**
1. Download the AppImage file
2. Make it executable and run:
   ```bash
   chmod +x ResearchBuddy-5.2-x86_64.AppImage
   ./ResearchBuddy-5.2-x86_64.AppImage
   ```

**Alternative:** [Download ResearchBuddy-linux.tar.gz](https://github.com/OhioMathTeacher/research-buddy/releases/download/v5.2/ResearchBuddy-linux.tar.gz)
- Extract: `tar -xzf ResearchBuddy-linux.tar.gz`
- Run: `cd release && ./ResearchBuddy`

**That's it!** The app will launch. AppImage is portable - just move the file anywhere and double-click to run.

- **Universal Linux executable - works on all distros** (Ubuntu, Fedora, Arch, Debian, Linux Mint, etc.)

---

## 🎥 **Video Tutorial - Quick Start Guide**

**New to Research Buddy? Watch this 8-minute walkthrough:**

[**📺 Watch Video Tutorial**](docs/video_tutorial/ResearchBuddyVideoTutorial.mp4)

Learn how to:
- ✅ Configure your first project
- ✅ Load and analyze PDF documents  
- ✅ Mark evidence and make judgments
- ✅ Export your research findings

*Video shows the complete workflow from setup to exporting results.*

---

## ✨ **What It Does**

* **PDF Viewer** – Professional navigation for academic papers
* **Text Selection** – Highlight and extract quotes for evidence
* **AI Assistant** – Optional AI pre-screening (requires OpenAI API key)
* **Manual Analysis** – Works immediately without any API keys
* **Training Data** – Export reviewer decisions for analysis
* **GitHub Integration** – Upload results automatically (optional)

---

## 🛠️ **For Developers**

### Running from Source
```bash
git clone https://github.com/OhioMathTeacher/research-buddy.git
cd research-buddy
pip install -r requirements.txt
python3 run_research_buddy.py  # On Windows, use 'python'
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

## 📁 **Project Structure**

```
research-buddy/
├── run_research_buddy.py          # Main entry point
├── enhanced_training_interface.py # Core application
├── configuration_dialog.py        # Settings interface  
├── github_report_uploader.py      # Upload functionality
├── requirements.txt               # Python dependencies
├── docs/                          # Documentation
├── legal/                         # License files
├── build_files/                   # Build and packaging
├── tests/                         # Test files
├── utils/                         # Utility modules
└── sample_pdfs/                   # Example documents
```
---

## 📜 **License**

**Academic and Educational Use Only**

This project is licensed under **Creative Commons Attribution-NonCommercial 4.0**:

* ✅ Free for academic research and education
* ✅ Share and modify for research purposes
* ❌ Commercial use requires separate licensing

See `legal/` directory for full license terms.

---

**Research Buddy** – Making positionality analysis accessible to everyone in academia.
