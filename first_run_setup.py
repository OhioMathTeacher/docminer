#!/usr/bin/env python3
"""
First Run Setup Dialog for Research Buddy

This dialog appears automatically when Research Buddy is launched
without proper configuration, guiding users through secure setup.
"""

import os
import sys
import json
from pathlib import Path
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout, QGridLayout,
    QLineEdit, QPushButton, QLabel, QMessageBox, QTextEdit, 
    QGroupBox, QTabWidget, QWidget, QCheckBox, QProgressBar,
    QScrollArea, QFrame
)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont, QPixmap, QIcon


class FirstRunSetupDialog(QDialog):
    """First-run setup dialog for Research Buddy configuration"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("🎉 Welcome to Research Buddy 3.1!")
        self.setFixedSize(800, 700)  # Increased size for better spacing
        self.setModal(True)
        
        # Configuration data
        self.config_data = {
            "openai_api_key": "",
            "github_token": "",
            "github_owner": "",
            "github_repo": "research-buddy"
        }
        
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the welcome and configuration UI"""
        layout = QVBoxLayout()
        
        # Welcome header
        self.create_welcome_header(layout)
        
        # Tab widget for different setup steps
        self.tab_widget = QTabWidget()
        
        # Tab 1: Welcome & Overview
        self.create_welcome_tab()
        
        # Tab 2: Environment Variables Setup
        self.create_environment_tab()
        
        # Tab 3: Repository Configuration
        self.create_repository_tab()
        
        # Tab 4: Test & Complete
        self.create_completion_tab()
        
        layout.addWidget(self.tab_widget)
        
        # Navigation buttons
        self.create_navigation_buttons(layout)
        
        self.setLayout(layout)
        
    def create_welcome_header(self, layout):
        """Create the welcome header"""
        header_frame = QFrame()
        header_frame.setStyleSheet(
            "QFrame { "
            "background: qlineargradient(x1:0, y1:0, x2:1, y2:1, "
            "stop:0 #2c5aa0, stop:1 #1e3a6f); "
            "border-radius: 10px; "
            "margin: 5px; "
            "}"
        )
        header_layout = QVBoxLayout()
        header_layout.setContentsMargins(20, 20, 20, 20)
        
        title = QLabel("🎉 Welcome to Research Buddy 3.1!")
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: white; padding: 15px;")
        
        subtitle = QLabel("Professional Positionality Analysis with Secure Configuration")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("color: #e6f3ff; font-size: 12px; padding-bottom: 15px;")
        
        header_layout.addWidget(title)
        header_layout.addWidget(subtitle)
        header_frame.setLayout(header_layout)
        layout.addWidget(header_frame)
        
    def create_welcome_tab(self):
        """Create the welcome and overview tab"""
        tab = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(20)  # Add generous spacing
        layout.setContentsMargins(30, 20, 30, 20)  # Add margins
        
        # Add avatar image at the top
        avatar_label = QLabel()
        try:
            # Try to load the avatar image
            avatar_pixmap = QPixmap("avatar_trio.png")  # Your avatar friends image
            if not avatar_pixmap.isNull():
                # Scale the image to a reasonable size
                scaled_pixmap = avatar_pixmap.scaled(200, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                avatar_label.setPixmap(scaled_pixmap)
                avatar_label.setAlignment(Qt.AlignCenter)
                layout.addWidget(avatar_label)
        except Exception:
            # If image not found, just add some emoji
            avatar_label.setText("🔬👨‍💻🤖👩‍🎓")
            avatar_label.setAlignment(Qt.AlignCenter)
            avatar_label.setStyleSheet("font-size: 36px; padding: 20px;")
            layout.addWidget(avatar_label)
        
        # Welcome message with better spacing and colors
        welcome_text = QLabel(
            "<h2>🔬 Research Buddy</h2>"
            "<p>Professional contextual document analysis software that helps you analyze academic papers for positionality statements.</p>"
            "<p>This setup wizard will guide you through configuring Research Buddy securely:</p>"
            "<h3>🔒 Secure by Design</h3>"
            "<ul>"
            "<li>API keys stored as environment variables (not in files)</li>"
            "<li>Professional security standards</li>"
            "<li>Works across Windows, macOS, and Linux</li>"
            "</ul>"
            "<h3>📚 What You'll Need</h3>"
            "<ul>"
            "<li>OpenAI API key (for AI analysis) - <em>Optional but recommended</em></li>"
            "<li>GitHub account and token (for saving results) - <em>Optional</em></li>"
            "<li>5 minutes to complete setup</li>"
            "</ul>"
            "<p><strong>🚀 Ready to get started?</strong> Click Next to begin!</p>"
        )
        welcome_text.setWordWrap(True)
        welcome_text.setStyleSheet(
            "QLabel { "
            "padding: 25px; "
            "line-height: 1.6; "
            "font-size: 14px; "
            "background-color: rgba(128, 128, 128, 0.1); "
            "border: 1px solid rgba(128, 128, 128, 0.3); "
            "border-radius: 8px; "
            "margin: 10px; "
            "}"
        )
        layout.addWidget(welcome_text)
        
        # Feature highlights with better spacing
        features_group = QGroupBox("✨ New in Version 3.1")
        features_group.setStyleSheet(
            "QGroupBox { "
            "font-weight: bold; "
            "font-size: 14px; "
            "margin-top: 15px; "
            "}"
            "QGroupBox::title { "
            "subcontrol-origin: margin; "
            "left: 10px; "
            "padding: 0 10px 0 10px; "
            "}"
        )
        features_layout = QVBoxLayout()
        features_layout.setSpacing(12)  # More generous spacing
        features_layout.setContentsMargins(20, 15, 20, 15)
        
        features = [
            "🔒 Secure environment variable configuration",
            "📊 Enhanced state persistence across sessions", 
            "🌐 Smart network connectivity detection",
            "📍 Clear upload destination visibility",
            "🎯 Improved user experience throughout"
        ]
        
        for feature in features:
            feature_label = QLabel(feature)
            feature_label.setStyleSheet(
                "QLabel { "
                "padding: 12px; "
                "font-size: 13px; "
                "background-color: rgba(46, 125, 50, 0.1); "
                "border: 1px solid rgba(46, 125, 50, 0.3); "
                "border-radius: 6px; "
                "margin: 3px; "
                "}"
            )
            features_layout.addWidget(feature_label)
            
        features_group.setLayout(features_layout)
        layout.addWidget(features_group)
        
        layout.addStretch()
        tab.setLayout(layout)
        self.tab_widget.addTab(tab, "👋 Welcome")
        
    def create_environment_tab(self):
        """Create the environment variables setup tab"""
        tab = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(25)  # Generous spacing like repository tab
        layout.setContentsMargins(30, 20, 30, 20)  # Consistent margins
        
        # Instructions with neutral colors
        instructions = QLabel(
            "<h3>🔑 Secure Credential Setup</h3>"
            "<p>Research Buddy uses environment variables for secure credential storage. "
            "This is the industry standard for professional applications and ensures "
            "your API keys are never stored in plain text files.</p>"
            "<p>You can set these up now or skip and configure them later.</p>"
        )
        instructions.setWordWrap(True)
        instructions.setStyleSheet(
            "QLabel { "
            "padding: 20px; "
            "background-color: rgba(33, 150, 243, 0.1); "
            "border: 1px solid rgba(33, 150, 243, 0.3); "
            "border-radius: 8px; "
            "margin-bottom: 20px; "
            "font-size: 14px; "
            "line-height: 1.5; "
            "}"
        )
        layout.addWidget(instructions)
        
        # API Key section with consistent spacing
        api_group = QGroupBox("🤖 OpenAI API Configuration (Optional)")
        api_group.setStyleSheet(
            "QGroupBox { "
            "font-weight: bold; "
            "font-size: 14px; "
            "margin-top: 10px; "
            "padding-top: 15px; "
            "}"
        )
        api_layout = QVBoxLayout()
        api_layout.setSpacing(15)  # Consistent with repository tab
        api_layout.setContentsMargins(20, 20, 20, 20)
        
        api_desc = QLabel(
            "An OpenAI API key enables AI-powered analysis of research papers. "
            "Without this, you can still use Research Buddy for manual analysis."
        )
        api_desc.setWordWrap(True)
        api_desc.setStyleSheet(
            "QLabel { "
            "padding: 12px; "
            "margin-bottom: 15px; "
            "font-size: 13px; "
            "line-height: 1.4; "
            "background-color: rgba(128, 128, 128, 0.1); "
            "border-radius: 6px; "
            "}"
        )
        api_layout.addWidget(api_desc)
        
        api_key_label = QLabel("OpenAI API Key:")
        api_key_label.setStyleSheet("font-weight: bold; margin-top: 5px;")
        api_layout.addWidget(api_key_label)
        
        self.openai_key_input = QLineEdit()
        self.openai_key_input.setPlaceholderText("sk-your-openai-api-key-here (optional)")
        self.openai_key_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.openai_key_input.setMinimumHeight(35)  # Taller for better usability
        self.openai_key_input.setStyleSheet(
            "QLineEdit { "
            "padding: 8px; "
            "font-size: 13px; "
            "border: 2px solid rgba(128, 128, 128, 0.3); "
            "border-radius: 6px; "
            "background-color: rgba(128, 128, 128, 0.05); "
            "} "
            "QLineEdit:focus { "
            "border-color: rgba(33, 150, 243, 0.6); "
            "}"
        )
        api_layout.addWidget(self.openai_key_input)
        
        self.show_openai_key = QCheckBox("Show API key")
        self.show_openai_key.toggled.connect(lambda checked: 
            self.openai_key_input.setEchoMode(QLineEdit.EchoMode.Normal if checked else QLineEdit.EchoMode.Password))
        api_layout.addWidget(self.show_openai_key)
        
        get_key_label = QLabel("🔗 <a href='https://platform.openai.com/api-keys'>Get your OpenAI API key here</a>")
        get_key_label.setOpenExternalLinks(True)
        get_key_label.setStyleSheet("color: #0066cc; margin-top: 5px;")
        api_layout.addWidget(get_key_label)
        
        api_group.setLayout(api_layout)
        layout.addWidget(api_group)
        
        # GitHub section
        github_group = QGroupBox("📦 GitHub Integration (Optional)")
        github_layout = QVBoxLayout()
        github_layout.setSpacing(10)  # Add spacing between elements
        
        github_desc = QLabel(
            "GitHub integration allows you to automatically save analysis results "
            "to a repository. This is optional - you can always save results locally."
        )
        github_desc.setWordWrap(True)
        github_desc.setStyleSheet(
            "color: #555; margin-bottom: 15px; font-size: 12px; "
            "line-height: 1.4; padding: 8px;"
        )
        github_layout.addWidget(github_desc)
        
        github_token_label = QLabel("GitHub Personal Access Token:")
        github_token_label.setStyleSheet("font-weight: bold; margin-top: 10px; font-size: 13px;")
        github_layout.addWidget(github_token_label)
        
        self.github_token_input = QLineEdit()
        self.github_token_input.setPlaceholderText("ghp_your-github-token-here (optional)")
        self.github_token_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.github_token_input.setMinimumHeight(35)  # Match other inputs
        self.github_token_input.setStyleSheet(
            "QLineEdit { "
            "padding: 8px; "
            "font-size: 13px; "
            "border: 2px solid rgba(128, 128, 128, 0.3); "
            "border-radius: 6px; "
            "background-color: rgba(128, 128, 128, 0.05); "
            "} "
            "QLineEdit:focus { "
            "border-color: rgba(33, 150, 243, 0.6); "
            "}"
        )
        github_layout.addWidget(self.github_token_input)
        
        self.show_github_token = QCheckBox("Show GitHub token")
        self.show_github_token.toggled.connect(lambda checked: 
            self.github_token_input.setEchoMode(QLineEdit.EchoMode.Normal if checked else QLineEdit.EchoMode.Password))
        github_layout.addWidget(self.show_github_token)
        
        get_token_label = QLabel("🔗 <a href='https://github.com/settings/tokens'>Generate GitHub token here</a> (needs 'repo' permissions)")
        get_token_label.setOpenExternalLinks(True)
        get_token_label.setStyleSheet("color: #0066cc; margin-top: 5px;")
        github_layout.addWidget(get_token_label)
        
        github_group.setLayout(github_layout)
        layout.addWidget(github_group)
        
        layout.addStretch()
        tab.setLayout(layout)
        self.tab_widget.addTab(tab, "🔑 Credentials")
        
    def create_repository_tab(self):
        """Create the repository configuration tab"""
        tab = QWidget()
        layout = QVBoxLayout()
        
        # Instructions with neutral colors
        instructions = QLabel(
            "<h3>📂 Repository Configuration</h3>"
            "<p>If you're using GitHub integration, specify where you'd like to save your analysis results. "
            "If you don't have a repository yet, you can create one on GitHub first, or skip this step.</p>"
        )
        instructions.setWordWrap(True)
        instructions.setStyleSheet(
            "QLabel { "
            "padding: 20px; "
            "background-color: rgba(128, 128, 128, 0.1); "
            "border: 1px solid rgba(128, 128, 128, 0.3); "
            "border-radius: 8px; "
            "margin-bottom: 20px; "
            "font-size: 14px; "
            "line-height: 1.5; "
            "}"
        )
        layout.addWidget(instructions)
        
        # Repository settings
        repo_group = QGroupBox("📦 Repository Settings")
        repo_layout = QFormLayout()
        repo_layout.setVerticalSpacing(15)  # Add more spacing between form rows
        
        self.github_owner_input = QLineEdit()
        self.github_owner_input.setPlaceholderText("your-github-username")
        self.github_owner_input.setMinimumHeight(35)
        self.github_owner_input.setStyleSheet(
            "QLineEdit { "
            "padding: 8px; "
            "font-size: 13px; "
            "border: 2px solid rgba(128, 128, 128, 0.3); "
            "border-radius: 6px; "
            "background-color: rgba(128, 128, 128, 0.05); "
            "} "
            "QLineEdit:focus { "
            "border-color: rgba(33, 150, 243, 0.6); "
            "}"
        )
        owner_label = QLabel("GitHub Username:")
        owner_label.setStyleSheet("font-weight: bold; font-size: 13px;")
        repo_layout.addRow(owner_label, self.github_owner_input)
        
        self.github_repo_input = QLineEdit()
        self.github_repo_input.setPlaceholderText("research-buddy")
        self.github_repo_input.setText("research-buddy")  # Default value
        self.github_repo_input.setMinimumHeight(35)
        self.github_repo_input.setStyleSheet(
            "QLineEdit { "
            "padding: 8px; "
            "font-size: 13px; "
            "border: 2px solid rgba(128, 128, 128, 0.3); "
            "border-radius: 6px; "
            "background-color: rgba(128, 128, 128, 0.05); "
            "} "
            "QLineEdit:focus { "
            "border-color: rgba(33, 150, 243, 0.6); "
            "}"
        )
        repo_label = QLabel("Repository Name:")
        repo_label.setStyleSheet("font-weight: bold; font-size: 13px;")
        repo_layout.addRow(repo_label, self.github_repo_input)
        
        repo_group.setLayout(repo_layout)
        layout.addWidget(repo_group)
        
        # Repository preview with neutral styling
        self.repo_preview = QLabel()
        self.repo_preview.setStyleSheet(
            "QLabel { "
            "background-color: rgba(33, 150, 243, 0.1); "
            "border: 1px solid rgba(33, 150, 243, 0.3); "
            "border-radius: 6px; "
            "padding: 12px; "
            "margin: 10px 0; "
            "font-size: 13px; "
            "}"
        )
        self.update_repo_preview()
        layout.addWidget(self.repo_preview)
        
        # Connect inputs to preview update
        self.github_owner_input.textChanged.connect(self.update_repo_preview)
        self.github_repo_input.textChanged.connect(self.update_repo_preview)
        
        # Help section
        help_group = QGroupBox("💡 Need a Repository?")
        help_layout = QVBoxLayout()
        
        help_text = QLabel(
            "1. Go to <a href='https://github.com/new'>GitHub.com/new</a><br>"
            "2. Create a repository named 'research-buddy' (or any name you prefer)<br>"
            "3. Make it public or private - your choice<br>"
            "4. Come back and enter your username and repository name above"
        )
        help_text.setOpenExternalLinks(True)
        help_text.setWordWrap(True)
        help_text.setStyleSheet("color: #666;")
        help_layout.addWidget(help_text)
        
        help_group.setLayout(help_layout)
        layout.addWidget(help_group)
        
        layout.addStretch()
        tab.setLayout(layout)
        self.tab_widget.addTab(tab, "📂 Repository")
        
    def create_completion_tab(self):
        """Create the completion and test tab"""
        tab = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(25)  # Consistent spacing
        layout.setContentsMargins(30, 20, 30, 20)
        
        # Summary with neutral colors
        summary_label = QLabel(
            "<h3>🎯 Setup Complete!</h3>"
            "<p>Review your configuration below and test the connections. "
            "You can always change these settings later through the Configuration menu.</p>"
        )
        summary_label.setWordWrap(True)
        summary_label.setStyleSheet(
            "QLabel { "
            "padding: 20px; "
            "background-color: rgba(76, 175, 80, 0.1); "
            "border: 1px solid rgba(76, 175, 80, 0.3); "
            "border-radius: 8px; "
            "margin-bottom: 20px; "
            "font-size: 14px; "
            "line-height: 1.5; "
            "}"
        )
        layout.addWidget(summary_label)
        
        # Configuration summary
        summary_label = QLabel("📋 Configuration Summary:")
        summary_label.setStyleSheet("font-weight: bold; font-size: 14px; margin-top: 15px;")
        layout.addWidget(summary_label)
        
        self.config_summary = QTextEdit()
        self.config_summary.setMaximumHeight(200)  # More height for readability
        self.config_summary.setReadOnly(True)
        self.config_summary.setStyleSheet(
            "QTextEdit { "
            "background-color: rgba(128, 128, 128, 0.05); "
            "border: 2px solid rgba(128, 128, 128, 0.3); "
            "border-radius: 6px; "
            "padding: 15px; "
            "font-size: 13px; "
            "line-height: 1.4; "
            "}"
        )
        layout.addWidget(self.config_summary)
        
        # Test button
        test_layout = QHBoxLayout()
        self.test_button = QPushButton("🧪 Test Configuration")
        self.test_button.clicked.connect(self.test_configuration)
        test_layout.addWidget(self.test_button)
        test_layout.addStretch()
        layout.addLayout(test_layout)
        
        # Test results
        self.test_results = QTextEdit()
        self.test_results.setMaximumHeight(140)  # Increased for better readability
        self.test_results.setReadOnly(True)
        self.test_results.setStyleSheet(
            "QTextEdit { "
            "background-color: rgba(128, 128, 128, 0.05); "
            "border: 2px solid rgba(128, 128, 128, 0.3); "
            "border-radius: 6px; "
            "padding: 12px; "
            "font-size: 13px; "
            "line-height: 1.3; "
            "}"
        )
        self.test_results.hide()
        layout.addWidget(self.test_results)
        
        layout.addStretch()
        tab.setLayout(layout)
        self.tab_widget.addTab(tab, "✅ Complete")
        
    def create_navigation_buttons(self, layout):
        """Create navigation buttons"""
        button_layout = QHBoxLayout()
        
        self.skip_button = QPushButton("⏭️ Skip Setup")
        self.skip_button.clicked.connect(self.skip_setup)
        button_layout.addWidget(self.skip_button)
        
        button_layout.addStretch()
        
        self.back_button = QPushButton("← Back")
        self.back_button.clicked.connect(self.go_back)
        self.back_button.setEnabled(False)
        button_layout.addWidget(self.back_button)
        
        self.next_button = QPushButton("Next →")
        self.next_button.clicked.connect(self.go_next)
        button_layout.addWidget(self.next_button)
        
        self.finish_button = QPushButton("🎉 Start Research Buddy!")
        self.finish_button.clicked.connect(self.finish_setup)
        self.finish_button.hide()
        button_layout.addWidget(self.finish_button)
        
        # Connect tab changes to update buttons
        self.tab_widget.currentChanged.connect(self.update_navigation_buttons)
        
        layout.addLayout(button_layout)
        
    def update_repo_preview(self):
        """Update the repository preview"""
        owner = self.github_owner_input.text().strip()
        repo = self.github_repo_input.text().strip() or "research-buddy"
        
        if owner:
            url = f"https://github.com/{owner}/{repo}"
            self.repo_preview.setText(f"📍 Upload destination: <a href='{url}'>{url}</a>")
            self.repo_preview.show()
        else:
            self.repo_preview.hide()
            
    def update_navigation_buttons(self):
        """Update navigation button states based on current tab"""
        current_index = self.tab_widget.currentIndex()
        total_tabs = self.tab_widget.count()
        
        # Update back button
        self.back_button.setEnabled(current_index > 0)
        
        # Update next/finish buttons
        if current_index == total_tabs - 1:  # Last tab
            self.next_button.hide()
            self.finish_button.show()
            self.update_config_summary()
        else:
            self.next_button.show()
            self.finish_button.hide()
            
    def update_config_summary(self):
        """Update the configuration summary on the last tab"""
        summary_lines = []
        
        # API Key status
        if self.openai_key_input.text().strip():
            summary_lines.append("✅ OpenAI API Key: Provided")
        else:
            summary_lines.append("⚪ OpenAI API Key: Not provided (AI analysis disabled)")
            
        # GitHub token status
        if self.github_token_input.text().strip():
            summary_lines.append("✅ GitHub Token: Provided")
        else:
            summary_lines.append("⚪ GitHub Token: Not provided (upload disabled)")
            
        # Repository settings
        owner = self.github_owner_input.text().strip()
        repo = self.github_repo_input.text().strip() or "research-buddy"
        
        if owner:
            summary_lines.append(f"✅ Repository: {owner}/{repo}")
        else:
            summary_lines.append("⚪ Repository: Not configured")
            
        self.config_summary.setPlainText("\n".join(summary_lines))
        
    def go_back(self):
        """Go to previous tab"""
        current = self.tab_widget.currentIndex()
        if current > 0:
            self.tab_widget.setCurrentIndex(current - 1)
            
    def go_next(self):
        """Go to next tab"""
        current = self.tab_widget.currentIndex()
        if current < self.tab_widget.count() - 1:
            self.tab_widget.setCurrentIndex(current + 1)
            
    def test_configuration(self):
        """Test the current configuration"""
        self.test_results.show()
        self.test_results.setPlainText("🧪 Testing configuration...\n")
        
        results = []
        
        # Test API key format
        api_key = self.openai_key_input.text().strip()
        if api_key:
            if api_key.startswith("sk-"):
                results.append("✅ OpenAI API key format is correct")
            else:
                results.append("❌ OpenAI API key should start with 'sk-'")
        else:
            results.append("⚪ OpenAI API key not provided")
            
        # Test GitHub token format  
        github_token = self.github_token_input.text().strip()
        if github_token:
            if github_token.startswith(("ghp_", "github_pat_")):
                results.append("✅ GitHub token format is correct")
            else:
                results.append("❌ GitHub token should start with 'ghp_' or 'github_pat_'")
        else:
            results.append("⚪ GitHub token not provided")
            
        # Test repository settings
        owner = self.github_owner_input.text().strip()
        repo = self.github_repo_input.text().strip()
        
        if owner and repo:
            results.append(f"✅ Repository configured: {owner}/{repo}")
        elif github_token:
            results.append("❌ GitHub token provided but repository not configured")
        else:
            results.append("⚪ Repository not configured")
            
        self.test_results.setPlainText("\n".join(results))
        
    def skip_setup(self):
        """Skip the setup process"""
        reply = QMessageBox.question(
            self, 
            "Skip Setup?", 
            "Are you sure you want to skip the setup?\n\n"
            "You can configure Research Buddy later through the Configuration menu.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.reject()
            
    def finish_setup(self):
        """Complete the setup process"""
        # Collect configuration
        api_key = self.openai_key_input.text().strip()
        github_token = self.github_token_input.text().strip()
        github_owner = self.github_owner_input.text().strip()
        github_repo = self.github_repo_input.text().strip() or "research-buddy"
        
        # Save repository settings to config file
        from configuration_dialog import save_configuration
        
        config = {
            "github_owner": github_owner,
            "github_repo": github_repo
        }
        
        if save_configuration(config):
            QMessageBox.information(
                self,
                "Setup Complete!",
                "✅ Repository settings saved successfully!\n\n"
                f"📍 Upload destination: https://github.com/{github_owner}/{github_repo}\n\n"
                "🔑 Don't forget to set your environment variables:\n"
                f"• RESEARCH_BUDDY_OPENAI_API_KEY\n"
                f"• RESEARCH_BUDDY_GITHUB_TOKEN\n\n"
                "You can set these in your system or through the Configuration menu."
            )
        
        # Show environment variable instructions if credentials were provided
        if api_key or github_token:
            self.show_environment_instructions(api_key, github_token)
            
        self.accept()
        
    def show_environment_instructions(self, api_key, github_token):
        """Show instructions for setting environment variables"""
        instructions = []
        
        if api_key:
            instructions.append(f"export RESEARCH_BUDDY_OPENAI_API_KEY=\"{api_key}\"")
        if github_token:
            instructions.append(f"export RESEARCH_BUDDY_GITHUB_TOKEN=\"{github_token}\"")
            
        if instructions:
            msg = QMessageBox(self)
            msg.setWindowTitle("Environment Variables Setup")
            msg.setIcon(QMessageBox.Icon.Information)
            msg.setText(
                "🔒 For security, add these lines to your shell configuration:\n\n"
                "macOS/Linux (~/.zshrc or ~/.bashrc):\n"
                + "\n".join(instructions) + "\n\n"
                "Then restart your terminal or run: source ~/.zshrc"
            )
            msg.exec()


def check_first_run():
    """Check if this is the first run and show setup dialog if needed"""
    config_path = Path.home() / ".research_buddy" / "interface_settings.json"
    
    # Check for environment variables
    has_api_key = bool(os.environ.get("RESEARCH_BUDDY_OPENAI_API_KEY"))
    has_github_token = bool(os.environ.get("RESEARCH_BUDDY_GITHUB_TOKEN"))
    
    # Check for config file
    has_config = config_path.exists()
    
    # If no configuration exists at all, show first run dialog
    if not (has_config or has_api_key or has_github_token):
        return True
        
    return False


if __name__ == "__main__":
    # Test the dialog
    from PySide6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    
    dialog = FirstRunSetupDialog()
    if dialog.exec() == QDialog.DialogCode.Accepted:
        print("Setup completed!")
    else:
        print("Setup skipped or cancelled")
        
    app.exec()