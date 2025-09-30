# 📋 Graduate Assistant Training Protocol

## 🎯 Objective
Use the manual training interface to systematically improve positionality detection through human expert analysis.

## 📚 Materials Needed
- 20-50 academic papers from diverse fields (education, anthropology, psychology, sociology)
- Training interface: `enhanced_training_interface.py`
- Papers placed in `sample_pdfs/` folder

## 🔄 GA Training Workflow

### Step 1: Paper Preparation
```bash
# Place academic papers in the sample_pdfs folder
cp /path/to/papers/*.pdf sample_pdfs/
```

### Step 2: Launch Training Interface
```bash
cd /home/todd/py-extractor
source /home/todd/monolith/bin/activate
python enhanced_training_interface.py
```

### Step 3: For Each Paper - GA Tasks

#### A. Read and Analyze
- **Read the entire paper** using the PDF viewer
- **Look for reflexive statements** where authors discuss their:
  - Position as researchers
  - Cultural background/identity
  - Potential biases or assumptions  
  - Relationship to research subject
  - Methodological reflexivity

#### B. Make Judgment
Select one:
- **Positive - Explicit**: Clear, direct positionality statements
- **Positive - Subtle**: Indirect or implied positioning
- **Negative**: No positionality discussion
- **Unclear**: Ambiguous or needs further review

#### C. Collect Evidence
- **Select text** containing positionality language
- **Copy to evidence field** using "Copy to Evidence" button
- **Include context** around the statement (full sentences)

#### D. Analyze Patterns
- **Check pattern types** that apply:
  - First-person reflexivity
  - Identity disclosure  
  - Methodological positioning
  - Privilege acknowledgment
  - Cultural positioning
  - Research context
- **Suggest new patterns** in the suggestions field

#### E. Rate Confidence
- **1-5 scale** for how certain you are about the judgment
- **Lower ratings** for borderline cases

### Step 4: Export Data
- Click **"Export Data"** when finished with batch
- Saves as `training_data_YYYYMMDD_HHMMSS.json`

## 📊 Analysis Phase (Instructor/Researcher)

### Step 1: Analyze Training Results
```bash
python training_analysis.py training_data_20250929_120000.json --pdf-folder sample_pdfs/
```

### Step 2: Discover New Patterns
- Review false negatives (missed by AI)
- Extract patterns from human evidence quotes
- Test new patterns against validation set

### Step 3: Update Detection System
- Add discovered patterns to `metadata_extractor.py`
- Test improved system performance
- Measure quantitative improvements

## 🎯 Expected Outcomes

### Quantitative Metrics:
- **Detection Rate**: % of positionality statements found
- **Precision**: % of detections that are correct
- **Recall**: % of actual statements detected
- **Human Agreement**: Correlation with expert judgment

### Qualitative Improvements:
- **Pattern Discovery**: New reflexive language patterns
- **Field Specificity**: Discipline-specific positionality norms
- **Cultural Sensitivity**: Diverse identity markers
- **Academic Authenticity**: Real vs. theoretical language

## 📝 Training Tips for GAs

### What to Look For:
✅ **Explicit statements**: "My positionality as a researcher..."  
✅ **Identity disclosure**: "As a Black woman researcher..."  
✅ **Background influence**: "My experience in X community shapes..."  
✅ **Methodological reflexivity**: "I recognize my position affects..."  
✅ **Research context**: "This study emerged from my work..."  

### What NOT to Count:
❌ **Theoretical discussions** of positionality (without personal reflection)  
❌ **Citations** of other authors' positionality work  
❌ **Methodology sections** describing reflexive methods (without personal application)  
❌ **General statements** about researcher bias (without personal specificity)  

### Edge Cases:
⚠️ **Collective positioning**: "We acknowledge our privilege..." (usually count as positive)  
⚠️ **Indirect implications**: "Having worked in this community for 10 years..." (context-dependent)  
⚠️ **Methodological notes**: "The researcher's position was..." (depends on specificity)  

## 🔄 Iterative Improvement

### Round 1: Baseline (20 papers)
- Establish current system performance
- Identify major pattern gaps
- Generate initial improvements

### Round 2: Validation (20 papers)  
- Test improved patterns
- Refine detection rules
- Address remaining false negatives

### Round 3: Specialization (20+ papers)
- Field-specific patterns
- Cultural/identity-specific language
- Advanced reflexivity forms

## 📋 Quality Control

### Inter-rater Reliability:
- **Multiple GAs** label same papers
- **Compare judgments** for consistency
- **Discuss disagreements** to refine criteria
- **Calculate agreement scores**

### Validation Checks:
- **Expert review** of edge cases
- **Pattern testing** on new papers
- **Performance monitoring** over time
- **Feedback integration** from users

---

**This systematic approach ensures that GA training work directly feeds into algorithmic improvements, creating a true human-in-the-loop enhancement system.**