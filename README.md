# 🧠 Search Buddy - Positionality Detection System

**Two powerful applications for academic research analysis:**

## 📊 **1. Automated Detection Engine** 
Extract and analyze positionality statements from academic papers using **AI + regex patterns**.

## 🎓 **2. Human Training Interface**
Professional PDF viewer for human experts to label papers and improve detection accuracy.

> 🚀 **Latest Update: September 2025** — Added comprehensive training interface with enhanced PDF viewer, text selection, and data collection tools

---

## � **How the Two Applications Work Together**

### **The Complete Workflow:**

1. **🤖 Automated Detection** - Process papers automatically using current AI + regex patterns
2. **👥 Human Review** - Experts review results using the training interface  
3. **📝 Data Collection** - Collect human judgments, evidence quotes, and pattern suggestions
4. **🔧 Pattern Improvement** - Use training data to enhance detection accuracy
5. **♻️ Iterate** - Re-test automated detection with improved patterns

### **Training Interface Purpose:**
- **Label test cases** - Create ground truth for validation
- **Find missed patterns** - Identify what the AI doesn't catch
- **Collect evidence** - Quote exact text for pattern development  
- **Quality control** - Review and correct automated results
- **Export training data** - Generate datasets for system improvement

Yes - the manual detection app creates test cases that we validate against the automation routines! 🎯

---

## �🛠 Requirements

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

## 🚀 Quick Setup

1. **Clone and install:**

   ```bash
   git clone https://github.com/Technology-Educators-Alliance/py-extractor.git
   cd py-extractor
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Choose your application:**

### **🤖 For Automated Detection:**

   ```bash
   # Launch original extraction GUI
   python gui_openai_05_15_25v3.py
   
   # OR use command line
   python test_extractor.py your_paper.pdf
   ```

   **Features:**
   * 🔑 OpenAI API integration for AI analysis
   * 📁 Batch PDF processing
   * 📊 CSV export with scores and snippets  
   * 🧾 Real-time processing feedback

### **🎓 For Human Training & Labeling:**

   ```bash
   # Launch enhanced training interface
   python enhanced_training_interface.py
   
   # OR use the launcher script
   ./start_training.sh
   ```

   **Features:**
   * 📖 Professional PDF viewer with text selection
   * 🏷️ Expert labeling interface (positive/negative examples)
   * 📝 Evidence collection with exact quotes
   * 💾 Training data export for analysis
   * 🔄 Settings persistence and folder management

---

## 💻 Command-Line Interface (CLI)

Run a quick batch extraction without launching the GUI:

```bash
python scripts/sample_report.py /path/to/pdf/folder
```

This outputs a Markdown-formatted table plus summary counts of detected positionality statements.

---

## 🎯 **Training Data Workflow**

### **Step 1: Generate Baseline Results**
```bash
# Process papers with current detection
python test_extractor.py /path/to/papers/
```

### **Step 2: Human Expert Review**  
```bash
# Launch training interface
python enhanced_training_interface.py
```
- Load papers from ExtractorPDFs folder
- Use PDF viewer to read and analyze each paper
- Select text containing positionality statements
- Label as positive/negative with evidence quotes
- Export training data when complete

### **Step 3: Analyze Training Results**
```bash  
# Analyze human labels vs AI predictions
python training_analysis.py training_data.json --pdf-folder /path/to/papers/
```
- Compare human judgments with AI predictions
- Identify false positives and false negatives  
- Generate new regex patterns from human evidence
- Get recommendations for improving detection

### **Step 4: Update Detection Patterns**
- Add new regex patterns to `metadata_extractor.py`
- Update AI prompts based on human insights
- Test improved detection on validation set

### **Step 5: Validate Improvements**
```bash
# Re-test with improved patterns
python validate_test_cases.py
```

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
