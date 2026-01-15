#!/usr/bin/env python3
"""
🔗 System Sync & Connectivity Auditor v3.0 (Auto-Map)
-------------------------------------
Dynamically generates the Vault Map by scanning all Core folders.
Ensures NO Orphan Nodes in the System Core.
"""

import os
import re
import datetime

# --- Configuration ---
VAULT_ROOT = "/storage/emulated/0/Download/Vinci"
CENTRAL_CMD = os.path.join(VAULT_ROOT, "0 - 🌌 Central Command.md")
CAPABILITIES = os.path.join(VAULT_ROOT, "1 - 🧠 The Construct/🤖 AI Core/⚙️ System Capabilities.md")
SAGA_DIR = os.path.join(VAULT_ROOT, "1 - 🧠 The Construct/📜 The Saga")

# --- Map Definitions ---
# Where to look -> Section Title in Dashboard
SCAN_TARGETS = {
    "The Brain": "1 - 🧠 The Construct/🤖 AI Core",
    "Contexts": "1 - 🧠 The Construct/🧠 Contexts",
    "Blueprints": "The Blueprints",
    "The Academy": "0 - Academic"
}

# Files to exclude from the map (e.g., indices, assets)
EXCLUDE_FILES = ["Index", "Asset", "IMG", ".jpg", ".png", "Icon"]

# --- Helpers ---
def get_clean_name(filename):
    """Removes extension and emojis for a clean display name if needed."""
    name = os.path.splitext(filename)[0]
    return name

def generate_vault_map():
    """Scans folders and builds the Vault Map section."""
    map_lines = []
    
    # 1. The Saga (Journal) - Special Case
    today = datetime.date.today()
    month_name = today.strftime("%B")
    year_month = today.strftime("%Y-%m")
    journal_path = f"1 - 🧠 The Construct/📜 The Saga/{year_month}-{month_name}"
    map_lines.append(f"- **The Saga:** [[{journal_path}|Current Journal]]")

    # 2. Dynamic Scans
    for section_name, folder in SCAN_TARGETS.items():
        full_path = os.path.join(VAULT_ROOT, folder)
        if not os.path.exists(full_path): continue
        
        files = []
        for f in sorted(os.listdir(full_path)):
            if not f.endswith(".md"):
                continue
            if any(x in f for x in EXCLUDE_FILES):
                continue
            
            # Special Handling for "System Core" vs "The Brain" split
            # We'll just dump everything found in AI Core into "The Brain" for now,
            # unless we want to split them based on a list.
            # Let's keep it simple: List everything found.
            
            clean_name = get_clean_name(f)
            # Shorten display names for cleanliness
            display_name = clean_name.replace("Context_", "").replace("Protocol_", "")
            
            link = f"[[{folder}/{clean_name}|{display_name}]]"
            files.append(link)
        
        if files:
            # Formatting: "Title: [[Link]] | [[Link]]"
            content = " | ".join(files)
            map_lines.append(f"- **{section_name}:** {content}")

    return "\n".join(map_lines)

def extract_toolbox_table():
    if not os.path.exists(CAPABILITIES): return None
    with open(CAPABILITIES, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    table_lines = []
    in_section = False
    for line in lines:
        if "## 5. 🛠️ Automation Suite" in line:
            in_section = True
            continue
        if in_section:
            if line.startswith("## "): break
            if line.strip().startswith("|"):
                table_lines.append(line.strip())
    return "\n".join(table_lines) if table_lines else None

def get_current_journal_data():
    today = datetime.date.today()
    month_name = today.strftime("%B")
    year_month = today.strftime("%Y-%m")
    journal_path = os.path.join(SAGA_DIR, f"{year_month}-{month_name}.md")
    
    if not os.path.exists(journal_path):
        return "No journal found for today.", "No friction points recorded."

    with open(journal_path, 'r', encoding='utf-8') as f:
        content = f.read()

    days = re.split(r"## 📅", content)
    today_tasks = []
    friction_points = []
    
    today_pattern = today.strftime("%A, %d")
    for day in days:
        if today_pattern in day:
            task_pattern = r"- \[ \] " + r".*"
            tasks = re.findall(task_pattern, day)
            today_tasks = [t.strip() for t in tasks]
            break
    
    for day in days[1:4]:
        lines = day.split('\n')
        for line in lines:
            if "#friction" in line:
                clean_line = line.strip()
                clean_line = re.sub(r"^> ", "", clean_line)
                clean_line = re.sub(r"^- `\[.*?\]`", "", clean_line)
                clean_line = re.sub(r"^- ", "", clean_line)
                clean_line = clean_line.strip()
                if clean_line: friction_points.append(clean_line)

    task_str = "\n".join(today_tasks) if today_tasks else "> ✅ All tasks complete or none set."
    f_list = []
    for f in friction_points[:5]:
        if f.startswith("- "): f_list.append(f)
        else: f_list.append(f"- {f}")
    friction_str = "\n".join(f_list) if f_list else "> ✅ No active friction points."
    
    return task_str, friction_str

def replace_section(full_text, marker, new_data):
    if marker not in full_text: return full_text
    parts = full_text.split(marker)
    post_marker = parts[1]
    
    indices = []
    for header in ["\n## ", "\n---"]:
        match = post_marker.find(header)
        if match != -1: indices.append(match)
    
    if indices:
        end_idx = min(indices)
        rest = post_marker[end_idx:]
    else:
        rest = ""
        
    return f"{parts[0]}{marker}\n{new_data}\n{rest}"

def update_central_command():
    if not os.path.exists(CENTRAL_CMD): 
        print("❌ Central Command not found.")
        return
    
    with open(CENTRAL_CMD, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. Get Data
    tasks, friction = get_current_journal_data()
    toolbox = extract_toolbox_table()
    vault_map = generate_vault_map()

    # 2. Update Sections
    content = replace_section(content, "## 🚨 Active Friction Points (Last 3 Days)", friction)
    content = replace_section(content, "## 📅 Daily Focus (Today)", tasks)
    content = replace_section(content, "## 📂 Vault Map", vault_map)
    
    if toolbox:
        content = replace_section(content, "## 🛠️ System Toolbox", toolbox)

    # 3. Write
    content = re.sub(r"\n{3,}", "\n\n", content)
    with open(CENTRAL_CMD, 'w', encoding='utf-8') as f:
        f.write(content)
    print("✅ Central Command Synchronized (Map Updated).")

if __name__ == "__main__":
    update_central_command()
