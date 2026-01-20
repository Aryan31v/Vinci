#!/bin/bash
# scripts/voice_capture.sh
# Quickly capture voice input using native Android dialog

CHAOS_STREAM="/storage/emulated/0/Download/Vinci/1 - 🌀 Chaos Stream.md"

# Trigger native dialog
RESPONSE=$(termux-dialog text -t "Vinci Voice Capture" -i "Say something...")

# Parse JSON response (using simple python one-liner to avoid jq dependency)
TEXT=$(echo "$RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin).get('text', ''))")

if [ -n "$TEXT" ]; then
    TIMESTAMP=$(date +"[%I:%M %p]")
    echo -e "\n- \`$TIMESTAMP\` $TEXT" >> "$CHAOS_STREAM"
    termux-toast "Vinci: Voice Captured"
fi
