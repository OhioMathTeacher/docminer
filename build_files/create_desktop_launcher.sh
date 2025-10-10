#!/bin/bash
# Creates a .desktop launcher file for the Research Buddy AppImage
# This allows users to double-click to launch on any Linux desktop environment

set -e

VERSION="5.1.1"
OUTPUT_DIR="releases"
DESKTOP_FILE="$OUTPUT_DIR/ResearchBuddy-${VERSION}.desktop"

echo "🚀 Creating desktop launcher for Research Buddy ${VERSION}..."

# Create the .desktop file
cat > "$DESKTOP_FILE" << 'EOF'
[Desktop Entry]
Version=1.0
Type=Application
Name=Research Buddy
Comment=Professional Positionality Analysis Interface
Exec=./ResearchBuddy-5.1.1-x86_64.AppImage
Icon=research-buddy
Terminal=false
Categories=Education;Science;
StartupNotify=true
EOF

# Make the desktop file executable
chmod +x "$DESKTOP_FILE"

echo "✅ Desktop launcher created: $DESKTOP_FILE"
echo ""
echo "📋 To use:"
echo "   1. Keep .desktop and .AppImage files in same folder"
echo "   2. Double-click ResearchBuddy-${VERSION}.desktop to launch"
