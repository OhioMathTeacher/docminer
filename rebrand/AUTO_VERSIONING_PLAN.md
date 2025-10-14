# Auto-Versioning and Release Strategy for DocMiner

This document explains the automated versioning and release system for DocMiner.

## Semantic Versioning (SemVer)

DocMiner uses **semantic versioning**: `MAJOR.MINOR.PATCH`

Example: `6.2.15`
- **6** = Major version (breaking changes, rebrands)
- **2** = Minor version (new features)
- **15** = Patch version (bug fixes, builds)

## Auto-Increment Strategy

### Automatic (Patch Bumps)
Every push to `main` branch:
1. Detects latest version (e.g., v6.2.14)
2. Auto-increments patch: v6.2.14 → v6.2.15
3. Creates GitHub release v6.2.15
4. Builds all platforms (Linux, macOS, Windows)
5. Uploads executables to the release
6. Marks as "Latest Release"

### Manual (Minor/Major Bumps)
When YOU want a significant version:

**New feature** (minor bump):
```bash
git tag v6.3.0
git push origin v6.3.0
```
→ Creates v6.3.0 release, next auto will be v6.3.1

**Major change** (major bump):
```bash
git tag v7.0.0
git push origin v7.0.0
```
→ Creates v7.0.0 release, next auto will be v7.0.1

## Workflow Behavior

### Scenario 1: Normal Development
```
You push code fix → v6.2.15 created (auto)
You push another fix → v6.2.16 created (auto)
You push enhancement → v6.2.17 created (auto)
```

### Scenario 2: New Feature Release
```
You tag v6.3.0 → v6.3.0 created (manual)
You push bug fix → v6.3.1 created (auto)
You push another fix → v6.3.2 created (auto)
```

### Scenario 3: Major Release
```
You tag v7.0.0 (DocMiner 2.0!) → v7.0.0 created (manual)
You push fix → v7.0.1 created (auto)
You push fix → v7.0.2 created (auto)
```

## Release Contents

Each release automatically includes:
- 📦 **DocMiner-{version}-x86_64.AppImage** (Linux)
- 🍎 **DocMiner-{version}-macOS.dmg** (macOS Intel + ARM)
- 🪟 **DocMiner-{version}-windows.zip** (Windows)
- 📝 Auto-generated release notes
- 📋 Installation instructions

## Advantages

✅ **Always up-to-date**: Latest release = latest code  
✅ **No manual work**: Push → build → release automatically  
✅ **Version control**: Every change gets a version number  
✅ **Rollback easy**: Download any previous version  
✅ **Professional**: Users always get versioned downloads  

## Configuration Options

You can configure in the workflow:

### Option A: Every Push (Most Automated)
- Every push to `main` → new release
- Pros: Always latest, zero manual work
- Cons: Many releases (could be 10+ per day during active dev)

### Option B: Manual Trigger + Auto-Version (Recommended)
- You trigger workflow when ready
- It auto-increments and releases
- Pros: Control over when releases happen
- Cons: Need to remember to trigger

### Option C: On Tag Only (Most Conservative)
- Only creates release when you push a tag
- Pros: Full manual control
- Cons: No automation benefit

**Recommendation for DocMiner**: Start with **Option B** (manual trigger with auto-version), can always switch to Option A later.

## GitHub Free vs Paid

### Free Account (What You Have)
- ✅ Unlimited public repos
- ✅ 2,000 Actions minutes/month
- ✅ 500 MB package storage
- ✅ Unlimited releases
- ⚠️ Queue times during peak hours

### GitHub Pro ($4/month)
- ✅ 3,000 Actions minutes/month (+50%)
- ✅ 2 GB package storage
- ✅ **Priority job queue** (faster builds!)
- ✅ Advanced code insights
- Not essential for your use case

### GitHub Team ($4/user/month)
- For organizations with multiple developers
- Not needed for solo project

### GitHub Actions Self-Hosted Runner (Free)
- Run builds on your own hardware
- Unlimited minutes
- Faster than GitHub's runners
- Requires server/VM to stay online

## Our Recommendation

**Stick with GitHub Free** for now because:
- ✅ 2,000 minutes/month is plenty (each build ~10 min = 200 builds/month)
- ✅ You can build Linux locally (AppImage script)
- ✅ You can build macOS locally (M1 Mac downstairs)
- ✅ Only need GitHub for Windows builds
- ✅ Auto-versioning works the same on free tier

**Consider paid IF**:
- ⚠️ Queue times consistently >30 minutes
- ⚠️ You exceed 2,000 minutes/month
- ⚠️ You want priority support

## Implementation Timeline

After rebrand to DocMiner:
1. ✅ Enable auto-versioning workflow
2. ✅ Set initial version to v6.0.0 (rebrand)
3. ✅ Test with a few pushes (v6.0.1, v6.0.2, etc.)
4. ✅ Adjust trigger (auto vs manual) based on preference
5. ✅ Enjoy automated releases! 🎉

## Example User Experience

**Before** (manual):
- User downloads "ResearchBuddy 5.2"
- No idea if it's latest
- No version history

**After** (auto):
- User sees "DocMiner v6.2.15 (released 2 hours ago)"
- Knows it's latest
- Can browse 50+ previous versions
- Each version has changelog

Much more professional! 🚀
