import os
import re
from datetime import datetime, timedelta

CONTEXT_DIR = "1 - 🧠 The Construct/🧠 Contexts"
RETENTION_DAYS = 30

def prune_memory():
    print(f"🧹 Running Context Hygiene (Retention: {RETENTION_DAYS} days)...")
    for file in os.listdir(CONTEXT_DIR):
        if not file.endswith(".md"): continue
        path = os.path.join(CONTEXT_DIR, file)
        
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()

        if "## 💾 Agent Memory" not in content: continue

        # Split into Active and Archived
        parts = content.split("## 💾 Agent Memory")
        pre_memory = parts[0]
        memory_content = parts[1]
        
        # Check for archive section
        if "### 🗄️ Archived Memory" in memory_content:
            mem_parts = memory_content.split("### 🗄️ Archived Memory")
            active_mem = mem_parts[0]
            archived_mem = mem_parts[1]
        else:
            active_mem = memory_content
            archived_mem = ""

        # Extract dated entries [202X-MM-DD]
        entries = re.split(r'(\n- .*?[\[]\d{4}-\d{2}-\d{2}[\]].*?)(?=\n- |\n#|$)', active_mem, flags=re.DOTALL)
        
        new_active = []
        new_archived = [archived_mem]
        
        now = datetime.now()
        
        for entry in entries:
            date_match = re.search(r'[\[](\d{4}-\d{2}-\d{2})[\]]', entry)
            if date_match:
                entry_date = datetime.strptime(date_match.group(1), "%Y-%m-%d")
                if now - entry_date > timedelta(days=RETENTION_DAYS):
                    new_archived.append(entry)
                else:
                    new_active.append(entry)
            else:
                new_active.append(entry)

        # Reconstruct file
        updated_content = pre_memory + "## 💾 Agent Memory" + "".join(new_active)
        if len(new_archived) > 1 or archived_mem.strip():
            updated_content += "\n### 🗄️ Archived Memory" + "".join(new_archived)
            
        with open(path, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        print(f"  ✅ Pruned: {file}")

if __name__ == "__main__":
    prune_memory()
