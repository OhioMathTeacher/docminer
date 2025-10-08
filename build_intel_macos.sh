#!/bin/bash
# Build Intel macOS version of Research Buddy 5.1.1

echo "🔨 Building Intel macOS version..."
echo "Architecture: $(uname -m)"

# Build with PyInstaller
python3 -m PyInstaller build_files/ResearchBuddy5.1.1.spec \
    --distpath ./dist-intel \
    --workpath ./build-intel \
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
file dist-intel/ResearchBuddy5.1.1.app/Contents/MacOS/ResearchBuddy5.1.1

# Create DMG
echo ""
echo "📀 Creating DMG..."
mkdir -p releases-intel
mkdir -p dmg-temp-intel
cp -R dist-intel/ResearchBuddy5.1.1.app dmg-temp-intel/
ln -s /Applications dmg-temp-intel/Applications

hdiutil create \
    -volname "ResearchBuddy 5.1.1 Intel" \
    -srcfolder dmg-temp-intel \
    -ov -format UDZO \
    releases-intel/ResearchBuddy-5.1.1-macos-intel.dmg

rm -rf dmg-temp-intel

echo ""
echo "✅ Intel DMG created: releases-intel/ResearchBuddy-5.1.1-macos-intel.dmg"
ls -lh releases-intel/

echo ""
echo "🎉 Done! You can now upload this DMG to GitHub releases."
