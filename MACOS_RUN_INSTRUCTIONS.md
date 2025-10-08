# 🍎 macOS Running Instructions

## Quick Fix: How to Run ResearchBuddy5.1.1

The macOS executable needs to be run from Terminal (it's not a `.app` bundle that you can double-click).

### **Option 1: Run from Terminal (Easiest)**

1. Open **Terminal** (Applications → Utilities → Terminal)
2. Drag and drop the **ResearchBuddy5.1.1 file** into the Terminal window
3. Press **Enter**

OR type these commands:

```bash
cd ~/Desktop/ResearchBuddy5.1.1
./ResearchBuddy5.1.1
```

### **Option 2: Create a Clickable Launcher**

Create a simple script you CAN double-click:

1. Open TextEdit
2. Paste this code:
```bash
#!/bin/bash
cd "$(dirname "$0")"
./ResearchBuddy5.1.1
```
3. Save as **"Launch ResearchBuddy.command"** in the ResearchBuddy5.1.1 folder
4. Open Terminal and make it executable:
```bash
chmod +x ~/Desktop/ResearchBuddy5.1.1/Launch\ ResearchBuddy.command
```
5. Now you can double-click **"Launch ResearchBuddy.command"**!

### **Option 3: Run from Source (Most Reliable)**

If you have Python installed:

```bash
git clone https://github.com/OhioMathTeacher/research-buddy.git
cd research-buddy
pip install -r requirements.txt
python3 run_research_buddy.py
```

---

## Why Can't I Double-Click It?

The GitHub Actions build created a standalone Unix executable instead of a macOS `.app` bundle. This is a known limitation of cross-platform builds.

**We're working on fixing the build process for the next release!**

---

## Need Help?

Open an issue at: https://github.com/OhioMathTeacher/research-buddy/issues
