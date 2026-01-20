import os
import subprocess
import datetime
import sys

# --- Configuration ---
VAULT_ROOT = "/storage/emulated/0/Download/Vinci"
CHAOS_STREAM = os.path.join(VAULT_ROOT, "1 - 🌀 Chaos Stream.md")
CENTRAL_CMD = os.path.join(VAULT_ROOT, "0 - 🌌 Central Command.md")
SAGA_DIR = os.path.join(VAULT_ROOT, "1 - 🧠 The Construct/📜 The Saga")

def get_current_journal():
    today = datetime.date.today()
    month = today.strftime("%B")
    year_month = today.strftime("%Y-%m")
    path = os.path.join(SAGA_DIR, f"{year_month}-{month}.md")
    return path

def notify(title, message):
    try:
        subprocess.run(["termux-notification", "-t", title, "-c", message, "--priority", "high"])
    except:
        pass

def process_chaos():
    if not os.path.exists(CHAOS_STREAM):
        return

    with open(CHAOS_STREAM, "r") as f:
        content = f.read().strip()

    if not content or len(content) < 10:
        return

    print("🧠 Chaos Engine: Analyzing unstructured data...")
    notify("Vinci Intelligence", "🌀 Processing Chaos Stream...")

    prompt = f"""
You are the Architect of the Vinci System. I have a list of unstructured entries from my 'Chaos Stream'.
Your task is to categorize each entry and provide the EXACT text to be appended to specific files.

FILES AVAILABLE:
1. JOURNAL: {get_current_journal()} (For thoughts, observations, feelings, dream logs)
2. TASKS: {CENTRAL_CMD} (For actionable items, to-dos)

ENTRIES:
{content}

INSTRUCTIONS:
- Identify if an entry is a TASK or a JOURNAL observation.
- For TASKS: Format as `- [ ] Entry Text #migrated`.
- For JOURNAL: Format as `- `[TIMESTAMP]` Entry Text`.
- Output your response in this EXACT format:
---START_TASKS---
[List of tasks]
---END_TASKS---
---START_JOURNAL---
[List of journal entries]
---END_JOURNAL---

If a category is empty, leave it blank. Do not add any other text.
"""

    try:
        # Call Gemini CLI
        result = subprocess.run(['gemini', '-p', prompt], capture_output=True, text=True, check=True)
        response = result.stdout.strip()

        # Parse Tasks
        tasks = ""
        if "---START_TASKS---" in response:
            tasks = response.split("---START_TASKS---")[1].split("---END_TASKS---")[0].strip()
        
        # Parse Journal
        journal_entries = ""
        if "---START_JOURNAL---" in response:
            journal_entries = response.split("---START_JOURNAL---")[1].split("---END_JOURNAL---")[0].strip()

        # Update Central Command (Tasks)
        if tasks:
            with open(CENTRAL_CMD, "r") as f:
                lines = f.readlines()
            new_lines = []
            found = False
            for line in lines:
                new_lines.append(line)
                if "## 📅 Daily Focus (Today)" in line:
                    found = True
                    new_lines.append(tasks + "\n")
            if not found:
                new_lines.append("\n## 📅 Daily Focus (Today)\n" + tasks + "\n")
            with open(CENTRAL_CMD, "w") as f:
                f.writelines(new_lines)

        # Update Journal
        if journal_entries:
            journal_path = get_current_journal()
            if os.path.exists(journal_path):
                with open(journal_path, "r") as f:
                    j_content = f.read()
                
                today_header = f"## 📅 {datetime.date.today().strftime('%A, %d')}"
                if today_header in j_content:
                    # Insert under Mind Stream -> Random Thoughts
                    parts = j_content.split("> [!abstract] Random Thoughts")
                    if len(parts) > 1:
                        updated_j = parts[0] + "> [!abstract] Random Thoughts\n" + journal_entries + "\n" + parts[1]
                        with open(journal_path, "w") as f:
                            f.write(updated_j)

        # CLEAR CHAOS STREAM (CRITICAL PROTOCOL)
        with open(CHAOS_STREAM, "w") as f:
            f.write("# 🌀 Chaos Stream\n> *\"Order from entropy.\"*\n\n---")
        
        notify("Vinci Intelligence", "✅ Chaos Processed & Sorted.")
        print("✅ Chaos Stream cleared.")

    except Exception as e:
        notify("Vinci Intelligence", f"❌ Failed to process chaos: {str(e)}")
        print(f"Error: {e}")

if __name__ == "__main__":
    process_chaos()
