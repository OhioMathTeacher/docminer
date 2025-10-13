# GitHub Actions Token Troubleshooting

## Current Configuration (After Multiple Attempts)

### Permissions Setup
```yaml
# Top-level (workflow)
permissions:
  contents: write
  actions: read
  packages: read

# Job-level (create-release)
create-release:
  permissions:
    contents: write
```

### Token Usage
**Currently:** No explicit token parameter - using default GITHUB_TOKEN

The action will automatically use the default `GITHUB_TOKEN` with the permissions we've granted.

## Why This Should Work

1. **Job has explicit write permission** - `permissions: contents: write` on the job
2. **No custom token conflicts** - Letting GitHub Actions handle it automatically
3. **Tag verification step** - Ensures v5.1.1 tag exists before release creation
4. **Checkout with token** - Has permission to push tags if needed

## What We've Tried

1. ❌ `secrets.GITHUB_TOKEN` - Not the right way to access it
2. ❌ `github.token` - Still gave permission errors  
3. ❌ Explicit token parameter with env block - Caused conflicts
4. ✅ **Default behavior with explicit job permissions** - Current approach

## If This Still Fails

### Option 1: Use a Personal Access Token (PAT)
1. Generate PAT with `repo` scope
2. Add as repository secret: `PERSONAL_ACCESS_TOKEN`
3. Update workflow:
```yaml
- name: Create or Update Release
  uses: softprops/action-gh-release@v2
  with:
    token: ${{ secrets.PERSONAL_ACCESS_TOKEN }}
    tag_name: v5.1.1
    # ... rest of config
```

### Option 2: Use GitHub CLI Instead
```yaml
- name: Create Release with gh CLI
  env:
    GH_TOKEN: ${{ github.token }}
  run: |
    gh release create v5.1.1 \
      --title "DocMiner 5.1.1" \
      --notes-file release-notes.md \
      release-files/*
```

### Option 3: Check Repository Settings
Go to: Settings → Actions → General → Workflow permissions
Ensure: **"Read and write permissions"** is selected

## Current Status

**Commit:** d3e022d  
**Approach:** Default GITHUB_TOKEN with explicit job permissions  
**Next Test:** Trigger workflow and see if it works

---

If this attempt fails, we'll need to use a PAT or GitHub CLI approach.
