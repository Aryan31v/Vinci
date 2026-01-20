#!/bin/bash
# vinci.sh - The Master Launcher

SCRIPTS_DIR="/storage/emulated/0/Download/Vinci/scripts"

case "$1" in
    "start")
        echo "👻 Starting Vinci Ghost Service (Persistent Mode)..."
        nohup bash "$SCRIPTS_DIR/daemon_ghost.sh" > /dev/null 2>&1 &
        echo "✅ Ghost is alive and watching (Logs: .gemini/tmp/ghost_daemon.log)"
        ;;
    "stop")
        echo "🛑 Stopping Vinci Ghost Service..."
        pkill -f "daemon_ghost.sh"
        pkill -f "ghost_service.py"
        termux-wake-unlock
        echo "✅ Ghost stopped and Wake Lock released."
        ;;
    "ui")
        python "$SCRIPTS_DIR/vinci_tui.py"
        ;;
    *)
        echo "Usage: vinci [start|stop|ui]"
        echo "  start - Start background clipboard monitoring"
        echo "  stop  - Stop background monitoring"
        echo "  ui    - Open the Terminal Command Center"
        ;;
esac
