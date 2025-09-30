#!/usr/bin/env python3
"""
First Run Setup Dialog for Research Buddy 3.1

Clean, direct setup flow: Credentials → Launch Main App
"""

import os
import sys
from pathlib import Path
from PySide6.QtWidgets import (
    QApplication, QDialog, QVBoxLayout, QHBoxLayout, QFormLayout,
    QLineEdit, QPushButton, QLabel, QMessageBox, QTabWidget, QWidget,
    QTextEdit, QGroupBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QIcon

class FirstRunSetupDialog(QDialog):
    """Clean first-run setup dialog"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Welcome to Research Buddy 3.1!")
        self.setModal(True)
        self.resize(800, 600)
        
        # Set simple, readable styling
        self.setStyleSheet("""
            QDialog {
                background-color: #e0e0e0;
            }
            QTabWidget::pane {
                border: 1px solid #999999;
                background-color: #f0f0f0;
                border-radius: 5px;
            }
            QTabBar::tab {
                background-color: #d0d0d0;
                border: 1px solid #999999;
                padding: 8px 16px;
                margin-right: 2px;
                border-radius: 3px 3px 0 0;
                color: black;
            }
            QTabBar::tab:selected {
                background-color: #f0f0f0;
                border-bottom: 1px solid #f0f0f0;
                color: black;
            }
            QTextEdit {
                background-color: #f5f5f5;
                border: 1px solid #999999;
                color: black;
            }
            QGroupBox {
                color: black;
                font-weight: bold;
            }
            QLabel {
                color: black;
            }
            QPushButton {
                background-color: #007bff;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            QPushButton:disabled {
                background-color: #6c757d;
            }
        """)
        
        # Initialize input fields
        self.openai_key_input = None
        self.github_token_input = None
        self.github_owner_input = None
        self.github_repo_input = None
        
        self.setup_ui()
        
    def setup_ui(self):
        """Set up the user interface"""
        layout = QVBoxLayout(self)
        
        # Research Buddy Banner Header
        banner_label = QLabel()
        banner_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        banner_label.setStyleSheet("""
            QLabel {
                background-color: transparent;
                padding: 20px;
                margin: 10px;
            }
        """)
        banner_label.setTextFormat(Qt.TextFormat.RichText)
        banner_label.setText("""
        <div style="text-align: center; background-color: transparent;">
            <div style="font-family: 'Arial Black', Arial; font-size: 48px; font-weight: bold; 
                        color: #1e3a5f; margin-bottom: 5px; text-shadow: 2px 2px 4px rgba(0,0,0,0.1);">
                ResearchBuddy
            </div>
            <div style="font-family: Arial; font-size: 16px; font-weight: bold; 
                        color: #e74c3c; margin-bottom: 15px;">
                Contextual Document Analysis Software for the Rest of Us
            </div>
            <div style="font-family: Arial; font-size: 14px; 
                        color: #34495e; margin-top: 10px;">
                AI-Assisted Positional Analysis with Secure Configuration
            </div>
        </div>
        """)
        layout.addWidget(banner_label)
        
        # Create tabs
        self.tabs = QTabWidget()
        self.tabs.addTab(self.create_welcome_tab(), "Welcome")
        self.tabs.addTab(self.create_credentials_tab(), "Credentials")
        self.tabs.addTab(self.create_repository_tab(), "Repository")
        self.tabs.addTab(self.create_complete_tab(), "Complete")
        layout.addWidget(self.tabs)
        
        # Navigation buttons
        button_layout = QHBoxLayout()
        
        self.skip_button = QPushButton("⏭ Skip Setup")
        self.skip_button.clicked.connect(self.skip_setup)
        button_layout.addWidget(self.skip_button)
        
        button_layout.addStretch()
        
        self.back_button = QPushButton("⬅ Back")
        self.back_button.clicked.connect(self.previous_tab)
        self.back_button.setEnabled(False)
        button_layout.addWidget(self.back_button)
        
        self.next_button = QPushButton("🚀 Start Research Buddy!")
        self.next_button.clicked.connect(self.next_tab)
        button_layout.addWidget(self.next_button)
        
        layout.addLayout(button_layout)
        
    def create_welcome_tab(self):
        """Create welcome tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Simple readable welcome text
        welcome_text = QTextEdit()
        welcome_text.setReadOnly(True)
        welcome_text.setStyleSheet("""
            QTextEdit {
                background-color: #f5f5f5;
                border: 1px solid #999999;
                color: black;
                font-family: Arial;
            }
        """)
        welcome_text.setHtml("""
        <div style="font-family: Arial; line-height: 1.6; color: black;">
        <h2 style="color: #333333;">🎯 What is Research Buddy?</h2>
        <p style="color: black;">Research Buddy helps you analyze research papers using AI to identify:</p>
        <ul style="color: black;">
            <li><strong>Positional claims</strong> and evidence quality</li>
            <li><strong>Research patterns</strong> and methodologies</li>
            <li><strong>Key insights</strong> for systematic reviews</li>
        </ul>
        
        <h2 style="color: #333333;">🔧 Quick Setup</h2>
        <p style="color: black;">We'll configure Research Buddy in just a few steps:</p>
        <ol style="color: black;">
            <li><strong>API Credentials</strong> - Connect to OpenAI for analysis</li>
            <li><strong>Repository Settings</strong> - Configure automatic report uploads</li>
            <li><strong>Launch</strong> - Start analyzing papers immediately</li>
        </ol>
        
        <h2 style="color: #333333;">🛡️ Your Privacy</h2>
        <p style="color: black;">All API keys are stored securely as environment variables - never in plain text files.</p>
        </div>
        """)
        layout.addWidget(welcome_text)
        
        return widget
        
    def create_credentials_tab(self):
        """Create credentials configuration tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # OpenAI section
        openai_group = QGroupBox("OpenAI Configuration")
        openai_layout = QFormLayout(openai_group)
        
        self.openai_key_input = QLineEdit()
        self.openai_key_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.openai_key_input.setPlaceholderText("sk-...")
        openai_layout.addRow("API Key:", self.openai_key_input)
        
        layout.addWidget(openai_group)
        
        # GitHub section  
        github_group = QGroupBox("GitHub Configuration (Optional)")
        github_layout = QFormLayout(github_group)
        
        self.github_token_input = QLineEdit()
        self.github_token_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.github_token_input.setPlaceholderText("ghp_...")
        github_layout.addRow("Personal Access Token:", self.github_token_input)
        
        layout.addWidget(github_group)
        
        layout.addStretch()
        return widget
        
    def create_repository_tab(self):
        """Create repository configuration tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        repo_group = QGroupBox("Report Upload Destination")
        repo_layout = QFormLayout(repo_group)
        
        self.github_owner_input = QLineEdit()
        self.github_owner_input.setText("OhioMathTeacher")
        self.github_owner_input.setPlaceholderText("username or organization")
        repo_layout.addRow("Repository Owner:", self.github_owner_input)
        
        self.github_repo_input = QLineEdit()
        self.github_repo_input.setText("research-buddy")
        self.github_repo_input.setPlaceholderText("repository name")
        repo_layout.addRow("Repository Name:", self.github_repo_input)
        
        layout.addWidget(repo_group)
        layout.addStretch()
        return widget
        
    def create_complete_tab(self):
        """Create completion tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Simple readable completion screen
        complete_text = QTextEdit()
        complete_text.setReadOnly(True)
        complete_text.setStyleSheet("""
            QTextEdit {
                background-color: #f5f5f5;
                border: 1px solid #999999;
                color: black;
                font-family: Arial;
            }
        """)
        complete_text.setHtml("""
        <div style="font-family: Arial; line-height: 1.6; text-align: center; color: black;">
        <h2 style="color: #333333;">🎉 Setup Complete!</h2>
        <p style="color: black; font-size: 16px;"><strong>Research Buddy is ready to analyze research papers!</strong></p>
        
        <h3 style="color: #333333;">✅ What's Configured:</h3>
        <ul style="text-align: left; display: inline-block; color: black;">
            <li>OpenAI API connection for AI analysis</li>
            <li>GitHub integration for report uploads</li>
            <li>Secure credential storage</li>
        </ul>
        
        <h3 style="color: #333333;">🚀 Ready to Start!</h3>
        <p style="color: black;">Click "Launch Research Buddy" to begin analyzing papers.</p>
        </div>
        """)
        layout.addWidget(complete_text)
        
        return widget
        
    def next_tab(self):
        """Move to next tab or finish setup"""
        current = self.tabs.currentIndex()
        
        if current < self.tabs.count() - 1:
            self.tabs.setCurrentIndex(current + 1)
            self.update_navigation()
        else:
            # Finish setup and launch
            self.finish_setup()
            
    def previous_tab(self):
        """Move to previous tab"""
        current = self.tabs.currentIndex()
        if current > 0:
            self.tabs.setCurrentIndex(current - 1)
            self.update_navigation()
            
    def update_navigation(self):
        """Update navigation button states"""
        current = self.tabs.currentIndex()
        total = self.tabs.count()
        
        self.back_button.setEnabled(current > 0)
        
        if current == total - 1:
            self.next_button.setText("🚀 Launch Research Buddy")
        else:
            self.next_button.setText("Next ➡")
            
    def skip_setup(self):
        """Skip the setup process"""
        reply = QMessageBox.question(
            self,
            "Skip Setup?",
            "Are you sure you want to skip the initial setup?\n\n"
            "You can configure Research Buddy later through the Configuration menu.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.reject()
            
    def finish_setup(self):
        """Complete setup and launch Research Buddy"""
        import os
        
        # Get input values
        api_key = self.openai_key_input.text().strip()
        github_token = self.github_token_input.text().strip()
        github_owner = self.github_owner_input.text().strip()
        github_repo = self.github_repo_input.text().strip() or "research-buddy"
        
        # Set environment variables for this session
        if api_key:
            os.environ["RESEARCH_BUDDY_OPENAI_API_KEY"] = api_key
        if github_token:
            os.environ["RESEARCH_BUDDY_GITHUB_TOKEN"] = github_token
        
        # Save repository settings
        from configuration_dialog import save_configuration
        
        config = {
            "github_owner": github_owner,
            "github_repo": github_repo
        }
        
        if save_configuration(config):
            # Show secure setup options
            msg = QMessageBox(self)
            msg.setWindowTitle("Setup Complete!")
            msg.setIcon(QMessageBox.Icon.Information)
            msg.setText(
                "✅ Repository settings saved!\n\n"
                "🔐 For secure API key setup, choose an option:"
            )
            
            secure_button = msg.addButton("Secure Setup", QMessageBox.ButtonRole.AcceptRole)
            manual_button = msg.addButton("Manual Setup", QMessageBox.ButtonRole.ActionRole)
            launch_button = msg.addButton("Launch Now", QMessageBox.ButtonRole.RejectRole)
            
            result = msg.exec()
            clicked_button = msg.clickedButton()
            
            if clicked_button == secure_button:
                # Launch secure setup
                self.launch_secure_setup()
            elif clicked_button == manual_button:
                # Show manual instructions
                self.show_manual_instructions()
            else:
                # Launch directly
                self.launch_main_app()
        else:
            QMessageBox.warning(
                self,
                "Setup Error", 
                "Could not save configuration. Please try again."
            )
            
    def launch_secure_setup(self):
        """Launch the secure environment setup script"""
        import subprocess
        import sys
        import os
        
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            secure_script_path = os.path.join(current_dir, "secure_env_setup.py")
            
            # Launch in a new terminal
            subprocess.run([sys.executable, secure_script_path])
            self.accept()
            
        except Exception as e:
            QMessageBox.warning(self, "Launch Error", f"Could not launch secure setup: {e}")
    
    def show_manual_instructions(self):
        """Show manual setup instructions"""
        msg = QMessageBox(self)
        msg.setWindowTitle("Manual Setup Instructions")
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setText(
            "🔧 Manual Environment Variable Setup:\n\n"
            "1. Open Terminal\n"
            "2. Run these commands:\n\n"
            "export RESEARCH_BUDDY_OPENAI_API_KEY=\"your-openai-key\"\n"
            "export RESEARCH_BUDDY_GITHUB_TOKEN=\"your-github-token\"\n\n"
            "3. Then launch Research Buddy:\n"
            "python3 enhanced_training_interface.py\n\n"
            "💡 These variables will only last for that terminal session."
        )
        msg.exec()
        self.accept()

    def launch_main_app(self):
        """Launch Research Buddy with configured environment"""
        import subprocess
        import sys
        import os
        
        try:
            # Get script directory
            current_dir = os.path.dirname(os.path.abspath(__file__))
            main_app_path = os.path.join(current_dir, "enhanced_training_interface.py")
            
            # Launch with current environment (including our API keys)
            env = os.environ.copy()
            subprocess.Popen([sys.executable, main_app_path], env=env)
            
            # Close setup dialog
            self.accept()
            
        except Exception as e:
            QMessageBox.warning(
                self, 
                "Launch Error", 
                f"Could not launch Research Buddy: {e}"
            )


def check_first_run():
    """Check if this is the first run"""
    import os
    from pathlib import Path
    
    config_path = Path.home() / ".research_buddy" / "interface_settings.json"
    
    # Check for existing configuration
    has_api_key = bool(os.environ.get("RESEARCH_BUDDY_OPENAI_API_KEY"))
    has_github_token = bool(os.environ.get("RESEARCH_BUDDY_GITHUB_TOKEN"))
    has_config = config_path.exists()
    
    # Show setup if no configuration exists
    if not (has_config or has_api_key or has_github_token):
        return True
        
    return False


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    dialog = FirstRunSetupDialog()
    if dialog.exec() == QDialog.DialogCode.Accepted:
        print("Setup completed successfully!")
    else:
        print("Setup was skipped or cancelled.")