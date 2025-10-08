#!/bin/bash
# Local build script for Research Buddy executables
# This builds a macOS .app bundle ready for distribution (Apple Silicon/ARM64)

set -e  # Exit on error

echo "🔨 Building Research Buddy 5.1.1 for macOS (Apple Silicon)..."
echo "=============================================================="
echo "Architecture: $(uname -m)"

# Clean previous builds
echo "🧹 Cleaning previous builds..."
rm -rf build dist releases

# Build the executable
echo "🔧 Building executable..."
python3 -m PyInstaller build_files/ResearchBuddy5.1.1.spec \
    --distpath ./dist \
    --workpath ./build \
    --clean \
    --noconfirm

if [ $? -ne 0 ]; then
    echo "❌ Build failed!"
    exit 1
fi

echo "✅ Build complete!"

# Check what was built
echo ""
echo "📦 Checking architecture..."
file dist/ResearchBuddy5.1.1.app/Contents/MacOS/ResearchBuddy5.1.1

# Create DMG
echo ""
echo "� Creating DMG..."
mkdir -p releases
mkdir -p dmg-temp
cp -R dist/ResearchBuddy5.1.1.app dmg-temp/
ln -s /Applications dmg-temp/Applications

hdiutil create \
    -volname "ResearchBuddy 5.1.1" \
    -srcfolder dmg-temp \
    -ov -format UDZO \
    releases/ResearchBuddy-5.1.1.dmg

rm -rf dmg-temp

echo ""
echo "✅ Apple Silicon DMG created: releases/ResearchBuddy-5.1.1.dmg"
ls -lh releases/

echo ""
echo "🎉 Done! You can now upload this DMG to GitHub releases."
echo ""
echo "To test the app:"
echo "  open dist/ResearchBuddy5.1.1.app"
echo ""
echo "To upload to GitHub releases:"
echo "  gh release upload v5.1.1 releases/ResearchBuddy-5.1.1.dmg --clobber"
