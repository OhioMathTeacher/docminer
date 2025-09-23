# 🧠 Search Buddy (`py-extractor`)

Extract **targeted content** from PDFs using **AI analysis** — via a simple **GUI** or **CLI**.

> 🚀 **Latest Release: v0.3.7** — final GUI version, persistent settings, improved metadata mapping, and smoother extraction flow

---

## 🛠 Requirements

* **Python** 3.10 or higher
* **pip** (package installer)

Install dependencies:

```bash
python3 -m pip install -r requirements.txt
```

Key libraries:

* `openai` for AI-powered positionality detection
* `PySide6` for the GUI
* `pdfplumber` & `PyPDF2` for PDF parsing
* `tabulate` for CLI output

---

## 🧰 Quick Setup (GUI)

1. **Clone or update** the repository:

   ```bash
   git clone https://github.com/Technology-Educators-Alliance/py-extractor.git
   cd py-extractor
   # or, if already cloned:
   git pull origin main
   ```

2. **Activate** your Python virtual environment:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Launch** the GUI:

   ```bash
   python gui_openai_05_15_25v3.py
   ```

4. **Use** the interface:

   * 🔑 Enter or confirm your OpenAI API key (auto‑saved between sessions)
   * 📁 Click **Select Folder** and choose your PDF directory
   * 🟢 Click **Run Extraction** to start processing
   * 🧾 Watch live debug output as each file is processed
   * 🧃 Click **Save CSV As...** (defaults to Desktop with timestamped filename)

---

## 💻 Command-Line Interface (CLI)

Run a quick batch extraction without launching the GUI:

```bash
python scripts/sample_report.py /path/to/pdf/folder
```

This outputs a Markdown-formatted table plus summary counts of detected positionality statements.

---

## 📝 Changelog & Roadmap

* **v0.3.7**: Final GUI layout; removed legacy options; fixed metadata key mapping; real-time progress updates
* **v0.3.6**: Persistent API key; improved prompt UX; smarter CSV defaults

**Upcoming**:

* Batch Dropbox/Drive integration
* Enhanced AI prompt customization

Contributions welcome! Fork, open an issue, or submit a pull request.

---

---

## 🧪 Test Cases & Validation

The application includes a comprehensive test suite with **6 carefully selected academic papers** to validate positionality detection across different scenarios:

### **Test Case Files (`/Users/todd/pdfs/`)**

| File | Expected Result | Test Purpose | Key Features |
|------|----------------|--------------|-------------|
| `Dean-ReflexivityLimitsStudy-2021.pdf` | **POSITIVE** | Explicit reflexivity study | Should contain clear positionality statements about research reflexivity |
| `Parks-ObstaclesAddressingRace-2012.pdf` | **POSITIVE** | Race-focused research | Likely contains author positioning on racial identity/perspective |
| `Vries-Transgenderpeoplecolor-2015.pdf` | **POSITIVE** | Identity-focused research | Should have positionality about transgender and racial identity |
| `cycyk-et-al-2022-moving-through-the-pipeline...pdf` | **NEGATIVE** | Multi-author quantitative | Large-scale study unlikely to have individual positionality |
| `datnow-et-al-2022-bridging-educational-change...pdf` | **NEGATIVE** | Policy/systems research | Institutional focus, less personal positioning |
| `henrekson-et-al-2025-the-purposes-of-education...pdf` | **NEGATIVE** | Theoretical/philosophical | Abstract research less likely to include personal positioning |

### **Detection Criteria Being Tested**

#### **Regex Pattern Tests:**
- `explicit_positionality`: Direct mentions of "positionality"
- `first_person_reflexivity`: "I reflect/acknowledge/recognize"
- `researcher_self`: "I, as a researcher"
- `author_self`: "I, as the author"
- `as_a_role`: "As a [role], I"
- `I_position`: "I position/situate"

#### **AI Analysis Tests:**
- **Header analysis**: First-person positioning in introductions
- **Full-text analysis**: Positionality in discussion/conclusion sections
- **Confidence scoring**: High (≥0.75), Medium (0.2-0.74), Low (<0.2)

### **Running Test Suite**

```bash
# Test all files with detailed output
python test_extractor.py /Users/todd/pdfs/

# Generate comparison report (requires valid OpenAI API key)
python scripts/sample_report.py /Users/todd/pdfs/
```

### **Expected Outcomes**

**Current Performance Issues:**
- **False Negatives**: May miss subtle positionality statements
- **Pattern Limitations**: Regex patterns too restrictive for academic writing styles
- **AI Dependency**: Requires expensive API calls for nuanced detection

**Validation Goals:**
- **3/6 positive detections** (Dean, Parks, Vries papers)
- **0/3 false positives** (multi-author institutional studies)
- **Confidence scores** correlate with statement explicitness

---

## 📄 License

Licensed under **CC BY-NC 4.0** (non-commercial educational use). See [LICENSE.txt](LICENSE.txt).
