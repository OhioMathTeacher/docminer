# Build Size Optimization for DocMiner

## Problem
ResearchBuddy 5.2 macOS DMG = **1.1 GB**  
ResearchBuddy 5.2 Linux AppImage = **134 MB**

**8x size difference!** 

## Root Cause

PyInstaller auto-detects and bundles libraries that aren't actually used:
- ❌ torch (PyTorch) - ~500 MB
- ❌ transformers - ~200 MB  
- ❌ scipy - ~100 MB
- ❌ pandas - ~50 MB
- ❌ matplotlib - ~50 MB
- ❌ numpy - ~30 MB
- ❌ sympy, numba, PIL, cv2, etc. - ~100+ MB combined

**These are NOT in requirements.txt and NOT used by the app!**

## What DocMiner Actually Needs

**Core Libraries (REQUIRED):**
- ✅ PySide6 - GUI framework (~50 MB)
- ✅ PyMuPDF (fitz) - PDF rendering (~20 MB)
- ✅ openai - API client (~5 MB)
- ✅ requests/httpx - HTTP (~5 MB)
- ✅ PyPDF2/pdfplumber - PDF parsing (~3 MB)
- ✅ tabulate - Formatting (~1 MB)

**Total needed**: ~80-100 MB

## Solution: Aggressive Exclusions

Created `DocMiner6.0-optimized.spec` with:
```python
excludes=[
    # ML frameworks (500+ MB saved)
    'torch', 'torchvision', 'torchaudio', 'transformers', 
    'tensorflow', 'keras',
    
    # Scientific computing (150+ MB saved)
    'numpy', 'scipy', 'pandas', 'matplotlib', 'sympy',
    'numba', 'llvmlite',
    
    # Image processing (100+ MB saved)
    'PIL', 'Pillow', 'skimage', 'cv2', 'imageio',
    
    # Other bloat (50+ MB saved)
    'pyarrow', 'lxml', 'cryptography', 'sqlite3',
    'tkinter', 'IPython', 'jupyter',
]
```

## Expected Results

**Optimized DocMiner 6.0 macOS:**
- Target size: **150-200 MB** (down from 1.1 GB)
- DMG compression should get it to **~100-130 MB**
- Comparable to AppImage size

**Size breakdown:**
- PySide6: ~50 MB
- PyMuPDF: ~20 MB
- Python runtime: ~30 MB
- Our code + dependencies: ~20 MB
- Sample PDFs: ~10 MB
- Overhead/compression: ~20 MB
- **Total: ~150 MB** ✅

## Testing Checklist

After building with optimized spec:

- [ ] App launches successfully
- [ ] Configuration dialog works
- [ ] PDF loading and rendering works
- [ ] Text selection works
- [ ] OpenAI API calls work (AI pre-screening)
- [ ] GitHub upload works
- [ ] Export functionality works
- [ ] No missing module errors

## Build Command

```bash
cd ~/research-buddy
pyinstaller build_files/DocMiner6.0-optimized.spec --clean
```

## Why Linux AppImage is Smaller

Linux benefits from:
- ✅ Shared system libraries (glibc, libstdc++, etc.)
- ✅ Better compression in AppImage format
- ✅ Doesn't need to bundle as much infrastructure
- ✅ Python often available on system

macOS bundles everything because:
- ❌ No system Python (removed in macOS 12.3)
- ❌ No shared scientific libraries
- ❌ App must be 100% self-contained
- ❌ Framework bundles are larger

## Migration Plan

1. ✅ Create optimized spec file
2. Test build with optimized spec
3. Verify all features work
4. Compare file sizes
5. Use optimized spec for DocMiner 6.0 release

**Goal: Get macOS DMG under 200 MB!** 🎯
