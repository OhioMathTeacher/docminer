#!/usr/bin/env python3
"""
Configuration Dialog for Research Buddy

Allows users to configure GitHub repository settings and API keys.
"""

import os
import json
from pathlib import Path
from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QFormLayout, 
                              QLineEdit, QPushButton, QLabel, QGroupBox,
                              QMessageBox, QCheckBox, QTextEdit)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

class ConfigurationDialog(QDialog):
    """Dialog for configuring Research Buddy settings"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("🔧 Research Buddy Configuration")
        self.setFixedSize(600, 500)
        self.config_file = Path("interface_settings.json")
        
        # Load existing configuration
        self.config = self.load_config()
        
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
        
        # API Configuration
        api_group = QGroupBox("🔑 API Configuration")
        api_layout = QFormLayout()
        
        self.openai_key_input = QLineEdit()
        self.openai_key_input.setEchoMode(QLineEdit.Password)
        self.openai_key_input.setPlaceholderText("sk-...")
        api_layout.addRow("OpenAI API Key:", self.openai_key_input)
        
        self.show_key_checkbox = QCheckBox("Show API key")
        self.show_key_checkbox.toggled.connect(self.toggle_key_visibility)
        api_layout.addRow("", self.show_key_checkbox)
        
        api_help = QLabel("💡 Tip: You can also set OPENAI_API_KEY environment variable")
        api_help.setWordWrap(True)
        api_help.setStyleSheet("color: #666; font-size: 11px;")
        api_layout.addRow("", api_help)
        
        api_group.setLayout(api_layout)
        layout.addWidget(api_group)
        
        # GitHub Configuration
        github_group = QGroupBox("📦 GitHub Upload Configuration")
        github_layout = QFormLayout()
        
        self.github_owner_input = QLineEdit()
        self.github_owner_input.setPlaceholderText("your-github-username")
        github_layout.addRow("GitHub Username:", self.github_owner_input)
        
        self.github_repo_input = QLineEdit()
        self.github_repo_input.setPlaceholderText("research-buddy")
        github_layout.addRow("Repository Name:", self.github_repo_input)
        
        self.github_token_input = QLineEdit()
        self.github_token_input.setEchoMode(QLineEdit.Password)
        self.github_token_input.setPlaceholderText("ghp_...")
        github_layout.addRow("GitHub Token:", self.github_token_input)
        
        self.show_token_checkbox = QCheckBox("Show GitHub token")
        self.show_token_checkbox.toggled.connect(self.toggle_token_visibility)
        github_layout.addRow("", self.show_token_checkbox)
        
        github_help = QTextEdit()
        github_help.setPlainText(
            "Instructions:\n"
            "1. Create a GitHub repository for storing analysis results\n"
            "2. Generate a Personal Access Token with 'repo' permissions\n"
            "3. Enter your GitHub username and repository name above\n"
            "4. Paste your GitHub token for upload authentication"
        )
        github_help.setMaximumHeight(80)
        github_help.setStyleSheet("background-color: #f5f5f5; color: #666; font-size: 11px;")
        github_layout.addRow("Setup Help:", github_help)
        
        github_group.setLayout(github_layout)
        layout.addWidget(github_group)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        test_btn = QPushButton("🧪 Test Configuration")
        test_btn.clicked.connect(self.test_configuration)
        button_layout.addWidget(test_btn)
        
        reset_btn = QPushButton("🔄 Reset to Defaults")
        reset_btn.clicked.connect(self.reset_to_defaults)
        button_layout.addWidget(reset_btn)
        
        button_layout.addStretch()
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)
        
        save_btn = QPushButton("💾 Save Configuration")
        save_btn.clicked.connect(self.save_configuration)
        save_btn.setDefault(True)
        save_btn.setStyleSheet("QPushButton { background-color: #0066cc; color: white; font-weight: bold; }")
        button_layout.addWidget(save_btn)
        
        layout.addLayout(button_layout)
        self.setLayout(layout)
        
    def toggle_key_visibility(self, checked):
        """Toggle OpenAI API key visibility"""
        if checked:
            self.openai_key_input.setEchoMode(QLineEdit.Normal)
        else:
            self.openai_key_input.setEchoMode(QLineEdit.Password)
            
    def toggle_token_visibility(self, checked):
        """Toggle GitHub token visibility"""
        if checked:
            self.github_token_input.setEchoMode(QLineEdit.Normal)
        else:
            self.github_token_input.setEchoMode(QLineEdit.Password)
    
    def load_config(self):
        """Load configuration from file"""
        default_config = {
            "openai_api_key": "",
            "github_owner": "",
            "github_repo": "research-buddy",
            "github_token": ""
        }
        
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                    # Merge with defaults to handle missing keys
                    default_config.update(config)
                    return default_config
            except Exception as e:
                print(f"Error loading config: {e}")
                
        return default_config
    
    def load_values(self):
        """Load values into the form"""
        # Load API key from environment or config
        env_key = os.getenv("OPENAI_API_KEY", "")
        config_key = self.config.get("openai_api_key", "")
        self.openai_key_input.setText(env_key or config_key)
        
        # Load GitHub settings
        self.github_owner_input.setText(self.config.get("github_owner", ""))
        self.github_repo_input.setText(self.config.get("github_repo", "research-buddy"))
        self.github_token_input.setText(self.config.get("github_token", ""))
        
    def save_configuration(self):
        """Save configuration and close dialog"""
        config = {
            "openai_api_key": self.openai_key_input.text().strip(),
            "github_owner": self.github_owner_input.text().strip(),
            "github_repo": self.github_repo_input.text().strip(),
            "github_token": self.github_token_input.text().strip()
        }
        
        # Validation
        if not config["github_owner"]:
            QMessageBox.warning(self, "Configuration Error", 
                              "GitHub username is required for uploading results.")
            return
            
        if not config["github_repo"]:
            QMessageBox.warning(self, "Configuration Error", 
                              "Repository name is required for uploading results.")
            return
        
        try:
            with open(self.config_file, 'w') as f:
                json.dump(config, f, indent=2)
                
            QMessageBox.information(self, "Configuration Saved", 
                                  "Configuration has been saved successfully!")
            self.accept()
            
        except Exception as e:
            QMessageBox.critical(self, "Save Error", f"Could not save configuration: {e}")
    
    def test_configuration(self):
        """Test the current configuration"""
        # Test OpenAI API key
        api_key = self.openai_key_input.text().strip()
        if not api_key:
            QMessageBox.warning(self, "Test Results", 
                              "⚠️ No OpenAI API key provided.\n\nAI analysis will not work without an API key.")
            return
            
        if not api_key.startswith("sk-"):
            QMessageBox.warning(self, "Test Results", 
                              "⚠️ OpenAI API key should start with 'sk-'.\n\nPlease check your API key.")
            return
            
        # Test GitHub configuration
        github_owner = self.github_owner_input.text().strip()
        github_repo = self.github_repo_input.text().strip()
        github_token = self.github_token_input.text().strip()
        
        if not github_owner or not github_repo:
            QMessageBox.warning(self, "Test Results", 
                              "⚠️ GitHub username and repository name are required.\n\n"
                              "Upload functionality will not work without these.")
            return
            
        if not github_token:
            QMessageBox.warning(self, "Test Results", 
                              "⚠️ GitHub token is required for uploads.\n\n"
                              "You can generate one at: https://github.com/settings/tokens")
            return
            
        QMessageBox.information(self, "Test Results", 
                              "✅ Configuration looks good!\n\n"
                              "• OpenAI API key format is correct\n"
                              "• GitHub settings are provided\n\n"
                              "Save configuration to use these settings.")
    
    def reset_to_defaults(self):
        """Reset configuration to defaults"""
        reply = QMessageBox.question(self, "Reset Configuration", 
                                   "Are you sure you want to reset all settings to defaults?\n\n"
                                   "This will clear all current values.")
        
        if reply == QMessageBox.Yes:
            self.openai_key_input.clear()
            self.github_owner_input.clear()
            self.github_repo_input.setText("research-buddy")
            self.github_token_input.clear()
            
    def get_config(self):
        """Get the current configuration"""
        return {
            "openai_api_key": self.openai_key_input.text().strip(),
            "github_owner": self.github_owner_input.text().strip(),
            "github_repo": self.github_repo_input.text().strip(),
            "github_token": self.github_token_input.text().strip()
        }