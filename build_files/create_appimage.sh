#!/bin/bash
# Create an AppImage for ResearchBuddy on Linux
# This creates a portable Linux application that runs on most distros

set -e

VERSION="5.1.1"
APP_NAME="ResearchBuddy"
APP_DIR="${APP_NAME}.AppDir"
OUTPUT_DIR="releases"

echo "🐧 Creating AppImage for ResearchBuddy ${VERSION}"
echo "================================================"
echo ""

# Create output directory
mkdir -p "$OUTPUT_DIR"

# Check if the executable exists
if [ ! -f "dist/ResearchBuddy5.1.1/ResearchBuddy5.1.1" ]; then
    echo "❌ Error: dist/ResearchBuddy5.1.1/ResearchBuddy5.1.1 not found"
    exit 1
fi

echo "✅ Found executable"

# Create AppDir structure
rm -rf "$APP_DIR"
mkdir -p "$APP_DIR/usr/bin"
mkdir -p "$APP_DIR/usr/share/applications"
mkdir -p "$APP_DIR/usr/share/icons/hicolor/256x256/apps"

echo "📦 Creating AppDir structure..."

# Copy the entire dist folder contents
cp -r dist/ResearchBuddy5.1.1/* "$APP_DIR/usr/bin/"
echo "   ✅ Copied application files"

# Create desktop file
cat > "$APP_DIR/${APP_NAME}.desktop" << 'EOF'
[Desktop Entry]
Type=Application
Name=Research Buddy
Comment=Professional Positionality Analysis Interface
Exec=ResearchBuddy5.1.1
Icon=researchbuddy
Categories=Education;Science;Office;
Terminal=false
EOF

cp "$APP_DIR/${APP_NAME}.desktop" "$APP_DIR/usr/share/applications/"
echo "   ✅ Created desktop file"

# Create a simple placeholder icon (1x1 pixel PNG)
echo 'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg==' | base64 -d > "$APP_DIR/researchbuddy.png"
cp "$APP_DIR/researchbuddy.png" "$APP_DIR/usr/share/icons/hicolor/256x256/apps/"
cp "$APP_DIR/researchbuddy.png" "$APP_DIR/.DirIcon"
echo "   ✅ Created icon"

# Create AppRun script
cat > "$APP_DIR/AppRun" << 'EOF'
#!/bin/bash
SELF=$(readlink -f "$0")
HERE=${SELF%/*}
export LD_LIBRARY_PATH="${HERE}/usr/bin:${LD_LIBRARY_PATH}"
export PATH="${HERE}/usr/bin:${PATH}"
exec "${HERE}/usr/bin/ResearchBuddy5.1.1" "$@"
EOF

chmod +x "$APP_DIR/AppRun"
echo "   ✅ Created AppRun script"

# Download and extract appimagetool (no FUSE needed)
APPIMAGETOOL="appimagetool-x86_64.AppImage"
if [ ! -f "$APPIMAGETOOL" ]; then
    echo ""
    echo "📥 Downloading appimagetool..."
    wget -q "https://github.com/AppImage/AppImageKit/releases/download/continuous/$APPIMAGETOOL"
    chmod +x "$APPIMAGETOOL"
    echo "   ✅ Downloaded appimagetool"
fi

# Extract appimagetool to avoid FUSE requirement on GitHub Actions
if [ ! -d "squashfs-root" ]; then
    echo "📦 Extracting appimagetool..."
    ./$APPIMAGETOOL --appimage-extract > /dev/null 2>&1
    echo "   ✅ Extracted"
fi

# Create the AppImage
echo ""
echo "🔨 Building AppImage..."
ARCH=x86_64 ./squashfs-root/AppRun "$APP_DIR" "$OUTPUT_DIR/ResearchBuddy-${VERSION}-x86_64.AppImage"

if [ -f "$OUTPUT_DIR/ResearchBuddy-${VERSION}-x86_64.AppImage" ]; then
    chmod +x "$OUTPUT_DIR/ResearchBuddy-${VERSION}-x86_64.AppImage"
    echo ""
    echo "🎉 SUCCESS! AppImage created!"
    echo "=============================================="
    echo "   📦 File: $OUTPUT_DIR/ResearchBuddy-${VERSION}-x86_64.AppImage"
    echo "   💾 Size: $(du -h $OUTPUT_DIR/ResearchBuddy-${VERSION}-x86_64.AppImage | cut -f1)"
    echo ""
else
    echo "❌ AppImage creation failed"
    exit 1
fi

# Clean up
rm -rf "$APP_DIR"
echo "✅ Cleaned up temporary files"
