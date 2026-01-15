import os
import re

# Configuration
VAULT_ROOT = "."
IGNORE_DIRS = {".git", ".obsidian", ".trash", "scripts", ".gemini"}
IGNORE_FILES = {".DS_Store", "deep_scan.py", "vault_auditor.py"}

# Core Concepts to Scan For (Term -> Canonical Link)
CONCEPTS = {
    "The Sage": "Context_Sage",
    "The Scholar": "Context_Scholar",
    "The Muse": "Context_Muse",
    "The Librarian": "Context_Librarian",
    "Academic Tutor": "Context_Academic_Tutor",
    "Automation Engineer": "Context_Automation_Engineer",
    "The Architect": "Context_Architect",
    "Shiva Sadhana": "Sadhana Practice",
    "Sankalp": "Sadhana Practice",
    "Hall of Mirrors": "Hall of Mirrors/Guide",
    "Identity Matrix": "Identity Matrix",
    "Prime Directive": "Prime Directive",
    "Chaos Stream": "Chaos Stream",
    "Input Stream": "Input Stream",
    "Time Capsule": "Time Capsule",
}

class DeepScanner:
    def __init__(self, root):
        self.root = root
        self.missing_links = [] # (file, term, line_num)
        self.all_files = set()
        self.referenced_files = set()

    def scan(self):
        print("🔍 Starting Deep Semantic Scan...")
        
        # 1. Map all files
        for dirpath, dirnames, filenames in os.walk(self.root):
            dirnames[:] = [d for d in dirnames if d not in IGNORE_DIRS]
            for f in filenames:
                if f.endswith(".md") and f not in IGNORE_FILES:
                    full_path = os.path.join(dirpath, f)
                    rel_path = os.path.relpath(full_path, self.root).replace("\\", "/")
                    self.all_files.add(rel_path)
                    
                    with open(full_path, "r", encoding="utf-8") as file:
                        lines = file.readlines()
                        self.analyze_content(rel_path, lines)

    def analyze_content(self, rel_path, lines):
        # Skip checking the file against itself (e.g. don't check Context_Sage for "The Sage")
        file_name = os.path.basename(rel_path)
        
        for i, line in enumerate(lines):
            # Check for missing links
            for term, link_target in CONCEPTS.items():
                # If term exists in line
                if term in line:
                    # Ignore if it's already linked [[...Term...]]
                    # This regex checks if the term is NOT inside [[ ... ]]
                    # Simplified check: if "[[" + term not in line and "|" + term not in line
                    # This is a rough heuristic but effective for finding raw text
                    if f"[[{term}" not in line and f"|{term}]]" not in line and f"| {term}]]" not in line:
                        # Exclude self-references (e.g. defining the term in its own file)
                        if link_target in rel_path:
                            continue
                        self.missing_links.append((rel_path, term, i + 1))

    def report(self):
        print("\n🔎 **Missing Link Candidates** (Text found, but not linked):")
        if self.missing_links:
            for f, term, line in self.missing_links:
                print(f"- [ ] [[{f}]] Line {line}: Mentioned **'{term}'** without linking.")
        else:
            print("✅ No missing concept links found.")

if __name__ == "__main__":
    scanner = DeepScanner(VAULT_ROOT)
    scanner.scan()
    scanner.report()
