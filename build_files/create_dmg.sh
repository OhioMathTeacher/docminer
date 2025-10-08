#!/bin/bash
# Create a professional DMG for ResearchBuddy
# This creates the standard macOS installation experience:
# - Double-click DMG to mount
# - Drag .app to Applications folder
# - Done!

set -e  # Exit on error

VERSION="5.1.1"
APP_NAME="ResearchBuddy${VERSION}.app"
DMG_NAME="ResearchBuddy-${VERSION}.dmg"
VOLUME_NAME="ResearchBuddy ${VERSION}"

echo "🔨 Creating DMG for ResearchBuddy ${VERSION}"
echo "=============================================="
echo ""

# Check if .app exists
if [ ! -d "dist/${APP_NAME}" ]; then
    echo "❌ Error: dist/${APP_NAME} not found"
    echo "   Please build the app first with:"
    echo "   python -m PyInstaller build_files/ResearchBuddy5.1.1.spec --clean --noconfirm"
    exit 1
fi

echo "✅ Found: dist/${APP_NAME}"

# Create temporary directory for DMG contents
DMG_TEMP="dmg-temp"
rm -rf "${DMG_TEMP}"
mkdir -p "${DMG_TEMP}"

echo "📦 Preparing DMG contents..."

# Copy the .app bundle
cp -R "dist/${APP_NAME}" "${DMG_TEMP}/"
echo "   ✅ Copied ${APP_NAME}"

# Create a symbolic link to /Applications
# This gives users the visual cue to drag the app there
ln -s /Applications "${DMG_TEMP}/Applications"
echo "   ✅ Created Applications symlink"

# Optional: Copy README or Quick Start guide
if [ -f "docs/QUICK_START_FOR_GAS.md" ]; then
    cp "docs/QUICK_START_FOR_GAS.md" "${DMG_TEMP}/Quick Start Guide.md"
    echo "   ✅ Added Quick Start Guide"
fi

# Create the DMG
echo ""
echo "🎨 Creating DMG image..."
hdiutil create \
    -volname "${VOLUME_NAME}" \
    -srcfolder "${DMG_TEMP}" \
    -ov \
    -format UDZO \
    "${DMG_NAME}"

# Clean up temp directory
rm -rf "${DMG_TEMP}"

# Get DMG size
DMG_SIZE=$(du -h "${DMG_NAME}" | cut -f1)

echo ""
echo "🎉 SUCCESS! DMG created successfully!"
echo "=============================================="
echo "   📦 File: ${DMG_NAME}"
echo "   💾 Size: ${DMG_SIZE}"
echo ""
echo "📍 Location: $(pwd)/${DMG_NAME}"
echo ""
echo "🧪 To test:"
echo "   1. Double-click ${DMG_NAME}"
echo "   2. Drag ResearchBuddy${VERSION}.app to Applications"
echo "   3. Open from Applications folder"
echo ""
echo "🚀 Ready for distribution!"
