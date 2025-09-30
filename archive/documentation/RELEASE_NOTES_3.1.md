# 🎉 Research Buddy 3.1 Release Notes

## 🚀 What's New in Research Buddy 3.1

### ✨ Enhanced State Management System
- **Paper State Persistence**: Your work is automatically saved when switching between papers
- **Smart Status Indicators**: Visual progress tracking with colored dots:
  - 🔴 Unprocessed papers
  - 🟡 Papers in progress (evidence collected, no decision yet)
  - 🟢 Completed papers (decision uploaded)
- **Seamless Navigation**: Switch between papers without losing your work
- **Progress Counter**: Real-time display of processed papers vs total papers

### ⚙️ Configurable GitHub Integration
- **User-Controlled Repositories**: No more hardcoded upload destinations!
- **Configuration Dialog**: Easy setup of GitHub repository settings
- **API Key Management**: Secure configuration of OpenAI and GitHub credentials
- **Repository Flexibility**: Upload results to YOUR organization's repository
- **Setup Wizard**: Built-in guidance for GitHub token and repository setup

### 🔧 Interface Improvements
- **Enhanced Navigation**: Previous/Next buttons now preserve all user input
- **Auto-Save Functionality**: Current paper state saved before navigation
- **Upload Status Tracking**: Papers marked as completed after successful upload
- **Configuration Menu**: File → Configuration for easy settings management
- **About Dialog**: Clear version and feature information

### 🛡️ Security & Reliability
- **No Hardcoded Credentials**: All repository settings are user-configurable
- **Environment Variable Support**: Standard OpenAI API key handling
- **Local Configuration Storage**: Settings saved securely in interface_settings.json
- **Error Prevention**: Better validation and user feedback
- **State Recovery**: Work is preserved across navigation and sessions

## 🔄 What Changed from Research Buddy 3.0

### Major Enhancements:
1. **State Persistence System**: Complete rework of data handling to preserve user work
2. **Visual Status System**: New colored indicator system for paper processing status
3. **Enhanced Navigation**: Smart save/load functionality integrated into paper switching
4. **Progress Tracking**: Real-time visual feedback on analysis progress
5. **Configurable Uploads**: Users can now specify their own GitHub repositories

### Technical Improvements:
- Added `paper_states` dictionary for comprehensive state tracking
- Enhanced `update_progress()` function with status indicators
- New state management functions: `save_current_paper_state()`, `load_current_paper_state()`, `mark_paper_uploaded()`
- Integrated state persistence into navigation workflow
- Configuration dialog system for repository and API settings
- Updated GitHubReportUploader to use user-specified repositories

### Breaking Changes:
- **Repository Configuration Required**: Users must now configure their own GitHub repository settings
- **No Default Upload Destination**: Hardcoded OhioMathTeacher/research-buddy repository removed

## 📋 System Requirements

- **macOS**: 10.14 or later (Intel/Apple Silicon)
- **Memory**: 4GB RAM minimum, 8GB recommended
- **Storage**: 500MB free space
- **Internet**: Required for AI analysis and GitHub uploads
- **OpenAI API Key**: Required for positionality analysis
- **GitHub Account**: Required for result uploads (with Personal Access Token)

## 🚀 Installation & Usage

### First-Time Setup:
1. **Download**: Get ResearchBuddy3.1 from the releases page
2. **Install**: Follow platform-specific installation instructions
3. **Configure**: Open File → Configuration to set up API keys and repository
4. **Test**: Use "Test Configuration" to verify settings
5. **Launch**: Start analyzing papers with enhanced state management!

### Configuration Steps:
1. **OpenAI API Key**: Get from [OpenAI API Keys](https://platform.openai.com/api-keys)
2. **GitHub Repository**: Create a repository for storing analysis results
3. **GitHub Token**: Generate at [GitHub Personal Access Tokens](https://github.com/settings/tokens) with `repo` scope
4. **Repository Setup**: Initialize git in your working directory or clone your repository

## 🐛 Bug Fixes

- Fixed API key exposure concerns (now user-configurable)
- Resolved navigation state loss issues
- Improved error handling in upload workflow
- Enhanced user feedback for decision recording
- Removed hardcoded repository dependencies

## 🔮 Coming Soon

- Enhanced upload decision workflow
- Extended file format support
- Batch processing improvements
- Multi-platform executable distribution

## 📞 Support

- **Configuration Guide**: See CONFIGURATION_GUIDE.md for detailed setup instructions
- **Documentation**: README.md and QUICK_REFERENCE.md
- **Issues**: Report bugs on GitHub
- **Community**: Join our discussions for tips and best practices

---

**Built with ❤️ for Graduate Assistants and Research Teams**

*Research Buddy 3.1 - Making academic positionality analysis faster, smarter, and more configurable.*