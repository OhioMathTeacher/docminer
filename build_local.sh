#!/bin/bash
# Local build script for Research Buddy executables
# This builds a macOS .app bundle ready for distribution

set -e  # Exit on error

echo "🔨 Building Research Buddy 5.1.1 for macOS..."
echo "================================================"

# Activate virtual environment
source .venv/bin/activate

# Clean previous builds
echo "🧹 Cleaning previous builds..."
rm -rf build dist

# Build the executable
echo "🔧 Building executable..."
python -m PyInstaller build_files/ResearchBuddy5.1.1.spec --distpath ./dist --workpath ./build --clean

# Create release package
echo "📦 Creating release package..."
mkdir -p releases
cp -r dist/ResearchBuddy5.1.1.app releases/

# Copy documentation
cp README.md releases/
cp docs/QUICK_START_FOR_GAS.md releases/ 2>/dev/null || echo "Quick start guide not found"

# Create ZIP archive
echo "🗜️  Creating ZIP archive..."
cd releases
zip -r ResearchBuddy5.1.1-macos.zip ResearchBuddy5.1.1.app README.md QUICK_START_FOR_GAS.md 2>/dev/null || zip -r ResearchBuddy5.1.1-macos.zip ResearchBuddy5.1.1.app README.md
cd ..

echo "✅ Build complete!"
echo "📍 Package location: releases/ResearchBuddy5.1.1-macos.zip"
echo ""
echo "To test the app:"
echo "  open dist/ResearchBuddy5.1.1.app"
echo ""
echo "To upload to GitHub releases:"
echo "  1. Go to https://github.com/OhioMathTeacher/research-buddy/releases"
echo "  2. Click 'Draft a new release'"
echo "  3. Upload releases/ResearchBuddy5.1.1-macos.zip"
