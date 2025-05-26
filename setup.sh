#!/bin/bash

# Bark.com Scraper Installation Script
# This script sets up the scraper environment and dependencies

echo "🚀 Setting up Bark.com Contact Information Scraper..."
echo "=================================================="

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8+ and try again."
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo "✅ Python version: $PYTHON_VERSION"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "📥 Installing dependencies..."
pip install -r requirements.txt

echo ""
echo "✅ Installation complete!"
echo ""
echo "🎯 Quick Start Guide:"
echo "==================="
echo ""
echo "1. Activate the virtual environment:"
echo "   source venv/bin/activate"
echo ""
echo "2. Run the scraper:"
echo "   python src/scraper_cli.py cleaners --location london --max 25"
echo ""
echo "3. View help:"
echo "   python src/scraper_cli.py --help"
echo ""
echo "4. Run the example demo:"
echo "   python examples/production_demo.py"
echo ""
echo "📁 Example commands:"
echo "   # Scrape cleaners in London"
echo "   python scraper_cli.py cleaners --location london --max 50"
echo ""
echo "   # Scrape web designers with websites"
echo "   python scraper_cli.py web-design --filter-website --max 30"
echo ""
echo "   # Scrape multiple services in Birmingham"
echo "   python scraper_cli.py cleaners gardeners --location birmingham --max 25"
echo ""
echo "🔍 Available services: cleaners, web-design, personal-trainer, accountants, photography"
echo "📍 Popular locations: london, birmingham, manchester, liverpool, bristol, glasgow"
echo ""
echo "Happy scraping! 🎉"
