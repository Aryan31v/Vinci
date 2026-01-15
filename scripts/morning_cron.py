#!/usr/bin/env python3
"""
🌅 Morning Cron Protocol v2.2
------------------------
1. Git Sync (Auto-commit state)
2. Journal Generation (Daily Template + Zombie Task Migration)
3. Sunday Archival (Move old journal entries)
4. System Health Check
5. Chaos/Input Stream Audit
"""

import os
import datetime
import subprocess
import sys
import re

# --- Configuration ---
VAULT_ROOT = "/storage/emulated/0/Download/Vinci"
SCRIPTS_DIR = os.path.join(VAULT_ROOT, "scripts")
SAGA_DIR = os.path.join(VAULT_ROOT, "1 - 🧠 The Construct/📜 The Saga")
TIME_CAPSULE = os.path.join(SAGA_DIR, "🕰️ Time Capsule.md")
CHAOS_PATH = os.path.join(VAULT_ROOT, "1 - 🧠 The Construct/1 - 🌀 Chaos Stream.md")

def run_command(cmd):
    """Run shell command and return output."""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=VAULT_ROOT)
        return result.stdout.strip(), result.returncode
    except Exception as e:
        return str(e), 1

def git_sync():
    print("🐙 [Git] Synchronizing Vault state...")
    run_command("git add .")
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    msg = f"Auto-sync: {timestamp}"
    out, code = run_command(f'git commit -m "{msg}"')
    if code == 0:
        print(f"  ✅ Changes committed: {msg}")
        print("  ☁️  Pushing to GitHub...")
        p_out, p_code = run_command("git push origin main")
        if p_code == 0:
            print("  ✅ Cloud Sync Complete.")
        else:
            print(f"  ❌ Cloud Sync Failed: {p_out}")
    else:
        print("  ℹ️  Nothing to commit (clean working tree).")

def extract_zombie_tasks(content):
    """
    Scans the journal content for the *previous* day's entry and extracts unchecked tasks.
    Assumes Reverse Chronological Order (Today is top).
    """
    lines = content.split('\n')
    zombie_tasks = []
    capture_mode = False
    
    # We want to find the FIRST occurrence of "## 📅" that is NOT today (because today doesn't exist yet in the file being read)
    # Actually, the file contains YESTERDAY as the top entry.
    # So we start capturing from the first header found.
    
    for line in lines:
        if line.startswith("## 📅"):
            capture_mode = True # Start scanning the most recent entry
        elif line.startswith("## 📅") and capture_mode:
            break # Stop when we hit the day BEFORE yesterday
            
        if capture_mode:
            # Regex for unchecked task: "- [ ] " or "- [ ]"
            if re.match(r'^\s*-\s*\[\s*\]', line):
                # Clean up the line (remove indentation for re-injection)
                clean_task = line.strip()
                zombie_tasks.append(clean_task)
                
    return zombie_tasks

def generate_daily_entry(today_date, zombie_tasks=None):
    """Creates the standard daily template with Mood Tracking and Migrated Tasks."""
    human_date = today_date.strftime("%A, %d")
    
    backlog_section = ""
    if zombie_tasks:
        backlog_list = "\n".join([f"    {task}" for task in zombie_tasks]) # Indent for callout
        backlog_section = f"""

> [!todo] Backlog (Migrated)
{backlog_list}
"""

    entry = f"""

## 📅 {human_date} (Today)
> [!quote] Daily Focus
> *Pending User Command.*

### 🧠 Mind Stream
> [!energy] Status Check
> **Energy:** [?/10] | **Mood:** [?/10]

> [!abstract] Random Thoughts
> - `[08:00 AM]` **Morning Protocol:** System initialized via Morning Cron.

### 📋 Action Plan
> [!todo] To-Do List
- [ ] 
{backlog_section}
---
"""
    return entry

def update_journal():
    """Ensures today's entry exists in the monthly journal file and migrates tasks."""
    today = datetime.date.today()
    month_name = today.strftime("%B")
    year_month = today.strftime("%Y-%m")
    journal_path = os.path.join(SAGA_DIR, f"{year_month}-{month_name}.md")
    
    # Create month file if it doesn't exist
    if not os.path.exists(journal_path):
        print(f"🆕 Creating new Month Journal: {journal_path}")
        with open(journal_path, 'w', encoding='utf-8') as f:
            f.write(f"# ❄️ {month_name} {today.year}\n> *\"The trial of you vs you.\"*\n\n---")
    
    # Read content
    with open(journal_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    today_header = f"## 📅 {today.strftime('%A, %d')}"
    
    if today_header in content:
        print("✅ Today's journal entry already exists.")
    else:
        print("📝 Generating new Daily Entry...")
        
        # 🧠 Zombie Task Logic
        zombies = extract_zombie_tasks(content)
        if zombies:
            print(f"  🧟 Found {len(zombies)} zombie tasks from yesterday. Migrating...")
        
        new_entry = generate_daily_entry(today, zombies)
        
        # Insert after the first separator (Month header)
        parts = content.split("---", 1)
        
        if len(parts) > 1:
            updated_content = parts[0] + "---" + new_entry + parts[1]
        else:
            updated_content = content + "\n" + new_entry
            
        with open(journal_path, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        print("✅ Daily entry added with migrated tasks.")

def run_archival():
    """Moves entries older than 7 days to the Time Capsule on Sundays."""
    today = datetime.date.today()
    if today.weekday() != 6: # 6 is Sunday
        return

    print("🧹 [Maintenance] Sunday detected. Running archival & backup protocol...")
    
    # Run Backup
    run_command("bash scripts/backup_system.sh")
    
    # Get all journal files...
    month_name = today.strftime("%B")
    year_month = today.strftime("%Y-%m")
    journal_path = os.path.join(SAGA_DIR, f"{year_month}-{month_name}.md")
    
    if not os.path.exists(journal_path): return

    with open(journal_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    days = []
    current_day = []
    header_found = False
    meta_block = [] 
    
    for line in lines:
        if line.startswith("## 📅"):
            if current_day: days.append(current_day)
            current_day = [line]
            header_found = True
        elif not header_found:
            meta_block.append(line)
        else:
            current_day.append(line)
    if current_day: days.append(current_day)

    if len(days) <= 7:
        print("  ℹ️  Less than 7 days of entries. Skipping archival.")
        return

    to_keep = days[:7]
    to_archive = days[7:]

    print(f"  📦 Archiving {len(to_archive)} days to Time Capsule...")
    
    if os.path.exists(TIME_CAPSULE):
        with open(TIME_CAPSULE, 'r', encoding='utf-8') as f:
            capsule_content = f.read()
    else:
        capsule_content = "# 🕰️ Time Capsule\n> Historical records of the saga.\n\n"

    archive_text = ""
    for day in to_archive:
        archive_text += "".join(day) + "\n---\n"

    header_parts = capsule_content.split("---", 1)
    if len(header_parts) > 1:
        new_capsule = header_parts[0] + "---" + archive_text + header_parts[1]
    else:
        new_capsule = capsule_content + "\n" + archive_text
    
    with open(TIME_CAPSULE, 'w', encoding='utf-8') as f:
        f.write(new_capsule)

    new_journal = "".join(meta_block)
    for day in to_keep:
        new_journal += "".join(day)
    
    with open(journal_path, 'w', encoding='utf-8') as f:
        f.write(new_journal)
    
    print("  ✅ Archival complete.")

def main():
    print(f"🌅 Morning Cron Started: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}")
    
    git_sync()
    update_journal()
    
    # 2. Health Check & Audits
    print("\n🩺 Running System Health Check...")
    run_command("python3 scripts/validate_system.py")
    run_command("python3 scripts/health_check.py")
    
    print("\n📊 Updating Analytics...")
    run_command("python3 scripts/analytics_engine.py")
    
    print("\n🕸️ Syncing System Core...")
    run_command("python3 scripts/system_sync.py")
    
    print("\n🔗 Auditing Links...")
    run_command("python3 scripts/link_auditor.py")

    print("\n🕸️ Analyzing Inter-Note Intelligence...")
    run_command("python3 scripts/vault_graph.py")

    print("\n🧹 Running Context Hygiene...")
    run_command("python3 scripts/memory_cleanup.py")
    
    print("")
    run_archival()
    
    if os.path.exists(CHAOS_PATH):
        with open(CHAOS_PATH, 'r') as f:
            if len(f.read().strip()) > 50:
                print("\n⚠️  Chaos Stream contains unprocessed data.")
    
    print("\n✅ Morning Protocol Complete.")

if __name__ == "__main__":
    main()