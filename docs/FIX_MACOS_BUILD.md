# 🔧 Fix macOS Build to Create .app Bundle

## Problem
The current macOS release creates a standalone Unix executable that can't be double-clicked. Users have to run it from Terminal.

## Root Cause
GitHub Actions or the build script is using `--onefile` instead of using the spec file that creates a proper `.app` bundle.

## Solution

### For Next Release (v5.1.2 or v5.2)

Update the GitHub Actions workflow or build instructions to ALWAYS use the spec file on macOS:

**In `.github/workflows/build.yml`**, change the macOS build step to:

```yaml
- name: Build executable (macOS)
  if: matrix.os == 'macos-latest'
  run: |
    python build_files/build.py macos --spec-file
```

### Immediate Fix for Current Users

Add the launcher script to existing downloads:

1. Create `Launch ResearchBuddy.command` in the distribution
2. Include `MACOS_RUN_INSTRUCTIONS.md` in the tarball
3. Update README with correct Terminal instructions

### Testing the Fix

Build locally on macOS to verify it creates a `.app`:

```bash
cd ~/research-buddy
python build_files/build.py macos --spec-file --clean
```

This should create:
- `dist/ResearchBuddy5.1.1.app/` (macOS app bundle - can be double-clicked!)

Instead of:
- `dist/ResearchBuddy5.1.1` (Unix executable - Terminal only)

### Verification Steps

After building with spec file:

```bash
# Check that .app was created
ls -la dist/
# Should see: ResearchBuddy5.1.1.app/

# Test the app
open dist/ResearchBuddy5.1.1.app

# Verify it's a proper bundle
file dist/ResearchBuddy5.1.1.app/Contents/MacOS/ResearchBuddy5.1.1
# Should show: Mach-O 64-bit executable arm64
```

### Distribution Package Structure

For next release, the macOS tarball should contain:

```
ResearchBuddy5.1.1-macos/
├── ResearchBuddy5.1.1.app/     ← The .app bundle
├── README.md
├── MACOS_RUN_INSTRUCTIONS.md   ← Just in case
└── sample_pdfs/
```

## References

- Spec file: `build_files/ResearchBuddy5.1.1.spec` (already has BUNDLE section)
- Build script: `build_files/build.py` (needs to use --spec-file for macOS)
- GitHub Actions: `.github/workflows/build.yml` (needs update)
