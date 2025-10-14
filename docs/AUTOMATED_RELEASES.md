# Automated Build & Release Process

## 🎯 How It Works

**You only need to push a version tag** - everything else is automatic!

```bash
# 1. Make your changes and commit them
git add .
git commit -m "Add awesome new feature"
git push origin main

# 2. Create and push a version tag
git tag v6.4.0
git push origin v6.4.0

# 3. Done! The build happens automatically
```

## 🤖 What Happens Automatically

1. **GitHub Actions detects the tag** (e.g., `v6.4.0`)
2. **Generates spec file** from template (`DocMiner.spec.template`)
   - Replaces `{{VERSION}}` with `6.4.0`
   - Replaces `{{VERSION_SHORT}}` with `6.4`
   - Creates `DocMiner6.4.spec` on-the-fly
3. **Builds on 3 platforms** (Linux, Windows, macOS)
4. **Creates GitHub Release** with all artifacts
5. **Uploads installers**:
   - `DocMiner-6.4.0-Linux.tar.gz` + AppImage
   - `DocMiner-6.4.0-Windows.zip`
   - `DocMiner-6.4.0-macOS.dmg`

## 📝 The Template System

### Before (Manual - Required a spec file for each version)
```
build_files/
  ├── DocMiner6.1.spec   ❌ Manual copy
  ├── DocMiner6.2.spec   ❌ Manual copy
  ├── DocMiner6.3.spec   ❌ Manual copy
  └── DocMiner6.4.spec   ❌ Manual copy
```

### After (Automated - One template for all versions)
```
build_files/
  └── DocMiner.spec.template   ✅ Auto-generates all versions
```

The workflow automatically replaces placeholders:
- `{{VERSION}}` → `6.4.0` (full version)
- `{{VERSION_SHORT}}` → `6.4` (major.minor)

## 🚀 Release Workflow

### Standard Release (Patch/Minor)
```bash
# Current version: v6.3.0
git tag v6.3.1          # Patch release
git push origin v6.3.1
# → Builds DocMiner6.3.spec automatically
```

### Major Release
```bash
# Current version: v6.3.0
git tag v7.0.0          # Major release
git push origin v7.0.0
# → Builds DocMiner7.0.spec automatically
```

## 📋 Version Tag Format

The workflow accepts any semantic version tag:

- ✅ `v6.3.0` → Creates `DocMiner6.3.spec`
- ✅ `v6.3.1` → Creates `DocMiner6.3.spec` (same major.minor)
- ✅ `v7.0.0` → Creates `DocMiner7.0.spec`
- ✅ `v7.1.2` → Creates `DocMiner7.1.spec`
- ❌ `6.3.0` (missing 'v' prefix - won't trigger)
- ❌ `release-6.3` (wrong format - won't trigger)

## 🔧 Customizing the Template

To change build settings for **all future versions**, edit:
```
build_files/DocMiner.spec.template
```

Changes you might make:
- Add/remove included files (datas)
- Add/remove excluded libraries
- Change icon or bundle settings
- Modify compiler options

**No need to update individual spec files anymore!**

## 🐛 Troubleshooting

### Build failed immediately
- Check that the tag follows format `v*.*.*`
- Verify `DocMiner.spec.template` exists and is valid

### Build succeeded but artifacts are missing
- Check GitHub Actions logs: https://github.com/OhioMathTeacher/docminer/actions
- Look for errors in platform-specific build steps

### Want to rebuild the same version
```bash
# Delete tag locally and remotely
git tag -d v6.3.0
git push origin :refs/tags/v6.3.0

# Create fresh tag and push
git tag v6.3.0
git push origin v6.3.0
```

## 📚 Quick Reference

| Command | What It Does |
|---------|-------------|
| `git tag v6.4.0` | Create version tag locally |
| `git push origin v6.4.0` | Push tag → triggers build |
| `git tag -l` | List all tags |
| `git tag -d v6.4.0` | Delete local tag |
| `git push origin :refs/tags/v6.4.0` | Delete remote tag |

## 🎉 Benefits

✅ **Zero manual spec file management**  
✅ **Consistent builds across all versions**  
✅ **One source of truth** (the template)  
✅ **Fast releases** (just push a tag)  
✅ **Easy to update** build settings globally  
✅ **No more "forgot to update version number" bugs**
