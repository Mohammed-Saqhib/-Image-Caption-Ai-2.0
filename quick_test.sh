#!/bin/bash

# 🚀 Quick Test Script for Next-Level Caption Enhancement
# This script helps you quickly test the enhanced caption feature

echo "🎯 Image Caption AI - Quick Test Suite"
echo "======================================"
echo ""

# Check if we're in the right directory
if [ ! -d "backend" ] || [ ! -d "frontend" ]; then
    echo "❌ Error: Please run this script from the project root directory"
    exit 1
fi

echo "📋 Available Commands:"
echo ""
echo "1. Test Backend Only"
echo "   cd backend && python main.py"
echo ""
echo "2. Test Frontend Only (requires backend running)"
echo "   cd frontend && npm start"
echo ""
echo "3. Build Frontend for Production"
echo "   cd frontend && npm run build"
echo ""
echo "4. Install Backend Dependencies"
echo "   cd backend && pip install -r requirements.txt"
echo ""
echo "5. Install Frontend Dependencies"
echo "   cd frontend && npm install"
echo ""

# Ask user what they want to do
read -p "What would you like to do? (1-5): " choice

case $choice in
    1)
        echo ""
        echo "🚀 Starting Backend Server..."
        echo "Backend will run at http://localhost:7860"
        echo ""
        cd backend
        python main.py
        ;;
    2)
        echo ""
        echo "🚀 Starting Frontend Development Server..."
        echo "Frontend will run at http://localhost:3000"
        echo ""
        cd frontend
        npm start
        ;;
    3)
        echo ""
        echo "🏗️  Building Frontend for Production..."
        echo ""
        cd frontend
        npm run build
        echo ""
        echo "✅ Build complete! Files are in frontend/build/"
        ;;
    4)
        echo ""
        echo "📦 Installing Backend Dependencies..."
        echo ""
        cd backend
        pip install -r requirements.txt
        echo ""
        echo "✅ Backend dependencies installed!"
        ;;
    5)
        echo ""
        echo "📦 Installing Frontend Dependencies..."
        echo ""
        cd frontend
        npm install
        echo ""
        echo "✅ Frontend dependencies installed!"
        ;;
    *)
        echo ""
        echo "❌ Invalid choice. Please run the script again."
        exit 1
        ;;
esac
