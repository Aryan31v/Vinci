#!/usr/bin/env python3
"""
🏷️ Tag Predictor
----------------
Scans the user's journal history to learn Keyword -> Tag associations.
Suggests tags for a given text input.
"""

import os
import re
import sys
from collections import defaultdict

VAULT_ROOT = "/storage/emulated/0/Download/Vinci"
SAGA_DIR = os.path.join(VAULT_ROOT, "1 - 🧠 The Construct/📜 The Saga")

STOP_WORDS = {"the", "and", "to", "of", "a", "in", "is", "it", "i", "my", "me", "for", "on", "that", "this", "with", "was", "at"}

def train_model():
    """Builds a simple frequency map of Word -> Tags."""
    tag_map = defaultdict(lambda: defaultdict(int))
    
    # 1. Scan Journals
    if not os.path.exists(SAGA_DIR): return tag_map

    for filename in os.listdir(SAGA_DIR):
        if not filename.endswith(".md"): continue
        
        path = os.path.join(SAGA_DIR, filename)
        try:
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
        except: continue

        # Split into blocks (paragraphs or bullets)
        blocks = content.split('\n')
        
        for block in blocks:
            # Find tags in this block
            tags = re.findall(r"(#[Wd-]+)", block)
            if not tags: continue
            
            # Clean text
            text = re.sub(r"[^Wd\s]", "", block.lower())
            words = set(text.split()) - STOP_WORDS
            
            # Map words to tags
            for word in words:
                if len(word) > 3: # Ignore short words
                    for tag in tags:
                        tag_map[word][tag] += 1
                        
    return tag_map

def predict(text, model):
    """Predicts tags for input text."""
    clean_text = re.sub(r"[^Wd\s]", "", text.lower())
    words = set(clean_text.split()) - STOP_WORDS
    
    scores = defaultdict(int)
    
    for word in words:
        if word in model:
            for tag, count in model[word].items():
                scores[tag] += count
                
    # Return top 3 tags
    sorted_tags = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return [t[0] for t in sorted_tags[:3]]

def main():
    if len(sys.argv) < 2:
        print("Usage: python tag_predictor.py 'Text to analyze'")
        sys.exit(1)
        
    input_text = sys.argv[1]
    
    # print("🧠 Training Model (Scanning Vault)...")
    model = train_model()
    
    suggestions = predict(input_text, model)
    
    if suggestions:
        print(f"🤖 Suggested Tags: {', '.join(suggestions)}")
    else:
        print("🤷 No suggestions found.")

if __name__ == "__main__":
    main()
