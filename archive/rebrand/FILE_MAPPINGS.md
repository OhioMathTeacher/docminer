# File Rename Mappings

This document lists all files that will be renamed during the rebrand.

## Python Files

| Old Name | New Name |
|----------|----------|
| `run_research_buddy.py` | `run_docminer.py` |
| `launch_research_buddy.py` | `launch_docminer.py` |

## Shell Scripts

| Old Name | New Name |
|----------|----------|
| `start_research_buddy.sh` | `start_docminer.sh` |

**Note**: The following scripts keep their current names:
- `test_config.sh` (generic name)
- `simulate_fresh_user.sh` (generic name)

## Build Specification Files

| Old Name | New Name |
|----------|----------|
| `ResearchBuddy.spec` | `DocMiner.spec` |
| `build_files/ResearchBuddy3.1.2.spec` | `build_files/DocMiner3.1.2.spec` |
| `build_files/ResearchBuddy4.0.spec` | `build_files/DocMiner4.0.spec` |
| `build_files/ResearchBuddy4.1.spec` | `build_files/DocMiner4.1.spec` |
| `build_files/ResearchBuddy4.2.spec` | `build_files/DocMiner4.2.spec` |
| `build_files/ResearchBuddy5.0.spec` | `build_files/DocMiner5.0.spec` |
| `build_files/ResearchBuddy5.2.spec` | `build_files/DocMiner5.2.spec` |

## Files NOT Renamed

These files keep their current names but will have text updated inside:

- `enhanced_training_interface.py` (main application)
- `configuration_dialog.py` (configuration UI)
- `github_report_uploader.py` (upload functionality)
- All documentation files (`.md`)
- All workflow files (`.yml`)
- All shell scripts in `build_files/`

## Directories NOT Renamed

- `training_reports/` (historical data)
- `batch_reports/` (historical data)
- `archive/` (historical versions)
- `.git/` (version control)
- All build output directories (`dist/`, `build/`, `AppDir/`)

## User Configuration

Current location: `~/.research_buddy/`

**Options:**
1. **Keep as-is** (backward compatible, just a hidden directory name)
2. **Migrate**: Add code to copy `~/.research_buddy/` → `~/.docminer/` on first launch

**Recommendation**: Keep as `~/.research_buddy/` for backward compatibility. It's hidden anyway.

## Generated Files (After Build)

These will be automatically named correctly after running the rebrand:

### Linux
- `dist/DocMiner5.2/` → `dist/DocMiner6.0/`
- `DocMiner-5.2-x86_64.AppImage` → `DocMiner-6.0-x86_64.AppImage`

### macOS
- `dist/DocMiner5.2.app/` → `dist/DocMiner6.0.app/`
- `DocMiner-5.2-macOS.dmg` → `DocMiner-6.0-macOS.dmg`

### Windows
- `dist/DocMiner5.2/DocMiner5.2.exe` → `dist/DocMiner6.0/DocMiner6.0.exe`
- `DocMiner-5.2-windows.zip` → `DocMiner-6.0-windows.zip`

## Icon Files

No renames needed:
- `build_files/robot_icon_256x256.png` (generic name)
- `build_files/app_icon_*.ico` (generic names)

These are referenced by path, not by name pattern matching.

## Desktop/Config Files

Text will be updated inside these files:

- `AppDir/ResearchBuddy.desktop` → Content updated to reference DocMiner
- `releases/ResearchBuddy-5.1.1.desktop` → Archive file, no change
- `interface_settings.json` → Template file, text updated

## GitHub-Specific

### Repository
- URL: `https://github.com/OhioMathTeacher/research-buddy`
- **New**: `https://github.com/OhioMathTeacher/docminer`

### Workflows
Files updated (not renamed):
- `.github/workflows/build.yml`
- `.github/workflows/build-executables.yml`
- `.github/workflows/manual-build.yml`

Content references to "ResearchBuddy" → "DocMiner"

## Total File Count

**Files to be renamed**: ~10-12  
**Files with text updated**: ~200+  
**Files skipped** (historical): ~50+

## Verification Commands

After rebrand, verify renames:

```bash
# Check for any remaining old references
grep -r "ResearchBuddy" --exclude-dir={rebrand,archive,training_reports,batch_reports,.git,__pycache__}

# Check for old script names
ls -la *.sh | grep research_buddy

# Check build specs
ls -la build_files/*.spec | grep ResearchBuddy
```

Expected result: No matches (except in excluded directories)
