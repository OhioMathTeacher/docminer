# DocMiner 6.1.0 - Professional Positionality Analysis Interface

**Simple, professional software for analyzing academic papers and detecting positionality statements.**

Perfect for graduate assistants, researchers, and academic institutions conducting qualitative research analysis.

---

## 🆕 **What's New in v6.1.0** (October 2025)

**Enhanced Training Interface with Visual Progress Tracking:**
- 🟢 🟡 🔴 **Status Dots**: Real-time visual indicators showing analysis state for each PDF
- 📊 **Position Counter**: "X of Y" display shows your progress through papers
- 💾 **Full Session Persistence**: All evidence, decisions, and progress automatically saved
- 📁 **Smart Folder Memory**: Remembers your last working folder across sessions
- 🎯 **Never Lose Work**: Pick up exactly where you left off

---

## 📥 **DOWNLOAD EXECUTABLES - Just Click and Run!**

**No Python, no setup, no terminal commands - just download and double-click!**

### **Coming Soon: v6.1.0 Builds**
*Executables are currently building via GitHub Actions and will be available shortly at:*
- 🍎 **macOS**: [Releases Page](https://github.com/OhioMathTeacher/docminer/releases/latest)
- 🪟 **Windows**: [Releases Page](https://github.com/OhioMathTeacher/docminer/releases/latest)
- 🐧 **Linux**: [Releases Page](https://github.com/OhioMathTeacher/docminer/releases/latest)

*Check the [Releases](https://github.com/OhioMathTeacher/docminer/releases) page for the latest builds!*

*For immediate access to v6.1.0 features, run from source (instructions below).*

---

## 🎥 **Video Tutorial - Quick Start Guide**

---

## �📥 **DOWNLOAD EXECUTABLES - Just Click and Run!**

**No Python, no setup, no terminal commands - just download and double-click!**

*Current builds are v5.2.1 - for latest v6.1.0 features, run from source (instructions below)*

### **macOS** ⭐ **v5.2.1 - AI Fixed + 93% Smaller!**
🍎 [**Download DocMiner-5.2.1-macos.dmg**](https://github.com/OhioMathTeacher/docminer/releases/download/v5.2.1/DocMiner-5.2.1-macos.dmg) **(81 MB)**
- **CRITICAL FIX**: AI positionality analysis now works! 
- **93% smaller**: 81 MB (was 1.1 GB)
- Download → Double-click the DMG → Drag `DocMiner5.2.1.app` to Applications
- **Includes sample PDF with JSTOR article links for testing**
- **Works on both Intel and Apple Silicon Macs** (Intel via Rosetta 2)

**First-time setup (security bypass):**
1. Try to open the app (it will show security warning)
2. Open Terminal and run: `xattr -cr /Applications/DocMiner5.2.1.app`
3. Now double-click the app - it will open!

**Alternative (no Terminal):**
- Right-click the .app → Open → Open (may need to do this twice)

**Note:** First launch stores your API keys and GitHub settings securely in `~/.research_buddy/` - you only configure once!

### **Windows**  
🪟 [**Download DocMiner-windows.zip**](https://github.com/OhioMathTeacher/docminer/releases/download/v5.2/DocMiner-windows.zip)
- Download → Extract → Double-click `DocMiner5.2.exe`
- If Windows Defender blocks: Click "More info" → "Run anyway"
- **Note:** v5.2.1 with AI fix coming soon via GitHub Actions

### **Linux**
🐧 [**Download DocMiner-5.2-x86_64.AppImage**](https://github.com/OhioMathTeacher/docminer/releases/download/v5.2/DocMiner-5.2-x86_64.AppImage) **(Recommended)**

**Easiest way - just 2 steps:**
1. Download the AppImage file
2. Make it executable and run:
   ```bash
   chmod +x DocMiner-5.2-x86_64.AppImage
   ./DocMiner-5.2-x86_64.AppImage
   ```

**Alternative:** [Download DocMiner-linux.tar.gz](https://github.com/OhioMathTeacher/docminer/releases/download/v5.2/DocMiner-linux.tar.gz)
- Extract: `tar -xzf DocMiner-linux.tar.gz`
- Run: `cd release && ./DocMiner`

**That's it!** The app will launch. AppImage is portable - just move the file anywhere and double-click to run.

- **Universal Linux executable - works on all distros** (Ubuntu, Fedora, Arch, Debian, Linux Mint, etc.)
- **Note:** v5.2.1 with AI fix coming soon via GitHub Actions

---

## 🎥 **Video Tutorial - Quick Start Guide**

**New to DocMiner? Watch this 8-minute walkthrough:**

[**📺 Watch Video Tutorial**](https://youtu.be/Y3nX3kSQsXU)

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
git clone https://github.com/OhioMathTeacher/docminer.git
cd docminer
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
docminer/
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

**DocMiner** – Making positionality analysis accessible to everyone in academia.
