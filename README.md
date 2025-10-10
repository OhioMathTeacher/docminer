# Research Buddy 5.1.1 - Professional Positionality Analysis Interface

**Simple, professional software for analyzing academic papers and detecting positionality statements.**

Perfect for graduate assistants, researchers, and academic institutions conducting qualitative research analysis.

---

## 📥 **DOWNLOAD EXECUTABLES - Just Click and Run!**

**No Python, no setup, no terminal commands - just download and double-click!**

### **macOS**
🍎 [**Download ResearchBuddy-5.1.1-macos.dmg**](https://github.com/OhioMathTeacher/research-buddy/releases/download/v5.1.1/ResearchBuddy-5.1.1-macos.dmg) 
- Download → Double-click the DMG → Drag `ResearchBuddy5.1.1.app` to Applications
- Open from Applications folder → Done!
- **Works on both Intel and Apple Silicon Macs**
- If Mac says "unidentified developer": Right-click the .app → Open → Open (only needed first time)

### **Windows**  
🪟 [**Download ResearchBuddy-5.1.1-windows.zip**](https://github.com/OhioMathTeacher/research-buddy/releases/download/v5.1.1/ResearchBuddy-5.1.1-windows.zip)
- Download → Extract → Double-click `ResearchBuddy5.1.1.exe`
- If Windows Defender blocks: Click "More info" → "Run anyway"

### **Linux**
🐧 [**Download ResearchBuddy-5.1.1-x86_64.AppImage**](https://github.com/OhioMathTeacher/research-buddy/releases/download/v5.1.1/ResearchBuddy-5.1.1-x86_64.AppImage)

**Simple 3-step install:**
1. Download the AppImage file
2. Open terminal in your Downloads folder
3. Run these two commands:
```bash
chmod +x ResearchBuddy-5.1.1-x86_64.AppImage
./ResearchBuddy-5.1.1-x86_64.AppImage
```

**That's it!** The app will launch. To run it again later, just double-click the AppImage file (or run the second command again).

- **Universal Linux executable - works on all distros** (Ubuntu, Fedora, Arch, Debian, etc.)

---

## ✨ **What It Does**

* **PDF Viewer** – Professional navigation for academic papers
* **Text Selection** – Highlight and extract quotes for evidence
* **AI Assistant** – Optional AI pre-screening (requires OpenAI API key)
* **Manual Analysis** – Works immediately without any API keys
* **Training Data** – Export reviewer decisions for analysis
* **GitHub Integration** – Upload results automatically (optional)

---

## ⚙️ **Configuration Guide**

### **First-Time Setup**

When you first launch Research Buddy, you'll need to configure two things:

#### **1. GitHub Repository Settings** (One-time setup)

When prompted with "GitHub Repository Not Configured", enter:
- **Owner**: `OhioMathTeacher`
- **Repository**: `research-buddy`

This tells the app where to upload training reports. Click **OK** to save.

> **Note**: These settings are saved to `~/.research_buddy/interface_settings.json` on your computer.

#### **2. Environment Variables** (Required for upload features)

The app needs two secure tokens to work with external services. These are set as **environment variables** (NOT saved in files for security).

##### **Setup Steps:**

**On macOS/Linux:**
1. Open Terminal
2. Edit your shell profile:
   ```bash
   nano ~/.bashrc    # or ~/.zshrc on macOS
   ```
3. Add these lines (replace with your actual tokens):
   ```bash
   export RESEARCH_BUDDY_OPENAI_API_KEY="sk-your-key-here"
   export RESEARCH_BUDDY_GITHUB_TOKEN="ghp_your-token-here"
   ```
4. Save (Ctrl+O, Enter, Ctrl+X) and reload:
   ```bash
   source ~/.bashrc   # or source ~/.zshrc
   ```

**Quick Start Script (macOS/Linux):**

After setting up your environment variables, you can use the provided startup script:
```bash
./start_research_buddy.sh
```

This script automatically loads your environment and launches the app - no need to remember commands!

**On Windows:**
1. Search for "Environment Variables" in Start Menu
2. Click "Edit system environment variables"
3. Click "Environment Variables" button
4. Under "User variables", click "New"
5. Add each variable:
   - Variable name: `RESEARCH_BUDDY_OPENAI_API_KEY`
   - Variable value: `sk-your-key-here`
   - Click OK
   - Repeat for `RESEARCH_BUDDY_GITHUB_TOKEN`

##### **Getting Your Tokens:**

**OpenAI API Key** (for AI-assisted analysis):
- Go to https://platform.openai.com/api-keys
- Create a new API key
- Copy and use in the environment variable above

**GitHub Token** (for uploading training reports):
- Go to https://github.com/settings/tokens
- Click "Generate new token (classic)"
- Give it a name: "Research Buddy - Training Reports"
- Select scope: ✅ `repo` (full control of private repositories)
- Set expiration: "No expiration" (or your preference)
- Generate and copy the token
- **Share this same token with all your GAs** - everyone can use the same one!

> **Security Note**: Tokens are stored as environment variables, NOT in config files. This keeps them secure and separate from your code.

### **Working Without Tokens**

**The app works perfectly in manual mode without any API keys!**
- Manual PDF review and analysis works immediately
- You can export training data locally
- Only AI features and GitHub upload require tokens

### **Important Notes**

- **Environment variables are loaded once per terminal session** - if you update your tokens in `.bashrc`, run `source ~/.bashrc` to reload them
- **Use `run_research_buddy.py` or `start_research_buddy.sh`** - avoid `launch_research_buddy.py` which prompts for credentials every time
- **The GitHub repository dialog only shows once** - after you enter Owner/Repo settings, they're saved to `~/.research_buddy/interface_settings.json`

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
