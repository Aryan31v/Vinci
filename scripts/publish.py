import re
import sys
import os

def clean_obsidian_syntax(content):
    # Remove WikiLinks [[Link|Alias]] -> Alias or [[Link]] -> Link
    content = re.sub(r'\[\[([^\]|]+\|)?([^\]]+)\]\]', r'\2', content)
    # Remove Callouts > [!info] -> >
    content = re.sub(r'>\s*\[![^\]]+\]', '>', content)
    # Remove Dataview blocks
    content = re.sub(r'```dataview.*?```', '', content, flags=re.DOTALL)
    return content

def publish_note(file_path):
    if not os.path.exists(file_path):
        print(f"Error: File {file_path} not found.")
        return

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    clean_content = clean_obsidian_syntax(content)
    
    base_name = os.path.basename(file_path)
    output_path = f"published_{base_name}"
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(clean_content)
    
    print(f"🚀 Published: {output_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scripts/publish.py [file_path]")
    else:
        publish_note(sys.argv[1])
