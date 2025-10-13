#!/bin/bash
# DocMiner - Simple Startup Script
# This script loads your environment variables and launches DocMiner

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Source environment variables from bashrc
source ~/.bashrc

# Change to the docminer directory
cd "$SCRIPT_DIR"

# Launch DocMiner
echo "🚀 Launching DocMiner..."
python3 run_research_buddy.py

# If Python 3 command fails, try just 'python'
if [ $? -ne 0 ]; then
    echo "Trying alternate Python command..."
    python run_research_buddy.py
fi
