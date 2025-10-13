#!/bin/bash
# Test configuration script for DocMiner

echo "🔍 Testing DocMiner Configuration"
echo "========================================"
echo ""

# Source bashrc to get environment variables
source ~/.bashrc

echo "1. Environment Variables Check:"
echo "   OPENAI_API_KEY: ${OPENAI_API_KEY:+✅ Set (${#OPENAI_API_KEY} chars)}"
echo "   RESEARCH_BUDDY_OPENAI_API_KEY: ${RESEARCH_BUDDY_OPENAI_API_KEY:+✅ Set (${#RESEARCH_BUDDY_OPENAI_API_KEY} chars)}"
echo "   RESEARCH_BUDDY_GITHUB_TOKEN: ${RESEARCH_BUDDY_GITHUB_TOKEN:+✅ Set (${#RESEARCH_BUDDY_GITHUB_TOKEN} chars)}"
echo ""

# If RESEARCH_BUDDY vars not set but OPENAI_API_KEY is, use that for testing
if [ -z "$RESEARCH_BUDDY_OPENAI_API_KEY" ] && [ -n "$OPENAI_API_KEY" ]; then
    echo "⚠️  Note: RESEARCH_BUDDY_OPENAI_API_KEY not set, but OPENAI_API_KEY is available"
    echo "   You can use OPENAI_API_KEY or set RESEARCH_BUDDY_OPENAI_API_KEY"
fi
echo ""

echo "2. Config Directory Check:"
if [ -d "$HOME/.research_buddy" ]; then
    echo "   ✅ ~/.research_buddy directory exists"
    echo "   Contents:"
    ls -la ~/.research_buddy/ | tail -n +4 | awk '{print "      " $9}'
else
    echo "   ❌ ~/.research_buddy directory does NOT exist"
fi
echo ""

echo "3. Config File Check:"
if [ -f "$HOME/.research_buddy/interface_settings.json" ]; then
    echo "   ✅ interface_settings.json exists"
    echo "   Contents:"
    cat ~/.research_buddy/interface_settings.json | sed 's/^/      /'
else
    echo "   ❌ interface_settings.json does NOT exist"
fi
echo ""

echo "4. Startup Script Check:"
if [ -f "./start_research_buddy.sh" ]; then
    if [ -x "./start_research_buddy.sh" ]; then
        echo "   ✅ start_research_buddy.sh exists and is executable"
    else
        echo "   ⚠️  start_research_buddy.sh exists but is NOT executable"
        echo "      Run: chmod +x start_research_buddy.sh"
    fi
else
    echo "   ❌ start_research_buddy.sh does NOT exist"
fi
echo ""

echo "5. Python Check:"
if command -v python3 &> /dev/null; then
    echo "   ✅ python3 found: $(python3 --version)"
else
    echo "   ❌ python3 NOT found"
fi
echo ""

echo "========================================"
echo "Test Complete!"
echo ""
echo "To fix missing environment variables, edit ~/.bashrc:"
echo "  nano ~/.bashrc"
echo "Then reload with:"
echo "  source ~/.bashrc"
