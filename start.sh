#!/bin/bash

echo "🚀 Starting Knowledge Base Portal..."
echo ""

# Check if .env exists
if [ ! -f "backend/.env" ]; then
    echo "❌ Error: backend/.env file not found!"
    echo ""
    echo "Please create backend/.env with your API keys:"
    echo "  cd backend"
    echo "  cp .env.example .env"
    echo "  # Edit .env and add your API keys"
    echo ""
    exit 1
fi

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is not installed!"
    exit 1
fi

# Check if requirements are installed
echo "📦 Checking dependencies..."
cd backend
if ! python3 -c "import flask" 2>/dev/null; then
    echo "Installing Python dependencies..."
    pip3 install -r requirements.txt
fi

# Start backend
echo "🔧 Starting backend server..."
python3 app.py &
BACKEND_PID=$!

echo "✅ Backend started (PID: $BACKEND_PID)"
echo ""
echo "🌐 Opening frontend in browser..."
sleep 2

# Open frontend
open ../app.html

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ Knowledge Base Portal is running!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Backend:  http://localhost:5000"
echo "Frontend: app.html (opened in browser)"
echo ""
echo "Press Ctrl+C to stop the server"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Wait for Ctrl+C
wait $BACKEND_PID
