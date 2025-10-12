#!/bin/bash
# Research Buddy - Simple Startup Script
# This script loads your environment variables and launches Research Buddy

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Source environment variables from bashrc
source ~/.bashrc

# Change to the research-buddy directory
cd "$SCRIPT_DIR"

# Launch Research Buddy
echo "🚀 Launching Research Buddy..."
python3 run_research_buddy.py

# If Python 3 command fails, try just 'python'
if [ $? -ne 0 ]; then
    echo "Trying alternate Python command..."
    python run_research_buddy.py
fi
