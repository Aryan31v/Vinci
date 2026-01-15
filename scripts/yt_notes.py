#!/usr/bin/env python3
"""
YouTube Transcript Fetcher (Scholar Standard)
Extracts transcript and formats with Source Callout + Frontmatter.
"""

import sys
import os
import re
import subprocess
from datetime import datetime

# --- Configuration ---
# Dumps to Input Stream for processing, or you can change to a specific folder
OUTPUT_DIR = "/storage/emulated/0/Download/Vinci/1 - 🧠 The Construct/2 - 🧩 Input Stream"
# ---------------------

def clean_filename(title):
    return re.sub(r'[^\w\s-]', '', title).strip().replace(' ', '_')[:80]

def get_video_id(url):
    patterns = [r'(?:v=|\])([0-9A-Za-z_-]{11}).*', r'(?:youtu\.be\/)([0-9A-Za-z_-]{11})']
    for pattern in patterns:
        match = re.search(pattern, url)
        if match: return match.group(1)
    return None

def get_title(url):
    try:
        result = subprocess.run(['yt-dlp', '--get-title', url], capture_output=True, text=True)
        return result.stdout.strip() if result.returncode == 0 else "YouTube Video"
    except: return "YouTube Video"

def get_transcript(url):
    try:
        cmd = ['yt-dlp', '--write-auto-sub', '--skip-download', '--sub-lang', 'en', '--output', 'temp_trans', url]
        subprocess.run(cmd, check=True, capture_output=True)
        
        files = os.listdir('.')
        vtt = next((f for f in files if f.startswith('temp_trans') and f.endswith('.vtt')), None)
        if not vtt: return None
        
        lines = []
        with open(vtt, 'r', encoding='utf-8') as f:
            for line in f:
                if '-->' in line or not line.strip() or line.startswith(('WEBVTT', 'Kind:', 'Language:')): continue
                text = re.sub(r'<[^>]+>', '', line.strip())
                if text and (not lines or lines[-1] != text): lines.append(text)
        os.remove(vtt)
        return " ".join(lines)
    except: return None

def main():
    if len(sys.argv) < 2:
        print("Usage: yt_notes.py <URL>")
        sys.exit(1)
        
    url = sys.argv[1]
    print(f"📺 Fetching Info: {url}")
    
    title = get_title(url)
    transcript = get_transcript(url)
    
    if not transcript:
        print("❌ No transcript found.")
        sys.exit(1)

    # Note Content (Scholar Standard)
    content = f"""---
created: {datetime.now().strftime('%Y-%m-%d %H:%M')}
source: {url}
tags: #input/video
---

# 📺 {title}

> [!info] Source
> [{title}]({url})

### 📝 Transcript
{transcript[:50000]}
"""
    
    filename = f"YT_{clean_filename(title)}.md"
    filepath = os.path.join(OUTPUT_DIR, filename)
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(filepath, 'w') as f:
        f.write(content)
        
    print(f"✅ Saved to: {filepath}")

if __name__ == "__main__":
    main()
