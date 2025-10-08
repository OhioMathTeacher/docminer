# Research Buddy Build Guide

This guide explains how to build Research Buddy executables for different platforms.

## Prerequisites

- Python 3.11 or higher
- All dependencies from `requirements.txt` installed
- PyInstaller 6.13.0 or higher

## Architecture Support

### macOS Builds

We provide **two separate macOS builds**:

1. **Apple Silicon (ARM64)** - `ResearchBuddy-5.1.1.dmg`
   - Native ARM64 build for M1/M2/M3 Macs
   - Build script: `./build_local.sh`
   - Best performance on Apple Silicon

2. **Intel (x86_64)** - `ResearchBuddy-5.1.1-macos-intel.dmg`
   - Native x86_64 build for Intel Macs
   - Build script: `./build_intel_macos.sh`
   - Required for older Intel Macs

**Note**: We use separate native builds instead of Universal2 binaries because some dependencies (like `pydantic_core`) don't support fat binaries.

## Building Locally

### Apple Silicon (ARM64) Build

```bash
# Install dependencies
pip3 install -r requirements.txt

# Build the DMG
./build_local.sh

# Output: releases/ResearchBuddy-5.1.1.dmg
```

### Intel (x86_64) Build

```bash
# Install dependencies (must be on Intel Mac or use Rosetta)
pip3 install -r requirements.txt

# Build the DMG
./build_intel_macos.sh

# Output: releases-intel/ResearchBuddy-5.1.1-macos-intel.dmg
```

## GitHub Actions Builds

The `.github/workflows/build-executables.yml` workflow automatically builds:
- macOS (Apple Silicon) DMG
- Windows executable
- Linux executable

Triggered by:
- Pushing a tag like `v5.1.1`
- Manual workflow dispatch

## Key Build Configuration

### Spec File: `build_files/ResearchBuddy5.1.1.spec`

Critical settings:
- `target_arch=None` - Builds for native architecture
- **Excludes QtWebEngine modules** to avoid corrupted universal binary issues
- Includes all required dependencies via `hiddenimports`

### Required Dependencies

Must be installed before building:
- `pdfplumber` - PDF text extraction
- `PySide6` - GUI framework
- `PyMuPDF` (fitz) - PDF rendering
- `openai` - API integration
- All others in `requirements.txt`

### Code Changes for Intel Compatibility

The following fix in `enhanced_training_interface.py` makes QtWebEngine optional:

```python
try:
    from PySide6.QtWebEngineWidgets import QWebEngineView
    HAS_WEBENGINE = True
except ImportError:
    QWebEngineView = None
    HAS_WEBENGINE = False
```

This allows the app to run even when QtWebEngine is excluded from the build.

## Troubleshooting

### Build Fails with "Module not found"

Make sure all dependencies are installed:
```bash
pip3 install -r requirements.txt
pip3 list | grep pdfplumber  # Should show version
```

### App Crashes on Launch

Check the architecture:
```bash
file dist/ResearchBuddy5.1.1.app/Contents/MacOS/ResearchBuddy5.1.1
```

Should show either:
- `Mach-O 64-bit executable arm64` (Apple Silicon)
- `Mach-O 64-bit executable x86_64` (Intel)

### Gatekeeper Blocks Downloaded App

On first launch:
1. Right-click the .app
2. Select "Open"
3. Click "Open" in the dialog

Or use Terminal:
```bash
open /path/to/ResearchBuddy-5.1.1.dmg
# Then double-click the app in the mounted volume
```

## Uploading Releases

Using GitHub CLI:
```bash
# Upload Apple Silicon version
gh release upload v5.1.1 releases/ResearchBuddy-5.1.1.dmg --clobber

# Upload Intel version
gh release upload v5.1.1 releases-intel/ResearchBuddy-5.1.1-macos-intel.dmg --clobber
```

## Version Updates

When updating version number:
1. Update version in spec file name and paths
2. Update `build_local.sh` script
3. Update `build_intel_macos.sh` script
4. Update README.md download links
5. Create new Git tag: `git tag v5.1.2 && git push origin v5.1.2`
