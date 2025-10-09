# Research Buddy 5.1.1 - Professional Positionality Analysis Interface

**Simple, professional software for analyzing academic papers and detecting positionality statements.**

Perfect for graduate assistants, researchers, and academic institutions conducting qualitative research analysis.

---

## 📥 **DOWNLOAD EXECUTABLES - Just Click and Run!**

**No Python, no setup, no terminal commands - just download and double-click!**

### **macOS**
🍎 [**Download ResearchBuddy-5.1.1-macos-intel.dmg**](https://github.com/OhioMathTeacher/research-buddy/releases/download/v5.1.1/ResearchBuddy-5.1.1-macos-intel.dmg) 
- Download → Double-click the DMG → Drag `ResearchBuddy5.1.1.app` to Applications
- Open from Applications folder → Done!
- **Works on both Intel and Apple Silicon Macs**
- If Mac says "unidentified developer": Right-click the .app → Open → Open (only needed first time)

### **Windows**  
🪟 [**Download ResearchBuddy-5.1.1-windows.zip**](https://github.com/OhioMathTeacher/research-buddy/releases/download/v5.1.1/ResearchBuddy-5.1.1-windows.zip)
- Download → Extract → Double-click `ResearchBuddy5.1.1.exe`
- If Windows Defender blocks: Click "More info" → "Run anyway"

### **Linux**
🐧 [**Download ResearchBuddy-5.1.1-x86_64.AppImage**](https://github.com/OhioMathTeacher/research-buddy/releases/download/v5.1.1/ResearchBuddy-5.1.1-x86_64.AppImage) **(Recommended)**
- Download → Make executable → Run:
  ```bash
  chmod +x ResearchBuddy-5.1.1-x86_64.AppImage
  ./ResearchBuddy-5.1.1-x86_64.AppImage
  ```
- **Works on all Linux distros** - no installation needed!

**Alternative:** [Download ResearchBuddy-5.1.1-linux.tar.gz](https://github.com/OhioMathTeacher/research-buddy/releases/download/v5.1.1/ResearchBuddy-5.1.1-linux.tar.gz)
- Extract: `tar -xzf ResearchBuddy-5.1.1-linux.tar.gz`
- Run: `cd ResearchBuddy5.1.1 && ./ResearchBuddy5.1.1`

---

## ✨ **What It Does**

* **PDF Viewer** – Professional navigation for academic papers
* **Text Selection** – Highlight and extract quotes for evidence
* **AI Assistant** – Optional AI pre-screening (requires OpenAI API key)
* **Manual Analysis** – Works immediately without any API keys
* **Training Data** – Export reviewer decisions for analysis
* **GitHub Integration** – Upload results automatically (optional)

### **Optional Configuration (for AI features):**
1. Launch the application
2. Go to **Configuration → Settings**
3. Enter your **OpenAI API key** (for AI analysis)
4. Enter your **GitHub token** (for uploading results)
5. Click **Save Configuration**

**Note:** The app works perfectly in manual mode without any API keys!

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

## ℹ️ **Need Help?**

* **Questions**: Open an [issue](https://github.com/OhioMathTeacher/research-buddy/issues)
* **Latest Release**: Check [releases page](https://github.com/OhioMathTeacher/research-buddy/releases)
* **Technical Support**: Contact your research supervisor or IT team

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
