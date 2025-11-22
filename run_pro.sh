#!/bin/bash

# AI Image Analysis Platform Launcher
# Professional Edition v2.0

echo "🚀 AI Image Analysis Platform - Professional Edition"
echo "=================================================="
echo ""

# Check Python installation
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.9 or higher."
    exit 1
fi

echo "✅ Python found: $(python3 --version)"
echo ""

# Check if running pro version or standard version
if [ "$1" == "pro" ]; then
    APP_FILE="src/app_pro.py"
    echo "🎯 Launching Professional Edition with Advanced Features..."
else
    APP_FILE="src/app_enhanced.py"
    echo "🎯 Launching Standard Edition..."
fi

echo ""
echo "🔧 Initializing engines..."
echo "   - OCR Engine (EasyOCR)"
echo "   - AI Caption Engine (BLIP)"
echo "   - Translation Engine (19 languages)"
echo "   - TTS Engine (Multi-language)"

if [ "$1" == "pro" ]; then
    echo "   - Image Processor (Advanced preprocessing)"
    echo "   - Export Engine (PDF, DOCX, JSON, SRT)"
    echo "   - Batch Processing"
    echo "   - Analytics Dashboard"
fi

echo ""
echo "🌐 Starting Streamlit server..."
echo ""

# Run Streamlit
/usr/bin/python3 -m streamlit run "$APP_FILE" \
    --server.port 8501 \
    --server.address localhost \
    --browser.gatherUsageStats false \
    --theme.base dark \
    --theme.primaryColor "#667eea" \
    --theme.backgroundColor "#1E1E1E" \
    --theme.secondaryBackgroundColor "#2D2D2D" \
    --theme.textColor "#E0E0E0"
