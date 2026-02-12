#!/bin/bash

echo "=================================="
echo "SmartAgro IoT Setup Script"
echo "=================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if Python is installed
echo "Checking Python installation..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo -e "${GREEN}✓${NC} Python is installed: $PYTHON_VERSION"
else
    echo -e "${RED}✗${NC} Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Check if Node.js is installed
echo "Checking Node.js installation..."
if command -v node &> /dev/null; then
    NODE_VERSION=$(node --version)
    echo -e "${GREEN}✓${NC} Node.js is installed: $NODE_VERSION"
else
    echo -e "${RED}✗${NC} Node.js is not installed. Please install Node.js 18 or higher."
    exit 1
fi

# Check for serviceAccountKey.json
echo ""
echo "Checking Firebase credentials..."
if [ -f "serviceAccountKey.json" ]; then
    echo -e "${GREEN}✓${NC} serviceAccountKey.json found"
else
    echo -e "${YELLOW}⚠${NC} serviceAccountKey.json not found"
    echo "  Please download your Firebase service account key:"
    echo "  1. Go to Firebase Console"
    echo "  2. Project Settings → Service Accounts"
    echo "  3. Generate New Private Key"
    echo "  4. Save as serviceAccountKey.json in this directory"
    echo ""
    read -p "Do you want to continue without it? (y/n) " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Check for model file
echo ""
echo "Checking ML model..."
if [ -f "irrigation_model.pkl" ]; then
    echo -e "${GREEN}✓${NC} irrigation_model.pkl found"
else
    echo -e "${YELLOW}⚠${NC} irrigation_model.pkl not found"
    echo "  The ML model file is missing. The prediction API may not work."
fi

# Create virtual environment
echo ""
echo "Setting up Python virtual environment..."
if [ -d "venv" ]; then
    echo -e "${YELLOW}⚠${NC} Virtual environment already exists"
else
    python3 -m venv venv
    echo -e "${GREEN}✓${NC} Virtual environment created"
fi

# Activate virtual environment
echo ""
echo "Activating virtual environment..."
source venv/bin/activate
echo -e "${GREEN}✓${NC} Virtual environment activated"

# Install Python dependencies
echo ""
echo "Installing Python dependencies..."
pip install -r requirements.txt
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓${NC} Python dependencies installed"
else
    echo -e "${RED}✗${NC} Failed to install Python dependencies"
    exit 1
fi

# Install Node.js dependencies for functions
echo ""
echo "Installing Node.js dependencies for Firebase Functions..."
cd functions
npm install
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓${NC} Functions dependencies installed"
    cd ..
else
    echo -e "${RED}✗${NC} Failed to install functions dependencies"
    cd ..
    exit 1
fi

# Install root Node.js dependencies (optional)
echo ""
echo "Installing root Node.js dependencies..."
npm install
echo -e "${GREEN}✓${NC} Root dependencies installed"

# Summary
echo ""
echo "=================================="
echo "Setup Complete!"
echo "=================================="
echo ""
echo "Next steps:"
echo ""
echo "1. Make sure you have serviceAccountKey.json in place"
echo ""
echo "2. Start the Flask API server:"
echo "   source venv/bin/activate"
echo "   python3 app.py"
echo ""
echo "3. In another terminal, serve the frontend:"
echo "   cd public"
echo "   python3 -m http.server 8000"
echo ""
echo "4. Open your browser to:"
echo "   http://localhost:8000/login.html"
echo ""
echo "5. Test with sensor data:"
echo "   python3 push_test_data.py continuous /sensor_data 5"
echo ""
echo "6. Monitor predictions:"
echo "   python3 fetch_and_predict.py listen /sensor_data 5"
echo ""
echo "For more information, see README.md"
echo ""
