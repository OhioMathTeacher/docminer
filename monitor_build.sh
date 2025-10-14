#!/bin/bash
# Build monitor for v6.3.0

RUN_ID="18500155716"
CHECK_INTERVAL=30

echo "🔍 Monitoring build $RUN_ID..."
echo "Checking every ${CHECK_INTERVAL}s"
echo "Press Ctrl+C to stop"
echo ""

while true; do
  STATUS=$(gh run view $RUN_ID --json status --jq '.status' 2>/dev/null)
  
  if [ "$STATUS" = "completed" ]; then
    CONCLUSION=$(gh run view $RUN_ID --json conclusion --jq '.conclusion' 2>/dev/null)
    
    echo ""
    echo "========================================="
    echo "🎉 BUILD COMPLETE!"
    echo "Result: $CONCLUSION"
    echo "========================================="
    echo ""
    
    if [ "$CONCLUSION" = "success" ]; then
      echo "✅ v6.3.0 Release is LIVE!"
      echo ""
      echo "📥 macOS Download (for your 11:30 meeting):"
      echo "https://github.com/OhioMathTeacher/docminer/releases/download/v6.3.0/DocMiner-6.3.0-macOS.dmg"
      echo ""
      echo "All platforms:"
      echo "https://github.com/OhioMathTeacher/docminer/releases/tag/v6.3.0"
      echo ""
      
      # Play a sound (macOS)
      afplay /System/Library/Sounds/Glass.aiff 2>/dev/null
      
      # Show notification
      osascript -e 'display notification "DocMiner v6.3.0 release is ready!" with title "Build Complete ✅"' 2>/dev/null
    else
      echo "❌ Build failed: $CONCLUSION"
      echo "Logs: https://github.com/OhioMathTeacher/docminer/actions/runs/$RUN_ID"
      
      osascript -e 'display notification "Build failed - check logs" with title "Build Failed ❌"' 2>/dev/null
    fi
    
    gh run view $RUN_ID
    exit 0
  else
    ELAPSED=$((SECONDS))
    MINS=$((ELAPSED / 60))
    SECS=$((ELAPSED % 60))
    echo "[$(date '+%H:%M:%S')] Still building... (${MINS}m ${SECS}s) - Status: $STATUS"
    sleep $CHECK_INTERVAL
  fi
done
