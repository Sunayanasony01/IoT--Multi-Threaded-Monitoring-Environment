#!/bin/bash

# 🌡️ Environmental Monitoring System - Setup and Run Script
# This script sets up and launches the IoT monitoring dashboard

echo "=================================================="
echo "🌡️  Environmental Monitoring System Setup"
echo "=================================================="
echo ""

# Color codes for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Step 1: Check if we're in the right directory
echo -e "${BLUE}[1/6]${NC} Checking project directory..."
if [ ! -f "main_csv.py" ]; then
    echo -e "${RED}❌ Error: main_csv.py not found. Please run this script from the project root directory.${NC}"
    exit 1
fi
echo -e "${GREEN}✅ Project directory verified${NC}"
echo ""

# Step 2: Check Python installation
echo -e "${BLUE}[2/6]${NC} Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Error: Python3 is not installed. Please install Python 3.x first.${NC}"
    exit 1
fi
PYTHON_VERSION=$(python3 --version)
echo -e "${GREEN}✅ Found: $PYTHON_VERSION${NC}"
echo ""

# Step 3: Install required packages
echo -e "${BLUE}[3/6]${NC} Installing required Python packages..."
echo "This may take a few minutes..."
pip3 install --quiet streamlit plotly requests 2>/dev/null
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Packages installed successfully${NC}"
else
    echo -e "${YELLOW}⚠️  Package installation may have had issues. Continuing anyway...${NC}"
fi
echo ""

# Step 4: Check if config.json exists
echo -e "${BLUE}[4/6]${NC} Checking configuration..."
if [ ! -f "config.json" ]; then
    echo -e "${YELLOW}⚠️  config.json not found${NC}"
    if [ -f "config.template.json" ]; then
        echo "Creating config.json from template..."
        cp config.template.json config.json
        echo -e "${YELLOW}📝 Please edit config.json with your API keys and credentials${NC}"
        echo -e "${YELLOW}   You can disable email alerts by setting 'enabled': false${NC}"
        echo ""
        read -p "Press Enter after you've edited config.json (or press Ctrl+C to exit)..."
    else
        echo -e "${RED}❌ Error: config.template.json not found${NC}"
        exit 1
    fi
else
    echo -e "${GREEN}✅ config.json found${NC}"
fi
echo ""

# Step 5: Initialize row tracker
echo -e "${BLUE}[5/6]${NC} Initializing row tracker..."
if [ ! -f "row_tracker.txt" ]; then
    echo "0" > row_tracker.txt
    echo -e "${GREEN}✅ row_tracker.txt created (starting from row 0)${NC}"
else
    CURRENT_ROW=$(cat row_tracker.txt)
    echo -e "${GREEN}✅ row_tracker.txt exists (current row: $CURRENT_ROW)${NC}"
    read -p "Do you want to reset to row 0? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "0" > row_tracker.txt
        echo -e "${GREEN}✅ Reset to row 0${NC}"
    fi
fi
echo ""

# Step 6: Check if data.csv exists
echo -e "${BLUE}[6/6]${NC} Checking data file..."
if [ ! -f "data.csv" ]; then
    echo -e "${RED}❌ Error: data.csv not found${NC}"
    echo "Please ensure data.csv exists in the project directory"
    exit 1
fi
ROW_COUNT=$(wc -l < data.csv)
echo -e "${GREEN}✅ data.csv found ($ROW_COUNT rows)${NC}"
echo ""

# All checks passed
echo "=================================================="
echo -e "${GREEN}✅ Setup Complete!${NC}"
echo "=================================================="
echo ""
echo -e "${BLUE}Starting the monitoring system...${NC}"
echo ""
echo "The system will:"
echo "  📊 Process sensor data every 20 seconds"
echo "  🌐 Launch dashboard at http://localhost:8505"
echo "  📧 Send email alerts (if enabled)"
echo "  ☁️  Upload data to ThingSpeak"
echo ""
echo -e "${YELLOW}Press Ctrl+C to stop the system${NC}"
echo ""
sleep 2

# Run the application
python3 main_csv.py
