#!/usr/bin/env python3
"""
Configuration Dialog for Research Buddy

Secure configuration with environment variables for sensitive data.
"""

import os
import json
from pathlib import Path
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout,
    QLineEdit, QPushButton, QLabel, QMessageBox, QTextEdit, QGroupBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont


def load_configuration():
    """Load configuration from config file.
    
    All settings (including API keys and tokens) are stored in the local config file.
    The file is stored in ~/.research_buddy/ which is user-specific and secure.
    Environment variables are checked as fallback for backward compatibility.
    """
    config_path = Path.home() / ".research_buddy" / "interface_settings.json"
    
    # Default configuration
    default_config = {
        "openai_api_key": "",
        "github_token": "",
        "github_owner": "",
        "github_repo": ""
    }
    
    config = default_config.copy()
    
    # Load from config file
    if config_path.exists():
        try:
            with open(config_path, 'r') as f:
                loaded_config = json.load(f)
                # Load all settings from file
                for key in default_config:
                    if key in loaded_config:
                        config[key] = loaded_config[key]
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error loading configuration file: {e}")
    
    # Fallback to environment variables if not in config file (backward compatibility)
    if not config["openai_api_key"]:
        config["openai_api_key"] = os.environ.get("RESEARCH_BUDDY_OPENAI_API_KEY", "")
    if not config["github_token"]:
        config["github_token"] = os.environ.get("RESEARCH_BUDDY_GITHUB_TOKEN", "")
    
    # SET environment variables from loaded config so AI functions can access them
    # This is critical for executables where env vars aren't set on launch
    if config["openai_api_key"]:
        os.environ["RESEARCH_BUDDY_OPENAI_API_KEY"] = config["openai_api_key"]
    if config["github_token"]:
        os.environ["RESEARCH_BUDDY_GITHUB_TOKEN"] = config["github_token"]
    
    return config


def save_configuration(config):
    """Save configuration to JSON file.
    
    Saves all settings including API keys and tokens to the local config file.
    The file is stored in ~/.research_buddy/ with user-only permissions (600).
    This allows users to configure once and not re-enter credentials every time.
    """
    config_dir = Path.home() / ".research_buddy"
    config_dir.mkdir(exist_ok=True)
    
    config_path = config_dir / "interface_settings.json"
    
    # Save all settings to file
    file_config = {
        "openai_api_key": config.get("openai_api_key", ""),
        "github_token": config.get("github_token", ""),
        "github_owner": config.get("github_owner", ""),
        "github_repo": config.get("github_repo", "")
    }
    
    try:
        with open(config_path, 'w') as f:
            json.dump(file_config, f, indent=2)
        
        # Set file permissions to user-only (600) for security
        os.chmod(config_path, 0o600)
        return True
    except IOError as e:
        print(f"Error saving configuration: {e}")
        return False


class ConfigurationDialog(QDialog):
    """Secure configuration dialog for Research Buddy settings"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("🔧 Research Buddy Configuration")
        self.setFixedSize(650, 700)
        
        # Make dialog truly modal - blocks interaction with parent window
        self.setWindowModality(Qt.ApplicationModal)
        
        # Ensure dialog stays on top
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        
        # Load existing configuration
        self.config = load_configuration()
        
        self.setup_ui()
        self.load_values()
        
    def setup_ui(self):
        """Setup the configuration dialog UI"""
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("🔧 Research Buddy Configuration")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Security notice
        security_notice = QLabel(
            "🔒 Secure Configuration\n\n"
            "Enter your API keys and tokens below. They will be set as environment variables "
            "for this session and can optionally be saved to your shell profile for persistence.\n\n"
            "Repository settings are saved to your local config file."
        )
        security_notice.setWordWrap(True)
        security_notice.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        security_notice.setStyleSheet(
            "QLabel { "
            "background-color: #f0f8ff; "
            "border: 1px solid #5b9bd5; "
            "border-radius: 5px; "
            "padding: 15px; "
            "margin: 10px; "
            "color: #2c3e50; "
            "font-size: 12px; "
            "}"
        )
        layout.addWidget(security_notice)
        
        # API Keys and Tokens Input
        api_group = QGroupBox("🔑 API Keys and Tokens")
        api_layout = QFormLayout()
        
        self.openai_key_input = QLineEdit()
        self.openai_key_input.setEchoMode(QLineEdit.Password)
        self.openai_key_input.setPlaceholderText("sk-your-openai-api-key-here")
        api_layout.addRow("OpenAI API Key:", self.openai_key_input)
        
        self.github_token_input = QLineEdit()
        self.github_token_input.setEchoMode(QLineEdit.Password)
        self.github_token_input.setPlaceholderText("ghp_your-github-token-here")
        api_layout.addRow("GitHub Token:", self.github_token_input)
        
        api_group.setLayout(api_layout)
        layout.addWidget(api_group)
        
        # Environment Variables Status
        env_group = QGroupBox("� Current Environment Status")
        env_layout = QFormLayout()
        
        self.openai_key_status = QLineEdit()
        self.openai_key_status.setReadOnly(True)
        self.openai_key_status.setPlaceholderText("Not currently set")
        env_layout.addRow("OpenAI API Key:", self.openai_key_status)
        
        self.github_token_status = QLineEdit()
        self.github_token_status.setReadOnly(True)
        self.github_token_status.setPlaceholderText("Not currently set")
        env_layout.addRow("GitHub Token:", self.github_token_status)
        
        env_group.setLayout(env_layout)
        layout.addWidget(env_group)
        
        # Repository Configuration
        repo_group = QGroupBox("📦 Repository Configuration")
        repo_layout = QFormLayout()
        
        self.github_owner_input = QLineEdit()
        self.github_owner_input.setPlaceholderText("your-github-username")
        repo_layout.addRow("GitHub Owner:", self.github_owner_input)
        
        self.github_repo_input = QLineEdit()
        self.github_repo_input.setPlaceholderText("research-buddy")
        repo_layout.addRow("GitHub Repository:", self.github_repo_input)
        
        repo_group.setLayout(repo_layout)
        layout.addWidget(repo_group)
        
        # Environment Setup Help
        help_text = QTextEdit()
        help_text.setPlainText(
            "To set environment variables:\n\n"
            "macOS/Linux (add to ~/.zshrc or ~/.bashrc):\n"
            "export RESEARCH_BUDDY_OPENAI_API_KEY=\"sk-your-key-here\"\n"
            "export RESEARCH_BUDDY_GITHUB_TOKEN=\"ghp_your-token-here\"\n\n"
            "Windows (Command Prompt):\n"
            "set RESEARCH_BUDDY_OPENAI_API_KEY=sk-your-key-here\n"
            "set RESEARCH_BUDDY_GITHUB_TOKEN=ghp_your-token-here\n\n"
            "Windows (PowerShell):\n"
            "$env:RESEARCH_BUDDY_OPENAI_API_KEY=\"sk-your-key-here\"\n"
            "$env:RESEARCH_BUDDY_GITHUB_TOKEN=\"ghp_your-token-here\""
        )
        help_text.setMaximumHeight(120)
        help_text.setStyleSheet("background-color: #f5f5f5; color: #333; font-size: 11px; font-family: monospace;")
        layout.addWidget(QLabel("💡 Environment Variable Setup:"))
        layout.addWidget(help_text)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        test_btn = QPushButton("🧪 Test Configuration")
        test_btn.clicked.connect(self.test_configuration)
        button_layout.addWidget(test_btn)
        
        button_layout.addStretch()
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)
        
        save_btn = QPushButton("💾 Save Configuration")
        save_btn.clicked.connect(self.save_configuration_data)
        save_btn.setDefault(True)
        save_btn.setStyleSheet("QPushButton { background-color: #0066cc; color: white; font-weight: bold; }")
        button_layout.addWidget(save_btn)
        
        layout.addLayout(button_layout)
        self.setLayout(layout)
        
    def load_values(self):
        """Load values into the form"""
        # Don't load actual API keys into input fields for security
        # Leave them empty - users can enter new ones if needed
        
        # Show environment variable status
        self.update_environment_status()
        
        # Load repository settings
        self.github_owner_input.setText(self.config.get("github_owner", ""))
        self.github_repo_input.setText(self.config.get("github_repo", "research-buddy"))
    
    def update_environment_status(self):
        """Update the environment status display"""
        openai_key = os.environ.get("RESEARCH_BUDDY_OPENAI_API_KEY", "")
        if openai_key:
            # Show that it's set, but don't imply it's validated with green checkmark
            self.openai_key_status.setText(f"Set (sk-****...)")
            self.openai_key_status.setStyleSheet("color: #0066cc; font-weight: bold;")  # Blue, not green
        else:
            self.openai_key_status.setText("❌ Not set")
            self.openai_key_status.setStyleSheet("color: #cc0000; font-weight: bold;")
            
        github_token = os.environ.get("RESEARCH_BUDDY_GITHUB_TOKEN", "")
        if github_token:
            token_prefix = "ghp_" if github_token.startswith("ghp_") else "github_pat_" if github_token.startswith("github_pat_") else "***"
            # Show that it's set, but don't imply it's validated with green checkmark
            self.github_token_status.setText(f"Set ({token_prefix}****...)")
            self.github_token_status.setStyleSheet("color: #0066cc; font-weight: bold;")  # Blue, not green
        else:
            self.github_token_status.setText("❌ Not set")
            self.github_token_status.setStyleSheet("color: #cc0000; font-weight: bold;")
        
    def save_configuration_data(self):
        """Save the current configuration and set environment variables."""
        # Get API key values from the input fields
        openai_key = self.openai_key_input.text().strip()
        github_token = self.github_token_input.text().strip()
        
        # Validate API key formats if provided
        if openai_key and not openai_key.startswith("sk-"):
            QMessageBox.warning(
                self, 
                "Invalid API Key", 
                "⚠️ OpenAI API key should start with 'sk-'. Please check your API key."
            )
            return
            
        if github_token and not github_token.startswith(("ghp_", "github_pat_")):
            QMessageBox.warning(
                self, 
                "Invalid Token", 
                "⚠️ GitHub token should start with 'ghp_' or 'github_pat_'. Please check your token."
            )
            return
        
        # Set environment variables for current process
        if openai_key:
            os.environ["RESEARCH_BUDDY_OPENAI_API_KEY"] = openai_key
            print(f"✅ Set RESEARCH_BUDDY_OPENAI_API_KEY in current process")
        
        if github_token:
            os.environ["RESEARCH_BUDDY_GITHUB_TOKEN"] = github_token
            print(f"✅ Set RESEARCH_BUDDY_GITHUB_TOKEN in current process")
        
        # Save ALL settings to file (including API keys and tokens)
        config = {
            "openai_api_key": openai_key,
            "github_token": github_token,
            "github_owner": self.github_owner_input.text().strip(),
            "github_repo": self.github_repo_input.text().strip()
        }
        
        if save_configuration(config):
            message = "Configuration saved successfully!\n\n"
            if openai_key:
                message += "✅ OpenAI API key saved permanently\n"
            if github_token:
                message += "✅ GitHub token saved permanently\n"
            message += "✅ Repository settings saved\n\n"
            
            if config['github_owner'] and config['github_repo']:
                message += f"📦 Upload destination: https://github.com/{config['github_owner']}/{config['github_repo']}\n\n"
            
            message += "All settings are saved to your secure config file.\n"
            message += "They will be automatically loaded when you restart the application."
            
            QMessageBox.information(self, "Configuration Saved", message)
            
            # Update the environment status display
            self.update_environment_status()
            
            # Accept the dialog to signal success
            self.accept()
            
        else:
            QMessageBox.critical(
                self, 
                "Save Error", 
                "Failed to save configuration. Please check file permissions."
            )
            
    def test_configuration(self):
        """Test the current configuration."""
        # Get values from input fields (prioritize) or environment variables
        openai_key = self.openai_key_input.text().strip() or os.environ.get("RESEARCH_BUDDY_OPENAI_API_KEY", "")
        github_token = self.github_token_input.text().strip() or os.environ.get("RESEARCH_BUDDY_GITHUB_TOKEN", "")
        github_owner = self.github_owner_input.text().strip()
        github_repo = self.github_repo_input.text().strip()
        
        # Validate required fields
        missing_fields = []
        if not openai_key:
            missing_fields.append("OpenAI API Key")
        if not github_token:
            missing_fields.append("GitHub Token")
        if not github_owner:
            missing_fields.append("GitHub Owner")
        if not github_repo:
            missing_fields.append("GitHub Repository")
        
        if missing_fields:
            QMessageBox.warning(
                self,
                "Missing Configuration",
                f"Please provide the following required items:\n• {chr(10).join(missing_fields)}"
            )
            return
            
        # Basic validation
        if not openai_key.startswith("sk-"):
            QMessageBox.warning(
                self, 
                "Configuration Issue", 
                "⚠️ OpenAI API key should start with 'sk-'. Please check your API key."
            )
            return
            
        if not github_token.startswith(("ghp_", "github_pat_")):
            QMessageBox.warning(
                self, 
                "Configuration Issue", 
                "⚠️ GitHub token should start with 'ghp_' or 'github_pat_'. Please check your token."
            )
            return
            
        # Show success
        repo_url = f"https://github.com/{github_owner}/{github_repo}"
        QMessageBox.information(
            self, 
            "Configuration Test", 
            f"✅ Configuration looks good!\n\n"
            f"• OpenAI API key format is correct\n"
            f"• GitHub token format is correct\n"
            f"• Repository settings are provided\n\n"
            f"📦 Upload Destination:\n{repo_url}"
        )
        
    def get_config(self):
        """Get the current configuration"""
        return {
            "openai_api_key": self.openai_key_input.text().strip() or os.environ.get("RESEARCH_BUDDY_OPENAI_API_KEY", ""),
            "github_token": self.github_token_input.text().strip() or os.environ.get("RESEARCH_BUDDY_GITHUB_TOKEN", ""),
            "github_owner": self.github_owner_input.text().strip(),
            "github_repo": self.github_repo_input.text().strip()
        }