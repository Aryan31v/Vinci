#!/usr/bin/env python3
"""
Web Article to Obsidian Notes (Scholar Standard)
Uses Trafilatura for extraction + Gemini for Intelligence (Emoji + Formatting).
"""

import sys
import os
import re
import subprocess
from datetime import datetime
import trafilatura

# --- Configuration ---
VAULT_PATH = "/storage/emulated/0/Download/Vinci/1 - 🧠 The Construct/2 - 🧩 Input Stream" # Default dump location
# ---------------------

def clean_filename(title):
    # Keep emojis and alphanumeric
    return re.sub(r'[^\w\s\-\U00010000-\U0010ffff]', '', title).strip()[:80]

def get_web_content(url):
    """Fetch and extract text from URL"""
    downloaded = trafilatura.fetch_url(url)
    if not downloaded:
        return None, None
    
    text = trafilatura.extract(downloaded, include_comments=False, include_tables=True)
    metadata = trafilatura.extract_metadata(downloaded)
    title = metadata.title if metadata and metadata.title else "Web Article"
    
    return title, text

def format_with_gemini(text, title, url):
    """
    Use Gemini to:
    1. Generate an Emoji-fied Title.
    2. Format the content with a Source Callout.
    """
    
    prompt = f'''You are a Scholar Assistant. Process this article for a Personal Knowledge Management system.

SOURCE METADATA:
- Title: {title}
- URL: {url}

INSTRUCTIONS:
1. **Title:** Generate a new title that is punchy and includes a relevant **Emoji** at the start.
2. **Source:** You MUST include a callout at the very top: `> [!info] Source` linking to the URL.
3. **Format:** Clean Markdown. Use H2/H3. Bold key concepts.
4. **Summary:** Provide a "tl;dr" or "Core Premise" callout after the source.

RAW TEXT:
{text[:20000]}

OUTPUT FORMAT:
# [Emoji] [Title]

> [!info] Source
> [{title}]({url})

... (Rest of the content)
'''

    # Call Gemini (Assumes 'gemini' CLI tool is installed and authenticated)
    try:
        result = subprocess.run(
            ['gemini', '-p', prompt],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except Exception as e:
        print(f"⚠️ Gemini processing failed: {e}")
        return None

def main():
    if len(sys.argv) < 2:
        print("Usage: python web_notes.py <url>")
        sys.exit(1)
        
    url = sys.argv[1]
    print(f"🌍 Fetching: {url}")
    
    orig_title, text = get_web_content(url)
    if not text:
        print("❌ Failed to extract content.")
        sys.exit(1)
        
    print(f"🧠 Processing with Gemini (Emoji + Source)...")
    markdown = format_with_gemini(text, orig_title, url)
    
    if not markdown:
        # Fallback if Gemini fails
        markdown = f"# 📄 {orig_title}\n\n> [!info] Source\n> {url}\n\n{text}"
        final_title = orig_title
    else:
        # Extract title from the first line of Markdown
        lines = markdown.split('\n')
        if lines[0].startswith('# '):
            final_title = lines[0].replace('# ', '').strip()
        else:
            final_title = orig_title

    # Create Filename
    filename = f"{clean_filename(final_title)}.md"
    filepath = os.path.join(VAULT_PATH, filename)
    
    # Add Frontmatter
    final_content = f"""---
created: {datetime.now().strftime('%Y-%m-%d %H:%M')}
source: {url}
tags: #input/web
---

{markdown}
"""
    
    # Save
    os.makedirs(VAULT_PATH, exist_ok=True)
    with open(filepath, 'w') as f:
        f.write(final_content)
        
    print(f"✅ Saved to: {filepath}")

if __name__ == "__main__":
    main()