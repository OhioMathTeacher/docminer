# Build Files

This directory contains all files related to building and packaging Research Buddy.

## Files:

- **build.py** - Main build script for creating executables
- **\*.spec** - PyInstaller specification files for different versions
  - `ResearchBuddy3.1.2.spec` - Legacy version
  - `ResearchBuddy4.0.spec` - Version 4.0
  - `ResearchBuddy5.0.spec` - Current production version

## Usage:

To build a new executable:

```bash
cd /path/to/research-buddy
python build_files/build.py
```

Or use PyInstaller directly:

```bash
pyinstaller build_files/ResearchBuddy5.0.spec
```

## Output:

Built executables are placed in the `dist/` directory (gitignored).