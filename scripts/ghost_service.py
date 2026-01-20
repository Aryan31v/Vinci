import os
import subprocess
import time
import re
from datetime import datetime

# --- Configuration ---
VAULT_ROOT = "/storage/emulated/0/Download/Vinci"
SCRIPTS_DIR = os.path.join(VAULT_ROOT, "scripts")
CENTRAL_CMD = os.path.join(VAULT_ROOT, "0 - 🌌 Central Command.md")
CHAOS_STREAM = os.path.join(VAULT_ROOT, "1 - 🌀 Chaos Stream.md")
GHOST_LOG = os.path.join(VAULT_ROOT, ".gemini/tmp/ghost_service.log")

def get_clipboard():
    try:
        result = subprocess.run(['termux-clipboard-get'], capture_output=True, text=True)
        return result.stdout.strip()
    except Exception as e:
        return ""

def log_event(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(GHOST_LOG, "a") as f:
        f.write(f"[{timestamp}] {message}\n")

def notify(title, message):
    try:
        subprocess.run(["termux-notification", "-t", title, "-c", message, "--priority", "high"])
    except:
        pass

def process_clipboard(text):
    # Pattern: .run [command]
    if text.startswith(".run "):
        cmd = text.replace(".run ", "").strip()
        log_event(f"Executing Remote Command: {cmd}")
        notify("Vinci Ghost", f"🏃 Executing: {cmd}")
        try:
            # Run in shell and capture output
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=VAULT_ROOT)
            output = result.stdout if result.stdout else result.stderr
            if output:
                # Log to chaos stream for record
                timestamp = datetime.now().strftime("[%I:%M %p]")
                with open(CHAOS_STREAM, "a") as f:
                    f.write(f"\n- `{timestamp}` **Remote Command Output:** `{cmd}`\n  ```\n  {output[:500]}\n  ```")
                notify("Vinci Ghost", "✅ Command Executed. Output logged to Chaos.")
            else:
                notify("Vinci Ghost", "✅ Command Executed (No Output).")
        except Exception as e:
            notify("Vinci Ghost", f"❌ Execution Failed: {str(e)}")
        return True

    # Pattern: .todo [text] or .task [text]
    elif text.startswith(".todo ") or text.startswith(".task "):
        if text.startswith(".todo "):
            task = text.replace(".todo ", "").strip()
        else:
            task = text.replace(".task ", "").strip()
            
        log_event(f"Adding Task: {task}")
        # Logic to append to Central Command
        with open(CENTRAL_CMD, "r") as f:
            lines = f.readlines()
        
        new_lines = []
        found_focus = False
        for line in lines:
            new_lines.append(line)
            if "## 📅 Daily Focus (Today)" in line:
                found_focus = True
                new_lines.append(f"- [ ] {task} #captured\n")
        
        if not found_focus:
            new_lines.append(f"\n## 📅 Daily Focus (Today)\n- [ ] {task} #captured\n")
            
        with open(CENTRAL_CMD, "w") as f:
            f.writelines(new_lines)
        notify("Vinci Ghost", f"📝 Task Captured: {task}")
        return True

    # Pattern: .chaos [text]
    elif text.startswith(".chaos "):
        entry = text.replace(".chaos ", "").strip()
        log_event(f"Adding to Chaos Stream: {entry}")
        timestamp = datetime.now().strftime("[%I:%M %p]")
        with open(CHAOS_STREAM, "a") as f:
            f.write(f"\n- `{timestamp}` {entry}")
        notify("Vinci Ghost", "🌀 Logged to Chaos Stream.")
        return True

    return False

def main():
    # Acquire Wake Lock to prevent Android from sleeping the process
    subprocess.run(["termux-wake-lock"])
    log_event("Ghost Service Started (Wake Lock Acquired).")
    
    last_clipboard = get_clipboard()
    
    while True:
        try:
            # 1. Clipboard Check
            current_clipboard = get_clipboard()
            if current_clipboard and current_clipboard != last_clipboard:
                processed = process_clipboard(current_clipboard)
                if processed:
                    subprocess.run(["termux-toast", "Vinci: Action Executed"])
                last_clipboard = current_clipboard
            
            time.sleep(2)
        except KeyboardInterrupt:
            log_event("Ghost Service Stopped.")
            break
        except Exception as e:
            log_event(f"Error: {str(e)}")
            time.sleep(5)

if __name__ == "__main__":
    main()
