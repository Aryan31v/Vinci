import os
import re
import datetime

# Configuration
VAULT_ROOT = "."
IGNORE_DIRS = {".git", ".obsidian", ".trash", "scripts", ".gemini"}
IGNORE_FILES = {".DS_Store"}
REPORT_FILE = "1 - 🧠 The Construct/🤖 AI Core/🤖 Agent_Audit_Log.md"

# Regex Patterns
LINK_PATTERN = re.compile(r"\[\[(.*?)\]\]")
TODO_PATTERN = re.compile(r"(TODO|FIXME|\[ \]|Pending User Command)")

class VaultAuditor:
    def __init__(self, root):
        self.root = root
        self.all_files = set()
        self.file_map = {} # path -> content
        self.links = [] # (source, target_raw)
        self.todos = [] # (file, line_num, line_content)
        self.orphans = set()
    
    def is_ignored(self, path):
        parts = path.split(os.sep)
        for part in parts:
            if part in IGNORE_DIRS:
                return True
        return False

    def scan_vault(self):
        print("Scanning vault...")
        for dirpath, dirnames, filenames in os.walk(self.root):
            # Filter directories
            dirnames[:] = [d for d in dirnames if d not in IGNORE_DIRS]
            
            for f in filenames:
                if f in IGNORE_FILES:
                    continue
                
                full_path = os.path.join(dirpath, f)
                rel_path = os.path.relpath(full_path, self.root)
                
                # Normalize path separators for consistency
                rel_path = rel_path.replace("\\", "/")
                
                if self.is_ignored(rel_path):
                    continue

                self.all_files.add(rel_path)
                
                # Only analyze markdown files for content
                if f.endswith(".md"):
                    try:
                        with open(full_path, "r", encoding="utf-8") as file:
                            lines = file.readlines()
                            self.analyze_file(rel_path, lines)
                    except Exception as e:
                        print(f"Error reading {rel_path}: {e}")

    def analyze_file(self, rel_path, lines):
        for i, line in enumerate(lines):
            # 1. Find Links
            matches = LINK_PATTERN.findall(line)
            for target in matches:
                # Handle aliases [[File|Alias]] -> File
                target_file = target.split("|")[0]
                # Handle anchors [[File#Section]] -> File
                target_file = target_file.split("#")[0]
                
                self.links.append((rel_path, target_file))

            # 2. Find TODOs
            if TODO_PATTERN.search(line):
                clean_line = line.strip()
                # Skip completed checkboxes
                if "[x]" in clean_line or "[X]" in clean_line:
                    continue
                self.todos.append((rel_path, i + 1, clean_line))

    def resolve_links(self):
        broken_links = []
        backlinks = {f: 0 for f in self.all_files}

        # Create a lookup map for case-insensitive and partial matching (Obsidian style)
        # Obsidian allows linking to "File" even if path is "Folder/File.md"
        # We need a robust resolver.
        
        name_to_path = {}
        for f in self.all_files:
            name = os.path.basename(f)
            name_no_ext = os.path.splitext(name)[0]
            name_to_path[name] = f
            name_to_path[name_no_ext] = f # Priority match

        for source, target_raw in self.links:
            target_clean = target_raw.strip()
            if not target_clean: continue
            
            # 1. Exact path match
            if target_clean in self.all_files:
                backlinks[target_clean] += 1
                continue
            
            # 2. Exact path with .md extension
            if target_clean + ".md" in self.all_files:
                backlinks[target_clean + ".md"] += 1
                continue

            # 3. Filename match (Obsidian fuzzy match)
            # If target is "File", find "path/to/File.md"
            if target_clean in name_to_path:
                backlinks[name_to_path[target_clean]] += 1
                continue

            # If still not found, it's broken
            broken_links.append((source, target_raw))

        return broken_links, backlinks

    def generate_report(self):
        broken, backlinks = self.resolve_links()
        
        # Identify Orphans (No backlinks, excluding Index/Dashboard/Root)
        # We allow root files to have no backlinks if they are top-level
        orphans = []
        for f, count in backlinks.items():
            if count == 0 and f.endswith(".md"):
                # Exclusions
                if f.startswith("0 -") or f.startswith("The Blueprints") or "Index" in f or "Map" in f:
                    continue
                orphans.append(f)

        # Write Report
        with open(REPORT_FILE, "w", encoding="utf-8") as f:
            f.write(f"# 🕵️ Vault Audit Report\n")
            f.write(f"> **Date:** {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
            f.write(f"> **Scope:** Full Scan of `{self.root}`\n\n")

            f.write("## 🔗 Broken Links\n")
            if broken:
                for source, target in broken:
                    f.write(f"- [] [[{source}]] contains broken link to: `{target}`\n")
            else:
                f.write("> ✅ No broken links found.\n")
            f.write("\n")

            f.write("## 🏝️ Orphaned Files\n")
            f.write("> *Files with no incoming links (excluding Dashboards/Indexes).*")
            if orphans:
                for orphan in sorted(orphans):
                    f.write(f"- [] [[{orphan}]]\n")
            else:
                f.write("> ✅ No orphaned files found.\n")
            f.write("\n")

            f.write("## 📝 Incomplete Items (TODOs)\n")
            if self.todos:
                current_file = ""
                for path, line, content in self.todos:
                    if path != current_file:
                        f.write(f"\n### [[{path}]]\n")
                        current_file = path
                    # Escape brackets for display if needed, or just print
                    f.write(f"- [] Line {line}: `{content}`\n")
            else:
                f.write("> ✅ No pending TODOs found.\n")

        return REPORT_FILE

if __name__ == "__main__":
    auditor = VaultAuditor(VAULT_ROOT)
    auditor.scan_vault()
    report_path = auditor.generate_report()
    print(f"Audit complete. Report generated at: {report_path}")
