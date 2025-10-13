# macOS Universal Binary Support - CRITICAL FIX

## Problem Identified (Oct 8, 2025)

The current macOS builds **ONLY work on Apple Silicon Macs (M1/M2/M3)**, not Intel Macs!

This is because:
1. GitHub Actions `macos-latest` uses Apple Silicon runners
2. PyInstaller was set to `target_arch=None` (builds only for current architecture)

## Solution Implemented

### 1. Updated PyInstaller Spec File
Changed `build_files/DocMiner5.1.1.spec`:
```python
target_arch='universal2'  # Was: target_arch=None
```

This creates a **Universal Binary** that works on BOTH:
- Intel Macs (x86_64)
- Apple Silicon Macs (arm64)

### 2. Build Requirements

For Universal Binary builds on macOS, you need:
- Python installed via official installer (not Homebrew) - supports both architectures
- OR: Build separately on Intel and Apple Silicon, then use `lipo` to combine

### 3. GitHub Actions Considerations

**Current situation:**
- `macos-latest` = Apple Silicon runner
- With `target_arch='universal2'`, PyInstaller will create Universal Binary IF Python supports it

**Verification needed:**
- Check if GitHub's Python installation supports Universal Binaries
- May need to use `macos-13` (Intel) + `macos-14` (Apple Silicon) and combine

### 4. Testing

To verify Universal Binary:
```bash
# Check architecture support
file dist/DocMiner5.1.1.app/Contents/MacOS/DocMiner5.1.1

# Should show: Mach-O universal binary with 2 architectures
# Or: Mach-O 64-bit executable x86_64 and arm64
```

### 5. Alternative: Build for Both Architectures Separately

If Universal Binary doesn't work, we can:
1. Build on Intel Mac → `DocMiner-5.1.1-intel.dmg`
2. Build on Apple Silicon → `DocMiner-5.1.1-apple-silicon.dmg`
3. Let users download the right version

## Action Required

1. **Test the build** with new `target_arch='universal2'` setting
2. **Verify** the .app works on both Intel and Apple Silicon Macs
3. **If it fails**, implement dual-architecture build strategy

## References

- PyInstaller Universal Binary docs: https://pyinstaller.org/en/stable/feature-notes.html#macos-multi-arch-support
- GitHub Actions macOS runners: https://github.com/actions/runner-images

---

**Status:** Fixed in spec file, needs testing  
**Priority:** HIGH - Half of macOS users might be on Intel!
