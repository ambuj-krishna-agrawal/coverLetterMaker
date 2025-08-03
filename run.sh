#!/bin/bash

echo "🚀 Starting Cover Letter Generator..."

# Activate virtual environment if it exists
if [ -d "coverletter_env" ]; then
    echo "📦 Activating virtual environment..."
    source coverletter_env/bin/activate
else
    echo "⚠️  Virtual environment not found. Please run setup.sh first."
    exit 1
fi

# Check if dependencies are installed
echo "🔍 Checking dependencies..."
python -c "import flask, google.genai" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ Dependencies not installed. Run setup.sh first."
    exit 1
fi

echo "✅ Dependencies OK"

# Start the Flask application
echo "🌟 Starting Flask server on http://localhost:5000"
echo "📝 Access the application in your browser"
echo "🛑 Press Ctrl+C to stop"
echo ""

python app.py