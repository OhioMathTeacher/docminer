# DocMiner Rebrand Kit

This directory contains everything needed to rebrand "Research Buddy" to "DocMiner".

## Why DocMiner?

The name "ResearchBuddy" is already taken. "DocMiner" better reflects the tool's purpose:
- **Doc** = Document analysis
- **Miner** = Extracting valuable insights from academic papers

## What's In This Kit

1. **`rebrand.py`** - Automated rebrand script (recommended)
2. **`REBRAND_PLAN.md`** - Detailed execution plan
3. **`FILE_MAPPINGS.md`** - List of all files that will be renamed
4. **`PREVIEW.md`** - Before/after examples

## Quick Start

### Option 1: Automated (Recommended)

```bash
cd rebrand
python3 rebrand.py --preview  # See what will change
python3 rebrand.py --execute  # Do the rebrand
```

### Option 2: Manual

Follow the step-by-step guide in `REBRAND_PLAN.md`

## What Gets Changed

### Text Replacements
- "Research Buddy" → "DocMiner"
- "ResearchBuddy" → "DocMiner" 
- "research-buddy" → "docminer"
- "researchbuddy" → "docminer"

### File Renames
- `build_files/ResearchBuddy5.2.spec` → `build_files/DocMiner5.2.spec`
- `start_research_buddy.sh` → `start_docminer.sh`
- And many more (see `FILE_MAPPINGS.md`)

### What Doesn't Change
- Historical training reports (archival data)
- Archive directory (historical versions)
- Git commit history

## Timeline Recommendation

**Before Rebrand:**
1. ✅ Upload new Linux AppImage (134MB)
2. ✅ Build macOS version
3. ✅ Build Windows version
4. ✅ Complete v5.2 release

**After Rebrand:**
1. Run rebrand script
2. Test locally
3. Push to GitHub
4. Rename repo on GitHub
5. Create v6.0 "DocMiner" release

## Safety

- The script creates a backup before making changes
- Preview mode shows all changes without applying them
- Git allows easy rollback if needed
- You can review every change before committing

## Questions?

Read `REBRAND_PLAN.md` for detailed information about the rebrand process.
