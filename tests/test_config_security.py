#!/usr/bin/env python3
"""
Test the configuration dialog security
"""

import sys
import os
sys.path.append('/Users/todd/docminer')

from PySide6.QtWidgets import QApplication
from configuration_dialog import ConfigurationDialog

# Set a test environment variable to show masking
os.environ["RESEARCH_BUDDY_OPENAI_API_KEY"] = "sk-test1234567890abcdef"
os.environ["RESEARCH_BUDDY_GITHUB_TOKEN"] = "ghp_test1234567890abcdef"

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    dialog = ConfigurationDialog()
    dialog.show()
    
    sys.exit(app.exec())