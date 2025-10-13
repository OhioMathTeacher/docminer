#!/bin/bash
#
# AppImage Build Script for DocMiner
# Run this on Linux (tested on Linux Mint / Ubuntu 20.04+)
#
# This script will:
# 1. Install dependencies
# 2. Build the standalone executable with PyInstaller
# 3. Create an AppImage using appimagetool
# 4. Output: DocMiner-5.2-x86_64.AppImage
#

set -e  # Exit on any error

echo "=========================================="
echo "DocMiner AppImage Build Script"
echo "=========================================="
echo ""

# Check if running on Linux
if [[ "$OSTYPE" != "linux-gnu"* ]]; then
    echo "ERROR: This script must be run on Linux"
    exit 1
fi

# Get the script directory and project root
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$( cd "$SCRIPT_DIR/.." && pwd )"

echo "Project root: $PROJECT_ROOT"
echo ""

# Version
VERSION="5.2"
APP_NAME="DocMiner"
FULL_NAME="${APP_NAME}-${VERSION}"

# Check for Python 3
if ! command -v python3 &> /dev/null; then
    echo "ERROR: python3 is required but not found"
    exit 1
fi

echo "Python version: $(python3 --version)"
echo ""

# Create/activate virtual environment
cd "$PROJECT_ROOT"
if [ ! -d "venv_appimage" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv_appimage
fi

echo "Activating virtual environment..."
source venv_appimage/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
pip install pyinstaller

# Clean previous builds
echo ""
echo "Cleaning previous builds..."
rm -rf build dist *.spec

# Build with PyInstaller
echo ""
echo "Building executable with PyInstaller..."
pyinstaller --onefile \
    --name "${APP_NAME}" \
    --icon=docs/icon.png \
    --hidden-import=tiktoken_ext.openai_public \
    --hidden-import=tiktoken_ext \
    --collect-data tiktoken_ext \
    --hidden-import=anthropic \
    --hidden-import=openai \
    --hidden-import=PyPDF2 \
    --collect-all anthropic \
    --collect-all openai \
    run_research_buddy.py

# Verify executable was created
if [ ! -f "dist/${APP_NAME}" ]; then
    echo "ERROR: PyInstaller build failed - executable not found"
    exit 1
fi

echo "Executable built successfully!"

# Download appimagetool if not present
echo ""
echo "Checking for appimagetool..."
if [ ! -f "appimagetool-x86_64.AppImage" ]; then
    echo "Downloading appimagetool..."
    wget -q https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage
    chmod +x appimagetool-x86_64.AppImage
else
    echo "appimagetool already present"
fi

# Create AppDir structure
echo ""
echo "Creating AppDir structure..."
rm -rf AppDir
mkdir -p AppDir/usr/bin
mkdir -p AppDir/usr/share/applications
mkdir -p AppDir/usr/share/icons/hicolor/256x256/apps

# Copy executable
cp "dist/${APP_NAME}" "AppDir/usr/bin/"

# Create .desktop file
cat > "AppDir/${APP_NAME}.desktop" << EOF
[Desktop Entry]
Type=Application
Name=${APP_NAME}
Comment=AI-Powered Research Analysis Tool
Exec=${APP_NAME}
Icon=${APP_NAME}
Categories=Education;Office;
Terminal=false
EOF

# Copy icon (use robot icon)
if [ -f "docs/icon.png" ]; then
    cp docs/icon.png "AppDir/usr/share/icons/hicolor/256x256/apps/${APP_NAME}.png"
    cp docs/icon.png "AppDir/${APP_NAME}.png"
    echo "Using robot icon from docs/icon.png"
elif [ -f "build_files/robot_icon_256x256.png" ]; then
    cp build_files/robot_icon_256x256.png "AppDir/usr/share/icons/hicolor/256x256/apps/${APP_NAME}.png"
    cp build_files/robot_icon_256x256.png "AppDir/${APP_NAME}.png"
    echo "Using robot icon from build_files/robot_icon_256x256.png"
else
    echo "Warning: No icon found, AppImage will have default icon"
fi

# Create AppRun script
cat > AppDir/AppRun << 'EOF'
#!/bin/bash
SELF=$(readlink -f "$0")
HERE=${SELF%/*}
export PATH="${HERE}/usr/bin:${PATH}"
export LD_LIBRARY_PATH="${HERE}/usr/lib:${LD_LIBRARY_PATH}"
exec "${HERE}/usr/bin/DocMiner" "$@"
EOF

chmod +x AppDir/AppRun

# Build AppImage
echo ""
echo "Building AppImage..."
ARCH=x86_64 ./appimagetool-x86_64.AppImage AppDir "${FULL_NAME}-x86_64.AppImage"

# Verify AppImage was created
if [ ! -f "${FULL_NAME}-x86_64.AppImage" ]; then
    echo "ERROR: AppImage creation failed"
    exit 1
fi

# Make it executable
chmod +x "${FULL_NAME}-x86_64.AppImage"

echo ""
echo "=========================================="
echo "SUCCESS!"
echo "=========================================="
echo ""
echo "AppImage created: ${FULL_NAME}-x86_64.AppImage"
echo "Size: $(du -h "${FULL_NAME}-x86_64.AppImage" | cut -f1)"
echo ""
echo "To test, run:"
echo "  ./${FULL_NAME}-x86_64.AppImage"
echo ""
echo "To upload to GitHub release:"
echo "  1. Go to https://github.com/OhioMathTeacher/docminer/releases/tag/v${VERSION}"
echo "  2. Click 'Edit release'"
echo "  3. Upload ${FULL_NAME}-x86_64.AppImage"
echo ""
