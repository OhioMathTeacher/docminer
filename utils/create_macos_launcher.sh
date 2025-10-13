#!/bin/bash
# Quick fix for DocMiner 5.1.1 macOS executable
# This creates a double-clickable launcher for the Unix executable

echo "🔧 DocMiner macOS Launcher Creator"
echo "========================================"
echo ""

# Find the DocMiner executable
if [ -f "./DocMiner5.1.1" ]; then
    EXEC_PATH="./DocMiner5.1.1"
elif [ -f "../DocMiner5.1.1" ]; then
    EXEC_PATH="../DocMiner5.1.1"
else
    echo "❌ Error: Could not find DocMiner5.1.1 executable"
    echo "   Please run this script from the DocMiner5.1.1 folder"
    exit 1
fi

echo "✅ Found executable: $EXEC_PATH"
echo ""

# Create the launcher script
cat > "Launch DocMiner.command" << 'EOF'
#!/bin/bash
# DocMiner Launcher
# This script launches the DocMiner executable

cd "$(dirname "$0")"

# Launch DocMiner
./DocMiner5.1.1

# Keep terminal open if there's an error
if [ $? -ne 0 ]; then
    echo ""
    echo "Press any key to close..."
    read -n 1
fi
EOF

# Make it executable
chmod +x "Launch DocMiner.command"

echo "✅ Created: Launch DocMiner.command"
echo ""
echo "🎉 Done! You can now double-click 'Launch DocMiner.command' to run the app"
echo ""
echo "💡 Tip: If macOS says it can't open it:"
echo "   1. Right-click the file"
echo "   2. Click 'Open'"
echo "   3. Click 'Open' again in the dialog"
echo ""
