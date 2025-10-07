# Building macOS Universal Executable on M1 Mac Mini

## 📋 Quick Reference

**Goal:** Build a Universal macOS executable for Research Buddy 5.1.1 that works on both Intel and Apple Silicon Macs.

**Location:** M1 Mac Mini (downstairs)

---

## ✅ Pre-Flight Checklist

Before you start, make sure:
- [ ] Current GitHub Actions build has completed (or failed - we'll replace it anyway)
- [ ] You're on the M1 Mac Mini
- [ ] You have internet connection to clone the repo

---

## 🚀 Step-by-Step Build Process

### 1. Clone the Repository (if not already there)

```bash
cd ~/
git clone https://github.com/OhioMathTeacher/research-buddy.git
cd research-buddy
```

If you already have it cloned:

```bash
cd ~/research-buddy
git fetch --all
git pull origin main
```

### 2. Install Python 3.11 (if not installed)

```bash
# Check if you have Python 3.11
python3 --version

# If not, install via Homebrew
brew install python@3.11
```

### 3. Create Virtual Environment

```bash
# From research-buddy directory
python3 -m venv .venv
source .venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
pip install pyinstaller
```

### 5. Build the Executable

```bash
# Clean any previous builds
rm -rf dist/ResearchBuddy5.1.1 build/ResearchBuddy5.1.1

# Build using the spec file
python -m PyInstaller build_files/ResearchBuddy5.1.1.spec --distpath ./dist --workpath ./build --clean
```

**Expected outcome:** This will create `dist/ResearchBuddy5.1.1/` folder with the executable.

### 6. Test the Executable

```bash
# Run the executable to make sure it works
./dist/ResearchBuddy5.1.1/ResearchBuddy5.1.1
```

**What to check:**
- Application launches
- Window appears
- You can click "Load PDF" button
- No immediate crashes

### 7. Create Release Package

```bash
# Create releases directory
mkdir -p releases

# Package as tar.gz
cd dist
tar -czf ../releases/ResearchBuddy5.1.1-macos.tar.gz ResearchBuddy5.1.1
cd ..

# Check the file was created
ls -lh releases/ResearchBuddy5.1.1-macos.tar.gz
```

**Expected size:** ~250-300MB

### 8. Upload to GitHub Release

**Option A: Using GitHub Web Interface (Easiest)**
1. Go to: https://github.com/OhioMathTeacher/research-buddy/releases/tag/v5.1.1
2. Click "Edit release"
3. Drag and drop `releases/ResearchBuddy5.1.1-macos.tar.gz` into the assets area
4. Click "Update release"

**Option B: Using Command Line (if you have GitHub CLI)**
```bash
# Install gh if needed
brew install gh

# Login (one time)
gh auth login

# Upload the release asset
gh release upload v5.1.1 releases/ResearchBuddy5.1.1-macos.tar.gz
```

---

## 🎯 Expected Results

After upload, the v5.1.1 release should have:
- ✅ `ResearchBuddy5.1.1-linux.tar.gz` (~278MB) - Already there
- ✅ `ResearchBuddy5.1.1-macos.tar.gz` (~250-300MB) - You just uploaded
- ⏳ `ResearchBuddy5.1.1-windows.zip` - From GitHub Actions (if it works)

---

## 🐛 Troubleshooting

### Build fails with "No module named 'PySide6'"
```bash
# Make sure you activated the virtual environment
source .venv/bin/activate
pip install -r requirements.txt
```

### Executable crashes immediately
```bash
# Run from terminal to see error messages
./dist/ResearchBuddy5.1.1/ResearchBuddy5.1.1
```

### "Permission denied" when running executable
```bash
chmod +x dist/ResearchBuddy5.1.1/ResearchBuddy5.1.1
```

### PyInstaller not found
```bash
source .venv/bin/activate
pip install pyinstaller
```

---

## 📝 Notes for Future Builds

### For Universal Binary (Intel + Apple Silicon)
The build on M1 will create an **ARM64** executable. To create a true Universal binary:

```bash
# This requires building twice and using lipo to combine
# For now, ARM64-only is fine since most Macs are Apple Silicon
```

### Build Time
- First build: ~5-10 minutes (downloads and compiles everything)
- Subsequent builds: ~2-3 minutes (cached)

### File Locations
- **Spec file:** `build_files/ResearchBuddy5.1.1.spec`
- **Build output:** `dist/ResearchBuddy5.1.1/`
- **Release package:** `releases/ResearchBuddy5.1.1-macos.tar.gz`
- **Build cache:** `build/ResearchBuddy5.1.1/`

---

## ✨ Quick Command Summary

```bash
# Complete build in one go (copy-paste friendly)
cd ~/research-buddy
git pull origin main
source .venv/bin/activate
pip install -r requirements.txt
pip install pyinstaller
rm -rf dist/ResearchBuddy5.1.1 build/ResearchBuddy5.1.1
python -m PyInstaller build_files/ResearchBuddy5.1.1.spec --distpath ./dist --workpath ./build --clean
cd dist
tar -czf ../releases/ResearchBuddy5.1.1-macos.tar.gz ResearchBuddy5.1.1
cd ..
ls -lh releases/ResearchBuddy5.1.1-macos.tar.gz
```

Then upload via GitHub web interface!

---

**Created:** October 7, 2025  
**For:** Research Buddy v5.1.1 macOS Build  
**Platform:** M1 Mac Mini (Apple Silicon)
