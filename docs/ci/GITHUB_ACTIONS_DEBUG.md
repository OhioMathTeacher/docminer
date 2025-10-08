# GitHub Actions Release Issues - Debugging

## Issue Timeline (Oct 8, 2025)

### Error 1: Pattern Matching Failed
```
Pattern 'artifacts/**/*.dmg' does not match any files
Pattern 'artifacts/**/*.AppImage' does not match any files
```

**Cause:** Artifacts downloaded into subdirectories, glob pattern couldn't find them

**Fix:** Added flattening step to copy all files into `release-files/` directory

### Error 2: Resource Not Accessible
```
Error: Resource not accessible by integration
```

**Cause:** Missing or duplicate GITHUB_TOKEN environment variable

**Fixes Applied:**
1. ✅ Added `permissions: contents: write` at top level (was already there)
2. ✅ Added explicit `env: GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}` to release step
3. ✅ Removed duplicate `env` block at end of file
4. ✅ Added `fail_on_unmatched_files: true` to catch issues early

## Current Workflow Structure

```yaml
permissions:
  contents: write  # Allow creating releases

jobs:
  build:
    # Builds for each platform
    # Uploads artifacts to releases/ directory
  
  create-release:
    needs: build
    steps:
      - Download artifacts
      - Flatten structure (copy to release-files/)
      - Create release with GITHUB_TOKEN
```

## What Should Happen

1. **Build job** creates platform-specific files:
   - macOS: `releases/ResearchBuddy-5.1.1.dmg`
   - Windows: `releases/ResearchBuddy-5.1.1-windows.zip`
   - Linux: `releases/ResearchBuddy-5.1.1-linux.tar.gz` + `releases/ResearchBuddy-5.1.1-x86_64.AppImage`

2. **Upload artifacts** to GitHub (each in its own subdirectory)

3. **Download artifacts** to `artifacts/` (creates subdirectories like `artifacts/ResearchBuddy-5.1.1-macos/`)

4. **Flatten** structure by copying all files to `release-files/`

5. **Create release** using files from `release-files/*`

## Next Test

Trigger the workflow again and check:
- [ ] Do all platforms build successfully?
- [ ] Does the flatten step find all files?
- [ ] Does the release get created?
- [ ] Are all 4 files (DMG, AppImage, ZIP, tar.gz) uploaded?

## If It Still Fails

Check the "Display and flatten artifacts" step output to see:
1. What's actually in `artifacts/` directory?
2. What gets copied to `release-files/`?
3. Are the file names exactly what we expect?

---

**Status:** Fixed (hopefully!) - Commit 3ee86cb  
**Next:** Trigger workflow and watch for success
