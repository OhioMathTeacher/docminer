# Quick Reference - Building DocMiner Executables

## On Your Linux Machine at Home:

### 1. Pull Latest Changes
```bash
cd docminer  # or clone if needed
git pull
```

### 2. Build Linux Executable (Fast Option)
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install pyinstaller
python -m PyInstaller build_files/DocMiner5.1.1.spec --distpath ./dist --workpath ./build --clean --noconfirm
cd dist && tar -czf ../DocMiner-5.1.1-linux.tar.gz DocMiner5.1.1
```

### 3. OR Use GitHub Actions (Builds All 3 Platforms)
- Go to: https://github.com/OhioMathTeacher/docminer/actions
- Click "Manual Build All Platforms"
- Click "Run workflow"
- Wait 10-15 min
- Download artifacts

### 4. Create Release
- Go to: https://github.com/OhioMathTeacher/docminer/releases
- "Draft new release"
- Tag: v5.1.1
- Upload the 3 executables
- Publish

## Files Your GAs Need:
- ✅ DocMiner-5.1.1-macos.zip
- ⏳ DocMiner-5.1.1-windows.zip
- ⏳ DocMiner-5.1.1-linux.tar.gz

## Emergency GA Solution:
Point them to GitHub Codespaces (already in README) - works immediately!

See NEXT_STEPS_LINUX.md for full details.
