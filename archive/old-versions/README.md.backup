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

* **v1.0.0**: 🎉 **Major Release** - Complete dual-application system with professional training interface, enhanced detection, and human-in-the-loop workflow
* **v0.3.7**: Final legacy GUI layout; improved metadata mapping; real-time progress updates
* **v0.3.6**: Persistent API key; improved prompt UX; smarter CSV defaults

**Future Enhancements**:

* Advanced pattern learning from training data
* Batch cloud storage integration (Dropbox/Drive)
* Multi-language positionality detection
* Collaborative training workflows

Contributions welcome! Fork, open an issue, or submit a pull request.

---

---

## 🧪 Testing & Validation

The system includes comprehensive testing capabilities for both applications:

### **🤖 Automated Detection Testing**

Test the detection engine with individual papers or batches:

```bash
# Test single paper
python test_extractor.py path/to/paper.pdf

# Test folder of papers  
python test_extractor.py /path/to/pdf/folder/

# Generate analysis report
python scripts/sample_report.py /path/to/pdf/folder/
```

### **🎓 Training Interface Validation**

Use the training interface to create ground truth data:

1. **Load test papers** in training interface
2. **Expert review** - human judgment on each paper
3. **Evidence collection** - quote exact positionality statements
4. **Export training data** - JSON format for analysis
5. **Compare with AI** - run analysis to find gaps

### **📊 Analysis & Improvement Workflow**

```bash
# Analyze training results vs AI predictions
python training_analysis.py training_data.json --pdf-folder /path/to/papers/

# Validate improvements after pattern updates
python validate_test_cases.py
```

### **🎯 Detection Patterns Tested**

The system tests for multiple positionality patterns:

- **Explicit statements**: Direct mentions of "positionality" or "my position"  
- **Identity disclosure**: "As a [identity] researcher" patterns
- **Reflexive awareness**: "I acknowledge/recognize/reflect" statements
- **Methodological positioning**: Author's relationship to research approach
- **Bias acknowledgment**: Recognition of limitations or perspectives

### **📈 Performance Metrics**

- **Precision**: Accuracy of positive detections (minimize false positives)
- **Recall**: Coverage of actual positionality statements (minimize false negatives)  
- **Human agreement**: Correlation between AI confidence and expert judgment
- **Pattern discovery**: New regex patterns identified from human examples

---

## 📄 License

Licensed under **CC BY-NC 4.0** (non-commercial educational use). See [LICENSE.txt](LICENSE.txt).
