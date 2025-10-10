# Research Buddy Video Tutorial - Feature Coverage Checklist

## ✅ Features to Demonstrate (from User Requirements)

### 1. First-Time Configuration Dialog ✅
- [ ] Shows automatically on first launch
- [ ] OpenAI API Key field
  - [ ] Explain WHY: Powers AI analysis of text
  - [ ] Where to get it: platform.openai.com
- [ ] GitHub Token field
  - [ ] Explain WHY: Uploads analysis to shared repository
  - [ ] Where to get it: GitHub Settings > Developer Settings > Personal Access Tokens
- [ ] GitHub Username field
  - [ ] Explain: "OhioMathTeacher" (Professor's account)
  - [ ] Why shared: Central collection point for all GA analyses
- [ ] GitHub Repository field
  - [ ] Explain: "research-buddy" 
  - [ ] Purpose: Where all training data is stored

**Script Coverage:** Scene 2 (2 minutes) ✅

---

### 2. User Input - Reviewer Name ✅
- [ ] Where to enter name
- [ ] Why it matters: Becomes part of filename
- [ ] Example: `Maya_Armstrong_positive_20251010.json`

**Script Coverage:** Scene 3 (1 minute) ✅

---

### 3. Loading PDFs ✅
- [ ] Click "Load PDF" button
- [ ] Select from file browser
- [ ] PDF displays in left panel
- [ ] Navigation controls (page forward/back)

**Script Coverage:** Scene 3 (1 minute) ✅

---

### 4. Human Evidence - Highlighting Text ✅
- [ ] How to select text (click and drag)
- [ ] Selected text appears in "Selected Text for Evidence" panel
- [ ] Why this matters: Human-identified training data
- [ ] Can select multiple passages
- [ ] Can edit text before submission

**Script Coverage:** Scene 4 (2 minutes) ✅

---

### 5. AI Pre-screening Analysis ✅
- [ ] Location of "AI Pre-screening Analysis" button
- [ ] What it does: Scans entire document for positionality candidates
- [ ] How to interpret results
- [ ] Limitations: May have false positives
- [ ] Why human review is essential
- [ ] Can edit AI-found text before submission

**Script Coverage:** Scene 5 (1.5 minutes) ✅

---

### 6. Making a Decision (Radio Buttons) ✅
- [ ] Three options explained:
  - [ ] Positive: Contains clear positionality statements
  - [ ] Negative: No positionality statements found
  - [ ] Needs Revision: Uncertain/requires more review
- [ ] Decision becomes part of filename

**Script Coverage:** Scene 6 (1 minute) ✅

---

### 7. Upload vs. Download Options ✅
- [ ] **Upload to GitHub** (Primary method)
  - [ ] Saves locally first (~/.research_buddy/training_reports/)
  - [ ] Copies to repository (repo/training_reports/)
  - [ ] Commits and pushes to GitHub
  - [ ] All analyses go to single shared folder
- [ ] **Download** (Offline/backup option)
  - [ ] Saves JSON file locally
  - [ ] When to use: Offline work, GitHub unavailable
  - [ ] Can upload manually later

**Script Coverage:** Scene 7 (2 minutes) ✅

---

### 8. The Big Picture - Training Data Collection ✅
- [ ] Where files are stored: training_reports/ folder
- [ ] All GAs contribute to shared dataset
- [ ] Goal: Each GA analyzes 5-10 articles
- [ ] Combined data trains the AI
- [ ] Show example of multiple files in folder
- [ ] New filename format makes files identifiable

**Script Coverage:** Scene 8 (1.5 minutes) ✅

---

### 9. Ultimate Goal & Purpose ✅
- [ ] Explain: Automate positionality detection
- [ ] Target: 95% accuracy or better
- [ ] Eliminate false negatives (missed statements)
- [ ] Eliminate false positives (incorrect identifications)
- [ ] How: Use human training data to improve AI
- [ ] Importance of careful, accurate human judgments

**Script Coverage:** Scene 8 (1.5 minutes) ✅

---

## Video Structure Summary

| Scene | Topic | Duration | Status |
|-------|-------|----------|--------|
| 1 | Introduction | 0:30 | ✅ |
| 2 | Configuration Dialog | 2:00 | ✅ |
| 3 | Name & PDF Loading | 1:00 | ✅ |
| 4 | Human Evidence Highlighting | 2:00 | ✅ |
| 5 | AI Pre-screening | 1:30 | ✅ |
| 6 | Making Decisions | 1:00 | ✅ |
| 7 | Upload vs Download | 2:00 | ✅ |
| 8 | Big Picture & Goals | 1:30 | ✅ |
| 9 | Closing | 0:30 | ✅ |
| **TOTAL** | | **~12 min** | ✅ |

---

## Additional Elements to Include (Visual Overlays)

### On-Screen Text Callouts:
- [ ] "API Key powers AI analysis"
- [ ] "GitHub Token uploads your work"
- [ ] "All analyses → one shared folder"
- [ ] "Filename: Reviewer_Paper_Decision_Date"
- [ ] "Goal: 95% accuracy"
- [ ] "5-10 papers per GA"

### Visual Highlights:
- [ ] Circle configuration fields as discussed
- [ ] Arrow pointing to selected text
- [ ] Highlight evidence panel
- [ ] Show file path: ~/.research_buddy/training_reports/
- [ ] Show GitHub repository folder
- [ ] Example filenames in folder view

### Screenshots to Capture:
- [ ] First-time configuration dialog
- [ ] Main interface (full view)
- [ ] PDF with highlighted text
- [ ] Evidence panel with text
- [ ] AI analysis results
- [ ] Radio button selections
- [ ] Upload success message
- [ ] GitHub folder with multiple files

---

## Character Distribution Check

**Speaking time roughly equal?**
- Professor Todd: ~35% (mentor/explainer role)
- Research Buddy: ~33% (technical helper role)
- Maya: ~32% (learner/questioner role)

✅ Well balanced - no single character dominates

---

## Post-Production Checklist

- [ ] Generate all audio in ElevenLabs
- [ ] Record screen demonstrations
- [ ] Sync audio with video
- [ ] Add character avatars in corners
- [ ] Add visual callouts/arrows/highlights
- [ ] Add background music (subtle)
- [ ] Add opening title card
- [ ] Add closing credits with resources:
  - [ ] GitHub repository URL
  - [ ] Documentation links
  - [ ] Contact information
- [ ] Export at 1080p
- [ ] Upload to YouTube/institutional platform
- [ ] Generate closed captions
- [ ] Add video description with timestamps

---

## Ready to Produce?

**All requirements covered:** ✅  
**Script complete:** ✅  
**ElevenLabs guide ready:** ✅  
**Waiting for:** Build to complete (executables ready)

**Next Steps:**
1. Wait for v5.1.1 build to finish (~10-15 min)
2. Download and test executables
3. Start ElevenLabs audio generation
4. Record screen demonstrations
5. Edit and publish!

🎬 **Let's make this tutorial!**
