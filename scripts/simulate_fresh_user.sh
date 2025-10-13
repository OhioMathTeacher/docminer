#!/bin/bash
# Simulate Fresh User Experience for DocMiner

echo "🎬 Setting up fresh user simulation..."
echo ""

# Step 1: Backup existing config
if [ -d "$HOME/.research_buddy" ]; then
    echo "📦 Backing up your existing config to ~/.research_buddy.BACKUP..."
    rm -rf "$HOME/.research_buddy.BACKUP"
    cp -r "$HOME/.research_buddy" "$HOME/.research_buddy.BACKUP"
    echo "   ✅ Backup created"
fi

# Step 2: Remove current config to simulate fresh install
echo ""
echo "🗑️  Removing current config (simulating first-time user)..."
rm -rf "$HOME/.research_buddy"
echo "   ✅ Config cleared"

# Step 3: Create instructions
echo ""
echo "========================================"
echo "🎬 READY FOR FRESH USER EXPERIENCE!"
echo "========================================"
echo ""
echo "Now you'll see exactly what a new user sees:"
echo ""
echo "1. First launch will show 'GitHub Repository Not Configured' dialog"
echo "   → Enter: Owner = OhioMathTeacher"
echo "   → Enter: Repository = docminer"
echo "   → Click OK"
echo ""
echo "2. If you haven't set environment variables in THIS terminal:"
echo "   → App will warn about missing GitHub token"
echo "   → But you can still use manual mode!"
echo ""
echo "3. To have tokens available, run:"
echo "   source ~/.bashrc"
echo ""
echo "========================================"
echo ""
echo "Press ENTER to launch DocMiner as a fresh user..."
read

echo "🚀 Launching DocMiner..."
echo ""

# Launch with environment loaded
source ~/.bashrc
python3 run_research_buddy.py

# After user closes the app
echo ""
echo "========================================"
echo "🔄 RESTORE YOUR ORIGINAL CONFIG?"
echo "========================================"
echo ""
echo "Press ENTER to restore your backed-up config,"
echo "or Ctrl+C to keep the fresh config..."
read

if [ -d "$HOME/.research_buddy.BACKUP" ]; then
    echo "♻️  Restoring your original config..."
    rm -rf "$HOME/.research_buddy"
    mv "$HOME/.research_buddy.BACKUP" "$HOME/.research_buddy"
    echo "   ✅ Original config restored!"
else
    echo "   ⚠️  No backup found - keeping current config"
fi

echo ""
echo "✅ Done!"
