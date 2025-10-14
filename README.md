# DocMiner 6.3.0 - Professional Positionality Analysis Interface

**Simple, professional software for analyzing academic papers and detecting positionality statements.**

Perfect for graduate assistants, researchers, and academic institutions conducting qualitative research analysis.

---

## 🆕 **What's New in v6.3.0** (October 2025)

**User-Adjustable Text Selection Sensitivity:**
- **Sensitivity Slider**: Dial in precise text selection tolerance (20-200%)
- **Column Mode Selector**: Choose Auto, 1-Col, or 2-Col for different page layouts
- **Perfect for Complex PDFs**: Handle single-column, two-column, and mixed layouts
- **Real-Time Adjustment**: Change sensitivity on-the-fly while selecting text
- **Cleaner Interface**: Streamlined toolbar with consistent styling

**Previous Features (v6.1.0):**
- **Status Dots**: Real-time visual indicators showing analysis state for each PDF
- **Position Counter**: "X of Y" display shows your progress through papers
- **Full Session Persistence**: All evidence, decisions, and progress automatically saved
- **Smart Folder Memory**: Remembers your last working folder across sessions

---

## 📥 **DOWNLOAD EXECUTABLES - Just Click and Run!**

**No Python, no setup, no terminal commands - just download and double-click!**

### **v6.3.0 - Latest Release** 🆕

**✅ Ready to download!** macOS • Windows • Linux (coming soon)

Choose your platform and download:

- **🍎 macOS** (Intel & Apple Silicon): [**Download DocMiner-6.3.0-macOS.dmg**](https://github.com/OhioMathTeacher/docminer/releases/download/v6.3.0/DocMiner-6.3.0-macOS.dmg)
- **🪟 Windows** (64-bit): [**Download DocMiner-6.3.0-Windows.zip**](https://github.com/OhioMathTeacher/docminer/releases/download/v6.3.0/DocMiner-6.3.0-Windows.zip)
- **🐧 Linux** (x86_64): [Browse All Releases](https://github.com/OhioMathTeacher/docminer/releases) (AppImage coming soon)

### **Installation Instructions**

**macOS:**
1. Download the DMG file
2. Double-click to open
3. Drag DocMiner to your Applications folder
4. If blocked by security: Open Terminal and run: `xattr -cr /Applications/DocMiner6.3.app`

**Windows:**
1. Download the ZIP file
2. Right-click → "Extract All..."
3. Open the extracted folder
4. Double-click `DocMiner6.3.exe`

**Linux:**
1. Download the AppImage file
2. Make it executable: `chmod +x DocMiner-6.3.0-x86_64.AppImage`
3. Run it: `./DocMiner-6.3.0-x86_64.AppImage`

*See all releases at: [Releases Page](https://github.com/OhioMathTeacher/docminer/releases)*

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

* **PDF Viewer** - Professional navigation with adjustable sensitivity for text selection
* **Smart Text Selection** - User-controlled tolerance slider for precise quote extraction
* **Column Detection** - Handle single-column, two-column, and complex page layouts
* **AI Assistant** - Optional AI pre-screening (requires OpenAI API key)
* **Manual Analysis** - Works immediately without any API keys
* **Training Data** - Export reviewer decisions for analysis
* **GitHub Integration** - Upload results automatically (optional)

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
