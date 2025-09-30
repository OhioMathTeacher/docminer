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
    """Load configuration from environment variables and JSON file.
    
    Sensitive data (API keys, tokens) comes from environment variables.
    Non-sensitive data (repository settings) comes from config file.
    """
    config_path = Path.home() / ".research_buddy" / "interface_settings.json"
    
    # Load non-sensitive settings from file
    default_file_config = {
        "github_owner": "",
        "github_repo": ""
    }
    
    file_config = default_file_config.copy()
    if config_path.exists():
        try:
            with open(config_path, 'r') as f:
                loaded_config = json.load(f)
                # Only load non-sensitive settings from file
                for key in default_file_config:
                    if key in loaded_config:
                        file_config[key] = loaded_config[key]
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error loading configuration file: {e}")
    
    # Get sensitive data from environment variables
    config = {
        "openai_api_key": os.environ.get("RESEARCH_BUDDY_OPENAI_API_KEY", ""),
        "github_token": os.environ.get("RESEARCH_BUDDY_GITHUB_TOKEN", ""),
        "github_owner": file_config["github_owner"],
        "github_repo": file_config["github_repo"]
    }
    
    return config


def save_configuration(config):
    """Save non-sensitive configuration to JSON file.
    
    Only saves repository settings to file. API keys and tokens
    should be set as environment variables.
    """
    config_dir = Path.home() / ".research_buddy"
    config_dir.mkdir(exist_ok=True)
    
    config_path = config_dir / "interface_settings.json"
    
    # Only save non-sensitive settings to file
    file_config = {
        "github_owner": config.get("github_owner", ""),
        "github_repo": config.get("github_repo", "")
    }
    
    try:
        with open(config_path, 'w') as f:
            json.dump(file_config, f, indent=2)
        return True
    except IOError as e:
        print(f"Error saving configuration: {e}")
        return False


class ConfigurationDialog(QDialog):
    """Secure configuration dialog for Research Buddy settings"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("🔧 Research Buddy Configuration")
        self.setFixedSize(650, 600)
        
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
            "🔒 <b>Secure Configuration</b><br>"
            "API keys and tokens are loaded from environment variables for security:<br>"
            "• <code>RESEARCH_BUDDY_OPENAI_API_KEY</code> - Your OpenAI API key<br>"
            "• <code>RESEARCH_BUDDY_GITHUB_TOKEN</code> - Your GitHub personal access token<br><br>"
            "Repository settings below are saved to your local config file."
        )
        security_notice.setWordWrap(True)
        security_notice.setStyleSheet(
            "QLabel { "
            "background-color: #f0f8ff; "
            "border: 1px solid #cce7ff; "
            "border-radius: 5px; "
            "padding: 15px; "
            "margin: 10px; "
            "}"
        )
        layout.addWidget(security_notice)
        
        # Environment Variables Status
        env_group = QGroupBox("🔑 Environment Variables Status")
        env_layout = QFormLayout()
        
        self.openai_key_status = QLineEdit()
        self.openai_key_status.setReadOnly(True)
        self.openai_key_status.setPlaceholderText("Set via RESEARCH_BUDDY_OPENAI_API_KEY environment variable")
        env_layout.addRow("OpenAI API Key:", self.openai_key_status)
        
        self.github_token_status = QLineEdit()
        self.github_token_status.setReadOnly(True)
        self.github_token_status.setPlaceholderText("Set via RESEARCH_BUDDY_GITHUB_TOKEN environment variable")
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
        
        save_btn = QPushButton("💾 Save Repository Settings")
        save_btn.clicked.connect(self.save_configuration_data)
        save_btn.setDefault(True)
        save_btn.setStyleSheet("QPushButton { background-color: #0066cc; color: white; font-weight: bold; }")
        button_layout.addWidget(save_btn)
        
        layout.addLayout(button_layout)
        self.setLayout(layout)
        
    def load_values(self):
        """Load values into the form"""
        # Show environment variable status
        openai_key = self.config.get("openai_api_key", "")
        if openai_key:
            self.openai_key_status.setText(f"✅ Set ({openai_key[:8]}...)")
            self.openai_key_status.setStyleSheet("color: green;")
        else:
            self.openai_key_status.setText("❌ Not set - export RESEARCH_BUDDY_OPENAI_API_KEY")
            self.openai_key_status.setStyleSheet("color: red;")
            
        github_token = self.config.get("github_token", "")
        if github_token:
            self.github_token_status.setText(f"✅ Set ({github_token[:8]}...)")
            self.github_token_status.setStyleSheet("color: green;")
        else:
            self.github_token_status.setText("❌ Not set - export RESEARCH_BUDDY_GITHUB_TOKEN")
            self.github_token_status.setStyleSheet("color: red;")
        
        # Load repository settings
        self.github_owner_input.setText(self.config.get("github_owner", ""))
        self.github_repo_input.setText(self.config.get("github_repo", "research-buddy"))
        
    def save_configuration_data(self):
        """Save the current configuration and set environment variables."""
        # Get API key values from the input fields
        openai_key = self.openai_key_input.text().strip()
        github_token = self.github_token_input.text().strip()
        
        # Set environment variables for current process
        if openai_key:
            os.environ["RESEARCH_BUDDY_OPENAI_API_KEY"] = openai_key
            print(f"✅ Set RESEARCH_BUDDY_OPENAI_API_KEY in current process")
        
        if github_token:
            os.environ["RESEARCH_BUDDY_GITHUB_TOKEN"] = github_token
            print(f"✅ Set RESEARCH_BUDDY_GITHUB_TOKEN in current process")
        
        # Save non-sensitive repository settings to file
        config = {
            "github_owner": self.github_owner_input.text().strip(),
            "github_repo": self.github_repo_input.text().strip()
        }
        
        if save_configuration(config):
            QMessageBox.information(
                self, 
                "Configuration Saved", 
                f"Configuration saved successfully!\n\n"
                f"✅ API keys set for current session\n"
                f"✅ Repository settings saved\n\n"
                f"Upload destination: https://github.com/{config['github_owner']}/{config['github_repo']}\n\n"
                f"Note: Environment variables are set for this session only.\n"
                f"For permanent setup, add to your shell profile:\n"
                f"export RESEARCH_BUDDY_OPENAI_API_KEY=\"your-key\"\n"
                f"export RESEARCH_BUDDY_GITHUB_TOKEN=\"your-token\""
            )
            
            # Update the configuration status display
            self.update_environment_status()
            
        else:
            QMessageBox.critical(
                self, 
                "Save Error", 
                "Failed to save configuration. Please check file permissions."
            )
            
    def test_configuration(self):
        """Test the current configuration."""
        # Get values from environment variables and form
        openai_key = os.environ.get("RESEARCH_BUDDY_OPENAI_API_KEY", "").strip()
        github_token = os.environ.get("RESEARCH_BUDDY_GITHUB_TOKEN", "").strip()
        github_owner = self.github_owner_input.text().strip()
        github_repo = self.github_repo_input.text().strip()
        
        # Validate required fields
        missing_fields = []
        if not openai_key:
            missing_fields.append("RESEARCH_BUDDY_OPENAI_API_KEY environment variable")
        if not github_token:
            missing_fields.append("RESEARCH_BUDDY_GITHUB_TOKEN environment variable")
        if not github_owner:
            missing_fields.append("GitHub Owner")
        if not github_repo:
            missing_fields.append("GitHub Repository")
        
        if missing_fields:
            QMessageBox.warning(
                self,
                "Missing Configuration",
                f"Please provide the following required items:\n• {chr(10).join(missing_fields)}\n\n"
                f"Set environment variables in your system or shell:"
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
            "openai_api_key": os.environ.get("RESEARCH_BUDDY_OPENAI_API_KEY", ""),
            "github_token": os.environ.get("RESEARCH_BUDDY_GITHUB_TOKEN", ""),
            "github_owner": self.github_owner_input.text().strip(),
            "github_repo": self.github_repo_input.text().strip()
        }