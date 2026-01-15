#!/bin/bash
# Phase 4: Redundant Sync Script
# To be run every 4 hours or manually for quick backup.

VAULT_ROOT="/storage/emulated/0/Download/Vinci"
cd "$VAULT_ROOT"

echo "🔄 Running Redundant Sync..."
git add .
timestamp=$(date +"%Y-%m-%d %H:%M")
git commit -m "Redundant sync: $timestamp"

# If a remote is configured, push changes
if git remote | grep -q 'origin'; then
    echo "📤 Pushing to remote..."
    git push origin main
else
    echo "ℹ️ No remote 'origin' found. Skipping push."
fi

echo "✅ Redundant Sync Complete."
