#!/bin/bash

# Environmental Monitoring System Launcher
# This script runs both the data collector and web dashboard

echo "=========================================="
echo "🚀 Starting Environmental Monitoring System"
echo "=========================================="
echo ""

# Check if main_csv.py is already running
if pgrep -f "main_csv.py" > /dev/null; then
    echo "✅ Data collector (main_csv.py) is already running"
else
    echo "⚠️  Data collector is not running!"
    echo "📌 Please start it in another terminal with:"
    echo "   python3 main_csv.py"
    echo ""
fi

echo "🌐 Starting Web Dashboard..."
echo "📊 Dashboard URL: http://localhost:5000"
echo ""
echo "🛑 Press CTRL+C to stop"
echo "=========================================="
echo ""

python3 web_dashboard.py
