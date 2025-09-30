#!/usr/bin/env python3
"""
Research Buddy - Main Entry Point

A GUI application for analyzing academic papers for positionality statements.
This is the main entry point for running Research Buddy from source.

For production use, see the pre-built app in releases:
https://github.com/OhioMathTeacher/research-buddy/releases

Usage:
    python run_research_buddy.py

Requirements:
    - Python 3.11+
    - See requirements.txt for dependencies
"""

import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Import and run the main application
from enhanced_training_interface import main

if __name__ == "__main__":
    main()