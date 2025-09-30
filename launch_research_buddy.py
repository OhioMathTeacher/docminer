#!/usr/bin/env python3
"""
Simple Research Buddy Launcher with Secure Credentials

Just double-click to run Research Buddy with your saved credentials.
"""

import os
import sys
import subprocess
from pathlib import Path
from PySide6.QtWidgets import QApplication, QMessageBox, QInputDialog, QDialog, QVBoxLayout, QLabel, QPushButton

class SimpleCredentialDialog(QDialog):
    """Simple dialog to get credentials and launch Research Buddy"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Research Buddy - Quick Launch")
        self.setModal(True)
        self.resize(400, 200)
        
        layout = QVBoxLayout(self)
        
        # Title
        title = QLabel("🚀 Research Buddy Quick Launch")
        title.setStyleSheet("font-size: 16px; font-weight: bold; margin: 10px;")
        layout.addWidget(title)
        
        # Info
        info = QLabel("Enter your credentials to launch Research Buddy securely.")
        info.setStyleSheet("margin: 10px; color: #666;")
        layout.addWidget(info)
        
        # Buttons
        launch_button = QPushButton("📝 Enter Credentials & Launch")
        launch_button.clicked.connect(self.get_credentials_and_launch)
        launch_button.setStyleSheet("""
            QPushButton {
                background-color: #007bff;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 5px;
                font-weight: bold;
                margin: 5px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
        """)
        layout.addWidget(launch_button)
        
        # Check if we already have saved credentials
        if self.has_saved_credentials():
            quick_launch_button = QPushButton("🚀 Quick Launch (Use Saved Credentials)")
            quick_launch_button.clicked.connect(self.quick_launch)
            quick_launch_button.setStyleSheet("""
                QPushButton {
                    background-color: #28a745;
                    color: white;
                    border: none;
                    padding: 10px;
                    border-radius: 5px;
                    font-weight: bold;
                    margin: 5px;
                }
                QPushButton:hover {
                    background-color: #1e7e34;
                }
            """)
            layout.addWidget(quick_launch_button)
    
    def has_saved_credentials(self):
        """Check if we have saved credentials"""
        env_script = Path.home() / ".research_buddy" / "scripts" / "set_env.sh"
        return env_script.exists()
    
    def get_credentials_and_launch(self):
        """Get credentials from user and launch"""
        from PySide6.QtWidgets import QLineEdit
        
        openai_key, ok1 = QInputDialog.getText(
            self, 
            "OpenAI API Key", 
            "Enter your OpenAI API Key:",
            QLineEdit.EchoMode.Password
        )
        
        if not ok1:
            return
            
        github_token, ok2 = QInputDialog.getText(
            self, 
            "GitHub Token", 
            "Enter your GitHub Personal Access Token (optional):",
            QLineEdit.EchoMode.Password
        )
        
        if not ok2:
            github_token = ""
        
        # Save and launch
        if self.save_credentials(openai_key, github_token):
            self.launch_research_buddy()
        else:
            QMessageBox.warning(self, "Error", "Could not save credentials.")
    
    def quick_launch(self):
        """Launch with existing credentials"""
        self.launch_research_buddy()
    
    def save_credentials(self, openai_key, github_token):
        """Save credentials securely"""
        try:
            # Create secure directory
            script_dir = Path.home() / ".research_buddy" / "scripts"
            script_dir.mkdir(parents=True, exist_ok=True)
            
            # Create environment script
            env_script = script_dir / "set_env.sh"
            
            content = "#!/bin/bash\n"
            if openai_key:
                content += f'export RESEARCH_BUDDY_OPENAI_API_KEY="{openai_key}"\n'
            if github_token:
                content += f'export RESEARCH_BUDDY_GITHUB_TOKEN="{github_token}"\n'
            
            with open(env_script, 'w') as f:
                f.write(content)
            
            # Set secure permissions
            os.chmod(env_script, 0o700)
            return True
            
        except Exception as e:
            print(f"Error saving credentials: {e}")
            return False
    
    def launch_research_buddy(self):
        """Launch Research Buddy with credentials"""
        try:
            # Get paths
            env_script = Path.home() / ".research_buddy" / "scripts" / "set_env.sh"
            app_dir = Path(__file__).parent
            app_script = app_dir / "enhanced_training_interface.py"
            
            # Create launch command that sources env and runs app
            cmd = f'source "{env_script}" && cd "{app_dir}" && python3 "{app_script}"'
            
            # Launch in background
            subprocess.Popen(["/bin/bash", "-c", cmd])
            
            # Show success and close
            QMessageBox.information(self, "Launched!", "Research Buddy is starting...")
            self.accept()
            
        except Exception as e:
            QMessageBox.critical(self, "Launch Error", f"Could not launch Research Buddy: {e}")

def main():
    app = QApplication(sys.argv)
    
    dialog = SimpleCredentialDialog()
    dialog.exec()

if __name__ == "__main__":
    main()