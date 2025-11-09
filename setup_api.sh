#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
NC='\033[0m' # No Color
BOLD='\033[1m'

# Print colored header
print_header() {
    echo -e "${CYAN}${BOLD}"
    echo "╔════════════════════════════════════════════════════════════╗"
    echo "║  🌤️  IoT LIVE WEATHER MONITORING - SETUP WIZARD           ║"
    echo "║  Real-time data from OpenWeatherMap API                    ║"
    echo "╚════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

# Print section header
print_section() {
    echo -e "\n${BOLD}${BLUE}▶ $1${NC}"
}

# Print success message
print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

# Print error message
print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Print warning message
print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

# Print info message
print_info() {
    echo -e "${CYAN}ℹ️  $1${NC}"
}

clear
print_header

# Step 1: Check if we're in the right directory
print_section "Step 1: Validating Project Directory"

if [ ! -f "main_api.py" ] || [ ! -f "api_weather_device.py" ]; then
    print_error "Setup script must be run from the project root directory!"
    print_info "Expected files: main_api.py, api_weather_device.py"
    exit 1
fi

print_success "Project directory validated"

# Step 2: Check Python installation
print_section "Step 2: Checking Python Installation"

if ! command -v python3 &> /dev/null; then
    print_error "Python 3 is not installed!"
    print_info "Please install Python 3.8 or higher from: https://www.python.org/downloads/"
    exit 1
fi

PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
print_success "Python ${PYTHON_VERSION} detected"

# Step 3: Install required packages
print_section "Step 3: Installing Required Python Packages"

echo -e "${CYAN}Installing: streamlit, plotly, requests...${NC}"

pip3 install --quiet streamlit plotly requests 2>/dev/null

if [ $? -eq 0 ]; then
    print_success "All packages installed successfully"
else
    print_warning "Some packages may have already been installed"
fi

# Step 4: Configure OpenWeatherMap API
print_section "Step 4: OpenWeatherMap API Setup"

if [ -f "config.json" ]; then
    print_info "config.json already exists"
    read -p "Do you want to reconfigure? (y/n): " RECONFIGURE
    if [ "$RECONFIGURE" != "y" ] && [ "$RECONFIGURE" != "Y" ]; then
        print_info "Skipping configuration..."
        SKIP_CONFIG=true
    fi
fi

if [ "$SKIP_CONFIG" != "true" ]; then
    echo ""
    echo -e "${BOLD}${MAGENTA}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${BOLD}${MAGENTA}  🔑 GET YOUR FREE OPENWEATHERMAP API KEY${NC}"
    echo -e "${BOLD}${MAGENTA}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
    echo -e "${YELLOW}1. Visit: ${BOLD}https://home.openweathermap.org/users/sign_up${NC}"
    echo -e "${YELLOW}2. Create a FREE account (takes 2 minutes)${NC}"
    echo -e "${YELLOW}3. Verify your email${NC}"
    echo -e "${YELLOW}4. Go to 'API keys' tab${NC}"
    echo -e "${YELLOW}5. Copy your API key${NC}"
    echo ""
    echo -e "${CYAN}Note: It may take 10-15 minutes for new API keys to activate${NC}"
    echo ""
    
    read -p "Press Enter once you have your API key ready..."
    
    echo ""
    read -p "Enter your OpenWeatherMap API key: " WEATHER_API_KEY
    
    if [ -z "$WEATHER_API_KEY" ]; then
        print_error "API key cannot be empty!"
        exit 1
    fi
    
    echo ""
    read -p "Enter your city (e.g., Bangalore, London, Tokyo): " CITY
    CITY=${CITY:-Bangalore}
    
    echo ""
    read -p "Enter country code (e.g., IN, US, GB, JP): " COUNTRY_CODE
    COUNTRY_CODE=${COUNTRY_CODE:-IN}
    
    echo ""
    print_info "Optional: ThingSpeak API Key (for cloud storage)"
    print_info "You can skip this by pressing Enter (system will still work)"
    read -p "Enter your ThingSpeak API key (or press Enter to skip): " THINGSPEAK_KEY
    THINGSPEAK_KEY=${THINGSPEAK_KEY:-YOUR_THINGSPEAK_API_KEY}
    
    echo ""
    print_info "Optional: Email Alerts Configuration"
    read -p "Do you want to enable email alerts? (y/n): " ENABLE_EMAIL
    
    if [ "$ENABLE_EMAIL" = "y" ] || [ "$ENABLE_EMAIL" = "Y" ]; then
        read -p "Enter sender email (Gmail): " SENDER_EMAIL
        read -p "Enter Gmail App Password: " EMAIL_PASSWORD
        read -p "Enter recipient email: " RECIPIENT_EMAIL
        EMAIL_ENABLED="true"
        SENDER_EMAIL_VAL="$SENDER_EMAIL"
        EMAIL_PASSWORD_VAL="$EMAIL_PASSWORD"
        RECIPIENT_EMAIL_VAL="$RECIPIENT_EMAIL"
    else
        EMAIL_ENABLED="false"
        SENDER_EMAIL_VAL="your-email@gmail.com"
        EMAIL_PASSWORD_VAL="your-app-password"
        RECIPIENT_EMAIL_VAL="recipient@gmail.com"
    fi
    
    # Create config.json
    print_info "Creating config.json..."
    
    cat > config.json << EOF
{
  "device_name": "Live Weather Sensor - $CITY",
  "api_key": "$THINGSPEAK_KEY",
  "update_interval": 20,
  "temperature_limit": 22,
  "humidity_limit": 45,
  "co2_limit": 1000,
  "weather_api": {
    "api_key": "$WEATHER_API_KEY",
    "city": "$CITY",
    "country_code": "$COUNTRY_CODE"
  },
  "email": {
    "enabled": $EMAIL_ENABLED,
    "smtp_server": "smtp.gmail.com",
    "smtp_port": 587,
    "use_tls": true,
    "from_addr": "$SENDER_EMAIL_VAL",
    "to_addr": "$RECIPIENT_EMAIL_VAL",
    "username": "$SENDER_EMAIL_VAL",
    "password": "$EMAIL_PASSWORD_VAL"
  }
}
EOF
    
    print_success "config.json created successfully"
fi

# Step 5: Initialize state file
print_section "Step 5: Initializing State File"

if [ ! -f "current_state.json" ]; then
    echo '{"co2": 0, "temperature": 0, "humidity": 0, "status": "Initializing", "warnings": [], "timestamp": ""}' > current_state.json
    print_success "current_state.json initialized"
else
    print_info "current_state.json already exists"
fi

# Step 6: Summary
print_section "Setup Complete! 🎉"

echo ""
echo -e "${GREEN}${BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}${BOLD}  ✅ YOUR SYSTEM IS READY!${NC}"
echo -e "${GREEN}${BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo -e "${CYAN}What's configured:${NC}"
echo -e "  📍 Location: $(jq -r '.weather_api.city' config.json), $(jq -r '.weather_api.country_code' config.json)"
echo -e "  ⏱️  Update Interval: $(jq -r '.update_interval' config.json) seconds"
echo -e "  🌡️  Temperature Limit: $(jq -r '.temperature_limit' config.json)°C"
echo -e "  💧 Humidity Limit: $(jq -r '.humidity_limit' config.json)%"
echo -e "  💨 CO₂ Limit: $(jq -r '.co2_limit' config.json) ppm"
echo ""
echo -e "${YELLOW}${BOLD}🚀 TO START THE SYSTEM:${NC}"
echo ""
echo -e "  ${CYAN}python3 main_api.py${NC}"
echo ""
echo -e "${YELLOW}${BOLD}📊 TO VIEW THE DASHBOARD:${NC}"
echo ""
echo -e "  In another terminal, run:"
echo -e "  ${CYAN}streamlit run streamlit_dashboard.py${NC}"
echo ""
echo -e "  Then open: ${BOLD}http://localhost:8501${NC}"
echo ""
echo -e "${YELLOW}${BOLD}🛑 TO STOP:${NC}"
echo ""
echo -e "  Press ${BOLD}Ctrl+C${NC} in the terminal"
echo ""
echo -e "${GREEN}${BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# Ask if user wants to start now
read -p "Do you want to start the monitoring system now? (y/n): " START_NOW

if [ "$START_NOW" = "y" ] || [ "$START_NOW" = "Y" ]; then
    echo ""
    print_success "Starting the system..."
    echo ""
    
    # Start streamlit in background
    streamlit run streamlit_dashboard.py --server.port 8501 &
    STREAMLIT_PID=$!
    
    sleep 2
    
    # Start main application
    python3 main_api.py
    
    # If main exits, kill streamlit
    kill $STREAMLIT_PID 2>/dev/null
else
    print_info "Setup complete. Run 'python3 main_api.py' when ready!"
    echo ""
fi
