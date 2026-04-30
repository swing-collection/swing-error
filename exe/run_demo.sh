#!/bin/bash

# Swing Error Demo - Quick Start Script
# =====================================

# Get the project root directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$SCRIPT_DIR/.."

echo "🚀 Starting Swing Error Demo..."
echo ""

# Check if virtual environment is activated
if [ -z "$VIRTUAL_ENV" ]; then
    echo "📦 Activating virtual environment..."
    source "$PROJECT_ROOT/.venv/bin/activate"
else
    echo "✅ Virtual environment already activated"
fi

echo ""
echo "🔍 Running Django system checks..."
python "$SCRIPT_DIR/manage.py" check

if [ $? -ne 0 ]; then
    echo "❌ System checks failed. Please fix the issues above."
    exit 1
fi

echo ""
echo "✅ All checks passed!"
echo ""
echo "🌐 Starting Django development server..."
echo ""
echo "📍 Open your browser to: http://localhost:8000"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Run the development server
python "$SCRIPT_DIR/manage.py" runserver 0.0.0.0:8000
