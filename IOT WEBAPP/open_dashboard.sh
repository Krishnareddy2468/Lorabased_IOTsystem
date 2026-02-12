#!/bin/bash
# Open SmartAgro Dashboard in Browser

echo "=================================================="
echo "  🌱 Opening SmartAgro Dashboard"
echo "=================================================="
echo ""

# Change to project directory
cd "$(dirname "$0")"

# Check if Flask API is running
if curl -s http://localhost:5001/ > /dev/null 2>&1; then
    echo "✓ Flask API is running on http://localhost:5001"
else
    echo "⚠️  Flask API is not running"
    echo "   Start it first with: ./start_api.sh"
    echo ""
fi

# Open dashboard in default browser
echo "🌐 Opening dashboard in your browser..."
echo ""
echo "Available pages:"
echo "  • Login: public/login.html"
echo "  • Dashboard: public/dashboard.html (requires login)"
echo "  • Real-time view: public/index.html"
echo ""

# Open login page
open public/login.html

echo "✓ Dashboard opened!"
echo ""
echo "=================================================="
