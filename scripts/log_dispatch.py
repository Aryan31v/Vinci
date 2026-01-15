#!/usr/bin/env python3
"""
✒️ Dispatch Logger
------------------
Appends a row to the Dispatch Log.
"""

import sys
import os
import datetime

LOG_FILE = "/storage/emulated/0/Download/Vinci/1 - ⚑ The Construct/🤖 AI Core/📋 Dispatch Log.md"

def log_action(agent, action, status="✅"):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    
    # Escape pipes to prevent breaking table
    action = action.replace("|", "-")
    
    row = f"| {timestamp} | **{agent}** | {action} | {status} |\n"
    
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'w') as f:
            f.write("# ⌛ Agent Dispatch Log\n| Timestamp | Agent | Action | Status |\n| :--- | :--- | :--- | :--- |\n")
            
    with open(LOG_FILE, 'a') as f:
        f.write(row)
    
    print(f"✠️ Logged: {agent} -> {action}")

def main():
    if len(sys.argv) < 3:
        print("Usage: python log_dispatch.py <AgentName> <ActionDescription> [Status]")
        sys.exit(1)
        
    agent = sys.argv[1]
    action = sys.argv[2]
    status = sys.argv[3] if len(sys.argv) > 3 else "✅"
    
    log_action(agent, action, status)

if __name__ == "__main__":
    main()
