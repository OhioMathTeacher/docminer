# Build Files

This directory contains all files related to building and packaging Research Buddy 5.1.

## Files:

- **build.py** - Main build script for creating executables (updated for v5.1)
- **\*.spec** - PyInstaller specification files for different versions
  - `ResearchBuddy3.1.2.spec` - Legacy version
  - `ResearchBuddy4.0.spec` - Version 4.0
  - `ResearchBuddy5.0.spec` - Previous version
  - `ResearchBuddy5.1.spec` - **Current version** (updated for tabbed dialog removal)

## Quick Build:

To build for your current platform:

```bash
cd /path/to/research-buddy
python3 -m PyInstaller build_files/ResearchBuddy5.1.spec --distpath ./dist --workpath ./build
```

Or use the build script:

```bash
cd build_files
python3 build.py linux --spec-file
```

## Cross-Platform Builds:

### Local Building:
```bash
cd build_files
python3 build.py linux      # Build for Linux
python3 build.py windows    # Build for Windows (requires Windows)
python3 build.py macos      # Build for macOS (requires macOS)
```

### GitHub Actions (Recommended):
The repository includes GitHub Actions workflow for automated cross-platform builds:

1. **Manual Trigger**: Go to Actions tab → Build Research Buddy Cross-Platform → Run workflow
2. **Tag Release**: Create a tag starting with 'v' (e.g., `v5.1.0`) to trigger automatic builds and releases

```bash
git tag v5.1.0
git push origin v5.1.0
```

## Build Output:

- **Local builds**: `dist/ResearchBuddy5.1/` directory with executable
- **GitHub builds**: Automatic releases with downloadable archives for all platforms
- **Size**: ~9MB executable with all dependencies included

## Changes in v5.1:

- ✅ Removed large tabbed dialog (`first_run_setup.py`)
- ✅ Fixed import paths for `utils.metadata_extractor`
- ✅ Preserved small individual API key dialogs
- ✅ Updated spec file to exclude removed modules
- ✅ Added GitHub Actions for cross-platform CI/CD

## Requirements:

- Python 3.10+
- PyInstaller 6.0+
- All dependencies from `requirements.txt`