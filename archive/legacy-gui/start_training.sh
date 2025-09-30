#!/bin/bash
# 🎓 Launch Enhanced Training Interface
# Simple launcher script for Graduate Assistant

echo "🎓 Starting Search Buddy Training Interface..."
echo "📖 Enhanced PDF Viewer Version"
echo ""

# Navigate to project directory
cd "$(dirname "$0")"

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Check if required packages are installed
echo "🔍 Checking dependencies..."
python -c "import PySide6, fitz; print('✅ All dependencies ready')" || {
    echo "❌ Missing dependencies. Installing..."
    pip install PySide6 PyMuPDF
}

# Launch the enhanced interface
echo "🚀 Launching training interface..."
echo ""
echo "📋 Instructions:"
echo "   1. Click 'Select PDF Folder' to choose your papers"
echo "   2. Use the PDF viewer to read each paper"
echo "   3. Label using the controls on the right"
echo "   4. Click 'Save & Next' to continue"
echo "   5. Export data when finished"
echo ""

python enhanced_training_interface.py

echo ""
echo "✅ Training session complete!"
echo "📊 Check training_data.json for saved labels"
echo "📈 Use training_analysis.py to analyze results"