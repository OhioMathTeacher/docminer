# Git Sync Setup for All Computers

## Quick Setup (Copy-Paste on Each Computer)

Run this command on each computer where you work on DocMiner:

```bash
cat >> ~/.bashrc << 'EOF'

# Git sync shortcuts
alias gsync='git pull origin main && git status'
alias gpush='git pull --rebase origin main && git push origin main'
EOF

source ~/.bashrc
```

## What These Do

### `gsync` - Sync Down
```bash
gsync
```
- **When to use:** Every time you sit down to work
- **What it does:** 
  - Pulls latest changes from GitHub
  - Shows you the current status
- **Use case:** "Let me see what's new and what I'm working on"

### `gpush` - Push Up Safely
```bash
gpush
```
- **When to use:** After committing your changes
- **What it does:**
  - Pulls latest changes with rebase (keeps history clean)
  - Pushes your commits
  - Avoids conflicts
- **Use case:** "I'm done with my changes, send them to GitHub"

## Daily Workflow

```bash
# Morning: Sit down at computer
cd ~/docminer
gsync                    # See what's new

# Work on code...
# Make changes...

# When ready to save:
git add .
git commit -m "Description of changes"
gpush                    # Send to GitHub safely

# Move to different computer:
cd ~/docminer
gsync                    # Get your latest changes
```

## Why This Matters

- **Multiple computers:** Your laptop, desktop, etc. all stay in sync
- **Avoids conflicts:** The rebase keeps your history clean
- **Safety first:** Always pull before pushing
- **Muscle memory:** Two simple commands: `gsync` and `gpush`

## Troubleshooting

### "I forgot to pull first!"
```bash
git pull --rebase origin main  # Fix it
git push origin main           # Try again
```

### "I have uncommitted changes!"
```bash
git status                     # See what's changed
git stash                      # Save changes temporarily
gsync                          # Pull latest
git stash pop                  # Restore your changes
```

### "Merge conflict!"
```bash
git status                     # See conflicted files
# Edit files to resolve conflicts
git add .
git rebase --continue
```

## Setup Verification

After adding the aliases, verify they work:

```bash
cd ~/docminer
gsync                          # Should pull and show status
echo "test" > test.txt
git add test.txt
git commit -m "Test commit"
gpush                          # Should push successfully
git rm test.txt
git commit -m "Remove test"
gpush
```

---

**Pro Tip:** Add these aliases on ALL computers where you use Git, not just DocMiner. They work with any Git repository!
