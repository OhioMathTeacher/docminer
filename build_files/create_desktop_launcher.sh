#!/bin/bash
# Creates a .desktop launcher file for the Research Buddy AppImage
# This allows users to double-click to launch on any Linux desktop environment

VERSION="5.1.1"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
DESKTOP_FILE="$PROJECT_ROOT/releases/ResearchBuddy-${VERSION}.desktop"
APPIMAGE_PATH="$PROJECT_ROOT/releases/ResearchBuddy-${VERSION}-x86_64.AppImage"

echo "🚀 Creating desktop launcher for Research Buddy ${VERSION}..."

# Create the .desktop file
cat > "$DESKTOP_FILE" << 'EOF'
[Desktop Entry]
Version=1.0
Type=Application
Name=Research Buddy
Comment=Professional Positionality Analysis Interface
Exec=APPIMAGE_PATH_PLACEHOLDER
Icon=research-buddy
Terminal=false
Categories=Education;Science;
StartupNotify=true
EOF

# Replace the placeholder with the actual AppImage path
# Use absolute path so it works from anywhere
ABSOLUTE_APPIMAGE="$(cd "$(dirname "$APPIMAGE_PATH")" && pwd)/$(basename "$APPIMAGE_PATH")"
sed -i "s|APPIMAGE_PATH_PLACEHOLDER|$ABSOLUTE_APPIMAGE|g" "$DESKTOP_FILE"

# Make the desktop file executable
chmod +x "$DESKTOP_FILE"

echo "✅ Desktop launcher created: $DESKTOP_FILE"
echo ""
echo "📋 To use:"
echo "   1. Double-click ResearchBuddy-${VERSION}.desktop to launch the app"
echo "   2. (Optional) Copy to ~/Desktop for a desktop shortcut"
echo "   3. (Optional) Copy to ~/.local/share/applications for system-wide launcher"
echo ""
echo "💡 The .desktop file will be included in the release download"
