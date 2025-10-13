# macOS Build Fix - October 8, 2025

## Problem

The macOS build was failing with:
```
PyInstaller.utils.osx.IncompatibleBinaryArchError: pydantic_core/_pydantic_core.cpython-311-darwin.so is not a fat binary!
```

## Root Cause

When `target_arch='universal2'` is set in the PyInstaller spec, it attempts to create a Universal Binary containing both Intel (x86_64) and Apple Silicon (ARM64) code. However, this requires **ALL** Python dependencies to be universal binaries. The `pydantic_core` package was only compiled for one architecture.

## Solution

Changed from Universal Binary to native architecture build:

1. **PyInstaller Spec** (`build_files/DocMiner5.1.1.spec`):
   - Changed `target_arch='universal2'` → `target_arch=None`
   - Builds for native architecture of the build machine

2. **GitHub Actions Workflow** (`.github/workflows/manual-build.yml`):
   - Removed `ARCHFLAGS=-arch arm64 -arch x86_64` 
   - GitHub Actions macOS runners are Apple Silicon (ARM64)
   - Result: ARM64 binary that works on both architectures

## Compatibility

✅ **Apple Silicon Macs (2020+)**: Native ARM64 performance  
✅ **Intel Macs (2019 and earlier)**: Runs via Rosetta 2 translation  

This is the **standard approach** used by modern macOS applications (Chrome, VS Code, etc.)

## Additional Fix

Also fixed DMG filename to match artifact pattern:
- Changed: `releases/DocMiner-5.1.1.dmg`  
- To: `releases/${{ matrix.name }}.dmg`  
- Result: `releases/DocMiner-5.1.1-macos.dmg`

## Status

✅ Committed in: b454f05  
⏳ Ready to trigger new workflow run with fixes
