#!/bin/bash
# Create an AppImage for ResearchBuddy on Linux
# This creates a portable Linux application that runs on most distros

set -e

VERSION="5.1.1"
APP_NAME="ResearchBuddy"
APP_DIR="${APP_NAME}.AppDir"

echo "🐧 Creating AppImage for ResearchBuddy ${VERSION}"
echo "================================================"
echo ""

# Check if we're on Linux
if [[ "$OSTYPE" != "linux-gnu"* ]]; then
    echo "❌ Error: AppImage can only be built on Linux"
    echo "   Run this on a Linux machine or use GitHub Actions"
    exit 1
fi

# Check if the executable exists
if [ ! -f "dist/ResearchBuddy5.1.1/ResearchBuddy5.1.1" ]; then
    echo "❌ Error: dist/ResearchBuddy5.1.1/ResearchBuddy5.1.1 not found"
    echo "   Please build the executable first with:"
    echo "   python -m PyInstaller build_files/ResearchBuddy5.1.1.spec --clean --noconfirm"
    exit 1
fi

echo "✅ Found executable"

# Create AppDir structure
rm -rf "$APP_DIR"
mkdir -p "$APP_DIR/usr/bin"
mkdir -p "$APP_DIR/usr/share/applications"
mkdir -p "$APP_DIR/usr/share/icons/hicolor/256x256/apps"
mkdir -p "$APP_DIR/usr/share/doc/$APP_NAME"

echo "📦 Creating AppDir structure..."

# Copy the entire dist folder contents
cp -r dist/ResearchBuddy5.1.1/* "$APP_DIR/usr/bin/"
echo "   ✅ Copied application files"

# Create desktop file
cat > "$APP_DIR/usr/share/applications/${APP_NAME}.desktop" << EOF
[Desktop Entry]
Type=Application
Name=Research Buddy
Comment=Professional Positionality Analysis Interface
Exec=ResearchBuddy5.1.1
Icon=researchbuddy
Categories=Education;Science;Office;
Terminal=false
EOF
echo "   ✅ Created desktop file"

# Create a simple icon (you can replace this with a real PNG later)
# For now, create a placeholder
if [ ! -f "icon.png" ]; then
    echo "   ⚠️  No icon.png found - using placeholder"
    # Create a simple colored square as placeholder
    convert -size 256x256 xc:#4A90E2 -font DejaVu-Sans -pointsize 72 \
            -fill white -gravity center -annotate +0+0 "RB" \
            "$APP_DIR/usr/share/icons/hicolor/256x256/apps/researchbuddy.png" 2>/dev/null || \
    echo "   (ImageMagick not installed - skipping icon)"
else
    cp icon.png "$APP_DIR/usr/share/icons/hicolor/256x256/apps/researchbuddy.png"
    echo "   ✅ Copied icon"
fi

# Create AppRun script
cat > "$APP_DIR/AppRun" << 'EOF'
#!/bin/bash
# AppRun script for ResearchBuddy

SELF=$(readlink -f "$0")
HERE=${SELF%/*}

# Export library paths
export LD_LIBRARY_PATH="${HERE}/usr/bin:${LD_LIBRARY_PATH}"
export PATH="${HERE}/usr/bin:${PATH}"

# Run the application
exec "${HERE}/usr/bin/ResearchBuddy5.1.1" "$@"
EOF

chmod +x "$APP_DIR/AppRun"
echo "   ✅ Created AppRun script"

# Create symlinks for AppImage standard
ln -sf usr/share/applications/${APP_NAME}.desktop "$APP_DIR/"
ln -sf usr/share/icons/hicolor/256x256/apps/researchbuddy.png "$APP_DIR/"
ln -sf usr/share/icons/hicolor/256x256/apps/researchbuddy.png "$APP_DIR/.DirIcon"

# Download appimagetool if not present
APPIMAGETOOL="appimagetool-x86_64.AppImage"
if [ ! -f "$APPIMAGETOOL" ]; then
    echo ""
    echo "📥 Downloading appimagetool..."
    wget -q "https://github.com/AppImage/AppImageKit/releases/download/continuous/$APPIMAGETOOL"
    chmod +x "$APPIMAGETOOL"
    echo "   ✅ Downloaded appimagetool"
fi

# Create the AppImage
echo ""
echo "🔨 Building AppImage..."
ARCH=x86_64 ./$APPIMAGETOOL "$APP_DIR" "ResearchBuddy-${VERSION}-x86_64.AppImage"

# Clean up
rm -rf "$APP_DIR"

echo ""
echo "🎉 SUCCESS! AppImage created!"
echo "=============================================="
echo "   📦 File: ResearchBuddy-${VERSION}-x86_64.AppImage"
echo "   💾 Size: $(du -h ResearchBuddy-${VERSION}-x86_64.AppImage | cut -f1)"
echo ""
echo "🧪 To test:"
echo "   chmod +x ResearchBuddy-${VERSION}-x86_64.AppImage"
echo "   ./ResearchBuddy-${VERSION}-x86_64.AppImage"
echo ""
echo "🚀 Users can run this on any Linux distro!"
