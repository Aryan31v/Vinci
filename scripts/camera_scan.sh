#!/bin/bash

# camera_scan.sh - Quick Capture via Termux Camera & OCR
# Dependency: termux-api, tesseract-ocr

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
IMG_PATH="$HOME/storage/shared/DCIM/Camera/Scan_$TIMESTAMP.jpg"
TXT_PATH="$HOME/.cache/ocr_output"
CHAOS_STREAM="/storage/emulated/0/Download/Vinci/1 - 🧠 The Construct/1 - 🌀 Chaos Stream.md"

echo "📸 Initiating Camera Scan..."

# 1. Check Dependencies
if ! command -v termux-camera-photo &> /dev/null; then
    echo "❌ Error: 'termux-api' not found. Run: pkg install termux-api"
    exit 1
fi

if ! command -v tesseract &> /dev/null; then
    echo "❌ Error: 'tesseract' not found. Run: pkg install tesseract"
    exit 1
fi

# 2. Take Photo
echo "  👉 Taking photo... (Check device notification/screen)"
termux-camera-photo -c 0 "$IMG_PATH"

if [ ! -f "$IMG_PATH" ]; then
    echo "❌ Photo capture failed."
    exit 1
fi

echo "  ✅ Photo saved: $IMG_PATH"

# 3. OCR Processing
echo "  🧠 Extracting text (OCR)..."
tesseract "$IMG_PATH" "$TXT_PATH" -l eng --psm 3 > /dev/null 2>&1

EXTRACTED_TEXT=$(cat "$TXT_PATH.txt")

if [ -z "$EXTRACTED_TEXT" ]; then
    echo "  ⚠️  No text found in image."
else
    # 4. Append to Chaos Stream
    echo "" >> "$CHAOS_STREAM"
    echo "### 📸 Camera Scan ($TIMESTAMP)" >> "$CHAOS_STREAM"
    echo "> [!file] Image: [[$IMG_PATH]]" >> "$CHAOS_STREAM"
    echo "" >> "$CHAOS_STREAM"
    echo "$EXTRACTED_TEXT" >> "$CHAOS_STREAM"
    echo "" >> "$CHAOS_STREAM"
    echo "---" >> "$CHAOS_STREAM"
    
    echo "  ✅ Text appended to Chaos Stream."
fi

# Cleanup
rm "$TXT_PATH.txt"
