#!/usr/bin/env python3
"""
Generate Anki .apkg files directly from notes using Gemini CLI
"""

import genanki
import subprocess
import os
import sys
import random
import re

# Create a unique model for your flashcards
MY_MODEL = genanki.Model(
    random.randrange(1 << 30, 1 << 31),
    'Gemini Generated Cards',
    fields=[
        {'name': 'Question'},
        {'name': 'Answer'},
        {'name': 'Source'},
    ],
    templates=[
        {
            'name': 'Card 1',
            'qfmt': '{{Question}}',
            'afmt': '{{FrontSide}}<hr id="answer">{{Answer}}<br><small>Source: {{Source}}</small>',
        },
    ])

def get_flashcards_from_gemini(note_content, topic):
    """Use Gemini CLI to generate flashcards"""
    
    prompt = f'''Create flashcards from these notes about "{topic}".

OUTPUT FORMAT (exactly like this, one per line):
Q: [question here]
A: [answer here]
---

RULES:
- Create 10-15 high-quality flashcards
- Focus on key concepts, definitions, and relationships
- Make questions specific and testable
- Keep answers concise

NOTES:
{note_content}

Generate flashcards:'''

    result = subprocess.run(
        ['gemini', '-p', prompt],
        capture_output=True,
        text=True
    )
    
    return result.stdout

def parse_flashcards(gemini_output):
    """Parse Gemini output into Q&A pairs"""
    cards = []
    
    # Split by separator
    blocks = gemini_output.split('---')
    
    for block in blocks:
        q_match = re.search(r'Q:\s*(.+?)(?=A:|$)', block, re.DOTALL)
        a_match = re.search(r'A:\s*(.+?)(?=---|$)', block, re.DOTALL)
        
        if q_match and a_match:
            question = q_match.group(1).strip()
            answer = a_match.group(1).strip()
            if question and answer:
                cards.append((question, answer))
    
    return cards

def create_anki_deck(cards, topic, source_file, output_path):
    """Create an Anki deck from flashcard pairs"""
    
    deck_id = random.randrange(1 << 30, 1 << 31)
    deck = genanki.Deck(deck_id, f'Gemini - {topic}')
    
    for question, answer in cards:
        note = genanki.Note(
            model=MY_MODEL,
            fields=[question, answer, source_file]
        )
        deck.add_note(note)
    
    output_file = os.path.join(output_path, f'{topic}.apkg')
    genanki.Package(deck).write_to_file(output_file)
    
    return output_file

def main():
    if len(sys.argv) < 2:
        print("Usage: python anki_generator.py <note_file.md>")
        sys.exit(1)
    
    note_file = sys.argv[1]
    
    if not os.path.exists(note_file):
        print(f"Error: File not found: {note_file}")
        sys.exit(1)
    
    # Read the note
    with open(note_file, 'r') as f:
        content = f.read()
    
    topic = os.path.basename(note_file).replace('.md', '')
    
    print(f"🧠 Generating flashcards for: {topic}")
    
    # Get flashcards from Gemini
    gemini_output = get_flashcards_from_gemini(content, topic)
    
    # Parse the output
    cards = parse_flashcards(gemini_output)
    
    if not cards:
        print("❌ No flashcards generated. Check Gemini output.")
        print(gemini_output)
        sys.exit(1)
    
    print(f"📝 Generated {len(cards)} flashcards")
    
    # Create output directory
    output_dir = "0 - Academic/Anki_Decks"
    os.makedirs(output_dir, exist_ok=True)
    
    # Create the deck
    output_file = create_anki_deck(cards, topic, note_file, output_dir)
    
    print(f"✅ Anki deck created: {output_file}")
    print("📱 Open this file with Anki app to import")

if __name__ == "__main__":
    main()
