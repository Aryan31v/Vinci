#!/bin/bash

# pdf-notes.sh - Extract text from PDF and generate detailed notes

PDF_CACHE="$HOME/.cache/pdf-text"
mkdir -p "$PDF_CACHE"

pdf_to_text() {
    local pdf_file="$1"
    local txt_file="$PDF_CACHE/$(basename "$pdf_file" .pdf).txt"
    
    echo "📄 Extracting text from PDF..."
    
    # Try pdftotext first
    if command -v pdftotext &> /dev/null; then
        pdftotext -layout "$pdf_file" "$txt_file"
    fi
    
    # Check if extraction yielded results. If not, try OCR.
    if [ ! -s "$txt_file" ] || [ $(wc -w < "$txt_file") -lt 10 ]; then
        echo "⚠️  Standard extraction failed or yielded little text. Attempting OCR..."
        if command -v tesseract &> /dev/null; then
            # Convert PDF to images and OCR (Tesseract handles PDF input in newer versions)
            tesseract "$pdf_file" "${txt_file%.txt}" -l eng > /dev/null 2>&1
        else
            echo "❌ OCR Error: 'tesseract' not installed. Run: pkg install tesseract"
        fi
    fi
    
    cat "$txt_file"
}

generate_pdf_notes() {
    local pdf_file="$1"
    local pdf_name=$(basename "$pdf_file" .pdf)
    
    echo "📥 Processing: $pdf_name"
    
    # Extract text
    text=$(pdf_to_text "$pdf_file")
    
    if [ -z "$text" ]; then
        echo "❌ Could not extract text from PDF"
        exit 1
    fi
    
    word_count=$(echo "$text" | wc -w)
    echo "📊 Extracted: $word_count words"
    
    # Process with Gemini for formatting, not just summary
    if [ $word_count -gt 20000 ]; then
        echo "📄 Large PDF detected, processing in sections..."
        
        # Split into chunks
        echo "$text" | split -l 1000 - "$PDF_CACHE/chunk_"
        
        notes=""
        for chunk in "$PDF_CACHE"/chunk_*; do
            # Instruction changed: Ask for detailed formatting, preserving content
            chunk_notes=$(gemini -p "You are a formatter. formatting this text from a PDF into clean Markdown. 
Do NOT summarize. Keep all details. Use headers, bullet points, and code blocks where appropriate.
Text section:
$(cat "$chunk")

Markdown output:" 2>/dev/null)
            notes="$notes\n\n$chunk_notes"
            rm "$chunk"
        done
        
        echo "$notes"
    else
        # Normal processing - Full detail
        gemini -p "Convert this PDF text into a clean, detailed Markdown document.
Do NOT summarize. Preserve all information, but format it beautifully with headers and lists.

DOCUMENT: $pdf_name
CONTENT:
$text

Markdown Output:"
    fi
}

# Main
if [ -z "$1" ]; then
    echo "📂 Select a PDF file:"
    echo ""
    
    # List PDFs in common locations
    find ~/storage/shared/Download ~/storage/shared/Documents -name "*.pdf" 2>/dev/null | head -20 | nl
    echo ""
    read -p "Enter number or path: " selection
    
    if [[ "$selection" =~ ^[0-9]+$ ]]; then
        pdf_file=$(find ~/storage/shared/Download ~/storage/shared/Documents -name "*.pdf" 2>/dev/null | sed -n "${selection}p")
    else
        pdf_file="$selection"
    fi
else
    pdf_file="$1"
fi

if [ ! -f "$pdf_file" ]; then
    echo "❌ File not found: $pdf_file"
    exit 1
fi

# Generate output path
output_dir="$HOME/storage/shared/Documents/Obsidian/YourVault/PDF Notes"
mkdir -p "$output_dir"
output_file="$output_dir/$(basename "$pdf_file" .pdf)_notes.md"

# Generate notes
generate_pdf_notes "$pdf_file" > "$output_file"

echo ""
echo "✅ Notes saved to: $output_file"
