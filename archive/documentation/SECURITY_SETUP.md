# Security Configuration for Research Buddy

Research Buddy 3.1 introduces secure credential management using environment variables instead of storing sensitive data in plain text files.

## Why Environment Variables?

✅ **Secure**: Credentials are not stored in files that could be accidentally shared
✅ **Cross-Platform**: Works on Windows, macOS, and Linux
✅ **Industry Standard**: Used by professional applications worldwide
✅ **Executable-Friendly**: Perfect for distributing standalone applications

## Required Environment Variables

Research Buddy needs two environment variables:

```bash
RESEARCH_BUDDY_OPENAI_API_KEY     # Your OpenAI API key (starts with sk-)
RESEARCH_BUDDY_GITHUB_TOKEN       # Your GitHub token (starts with ghp_ or github_pat_)
```

## Quick Setup

### Option 1: Automated Setup Script
```bash
python3 setup_environment.py
```

### Option 2: Manual Setup

#### macOS/Linux
Add these lines to your shell configuration file (`~/.zshrc`, `~/.bashrc`, etc.):

```bash
export RESEARCH_BUDDY_OPENAI_API_KEY="sk-your-actual-key-here"
export RESEARCH_BUDDY_GITHUB_TOKEN="ghp_your-actual-token-here"
```

Then reload your shell:
```bash
source ~/.zshrc
```

#### Windows Command Prompt
```cmd
set RESEARCH_BUDDY_OPENAI_API_KEY=sk-your-actual-key-here
set RESEARCH_BUDDY_GITHUB_TOKEN=ghp_your-actual-token-here
```

#### Windows PowerShell
```powershell
$env:RESEARCH_BUDDY_OPENAI_API_KEY="sk-your-actual-key-here"
$env:RESEARCH_BUDDY_GITHUB_TOKEN="ghp_your-actual-token-here"
```

## Getting Your Credentials

### OpenAI API Key
1. Go to [OpenAI API Keys](https://platform.openai.com/api-keys)
2. Create a new secret key
3. Copy the key (starts with `sk-`)

### GitHub Token
1. Go to [GitHub Settings > Personal access tokens](https://github.com/settings/tokens)
2. Generate a new token (classic)
3. Select `repo` permissions
4. Copy the token (starts with `ghp_` or `github_pat_`)

## Verification

Test your setup:
```bash
python3 test_environment.py
```

## Configuration Dialog

After setting environment variables, use the configuration dialog in Research Buddy to:
- View environment variable status
- Set GitHub repository settings (owner/repo name)
- Test your complete configuration

The configuration dialog will show:
- ✅ Green checkmarks for properly set environment variables
- ❌ Red warnings for missing variables
- Instructions for setting up missing credentials

## Security Benefits

🔒 **No Plain Text Storage**: API keys and tokens are never written to files
🔒 **Environment Isolation**: Each user's credentials are separate
🔒 **Audit Trail**: System administrators can track environment variable usage
🔒 **Easy Rotation**: Change credentials by updating environment variables

## Troubleshooting

### Environment Variables Not Working?
1. Make sure you've restarted your terminal after setting variables
2. Check spelling: `RESEARCH_BUDDY_OPENAI_API_KEY` (exact case)
3. Run `echo $RESEARCH_BUDDY_OPENAI_API_KEY` to verify (macOS/Linux)
4. Run `echo %RESEARCH_BUDDY_OPENAI_API_KEY%` to verify (Windows)

### Still Having Issues?
1. Run `python3 test_environment.py` for detailed diagnostics
2. Use the automated setup: `python3 setup_environment.py`
3. Check the configuration dialog for status indicators

## Distribution and Packaging

This security model is perfect for creating distributable executables:
- No sensitive data is embedded in the application
- Users set their own credentials securely
- Works across all platforms
- Professional security standards

When packaging with PyInstaller or similar tools, the environment variable approach ensures your distributed application remains secure and professional.