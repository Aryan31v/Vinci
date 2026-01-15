import os
import re

VAULT_ROOT = "."
IGNORE_DIRS = [".git", ".obsidian", ".gemini", "scripts"]

def get_note_metadata():
    graph = {}
    for root, dirs, files in os.walk(VAULT_ROOT):
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
        for file in files:
            if file.endswith(".md"):
                path = os.path.join(root, file)
                with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    tags = re.findall(r'#[\w/-]+', content)
                    links = re.findall(r'\[\[([^\]|]+)(?:\|[^\]]+)?\]\]', content)
                    graph[file] = {"path": path, "tags": set(tags), "links": set(links)}
    return graph

def suggest_links(graph):
    print("🕸️ Analyzing Inter-Note Intelligence...")
    notes = list(graph.keys())
    suggestions = []

    for i in range(len(notes)):
        for j in range(i + 1, len(notes)):
            n1, n2 = notes[i], notes[j]
            shared_tags = graph[n1]["tags"].intersection(graph[n2]["tags"])
            
            # If they share tags but aren't linked
            if shared_tags and n2.replace(".md", "") not in graph[n1]["links"]:
                suggestions.append(f"🔗 Suggestion: [[{n1}]] <-> [[{n2}]] (Shared: {', '.join(shared_tags)})")
    
    return suggestions

if __name__ == "__main__":
    vault_data = get_note_metadata()
    results = suggest_links(vault_data)
    for res in results[:10]: # Limit to top 10 to avoid noise
        print(res)
