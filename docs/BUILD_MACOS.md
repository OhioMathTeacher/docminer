# Building DocMiner 5.2 for macOS (M1/ARM64)

## Quick Build Instructions

### 1. Clone or Update Repository
```bash
# If not already cloned:
git clone https://github.com/OhioMathTeacher/docminer.git
cd docminer

# OR if already cloned:
cd docminer
git pull origin main
```

### 2. Install Dependencies
```bash
# Install Python packages
pip3 install -r requirements.txt
pip3 install pyinstaller
```

### 3. Build the macOS Application
```bash
# Build with PyInstaller
pyinstaller build_files/DocMiner5.2.spec --clean
```

This will create: `dist/DocMiner5.2.app/`

### 4. Test the Build
```bash
# Launch the app
open dist/DocMiner5.2.app
```

Test:
- ✅ Configuration dialog appears on first launch
- ✅ Robot icon displays correctly
- ✅ Settings save to `~/.research_buddy/interface_settings.json`
- ✅ App functions normally

### 5. Package for Distribution

#### Option A: Create ZIP Archive (Simple)
```bash
cd dist
zip -r DocMiner-5.2-macOS.zip DocMiner5.2.app
```

#### Option B: Create DMG (Recommended)
```bash
# Install create-dmg if needed
brew install create-dmg

# Create DMG
create-dmg \
  --volname "DocMiner 5.2" \
  --window-pos 200 120 \
  --window-size 600 400 \
  --icon-size 100 \
  --icon "DocMiner5.2.app" 175 120 \
  --hide-extension "DocMiner5.2.app" \
  --app-drop-link 425 120 \
  "DocMiner-5.2-macOS.dmg" \
  "dist/DocMiner5.2.app"
```

### 6. Upload to GitHub Release

1. Go to: https://github.com/OhioMathTeacher/docminer/releases/tag/v5.2
2. Click "Edit release"
3. Upload: `DocMiner-5.2-macOS.dmg` (or `.zip`)
4. Click "Update release"

## Build Details

- **Architecture**: ARM64 (M1 native)
- **Compatibility**: macOS 11.0+ (Big Sur and later)
- **Intel Support**: Yes, via Rosetta 2
- **Expected Size**: ~100-150 MB (DMG/ZIP)

## Troubleshooting

### Issue: PyInstaller not found
```bash
pip3 install --upgrade pyinstaller
```

### Issue: Missing dependencies
```bash
pip3 install --upgrade -r requirements.txt
```

### Issue: Permission denied
```bash
chmod +x dist/DocMiner5.2.app/Contents/MacOS/DocMiner5.2
```

### Issue: "App is damaged" warning
```bash
# Remove quarantine flag
xattr -cr dist/DocMiner5.2.app
```

## Notes

- Build time: ~1-2 minutes on M1 Mac
- The .spec file automatically includes the robot icon
- Configuration is stored in `~/.research_buddy/` (platform-independent)
- This build includes the persistent configuration feature (v5.2+)
