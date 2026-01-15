#!/usr/bin/env python3
"""
🧪 System Configuration Validator
--------------------------------
Checks if the vault is healthy and all scripts are functional.
"""

import os
import subprocess
import sys

VAULT_ROOT = "/storage/emulated/0/Download/Vinci"
SCRIPTS_DIR = os.path.join(VAULT_ROOT, "scripts")

REQUIRED_FILES = [
    "1 - 🧠 The Construct/🤖 AI Core/🤖 Prime Directive.md",
    "1 - 🧠 The Construct/🤖 AI Core/🧬 Identity Matrix.md",
    "1 - 🧠 The Construct/🤖 AI Core/🚀 Ignition Sequence.md",
    "1 - 🧠 The Construct/🤖 AI Core/⚙️ System Capabilities.md",
    "1 - 🧠 The Construct/🤖 AI Core/🛠️ System Roadmap.md",
    "0 - 🌌 Central Command.md"
]

REQUIRED_SCRIPTS = [
    "morning_cron.py",
    "yt_notes.py",
    "pdf-notes.sh",
    "anki_generator.py",
    "backup_system.sh"
]

def check_files():
    print("🔍 Checking Core Files...")
    missing = []
    for f in REQUIRED_FILES:
        path = os.path.join(VAULT_ROOT, f)
        if not os.path.exists(path):
            print(f"  ❌ Missing: {f}")
            missing.append(f)
        else:
            print(f"  ✅ Found: {f}")
    return missing

def check_scripts():
    print("\n🔍 Checking Automation Scripts...")
    failures = []
    for s in REQUIRED_SCRIPTS:
        path = os.path.join(SCRIPTS_DIR, s)
        if not os.path.exists(path):
            print(f"  ❌ Missing: {s}")
            failures.append(s)
        elif not os.access(path, os.R_OK):
            print(f"  ⚠️  Not Readable: {s}")
            failures.append(s)
        else:
            print(f"  ✅ Ready: {s}")
    return failures

def check_dependencies():
    print("\n🔍 Checking External Dependencies...")
    deps = ["git", "gemini", "python", "yt-dlp", "pdftotext"]
    for d in deps:
        result = subprocess.run(["type", d], capture_output=True, shell=True)
        if result.returncode == 0:
            print(f"  ✅ {d} is installed.")
        else:
            print(f"  ❌ {d} is NOT found.")

def main():
    print("=== Vinci System Health Check ===\n")
    m_files = check_files()
    f_scripts = check_scripts()
    check_dependencies()
    
    print("\n--- Summary ---")
    if not m_files and not f_scripts:
        print("🟢 SYSTEM HEALTHY. All core protocols active.")
    else:
        print(f"🔴 SYSTEM ISSUES DETECTED: {len(m_files)} files missing, {len(f_scripts)} scripts failing.")
        sys.exit(1)

if __name__ == "__main__":
    main()