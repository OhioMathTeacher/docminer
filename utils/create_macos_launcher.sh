#!/bin/bash
# Quick fix for ResearchBuddy 5.1.1 macOS executable
# This creates a double-clickable launcher for the Unix executable

echo "🔧 ResearchBuddy macOS Launcher Creator"
echo "========================================"
echo ""

# Find the ResearchBuddy executable
if [ -f "./ResearchBuddy5.1.1" ]; then
    EXEC_PATH="./ResearchBuddy5.1.1"
elif [ -f "../ResearchBuddy5.1.1" ]; then
    EXEC_PATH="../ResearchBuddy5.1.1"
else
    echo "❌ Error: Could not find ResearchBuddy5.1.1 executable"
    echo "   Please run this script from the ResearchBuddy5.1.1 folder"
    exit 1
fi

echo "✅ Found executable: $EXEC_PATH"
echo ""

# Create the launcher script
cat > "Launch ResearchBuddy.command" << 'EOF'
#!/bin/bash
# ResearchBuddy Launcher
# This script launches the ResearchBuddy executable

cd "$(dirname "$0")"

# Launch ResearchBuddy
./ResearchBuddy5.1.1

# Keep terminal open if there's an error
if [ $? -ne 0 ]; then
    echo ""
    echo "Press any key to close..."
    read -n 1
fi
EOF

# Make it executable
chmod +x "Launch ResearchBuddy.command"

echo "✅ Created: Launch ResearchBuddy.command"
echo ""
echo "🎉 Done! You can now double-click 'Launch ResearchBuddy.command' to run the app"
echo ""
echo "💡 Tip: If macOS says it can't open it:"
echo "   1. Right-click the file"
echo "   2. Click 'Open'"
echo "   3. Click 'Open' again in the dialog"
echo ""
