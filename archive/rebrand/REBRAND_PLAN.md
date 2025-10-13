# DocMiner Rebrand Execution Plan

## Overview

This plan outlines the complete process to rebrand "Research Buddy" to "DocMiner".

## Why Rebrand?

- "ResearchBuddy" name is already taken
- "DocMiner" better reflects the tool's purpose
- Clean break for a fresh start

## What Is DocMiner?

**DocMiner** = Document Miner for Academic Research
- Mines academic papers for positionality statements
- Extracts valuable insights from research documents
- Professional, descriptive, unique name

## Pre-Rebrand Checklist

- [ ] Complete Research Buddy v5.2 release
- [ ] Upload all platform executables (Linux, macOS, Windows)
- [ ] Ensure all features are working
- [ ] Create final backup of repository

## Rebrand Process

### Phase 1: Automated Text Replacement

Run the rebrand script:

```bash
cd rebrand

# Step 1: Preview changes (safe, read-only)
python3 rebrand.py --preview

# Step 2: Review the preview output
# Make sure everything looks correct

# Step 3: Execute the rebrand
python3 rebrand.py --execute
```

This will:
- ✅ Replace all "Research Buddy" → "DocMiner" in text
- ✅ Replace all "ResearchBuddy" → "DocMiner" in code
- ✅ Rename files and build specs
- ✅ Create a backup before making changes

### Phase 1.5: UI/UX Updates

**Force Light Theme** (Dark theme looks bad!)

Update `enhanced_training_interface.py` to force light/grey theme:

```python
# Add at the top of the file, after imports
from PySide6.QtGui import QPalette, QColor
from PySide6.QtWidgets import QApplication

# In the main() function or __init__, add:
app.setStyle("Fusion")  # Use Fusion style for consistency

# Force light palette
palette = QPalette()
palette.setColor(QPalette.Window, QColor(240, 240, 240))
palette.setColor(QPalette.WindowText, QColor(0, 0, 0))
palette.setColor(QPalette.Base, QColor(255, 255, 255))
palette.setColor(QPalette.AlternateBase, QColor(245, 245, 245))
palette.setColor(QPalette.ToolTipBase, QColor(255, 255, 220))
palette.setColor(QPalette.ToolTipText, QColor(0, 0, 0))
palette.setColor(QPalette.Text, QColor(0, 0, 0))
palette.setColor(QPalette.Button, QColor(240, 240, 240))
palette.setColor(QPalette.ButtonText, QColor(0, 0, 0))
palette.setColor(QPalette.BrightText, QColor(255, 0, 0))
palette.setColor(QPalette.Link, QColor(42, 130, 218))
palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
palette.setColor(QPalette.HighlightedText, QColor(255, 255, 255))
app.setPalette(palette)
```

**Other UI Improvements:**
- [ ] Consistent grey/white color scheme
- [ ] Better dialog styling
- [ ] Improved button contrast
- [ ] Professional appearance regardless of OS theme

### Phase 2: Test Locally

```bash
# Test the renamed application
cd ..
python3 run_docminer.py

# Build and test
pyinstaller build_files/DocMiner5.2.spec --clean
./dist/DocMiner5.2/DocMiner5.2
```

Verify:
- [ ] Application launches
- [ ] **Light theme is enforced (no dark mode)**
- [ ] Configuration dialog works
- [ ] PDF loading works
- [ ] Evidence marking works
- [ ] Upload to GitHub works

### Phase 3: Update Git Repository

```bash
# Review all changes
git status
git diff

# Stage all changes
git add .

# Commit the rebrand
git commit -m "Rebrand to DocMiner

- Changed all 'Research Buddy' references to 'DocMiner'
- Renamed build specs and executables
- Updated documentation and README
- Renamed startup scripts
- Version bumped to 6.0 for new brand"

# Push to GitHub (still as research-buddy repo)
git push origin main
```

### Phase 4: Rename GitHub Repository

1. Go to: https://github.com/OhioMathTeacher/research-buddy/settings
2. Scroll to "Repository name"
3. Change from `research-buddy` to `docminer`
4. Click "Rename"

⚠️ **Important**: GitHub will auto-redirect old URLs for a while, but update your local remote:

```bash
# Update your local git remote
git remote set-url origin https://github.com/OhioMathTeacher/docminer.git

# Rename local directory (optional)
cd ..
mv research-buddy docminer
cd docminer
```

### Phase 5: Create DocMiner v6.0 Release

1. **Bump Version to 6.0**
   - Update version in `build_files/DocMiner6.0.spec` (copy from 5.2 spec)
   - Update version in documentation
   - Version 6.0 signifies the rebrand

2. **Build New Executables**
   ```bash
   # Linux AppImage
   pyinstaller build_files/DocMiner6.0.spec --clean
   ./build_files/create_appimage.sh  # Update script for DocMiner
   
   # macOS (on M1 Mac)
   pyinstaller build_files/DocMiner6.0.spec --clean
   create-dmg ...
   
   # Windows (GitHub Actions)
   # Trigger workflow
   ```

3. **Create GitHub Release**
   - Tag: `v6.0`
   - Title: "🚀 DocMiner v6.0 - New Brand, Same Great Tool"
   - Description: Explain the rebrand from Research Buddy
   - Upload executables:
     * `DocMiner-6.0-x86_64.AppImage` (Linux)
     * `DocMiner-6.0-macOS.dmg` (macOS)
     * `DocMiner-6.0-windows.zip` (Windows)

### Phase 6: Update Documentation

Update these key files:
- [ ] `README.md` - Download links, screenshots
- [ ] `docs/SETUP_GUIDE_FOR_GAS.md` - Instructions
- [ ] `docs/BUILD_MACOS.md` - Build instructions
- [ ] License files (if they mention the name)

### Phase 7: Announce the Rebrand

Consider:
- Update any external documentation
- Notify users if applicable
- Update any citations or references

## Rollback Plan

If something goes wrong:

```bash
# Restore from backup
cd ..
rm -rf research-buddy
cp -r research-buddy_backup_before_rebrand research-buddy
cd research-buddy

# OR use git
git reset --hard HEAD~1  # Undo last commit
```

## Configuration Directories

⚠️ **User Configuration**: The config directory `~/.research_buddy/` will remain as-is for backward compatibility. This is fine - it's just a hidden directory name.

**Alternative**: Update config path in code from `~/.research_buddy/` to `~/.docminer/` but include migration logic to copy old settings.

## Testing Checklist

After rebrand, test:
- [ ] Application launches with new name
- [ ] Window titles show "DocMiner"
- [ ] About dialog shows "DocMiner"
- [ ] File uploads still work
- [ ] Configuration saves correctly
- [ ] All documentation references are updated
- [ ] Build process works for all platforms
- [ ] GitHub workflows build successfully

## Timeline Estimate

- **Preview & Review**: 15 minutes
- **Execute Script**: 5 minutes
- **Local Testing**: 30 minutes
- **Git Commit/Push**: 10 minutes
- **GitHub Rename**: 5 minutes
- **Build v6.0**: 1-2 hours (all platforms)
- **Create Release**: 30 minutes

**Total**: ~3-4 hours for complete rebrand

## Notes

- The rebrand script skips historical files (training_reports, batch_reports, archive)
- These are archival data and don't need to be changed
- Git history is preserved - all commits remain intact
- GitHub redirects old URLs automatically (for a while)

## Questions Before Starting?

Review:
1. `rebrand.py --preview` output
2. `FILE_MAPPINGS.md` for all renames
3. `PREVIEW.md` for before/after examples

Ready when you are! 🚀
