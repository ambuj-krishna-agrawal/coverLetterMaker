#!/bin/bash

echo "🔧 Setting up Cover Letter Generator..."

# Create virtual environment
if [ ! -d "coverletter_env" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv coverletter_env
fi

# Activate virtual environment
echo "⚡ Activating virtual environment..."
source coverletter_env/bin/activate

# Upgrade pip
echo "📈 Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📚 Installing dependencies..."
pip install -r requirements.txt

# Extract resume information
echo "📄 Extracting resume information..."
python extract_resume.py

# Test core functionality
echo "🧪 Testing core functionality..."
python test_core.py

echo ""
echo "✅ Setup complete!"
echo "🚀 Run './run.sh' to start the application"
echo "🌐 Then visit http://localhost:5000 in your browser"