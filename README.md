# 📖 Research Buddy – Positionality Detection Training# 📖 Research Buddy – Pos### Step 2: Install & Run



**Simple, professional software for analyzing academic papers and detecting positionality statements.****For Executables (Easy!):**

1. Extract/unzip the downloaded file

Perfect for graduate assistants, researchers, and academic institutions conducting qualitative research analysis.2. **Windows**: Double-click `ResearchBuddy.exe`

3. **macOS**: Double-click `ResearchBuddy.app` (right-click → Open if needed)

---4. **Linux**: Run `./ResearchBuddy` in terminal

5. **Done!** No Python installation requiredality Detection Training

## 🚀 Quick Start

**Simple, professional software for analyzing academic papers and detecting positionality statements.**

### Step 1: Download the Latest Release

Perfect for graduate assistants, researchers, and academic institutions conducting qualitative research analysis.  

**Production Ready (Recommended):**  

📦 **Download from GitHub Releases:**

- Visit [Research Buddy Releases](https://github.com/OhioMathTeacher/research-buddy/releases/latest)---

- Download `ResearchBuddy5.0.app.zip` (macOS)

- Extract and double-click to run## 🚀 Quick Start



**For Developers:**### Step 1: Download

```bash

git clone https://github.com/OhioMathTeacher/research-buddy.git**Clickable Executables (Recommended)**  

cd research-buddy📦 **Direct Downloads:**

python run_research_buddy.py- **Windows**: [ResearchBuddy-windows.zip](https://github.com/OhioMathTeacher/research-buddy/releases/latest/download/ResearchBuddy-windows.zip)

```- **macOS**: [ResearchBuddy-macos.zip](https://github.com/OhioMathTeacher/research-buddy/releases/latest/download/ResearchBuddy-macos.zip)

- **Linux**: [ResearchBuddy-linux.tar.gz](https://github.com/OhioMathTeacher/research-buddy/releases/latest/download/ResearchBuddy-linux.tar.gz)

### Step 2: Start Using

**If download links don't work yet:** Visit [Releases](https://github.com/OhioMathTeacher/research-buddy/releases) page

1. **Extract** the downloaded zip file

2. **Double-click** `ResearchBuddy5.0.app` to launch### Step 2: Install

3. **Select** your PDF folder to analyze

4. **Start analyzing!** (Works immediately for manual analysis)1. Extract/unzip the downloaded file

2. Double-click the application to run

### Step 3: Optional Setup (for AI features)3. **That’s it!** No Python or technical setup required



1. Go to **Configuration → Settings**### Step 3: Start Analyzing

2. Enter your **OpenAI API key** (for AI analysis)

3. Enter your **GitHub token** (for uploading results)1. The software opens with a training document

4. Click **Save Configuration**2. Add your PDF papers to the `~/ExtractorPDFs` folder

3. Select text and mark positionality statements

---4. Export your training data when finished



## 📋 What It Does---



* **PDF Viewer** – Professional navigation for academic papers## 📋 What It Does

* **Text Selection** – Highlight and extract quotes for evidence

* **AI Assistant** – Optional AI pre-screening (requires OpenAI API key)* **PDF Viewer** – Professional navigation for academic papers

* **Training Data** – Export reviewer decisions for analysis* **Text Selection** – Highlight and extract quotes for evidence

* **Smart Buttons** – Color-coded status indicators for easy setup* **AI Assistant** – Optional AI pre-screening (requires OpenAI API key)

* **Secure Configuration** – Password-protected API key entry* **Training Data** – Export reviewer decisions

* **Manual Mode** – Works completely offline without AI

---

---

## 📁 Project Structure

## 💡 Need Help?

```

research-buddy/* **Getting Started**: See `QUICK_START_FOR_GAS.md`

├── run_research_buddy.py          # Main entry point for developers* **Questions**: Open an [issue](https://github.com/OhioMathTeacher/research-buddy/issues)

├── enhanced_training_interface.py # Core application* **Technical Support**: Contact your research supervisor or IT team

├── configuration_dialog.py        # Settings interface  

├── github_report_uploader.py      # Upload functionality---

├── launch_research_buddy.py       # Legacy launcher

├── requirements.txt               # Python dependencies## 📄 License

├── docs/                          # Documentation

│   ├── QUICK_START_FOR_GAS.md    # Quick start guide**Academic and Educational Use Only**

│   ├── RELEASE_v5.0.md           # Latest release notesThis project is licensed under **Creative Commons Attribution-NonCommercial 4.0**:

│   └── about_EVIDENCE.txt        # Evidence export info

├── legal/                         # License files* ✅ Free for academic research and education

│   ├── LICENSE                   # Main MIT license* ✅ Share and modify for research purposes

│   ├── LICENSE-ACADEMIC          # Academic use terms* ❌ Commercial use requires separate licensing

│   └── LICENSE-NONCOMMERCIAL     # Non-commercial terms

├── build_files/                   # Build and packagingFor commercial licensing, contact the project maintainer.

│   ├── build.py                  # Build script

│   └── *.spec                    # PyInstaller configs---

├── tests/                         # Test files

├── utils/                         # Utility modules**Research Buddy** – Making contextual analysis accessible to everyone in academia.

├── scripts/                       # Helper scripts
├── cli/                          # Command-line tools
└── sample_pdfs/                  # Example documents
```

---

## 💡 Need Help?

* **Getting Started**: See `docs/QUICK_START_FOR_GAS.md`
* **Questions**: Open an [issue](https://github.com/OhioMathTeacher/research-buddy/issues)
* **Technical Support**: Contact your research supervisor or IT team

---

## 🔧 For Developers

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

## 📄 License

**Academic and Educational Use Only**
This project is licensed under **Creative Commons Attribution-NonCommercial 4.0**:

* ✅ Free for academic research and education
* ✅ Share and modify for research purposes
* ❌ Commercial use requires separate licensing

See `legal/` directory for full license terms.

---

**Research Buddy** – Making contextual analysis accessible to everyone in academia.