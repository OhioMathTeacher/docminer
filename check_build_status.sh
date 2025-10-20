#!/bin/bash
# Quick script to check if v6.3.0 build is complete

echo "🔍 Checking GitHub Actions build status for v6.3.0..."
echo ""
echo "Visit: https://github.com/OhioMathTeacher/docminer/actions"
echo ""
echo "Once build completes:"
echo "1. Verify executables at: https://github.com/OhioMathTeacher/docminer/releases/tag/v6.3.0"
echo "2. Remove this line from README.md:"
echo "   '*Note: Download links will be active once the build completes (~15 minutes after tagging)*'"
echo ""
echo "Commands to update README:"
echo "  cd ~/docminer"
echo "  # Edit README.md and remove the note line"
echo "  git add README.md"
echo "  git commit -m 'Remove build completion note from README'"
echo "  gpush"
