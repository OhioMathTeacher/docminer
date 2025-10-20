#!/bin/bash
# Upload DocMiner-6.3 AppImage to GitHub release v6.3.0
# This uses the GitHub CLI (gh)

echo "📤 Uploading AppImage to GitHub Release v6.3.0"
echo "=============================================="
echo ""

if ! command -v gh &> /dev/null; then
    echo "❌ GitHub CLI (gh) not found"
    echo ""
    echo "Please install it:"
    echo "  Ubuntu/Debian: sudo apt install gh"
    echo "  Or visit: https://cli.github.com/"
    echo ""
    echo "Then authenticate: gh auth login"
    exit 1
fi

if [ ! -f "DocMiner-6.3-x86_64.AppImage" ]; then
    echo "❌ DocMiner-6.3-x86_64.AppImage not found in current directory"
    exit 1
fi

echo "✅ Found AppImage ($(du -h DocMiner-6.3-x86_64.AppImage | cut -f1))"
echo ""
echo "Uploading to release v6.3.0..."

gh release upload v6.3.0 DocMiner-6.3-x86_64.AppImage --clobber

if [ $? -eq 0 ]; then
    echo ""
    echo "🎉 SUCCESS! AppImage uploaded to:"
    echo "   https://github.com/OhioMathTeacher/docminer/releases/tag/v6.3.0"
else
    echo ""
    echo "❌ Upload failed. You may need to:"
    echo "   1. Authenticate: gh auth login"
    echo "   2. Check you have write access to the repository"
fi
