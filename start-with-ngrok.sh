#!/bin/bash

# Start backend with ngrok for public access
echo "🚀 Starting Knowledge Base Portal with ngrok..."

# Check if backend is already running
if lsof -Pi :5001 -sTCP:LISTEN -t >/dev/null ; then
    echo "✅ Backend already running on port 5001"
else
    echo "🔧 Starting backend server..."
    cd backend
    python3 app.py &
    BACKEND_PID=$!
    cd ..
    sleep 3
    echo "✅ Backend started (PID: $BACKEND_PID)"
fi

# Check if ngrok is installed
if ! command -v ngrok &> /dev/null; then
    echo "❌ ngrok not found"
    echo ""
    echo "📥 Install ngrok:"
    echo "   brew install ngrok"
    echo "   OR download from: https://ngrok.com/download"
    echo ""
    echo "After installing:"
    echo "1. Sign up at https://ngrok.com"
    echo "2. Run: ngrok config add-authtoken YOUR_TOKEN"
    echo "3. Run this script again"
    exit 1
fi

# Start ngrok
echo ""
echo "🌐 Starting ngrok tunnel..."
echo "📍 Exposing http://localhost:5001"
echo ""
echo "⚠️  Keep this terminal open!"
echo "⚠️  Press Ctrl+C to stop"
echo ""

ngrok http 5001
