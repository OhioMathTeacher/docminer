# Quick Fix for Graduate Assistants

If you get "no such file or directory" when running `cd research-buddy`, the git clone probably failed.

## Step-by-Step Troubleshooting:

### 1. Check if git is installed:
```bash
git --version
```
If this fails, git isn't installed.

### 2. Try the clone again with verbose output:
```bash
git clone https://github.com/OhioMathTeacher/research-buddy.git
```

### 3. Check what folders exist:
```bash
ls -la
```

### 4. If clone worked, you should see a folder called `research-buddy`

### 5. If git isn't available, try GitHub Codespaces instead:
- Go to https://github.com/OhioMathTeacher/research-buddy
- Click green "Code" button
- Click "Codespaces" tab  
- Click "Create codespace"
- Wait for VS Code to load in browser
- Run: `python run_research_buddy.py`

## Alternative: Download ZIP
If git doesn't work:
1. Go to https://github.com/OhioMathTeacher/research-buddy
2. Click green "Code" button → "Download ZIP"
3. Extract the ZIP file
4. Open the extracted folder in VS Code
5. Open terminal and run: `python run_research_buddy.py`