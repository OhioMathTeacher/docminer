# 📝 Google Form Design for Positionality Training Data Collection

## **Form Structure for Graduate Assistant**

### **Section 1: Paper Information**
- **Paper Filename** (auto-populated or dropdown)
- **Paper Title** (extracted automatically)
- **Author(s)** (extracted automatically)

### **Section 2: Positionality Assessment**
- **Does this paper contain positionality statements?**
  - ☐ Yes, explicit positionality statements
  - ☐ Yes, subtle/implicit positionality
  - ☐ No positionality statements
  - ☐ Uncertain/borderline

### **Section 3: Evidence Collection**
- **If YES, quote the specific text:**
  ```
  [Large text box for exact quotes]
  ```

- **Location of statement:**
  - ☐ Introduction/Background
  - ☐ Methods/Methodology
  - ☐ Discussion/Conclusion
  - ☐ Author Note/Acknowledgments
  - ☐ Other: ___________

### **Section 4: Classification Details**
- **Type of positionality statement:**
  - ☐ Identity disclosure (race, gender, class, etc.)
  - ☐ Researcher positioning ("As a researcher...")
  - ☐ Bias acknowledgment ("I acknowledge my bias...")
  - ☐ Reflexive awareness ("I recognize that...")
  - ☐ Methodological reflexivity
  - ☐ Social location/standpoint
  - ☐ Other: ___________

- **Confidence in judgment:**
  - ☐ Very confident (clear example)
  - ☐ Moderately confident (good example)
  - ☐ Somewhat confident (borderline case)
  - ☐ Low confidence (difficult to judge)

### **Section 5: Training Insights**
- **Why does/doesn't this count as positionality?**
  ```
  [Text box for explanation]
  ```

- **What patterns should the AI look for?**
  ```
  [Text box for pattern suggestions]
  ```

## **Data Processing Workflow**

1. **Export Google Form responses** to CSV
2. **Parse and validate** human judgments
3. **Create training dataset** with:
   - PDF text snippets
   - Human labels (positive/negative/uncertain)
   - Reasoning explanations
   - Pattern suggestions
4. **Update detection patterns** based on insights
5. **Validate improvements** against human judgments

## **Sample Training Data Format**
```json
{
  "paper_id": "smith_2023_qualitative.pdf",
  "human_label": "positive",
  "confidence": "high",
  "text_snippet": "As a White researcher working with communities of color, I acknowledge my positionality...",
  "location": "methods",
  "pattern_type": "identity_disclosure",
  "explanation": "Explicit identity disclosure with reflexive awareness of research dynamics",
  "suggested_patterns": ["White researcher", "acknowledge my positionality", "working with communities"]
}
```

## **Benefits of Google Form Approach**
- ✅ **Easy for Graduate Assistant** - familiar interface
- ✅ **Systematic data collection** - structured responses
- ✅ **Remote collaboration** - work from anywhere
- ✅ **Export to spreadsheet** - easy analysis
- ✅ **Progress tracking** - see completion status
- ✅ **Quality control** - review responses before processing