import os
import subprocess

SCRIPTS_DIR = "scripts"
REQUIRED_SCRIPTS = [
    "morning_cron.py", "system_sync.py", "analytics_engine.py",
    "validate_system.py", "link_auditor.py", "log_dispatch.py",
    "tag_predictor.py", "yt_notes.py", "pdf-notes.sh",
    "web_notes.py", "camera_scan.sh", "anki_generator.py",
    "webhook_listener.py", "vault_auditor.py", "backup_system.sh",
    "simulator.py", "smart-notes.sh", "canvas_generator.py"
]

def check_scripts():
    print("🔍 Starting System Health Audit...")
    missing = []
    for script in REQUIRED_SCRIPTS:
        path = os.path.join(SCRIPTS_DIR, script)
        if not os.path.exists(path):
            missing.append(script)
            print(f"❌ MISSING: {script}")
        else:
            print(f"✅ FOUND: {script}")
    
    if missing:
        print(f"\n⚠️ AUDIT FAILED: {len(missing)} scripts missing.")
    else:
        print("\n✨ AUDIT PASSED: All core scripts present.")

if __name__ == "__main__":
    check_scripts()
