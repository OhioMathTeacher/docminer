# DocMiner - Quick Setup Guide for Graduate Assistants

## One-Time Setup (15 minutes)

### Step 1: Download DocMiner
- Download the appropriate version for your OS from the releases page
- macOS: `.dmg` file → Drag to Applications
- Windows: `.zip` file → Extract and run `.exe`
- Linux: `.AppImage` file → Make executable and run

### Step 2: Get Your Tokens
Your supervisor will provide you with two tokens. Keep them secure!

1. **OpenAI API Key** - starts with `sk-...`
2. **GitHub Token** - starts with `ghp_...`

### Step 3: Set Up Environment Variables

**macOS/Linux:**
1. Open Terminal
2. Run: `nano ~/.bashrc` (or `nano ~/.zshrc` on macOS)
3. Add these lines at the bottom (paste your actual tokens):
   ```bash
   # DocMiner Configuration
   export RESEARCH_BUDDY_OPENAI_API_KEY="sk-your-key-here"
   export RESEARCH_BUDDY_GITHUB_TOKEN="ghp-your-token-here"
   ```
4. Save: Press `Ctrl+O`, `Enter`, then `Ctrl+X`
5. Reload: `source ~/.bashrc` (or `source ~/.zshrc`)

**Windows:**
1. Search "Environment Variables" in Start Menu
2. Click "Edit system environment variables"
3. Click "Environment Variables" button
4. Under "User variables", click "New" for each:
   - Name: `RESEARCH_BUDDY_OPENAI_API_KEY` → Value: your OpenAI key
   - Name: `RESEARCH_BUDDY_GITHUB_TOKEN` → Value: your GitHub token
5. Click OK to save

### Step 4: First Launch Configuration

When you first run DocMiner, you'll see a dialog asking for:
- **Owner**: `OhioMathTeacher`
- **Repository**: `docminer`

Enter these exactly as shown, click OK. You'll only see this once!

---

## Daily Usage

### Starting DocMiner

**macOS/Linux (from source):**
```bash
cd ~/docminer
./start_research_buddy.sh
```

**Windows/Executables:**
- Just double-click the app icon!

### Your Workflow

1. **Enter your name** in the GA Name field (top of window)
2. **Load PDFs** from your assigned folder
3. **Review papers** and mark evidence
4. **Upload reports** to GitHub when done

---

## Troubleshooting

### "GitHub token not found" error
- Your environment variables aren't set correctly
- Re-check Step 3 above
- Make sure you ran `source ~/.bashrc` after editing

### "GitHub Repository Not Configured" dialog
- Enter: Owner = `OhioMathTeacher`, Repository = `docminer`
- This only happens once

### App prompts for credentials every time
- You're using `launch_research_buddy.py` instead of `run_research_buddy.py`
- Use the `start_research_buddy.sh` script instead

---

## Security Reminders

- ✅ Environment variables keep your tokens secure
- ✅ Never share your tokens via email or chat
- ✅ Never commit tokens to git repositories
- ⚠️ If you accidentally expose a token, tell your supervisor immediately so they can revoke and regenerate it

---

## Questions?

Contact your research supervisor or check the main README.md file.
