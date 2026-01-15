#!/bin/bash

# smart-notes.sh - Universal note generator

echo "╔════════════════════════════════════════╗"
echo "║    🧠 Smart Notes Generator            ║"
echo "╠════════════════════════════════════════╣"
echo "║  1. 🎥 YouTube Video                   ║"
echo "║  2. 📄 PDF Document                    ║"
echo "║  3. 📚 Generate Anki from Notes        ║"
echo "║  4. 📝 Quick Note with AI              ║"
echo "║  5. 🔄 Process All Today's Notes       ║"
echo "║  6. 🌍 Web Article URL                 ║"
echo "╚════════════════════════════════════════╝"
echo ""
read -p "Choose option (1-6): " choice

case $choice in
    1)
        read -p "YouTube URL: " url
        python ~/scripts/yt_notes.py "$url"
        ;;
    2)
        bash ~/scripts/pdf-notes.sh
        ;;
    3)
        bash ~/scripts/anki-maker.sh
        ;;
    4)
        read -p "Topic: " topic
        gemini -p "Create a comprehensive note about: $topic" | tee "$HOME/storage/shared/Documents/Obsidian/YourVault/Quick Notes/${topic// /_}.md"
        ;;
    5)
        echo "Processing today's notes for Anki..."
        today=$(date +%Y-%m-%d)
        find ~/storage/shared/Documents/Obsidian -name "*.md" -newermt "$today" | while read f; do
            python ~/scripts/anki_generator.py "$f"
        done
        ;;
    6)
        read -p "Article URL: " url
        python ~/scripts/web_notes.py "$url"
        ;;
    *)
        echo "Invalid option"
        ;;
esac
