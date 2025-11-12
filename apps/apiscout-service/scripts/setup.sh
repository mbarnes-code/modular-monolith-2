#!/bin/bash

# APIScout NX Service Installation Script
# This script sets up the APIScout service in the NX workspace

echo "🔧 Setting up APIScout Service..."

# Navigate to the service directory
cd "$(dirname "$0")"

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

# Install the package in development mode
echo "🔧 Installing APIScout in development mode..."
pip install -e .

# Verify installation
echo "✅ Verifying installation..."
python -c "import sys; sys.path.insert(0, 'src'); from apiscout.ApiScout import ApiScout; print('APIScout installed successfully!')"

echo "🎉 APIScout Service setup complete!"
echo ""
echo "Available commands:"
echo "  nx serve apiscout-service          # Run scout.py"
echo "  nx serve:collect apiscout-service  # Run collect.py"
echo "  nx serve:match apiscout-service    # Run match.py"
echo "  nx serve:export apiscout-service   # Run export.py"
echo "  nx test apiscout-service           # Run tests"
echo ""
echo "Direct usage:"
echo "  python scout.py --help"
echo "  python collect.py --help"
echo ""