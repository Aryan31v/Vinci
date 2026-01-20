#!/bin/bash
# scripts/daemon_ghost.sh
# Supervisor script to keep ghost_service.py running persistently

LOG_FILE="/storage/emulated/0/Download/Vinci/.gemini/tmp/ghost_daemon.log"
SCRIPT_PATH="/storage/emulated/0/Download/Vinci/scripts/ghost_service.py"

# Ensure directory exists
mkdir -p "$(dirname "$LOG_FILE")"

echo "--- Daemon Started at $(date) ---" >> "$LOG_FILE"

# Acquire wake lock immediately
termux-wake-lock
echo "Wake lock acquired." >> "$LOG_FILE"

while true; do
    echo "Starting Ghost Service instance..." >> "$LOG_FILE"
    
    # Run the python script
    # We allow it to print to the log
    python "$SCRIPT_PATH" >> "$LOG_FILE" 2>&1
    
    EXIT_CODE=$?
    echo "Ghost Service instance exited with code $EXIT_CODE at $(date)" >> "$LOG_FILE"
    
    # Prevent tight loop if script crashes instantly
    sleep 5
done
