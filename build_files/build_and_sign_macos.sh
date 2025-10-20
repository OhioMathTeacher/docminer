#!/bin/bash
set -e

echo "======================================"
echo "Building and Signing DocMiner for macOS"
echo "======================================"

# Configuration
APP_NAME="DocMiner"
VERSION="6.3"
SPEC_FILE="build_files/DocMiner6.3.spec"
DIST_DIR="dist"
APP_BUNDLE="${DIST_DIR}/${APP_NAME}${VERSION}/${APP_NAME}${VERSION}.app"
DMG_NAME="${APP_NAME}-${VERSION}-macOS.dmg"
ENTITLEMENTS="build_files/entitlements.plist"

# Check environment variables
if [ -z "$APPLE_DEVELOPER_ID" ] || [ -z "$APPLE_ID" ] || [ -z "$APPLE_APP_PASSWORD" ] || [ -z "$APPLE_TEAM_ID" ]; then
    echo "ERROR: Required environment variables not set!"
    echo "Please ensure APPLE_DEVELOPER_ID, APPLE_ID, APPLE_APP_PASSWORD, and APPLE_TEAM_ID are set in ~/.zshrc"
    exit 1
fi

# Step 1: Build with PyInstaller
echo ""
echo "Step 1: Building with PyInstaller..."
python3 -m PyInstaller "$SPEC_FILE" --clean --noconfirm

# Step 2: Sign the app bundle
echo ""
echo "Step 2: Code signing the app bundle..."
codesign --deep --force --verify --verbose \
    --sign "$APPLE_DEVELOPER_ID" \
    --options runtime \
    --entitlements "$ENTITLEMENTS" \
    "$APP_BUNDLE"

# Verify the signature
echo ""
echo "Verifying signature..."
codesign --verify --verbose=4 "$APP_BUNDLE"
spctl --assess --verbose=4 --type execute "$APP_BUNDLE"

# Step 3: Create DMG
echo ""
echo "Step 3: Creating DMG..."
if [ -f "$DMG_NAME" ]; then
    rm "$DMG_NAME"
fi

# Create temporary directory for DMG contents
DMG_TEMP_DIR="${DIST_DIR}/dmg_temp"
rm -rf "$DMG_TEMP_DIR"
mkdir -p "$DMG_TEMP_DIR"
cp -R "$APP_BUNDLE" "$DMG_TEMP_DIR/"

# Create the DMG
hdiutil create -volname "$APP_NAME" \
    -srcfolder "$DMG_TEMP_DIR" \
    -ov -format UDZO \
    "$DMG_NAME"

# Clean up temp directory
rm -rf "$DMG_TEMP_DIR"

# Step 4: Sign the DMG
echo ""
echo "Step 4: Code signing the DMG..."
codesign --force --sign "$APPLE_DEVELOPER_ID" "$DMG_NAME"

# Step 5: Notarize the DMG
echo ""
echo "Step 5: Submitting DMG for notarization..."
echo "This may take several minutes..."

xcrun notarytool submit "$DMG_NAME" \
    --apple-id "$APPLE_ID" \
    --password "$APPLE_APP_PASSWORD" \
    --team-id "$APPLE_TEAM_ID" \
    --wait

# Step 6: Staple the notarization ticket
echo ""
echo "Step 6: Stapling notarization ticket to DMG..."
xcrun stapler staple "$DMG_NAME"

# Verify stapling
echo ""
echo "Verifying stapled ticket..."
xcrun stapler validate "$DMG_NAME"

echo ""
echo "======================================"
echo "✅ SUCCESS!"
echo "======================================"
echo "Signed and notarized DMG: $DMG_NAME"
echo ""
echo "You can now distribute this DMG without security warnings!"
