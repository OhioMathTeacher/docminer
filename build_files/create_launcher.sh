#!/bin/bash
# Create a clickable launcher for macOS executable
# This script should be run in the distribution folder after building

cat > "Launch ResearchBuddy.command" << 'EOF'
#!/bin/bash
# ResearchBuddy Launcher for macOS
cd "$(dirname "$0")"
./ResearchBuddy5.1.1
EOF

chmod +x "Launch ResearchBuddy.command"
echo "✅ Created Launch ResearchBuddy.command"
echo "Users can now double-click this file to launch ResearchBuddy"
