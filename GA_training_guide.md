# 🎓 Graduate Assistant Training Setup Guide

## **Quick Start for Positionality Training**

### **Option 1: Use Integrated Training Interface (Recommended)**

1. **Open Terminal/Command Prompt**
2. **Navigate to project:**
   ```bash
   cd /Users/todd/py-extractor
   source venv/bin/activate
   ```
3. **Launch training interface:**
   ```bash
   python training_interface.py
   ```
4. **Use the interface:**
   - Click "Select PDF Folder" → choose folder with test papers
   - Read paper content on left side
   - See current AI detection results
   - Label with your expert judgment on right side
   - Add evidence quotes and explanations
   - Click "Save & Next" to continue

### **Option 2: Google Form Workflow**

1. **Access Google Form** (Todd will create and share link)
2. **For each paper:**
   - Download/open PDF
   - Read through carefully
   - Answer form questions about positionality presence
   - Provide specific quotes and explanations
   - Submit form

## **Training Guidelines**

### **What counts as positionality?**
✅ **POSITIVE examples:**
- Explicit identity disclosure: "As a Black researcher..."
- Reflexive awareness: "I acknowledge my position as..."
- Bias recognition: "I must recognize my own assumptions..."
- Social location: "Coming from a working-class background..."
- Methodological reflexivity: "My insider status allowed..."

❌ **NEGATIVE examples:**
- Generic "I argue..." statements (just theoretical positioning)
- Citations of others' positionality work
- Methodology descriptions without personal reflection
- Abstract theoretical discussions

### **Labeling Strategy**
1. **Read introduction and methods sections first** (most likely locations)
2. **Look for first-person language** that goes beyond just "I argue"
3. **Check discussion/conclusion** for reflexive commentary  
4. **When in doubt, mark as "uncertain"** and explain why

### **Quality Tips**
- **Quote exact text** - this helps improve AI patterns
- **Explain your reasoning** - why does/doesn't this count?
- **Suggest patterns** - what should the AI look for?
- **Be consistent** - use similar criteria across papers

## **Training Data Collection Goals**

### **Immediate Target: 20-30 papers**
- Mix of positive and negative examples
- Various academic disciplines  
- Different positionality styles
- Clear rationales for each decision

### **Success Metrics**
- **Inter-rater reliability** - consistent labeling
- **Pattern discovery** - new AI patterns from your examples
- **Improved accuracy** - AI performance increases with training
- **Coverage expansion** - detect subtle positionality types

## **Technical Notes**

### **File Outputs**
- `training_data.json` - Automatically saved training labels
- Export function creates timestamped backups
- Data can be analyzed with `training_analysis.py`

### **Integration with AI System**
- Your labels become "ground truth" for evaluation
- Evidence quotes help generate new regex patterns  
- Explanations guide AI prompt engineering
- Confidence ratings help set detection thresholds

## **Contact Todd for:**
- Access to additional papers for training
- Questions about edge cases or difficult papers
- Technical issues with the interface
- Discussion of training results and next steps

---

**Remember:** Your expert judgment is training the AI to be better at detecting positionality statements. The more detailed and consistent your labeling, the better the system will become!