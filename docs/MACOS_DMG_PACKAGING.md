# 🍎 macOS Professional Packaging with DMG

## Why DMG is the Gold Standard for macOS Apps

### Current Problems:
- ❌ Malware warnings on every file
- ❌ Users have to extract tar.gz manually
- ❌ Files scattered in Downloads folder
- ❌ Looks unprofessional
- ❌ Terminal scripts are clunky

### What a .dmg provides:
- ✅ **Professional appearance** - looks like a real Mac app
- ✅ **Drag-to-install** - users drag app to Applications folder
- ✅ **Code signing support** - can be notarized to eliminate warnings
- ✅ **Custom background** - can include instructions/branding
- ✅ **Single file** - just download and double-click
- ✅ **Auto-mounting** - no extraction needed

## Implementation Plan

### 1. First: Fix the .app Bundle (Required for DMG)

The spec file already creates `ResearchBuddy5.1.1.app`, but GitHub Actions isn't packaging it correctly.

**Test locally:**
```bash
cd ~/research-buddy
python -m PyInstaller build_files/ResearchBuddy5.1.1.spec --clean --noconfirm
ls -la dist/
# Should see: ResearchBuddy5.1.1.app/
```

### 2. Create DMG with create-dmg Tool

Install the tool:
```bash
brew install create-dmg
```

Create the DMG:
```bash
create-dmg \
  --volname "ResearchBuddy 5.1.1" \
  --volicon "app-icon.icns" \
  --window-pos 200 120 \
  --window-size 800 400 \
  --icon-size 100 \
  --icon "ResearchBuddy5.1.1.app" 200 190 \
  --hide-extension "ResearchBuddy5.1.1.app" \
  --app-drop-link 600 185 \
  "ResearchBuddy-5.1.1.dmg" \
  "dist/ResearchBuddy5.1.1.app"
```

### 3. Alternative: Simple DMG Creation

Without extra tools, using hdiutil:
```bash
#!/bin/bash
# Create a DMG for ResearchBuddy

# Create a temporary directory
mkdir -p dmg-temp
cp -R dist/ResearchBuddy5.1.1.app dmg-temp/
cp README.md dmg-temp/
ln -s /Applications dmg-temp/Applications

# Create the DMG
hdiutil create -volname "ResearchBuddy 5.1.1" \
  -srcfolder dmg-temp \
  -ov -format UDZO \
  ResearchBuddy-5.1.1.dmg

# Clean up
rm -rf dmg-temp

echo "✅ Created ResearchBuddy-5.1.1.dmg"
```

### 4. Add to Build Script

Update `build_files/build.py` to create DMG on macOS:

```python
def create_dmg_package(app_path, version):
    """Create a macOS DMG package"""
    import subprocess
    
    dmg_name = f"ResearchBuddy-{version}.dmg"
    
    # Create temp directory
    temp_dir = Path("dmg-temp")
    temp_dir.mkdir(exist_ok=True)
    
    # Copy app bundle
    shutil.copytree(app_path, temp_dir / app_path.name)
    
    # Create Applications symlink
    (temp_dir / "Applications").symlink_to("/Applications")
    
    # Create DMG
    subprocess.run([
        "hdiutil", "create",
        "-volname", f"ResearchBuddy {version}",
        "-srcfolder", str(temp_dir),
        "-ov", "-format", "UDZO",
        dmg_name
    ], check=True)
    
    # Clean up
    shutil.rmtree(temp_dir)
    
    print(f"✅ Created {dmg_name}")
```

## User Experience Comparison

### Current (tar.gz with executable):
1. Download tar.gz
2. Extract it
3. Find the file
4. Open Terminal
5. Run chmod command
6. Run executable or create .command file
7. Get malware warning
8. Right-click → Open
9. **Finally** app launches

### With DMG:
1. Download DMG
2. Double-click to mount
3. Drag app to Applications
4. Double-click app
5. **Done!** (One malware warning, then never again)

## Code Signing & Notarization (Optional but Recommended)

To **completely eliminate** the malware warning:

1. **Get an Apple Developer Account** ($99/year)
2. **Sign the app:**
   ```bash
   codesign --deep --force --verify --verbose \
     --sign "Developer ID Application: Your Name" \
     ResearchBuddy5.1.1.app
   ```
3. **Notarize with Apple:**
   ```bash
   xcrun notarytool submit ResearchBuddy-5.1.1.dmg \
     --apple-id your@email.com \
     --password app-specific-password \
     --team-id TEAMID
   ```
4. **Staple the notarization:**
   ```bash
   xcrun stapler staple ResearchBuddy-5.1.1.dmg
   ```

## Implementation Steps

### Immediate (No cost):
1. ✅ Fix GitHub Actions to package the .app bundle (already done in our changes)
2. ✅ Add DMG creation to build script
3. ✅ Test locally
4. ✅ Update release workflow

### Future (With budget):
1. Get Apple Developer account
2. Add code signing to build process
3. Add notarization to release workflow
4. **Zero warnings** for users!

## Example GitHub Actions Update

```yaml
- name: Create macOS DMG
  if: matrix.os == 'macos-latest'
  run: |
    # Create DMG from .app bundle
    mkdir -p dmg-temp
    cp -R dist/ResearchBuddy5.1.1.app dmg-temp/
    ln -s /Applications dmg-temp/Applications
    
    hdiutil create -volname "ResearchBuddy 5.1.1" \
      -srcfolder dmg-temp \
      -ov -format UDZO \
      releases/ResearchBuddy-5.1.1.dmg
    
    rm -rf dmg-temp
```

## Benefits Summary

| Feature | Current .tar.gz | With .dmg | With Signed .dmg |
|---------|----------------|-----------|------------------|
| Professional look | ❌ | ✅ | ✅ |
| Easy installation | ❌ | ✅ | ✅ |
| No Terminal needed | ❌ | ✅ | ✅ |
| Malware warnings | Many | One | None |
| Auto-updates | ❌ | ❌ | ✅ (with Sparkle) |
| Cost | Free | Free | $99/year |

## Next Steps

1. **Test the .app build locally** (to verify it works)
2. **Create DMG creation script**
3. **Update GitHub Actions** to create DMG
4. **Test DMG on clean Mac**
5. **Release v5.1.2** with DMG
6. **Consider code signing** for future releases

