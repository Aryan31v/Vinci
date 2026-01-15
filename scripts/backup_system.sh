#!/bin/bash

# backup_system.sh - Snapshot the Vault Configuration & Core Files
# Part of Phase 1: Resilience

BACKUP_DIR="$HOME/storage/shared/Backups/Vinci_Snapshots"
DATE=$(date +%Y%m%d_%H%M%S)
SNAPSHOT_NAME="Vinci_Snapshot_$DATE"
TARGET="$BACKUP_DIR/$SNAPSHOT_NAME"

echo "🛡️ Initiating System Backup: $SNAPSHOT_NAME"

# Create backup directory
mkdir -p "$TARGET"

# 1. Backup Core Brain (AI Core)
echo "🧠 Backing up AI Core..."
mkdir -p "$TARGET/AI_Core"
cp -r "1 - 🧠 The Construct/🤖 AI Core/"* "$TARGET/AI_Core/"

# 2. Backup Contexts (Agents)
echo "👥 Backing up Agent Contexts..."
mkdir -p "$TARGET/Contexts"
cp -r "1 - 🧠 The Construct/🧠 Contexts/"* "$TARGET/Contexts/"

# 3. Backup Scripts
echo "🛠️ Backing up Automation Scripts..."
mkdir -p "$TARGET/scripts"
cp -r "scripts/"* "$TARGET/scripts/"

# 4. Backup Obsidian Config (Settings only, not plugins to save space, or full?)
# User asked for "configurations".
echo "⚙️ Backing up Obsidian Config..."
mkdir -p "$TARGET/Obsidian_Config"
cp .obsidian/*.json "$TARGET/Obsidian_Config/" 2>/dev/null

echo "✅ Backup Complete at: $TARGET"
echo "To restore, copy files back to their original locations."
