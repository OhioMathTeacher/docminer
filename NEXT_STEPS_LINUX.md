# 🐧 Next Steps on Linux Machine

**Last updated:** October 7, 2025  
**Current status:** macOS build in progress, README updated, workflows ready

---

## 📋 What Was Just Done

✅ Fixed corrupted README title  
✅ Moved download links to TOP of README (your request!)  
✅ Created `manual-build.yml` GitHub Actions workflow  
✅ Created `build_local.sh` for macOS builds  
✅ Added GA troubleshooting documentation  
✅ All changes committed and pushed to GitHub

---

## 🎯 PRIORITY: Build Executables for GAs

### **Option 1: Trigger GitHub Actions (EASIEST)**

This will build all three platforms automatically:

1. Go to: https://github.com/OhioMathTeacher/research-buddy/actions
2. Click **"Manual Build All Platforms"** workflow
3. Click **"Run workflow"** → **"Run workflow"** button
4. Wait 10-15 minutes for builds to complete
5. Download artifacts from the workflow run
6. Create GitHub release and upload the files

**Files you'll get:**
- `ResearchBuddy-5.1.1-macos.zip` (macOS .app bundle)
- `ResearchBuddy-5.1.1-windows.zip` (Windows .exe)
- `ResearchBuddy-5.1.1-linux.tar.gz` (Linux executable)

### **Option 2: Build Linux Executable Locally**

On your Linux machine:

```bash
# Clone if not already there
git clone https://github.com/OhioMathTeacher/research-buddy.git
cd research-buddy
git pull  # Get latest changes

# Set up Python environment
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install pyinstaller

# Build the Linux executable
python -m PyInstaller build_files/ResearchBuddy5.1.1.spec \
    --distpath ./dist \
    --workpath ./build \
    --clean \
    --noconfirm

# Create distribution package
mkdir -p releases
cd dist
tar -czf ../releases/ResearchBuddy-5.1.1-linux.tar.gz ResearchBuddy5.1.1
cd ..

# Test it
./dist/ResearchBuddy5.1.1/ResearchBuddy5.1.1
```

### **Option 3: Create Linux AppImage (Optional - More User Friendly)**

AppImages are single-file executables that work on any Linux distro:

```bash
# After building with PyInstaller (Option 2 above)

# Download appimagetool
wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage
chmod +x appimagetool-x86_64.AppImage

# Create AppImage directory structure
mkdir -p ResearchBuddy.AppDir/usr/bin
mkdir -p ResearchBuddy.AppDir/usr/share/applications
mkdir -p ResearchBuddy.AppDir/usr/share/icons/hicolor/256x256/apps

# Copy executable
cp -r dist/ResearchBuddy5.1.1/* ResearchBuddy.AppDir/usr/bin/

# Create .desktop file
cat > ResearchBuddy.AppDir/usr/share/applications/researchbuddy.desktop << 'EOF'
[Desktop Entry]
Type=Application
Name=Research Buddy
Exec=ResearchBuddy5.1.1
Icon=researchbuddy
Categories=Education;Science;
EOF

# Create AppRun script
cat > ResearchBuddy.AppDir/AppRun << 'EOF'
#!/bin/bash
SELF=$(readlink -f "$0")
HERE=${SELF%/*}
export PATH="${HERE}/usr/bin/:${PATH}"
exec "${HERE}/usr/bin/ResearchBuddy5.1.1" "$@"
EOF
chmod +x ResearchBuddy.AppDir/AppRun

# Build AppImage
./appimagetool-x86_64.AppImage ResearchBuddy.AppDir ResearchBuddy-5.1.1-x86_64.AppImage

# Test it
./ResearchBuddy-5.1.1-x86_64.AppImage
```

---

## 📦 Creating GitHub Release

Once you have all three executables:

1. Go to: https://github.com/OhioMathTeacher/research-buddy/releases
2. Click **"Draft a new release"**
3. Tag: `v5.1.1`
4. Title: **Research Buddy 5.1.1 - Complete Cross-Platform Release**
5. Upload files:
   - `ResearchBuddy-5.1.1-macos.zip`
   - `ResearchBuddy-5.1.1-windows.zip`
   - `ResearchBuddy-5.1.1-linux.tar.gz` (or `.AppImage`)
6. Description:

```markdown
# 🚀 Research Buddy 5.1.1 - Ready to Run!

**NO Python, NO setup, NO terminal - just download and run!**

## 📥 Downloads

- **macOS**: Download → Extract → Double-click `.app`
- **Windows**: Download → Extract → Double-click `.exe`  
- **Linux**: Download → Extract → Run `./ResearchBuddy5.1.1`

## ✨ Features

- Professional PDF viewer with text selection
- AI-assisted positionality detection
- Manual analysis mode without AI
- Evidence collection and quote extraction
- GitHub integration for training reports

## 🎯 Perfect for Graduate Assistants

Zero installation required - just download and start analyzing academic papers!

## 🆘 Troubleshooting

If downloads don't work, use **GitHub Codespaces** (zero installation):
1. Click green "Code" button → "Codespaces" tab
2. Click "Create codespace"
3. Run: `python run_research_buddy.py`
```

7. Click **"Publish release"**

---

## 🔄 Updating README Links

After creating the release, the download links in README.md should work automatically since they point to:

```
https://github.com/OhioMathTeacher/research-buddy/releases/download/v5.1.1/ResearchBuddy-5.1.1-macos.zip
https://github.com/OhioMathTeacher/research-buddy/releases/download/v5.1.1/ResearchBuddy-5.1.1-windows.zip
https://github.com/OhioMathTeacher/research-buddy/releases/download/v5.1.1/ResearchBuddy-5.1.1-linux.tar.gz
```

If you change file names, update README.md accordingly.

---

## 🧪 Testing Executables

Before sharing with GAs, test each executable:

### macOS:
```bash
unzip ResearchBuddy-5.1.1-macos.zip
open ResearchBuddy5.1.1.app
```

### Windows (if you have access):
1. Extract ZIP
2. Double-click `ResearchBuddy5.1.1.exe`
3. If Windows Defender blocks: "More info" → "Run anyway"

### Linux:
```bash
tar -xzf ResearchBuddy-5.1.1-linux.tar.gz
cd ResearchBuddy5.1.1
./ResearchBuddy5.1.1
```

---

## 📝 Current Issues / Known Work

1. **macOS build was in progress** when you left - may need to restart
2. **Windows build** requires GitHub Actions or Windows machine
3. **Linux build** you can do on your home machine
4. **AppImage** is optional but more user-friendly for Linux

---

## 🚨 If GAs Need Software NOW

Direct them to GitHub Codespaces (already in README):

1. Go to repository page
2. Green "Code" button → "Codespaces" tab
3. "Create codespace"
4. Run: `python run_research_buddy.py`

**This works immediately on ANY computer!**

---

## 📂 Important Files Reference

- **Main entry point:** `enhanced_training_interface.py`
- **Developer entry:** `run_research_buddy.py`
- **Build spec:** `build_files/ResearchBuddy5.1.1.spec`
- **Workflows:** `.github/workflows/manual-build.yml`
- **Requirements:** `requirements.txt`

---

## 🎯 Your Goal

Get these three files available for download:

1. ✅ `ResearchBuddy-5.1.1-macos.zip` (macOS .app)
2. ⏳ `ResearchBuddy-5.1.1-windows.zip` (Windows .exe) 
3. ⏳ `ResearchBuddy-5.1.1-linux.tar.gz` (Linux executable or AppImage)

Then update README if needed and tell your GAs to download and run!

---

**Good luck on your Linux machine! Everything is synced and ready to go.** 🚀
