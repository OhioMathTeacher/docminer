# 🔧 Research Buddy 3.1 Configuration Guide

## 🎯 Overview

Research Buddy 3.1 now includes configurable GitHub repository settings, allowing users to upload analysis results to their own repositories instead of hardcoded destinations.

## ⚙️ Configuration Setup

### 1. Access Configuration
- **Menu**: File → Configuration...
- **Purpose**: Set up API keys and GitHub repository settings for your organization

### 2. Required Settings

#### 🔑 OpenAI API Key
- **Required for**: AI-powered positionality analysis
- **Format**: `sk-...` (starts with "sk-")
- **Alternative**: Set `OPENAI_API_KEY` environment variable

#### 📦 GitHub Repository Settings
- **GitHub Username**: Your GitHub account name
- **Repository Name**: Target repository for analysis results (default: "research-buddy")
- **GitHub Token**: Personal access token with `repo` permissions

### 3. GitHub Token Setup

1. Go to [GitHub Settings → Developer settings → Personal access tokens](https://github.com/settings/tokens)
2. Click "Generate new token (classic)"
3. Select `repo` scope (full control of private repositories)
4. Copy the generated token (starts with `ghp_...`)
5. Paste into Research Buddy configuration

### 4. Repository Setup

For analysis uploads to work, you need:

1. **Create a repository** on GitHub (public or private)
2. **Clone it locally** to your machine
3. **Run Research Buddy from within the repository folder**

OR

1. **Initialize git** in your Research Buddy folder:
   ```bash
   git init
   git remote add origin https://github.com/YOUR-USERNAME/YOUR-REPO.git
   ```

## 🚀 Usage Workflow

### First-Time Setup
1. **Install Research Buddy 3.1**
2. **Open Configuration** (File → Configuration...)
3. **Enter your OpenAI API key**
4. **Configure GitHub settings** with your repository details
5. **Test configuration** using the "Test Configuration" button
6. **Save settings**

### Daily Usage
1. **Load PDFs** for analysis
2. **Analyze papers** with AI assistance
3. **Make decisions** with evidence collection
4. **Upload results** - now goes to YOUR repository!

## 🔒 Security Features

✅ **No Hardcoded Credentials**: All settings are user-configurable
✅ **Local Storage**: Configuration saved in `interface_settings.json`
✅ **Environment Variables**: Supports standard OpenAI API key setup
✅ **Token Protection**: GitHub tokens are stored locally and password-masked

## 🆘 Troubleshooting

### Configuration Issues
- **"No OpenAI API key"**: Get key from [OpenAI API Keys](https://platform.openai.com/api-keys)
- **"GitHub upload failed"**: Ensure you're in a git repository with correct remote
- **"Permission denied"**: Check GitHub token has `repo` scope

### Upload Issues
- **"Not in git repository"**: Initialize git in your working directory
- **"Git push failed"**: Verify GitHub token and repository permissions
- **"Remote not set"**: Add GitHub repository as remote origin

## 📋 Configuration File

Settings are stored in `interface_settings.json`:

```json
{
  "openai_api_key": "sk-...",
  "github_owner": "your-username",
  "github_repo": "research-buddy",
  "github_token": "ghp_..."
}
```

## 🔄 Migration from 3.0

If upgrading from Research Buddy 3.0:

1. **Open Configuration** dialog
2. **Enter your repository details** (no longer hardcoded to OhioMathTeacher/research-buddy)
3. **Test and save** new settings
4. **Existing analysis workflows remain the same**

---

*Your analysis results now go to YOUR repository, giving you full control over data and privacy! 🎉*