# DocMiner Rebrand Preview

This document shows before/after examples of the rebrand changes.

## Application Window Titles

### Before
```
Research Buddy 5.2 - Professional Positionality Analysis Interface
```

### After
```
DocMiner 5.2 - Professional Positionality Analysis Interface
```

---

## README.md Download Section

### Before
```markdown
🐧 [**Download ResearchBuddy-5.2-x86_64.AppImage**](https://github.com/OhioMathTeacher/research-buddy/releases/download/v5.2/ResearchBuddy-5.2-x86_64.AppImage)

🍎 [**Download ResearchBuddy-macos.dmg**](https://github.com/OhioMathTeacher/research-buddy/releases/download/v5.2/ResearchBuddy-macos.dmg)

🪟 [**Download ResearchBuddy-windows.zip**](https://github.com/OhioMathTeacher/research-buddy/releases/download/v5.2/ResearchBuddy-windows.zip)
```

### After
```markdown
🐧 [**Download DocMiner-6.0-x86_64.AppImage**](https://github.com/OhioMathTeacher/docminer/releases/download/v6.0/DocMiner-6.0-x86_64.AppImage)

🍎 [**Download DocMiner-macos.dmg**](https://github.com/OhioMathTeacher/docminer/releases/download/v6.0/DocMiner-macos.dmg)

🪟 [**Download DocMiner-windows.zip**](https://github.com/OhioMathTeacher/docminer/releases/download/v6.0/DocMiner-windows.zip)
```

---

## About Dialog

### Before
```python
QMessageBox.about(self, "About Research Buddy 5.2", 
    "🎓 Research Buddy 5.2\n\n"
    "Professional Positionality Analysis Interface\n\n"
    "..."
    "Research Buddy Project"
)
```

### After
```python
QMessageBox.about(self, "About DocMiner 5.2", 
    "🎓 DocMiner 5.2\n\n"
    "Professional Positionality Analysis Interface\n\n"
    "..."
    "DocMiner Project"
)
```

---

## Build Specification

### Before (build_files/ResearchBuddy5.2.spec)
```python
exe = EXE(
    pyz,
    a.scripts,
    name='ResearchBuddy5.2',
    # ...
)

app = BUNDLE(
    exe,
    name='ResearchBuddy5.2.app',
    bundle_identifier='edu.university.researchbuddy',
)
```

### After (build_files/DocMiner6.0.spec)
```python
exe = EXE(
    pyz,
    a.scripts,
    name='DocMiner6.0',
    # ...
)

app = BUNDLE(
    exe,
    name='DocMiner6.0.app',
    bundle_identifier='edu.university.docminer',
)
```

---

## Startup Script

### Before (start_research_buddy.sh)
```bash
#!/bin/bash
# Research Buddy - Simple Startup Script
# This script loads your environment variables and launches Research Buddy

# Launch Research Buddy
echo "🚀 Launching Research Buddy..."
python3 run_research_buddy.py
```

### After (start_docminer.sh)
```bash
#!/bin/bash
# DocMiner - Simple Startup Script
# This script loads your environment variables and launches DocMiner

# Launch DocMiner
echo "🚀 Launching DocMiner..."
python3 run_docminer.py
```

---

## Configuration Dialog

### Before
```python
self.setWindowTitle("🔧 Research Buddy Configuration")

title = QLabel("🔧 Research Buddy Configuration")
```

### After
```python
self.setWindowTitle("🔧 DocMiner Configuration")

title = QLabel("🔧 DocMiner Configuration")
```

---

## GitHub Workflow

### Before (.github/workflows/build-executables.yml)
```yaml
name: 🚀 Build Research Buddy Executables

jobs:
  build:
    strategy:
      matrix:
        include:
          - os: ubuntu-latest
            name: ResearchBuddy-linux
          - os: windows-latest
            name: ResearchBuddy-windows
          - os: macos-latest
            name: ResearchBuddy-macos
```

### After
```yaml
name: 🚀 Build DocMiner Executables

jobs:
  build:
    strategy:
      matrix:
        include:
          - os: ubuntu-latest
            name: DocMiner-linux
          - os: windows-latest
            name: DocMiner-windows
          - os: macos-latest
            name: DocMiner-macos
```

---

## AppImage Build Script

### Before (build_files/create_appimage.sh)
```bash
#!/bin/bash
# Create an AppImage for ResearchBuddy on Linux

VERSION="5.2"
APP_NAME="ResearchBuddy"

echo "🐧 Creating AppImage for ResearchBuddy ${VERSION}"

if [ ! -f "dist/ResearchBuddy5.2/ResearchBuddy5.2" ]; then
    echo "❌ Error: dist/ResearchBuddy5.2/ResearchBuddy5.2 not found"
    exit 1
fi
```

### After
```bash
#!/bin/bash
# Create an AppImage for DocMiner on Linux

VERSION="6.0"
APP_NAME="DocMiner"

echo "🐧 Creating AppImage for DocMiner ${VERSION}"

if [ ! -f "dist/DocMiner6.0/DocMiner6.0" ]; then
    echo "❌ Error: dist/DocMiner6.0/DocMiner6.0 not found"
    exit 1
fi
```

---

## Desktop Entry File

### Before
```desktop
[Desktop Entry]
Type=Application
Name=Research Buddy
Exec=ResearchBuddy
Icon=researchbuddy
Categories=Education;Science;
```

### After
```desktop
[Desktop Entry]
Type=Application
Name=DocMiner
Exec=DocMiner
Icon=docminer
Categories=Education;Science;
```

---

## README Title

### Before
```markdown
# Research Buddy 5.2 - Professional Positionality Analysis Interface

**Research Buddy** – Making positionality analysis accessible to everyone in academia.
```

### After
```markdown
# DocMiner 5.2 - Professional Positionality Analysis Interface

**DocMiner** – Making positionality analysis accessible to everyone in academia.
```

---

## License Files

### Before (legal/LICENSE)
```
Research Buddy - Positionality Detection Software for Academic Research
Copyright (c) 2025 [Your Name]
```

### After
```
DocMiner - Positionality Detection Software for Academic Research
Copyright (c) 2025 [Your Name]
```

---

## Installation Instructions

### Before
```markdown
### macOS
1. Download ResearchBuddy-5.2-macOS.dmg
2. Double-click the DMG
3. Drag ResearchBuddy5.2.app to Applications
```

### After
```markdown
### macOS
1. Download DocMiner-6.0-macOS.dmg
2. Double-click the DMG
3. Drag DocMiner6.0.app to Applications
```

---

## URL Changes

### Repository URL
- **Before**: `https://github.com/OhioMathTeacher/research-buddy`
- **After**: `https://github.com/OhioMathTeacher/docminer`

### Download URLs
- **Before**: `https://github.com/OhioMathTeacher/research-buddy/releases/download/v5.2/ResearchBuddy-5.2-x86_64.AppImage`
- **After**: `https://github.com/OhioMathTeacher/docminer/releases/download/v6.0/DocMiner-6.0-x86_64.AppImage`

### Git Clone
- **Before**: `git clone https://github.com/OhioMathTeacher/research-buddy.git`
- **After**: `git clone https://github.com/OhioMathTeacher/docminer.git`

---

## What Stays the Same

✅ **Unchanged**:
- Git commit history
- Training reports content (historical data)
- Archive directory content
- Core functionality
- Features and capabilities
- License type
- File structure (mostly)

---

## Summary Statistics

Based on grep search results:
- **~200 text occurrences** of "Research Buddy" / "ResearchBuddy"
- **~12 files** to rename
- **~50 files** with text content changes
- **~0 functional changes** (pure rebrand)

---

## Notes

1. **Version Number**: Consider bumping to v6.0 to mark the rebrand
2. **User Config**: `~/.research_buddy/` can stay as-is (backward compatible)
3. **GitHub Redirects**: Old URLs will redirect automatically (for a while)
4. **Git History**: 100% preserved, no commits lost

Ready to rebrand when you are! 🎨
