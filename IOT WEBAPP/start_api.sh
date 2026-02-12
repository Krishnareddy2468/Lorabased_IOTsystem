#!/bin/bash
# SmartAgro Flask API Startup Script

echo "=================================================="
echo "  🌱 SmartAgro - IoT Agriculture Dashboard"
echo "=================================================="
echo ""

# Change to project directory
cd "$(dirname "$0")"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "⚠️  Virtual environment not found. Creating..."
    python3 -m venv venv
    echo "✓ Virtual environment created"
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Check if packages are installed
if ! python3 -c "import flask" 2>/dev/null; then
    echo "📦 Installing Python dependencies..."
    pip install -r requirements.txt
fi

echo ""
echo "✓ Environment ready!"
echo ""
echo "🚀 Starting Flask API server on http://localhost:5001"
echo "   Press Ctrl+C to stop"
echo ""
echo "=================================================="
echo ""

# Run the Flask app
python3 app.py
