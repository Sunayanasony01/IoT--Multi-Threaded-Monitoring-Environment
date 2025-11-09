# 🌡️ Multi-Threaded Environmental Monitoring System

A real-time IoT environmental monitoring system that reads sensor data from CSV files, displays live readings on an interactive web dashboard, monitors threshold violations, and sends automated email alerts.

## 📋 Table of Contents
- [Quick Start Guide](#-quick-start-guide)
- [Overview](#overview)
- [Features](#features)
- [System Architecture](#system-architecture)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Installation & Setup](#installation--setup)
- [Configuration](#configuration)
- [Usage](#usage)
- [Dashboard Features](#dashboard-features)
- [How It Works](#how-it-works)
- [Threshold Monitoring](#threshold-monitoring)
- [Email Alerts](#email-alerts)
- [API Integration](#api-integration)

---

## 🚀 Quick Start Guide

**For someone forking/cloning this project for the first time:**

### ⚡ Option 1: Automated Setup (Recommended)

Just run the setup script - it does everything for you!

```bash
# Clone the repository
git clone <repository-url>
cd A-Multi-Threaded-Environmental-Monitoring-System-main-2

# Run the automated setup script
./setup_and_run.sh
```

The script will automatically:
- ✅ Check Python installation
- ✅ Install required packages (streamlit, plotly, requests)
- ✅ Create config.json from template
- ✅ Initialize row tracker
- ✅ Validate data files
- ✅ Launch the dashboard at http://localhost:8505

**That's it!** The system will start automatically. 🎉

---

### 🔧 Option 2: Manual Setup

If you prefer to set up manually:

#### Step 1: Clone the Repository
```bash
# Clone the repository
git clone <repository-url>
cd A-Multi-Threaded-Environmental-Monitoring-System-main-2

# Or if you downloaded as ZIP, extract and navigate to the folder
cd A-Multi-Threaded-Environmental-Monitoring-System-main-2
```

#### Step 2: Install Dependencies
```bash
# Option 1: Using pip
pip install streamlit plotly requests

# Option 2: Using conda (recommended)
conda install -c conda-forge streamlit plotly requests
```

#### Step 3: Set Up Configuration
```bash
# Copy the template to create your config file
cp config.template.json config.json

# Edit config.json with your details (use any text editor)
# You need to add:
# - ThingSpeak API key (get free at thingspeak.com)
# - Gmail credentials for alerts (optional - can disable)
```

**Minimal config.json to get started** (without email alerts):
```json
{
  "device_name": "Test Sensor",
  "api_key": "YOUR_THINGSPEAK_KEY",
  "data_file": "data.csv",
  "update_interval": 20,
  "temperature_limit": 22,
  "humidity_limit": 45,
  "co2_limit": 1000,
  "email": {
    "enabled": false
  }
}
```

#### Step 4: Initialize Tracker File
```bash
# Create the row tracker (starts from first row)
echo "0" > row_tracker.txt
```

#### Step 5: Run the Application
```bash
# Start the system
python3 main_csv.py
```

#### Step 6: Access the Dashboard
Open your browser and go to:
```
http://localhost:8505
```

**That's it!** 🎉 The system will start reading sensor data every 20 seconds and display it on the dashboard.

---

### 📝 Quick Commands Reference

| Command | Purpose |
|---------|---------|
| `./setup_and_run.sh` | **🚀 Automated setup and run (easiest!)** |
| `python3 main_csv.py` | Start the monitoring system manually |
| `Ctrl + C` | Stop the system |
| `echo "0" > row_tracker.txt` | Reset to first row |
| `cat current_state.json` | View current readings |
| `tail -f row_tracker.txt` | Monitor progress |
| `chmod +x setup_and_run.sh` | Make setup script executable (if needed) |

---

## 🎯 Overview

This project simulates an IoT environmental monitoring system for indoor air quality management. It reads sensor data (CO₂, Temperature, Humidity) from a CSV file sequentially, processes each reading with configurable time intervals, displays the data on a modern web dashboard, and triggers alerts when values exceed predefined thresholds.

**Use Case**: Office building environmental monitoring, smart home automation, data center climate control, greenhouse management.

---

## ✨ Features

### Core Functionality
- ✅ **Sequential CSV Data Processing** - Reads sensor data row-by-row with configurable intervals (default: 20 seconds)
- ✅ **Non-Destructive Reading** - Preserves original CSV data using a position tracker system
- ✅ **Real-Time Web Dashboard** - Interactive Streamlit-based UI with auto-refresh
- ✅ **Multi-Threaded Architecture** - Concurrent data processing and web serving
- ✅ **Threshold Monitoring** - Automatic detection of abnormal readings
- ✅ **Email Alerts** - SMTP-based notifications when thresholds are exceeded
- ✅ **Cloud Integration** - Automatic data upload to ThingSpeak IoT platform
- ✅ **Professional Visualization** - Gauge charts with color-coded zones

### Dashboard Features
- 🎯 **Real-Time Gauge Charts** - Separate gauges for each metric with appropriate scales
- 📊 **Live Metric Cards** - Current readings with color-coded status indicators
- 🔔 **Alert Notifications** - Visual warnings when thresholds are exceeded
- 📍 **Row Progress Tracker** - Shows current position in dataset
- ⏱️ **System Status Footer** - Displays update interval, email status, and timestamp
- 🎨 **Responsive Design** - Professional IoT dashboard styling

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Main Application                         │
│                    (main_csv.py)                             │
└────────────────────────┬────────────────────────────────────┘
                         │
                    ┌────▼────┐
                    │ Config  │
                    │  Loader │
                    └────┬────┘
                         │
        ┌────────────────┴────────────────┐
        │                                  │
   ┌────▼─────┐                    ┌──────▼────────┐
   │  Thread 1│                    │   Thread 2    │
   │CSV Sensor│                    │   Streamlit   │
   │ Processor│                    │   Dashboard   │
   └────┬─────┘                    └──────┬────────┘
        │                                  │
        │  ┌──────────────────────────┐   │
        ├─►│   data.csv (Source)      │   │
        │  └──────────────────────────┘   │
        │                                  │
        │  ┌──────────────────────────┐   │
        ├─►│ row_tracker.txt (Index)  │   │
        │  └──────────────────────────┘   │
        │                                  │
        │  ┌──────────────────────────┐   │
        ├─►│ current_state.json       │◄──┤
        │  │ (Shared State)           │   │
        │  └──────────────────────────┘   │
        │                                  │
        │  ┌──────────────────────────┐   │
        ├─►│ ThingSpeak API           │   │
        │  └──────────────────────────┘   │
        │                                  │
        │  ┌──────────────────────────┐   │
        └─►│ SMTP Email Server        │   │
           └──────────────────────────┘   │
                                           │
                                    ┌──────▼────────┐
                                    │  Web Browser  │
                                    │ (localhost:   │
                                    │     8505)     │
                                    └───────────────┘
```

---

## 🛠️ Technology Stack

### Backend
- **Python 3.x** - Core programming language
- **Threading** - Concurrent execution of sensor reading and web dashboard
- **CSV Module** - Data file handling
- **SMTP (smtplib)** - Email alert system
- **Requests** - HTTP API calls to ThingSpeak

### Frontend
- **Streamlit** - Modern web dashboard framework
- **Plotly** - Interactive gauge chart visualizations
- **Custom CSS** - Professional styling and layout

### APIs & Services
- **ThingSpeak** - IoT data platform for cloud storage and analytics
- **Gmail SMTP** - Email notification delivery

### Data Storage
- **CSV Files** - Sensor data storage
- **JSON Files** - Configuration and state management
- **Text Files** - Row position tracking

---

## 📁 Project Structure

```
A-Multi-Threaded-Environmental-Monitoring-System/
│
├── setup_and_run.sh            # 🚀 Automated setup and launch script
│
├── main_csv.py                 # Main entry point - starts both threads
├── csv_device.py               # Core sensor reading and processing logic
├── streamlit_dashboard.py      # Web dashboard UI
│
├── config.json                 # System configuration (API keys, thresholds)
├── config.template.json        # Template for configuration setup
│
├── data.csv                    # Sensor data source (25 rows of readings)
├── row_tracker.txt            # Tracks current row position
├── current_state.json         # Shared state between threads
│
└── README.md                   # This file
```

### File Descriptions

#### `setup_and_run.sh`
- **Type**: Bash script
- **Purpose**: Automated setup and launch script
- **Features**:
  - Validates project directory and Python installation
  - Auto-installs required packages (streamlit, plotly, requests)
  - Creates config.json from template if needed
  - Initializes row_tracker.txt
  - Checks data.csv exists
  - Launches the monitoring system
  - Provides colorful, user-friendly progress output
- **Usage**: `./setup_and_run.sh`
- **Benefit**: One-command setup for new users

#### `main_csv.py`
- Entry point for the application
- Loads configuration from `config.json`
- Creates `CsvSensor` instance
- Starts sensor reading in a background thread
- Launches Streamlit dashboard on port 8505

#### `csv_device.py`
- **Class**: `CsvSensor`
- **Key Methods**:
  - `_get_current_row_index()` - Reads current position from tracker
  - `_update_row_index(index)` - Updates position in tracker
  - `_read_data_from_csv()` - Reads specific row from CSV
  - `_send_to_thingspeak()` - Uploads data to cloud platform
  - `_send_email_alert()` - Sends SMTP email notifications
  - `run_simulation()` - Main loop that processes data every 20 seconds

#### `streamlit_dashboard.py`
- **Functions**:
  - `load_config()` - Loads system configuration
  - `load_current_data()` - Reads latest sensor data
  - `get_row_info()` - Gets current row progress
  - `create_enhanced_visualization()` - Creates gauge charts
  - `main()` - Dashboard layout and rendering

#### `config.json`
- Contains all system settings:
  - Device name and API credentials
  - Data file path and update interval
  - Threshold values for alerts
  - Email configuration (server, credentials, recipients)

#### `data.csv`
- Contains 25 rows of sensor readings
- Format: `CO2,Temperature,Humidity`
- Example: `400,22,40` (400 ppm CO₂, 22°C, 40% humidity)
- Data is preserved (not deleted) during processing

#### `row_tracker.txt`
- Simple text file storing current row index
- Allows system to resume from last position
- Prevents data duplication

#### `current_state.json`
- Shared data structure between threads
- Contains: latest readings, status, timestamp
- Updated by sensor thread, read by dashboard

---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.x installed
- Internet connection (for ThingSpeak and email)
- Gmail account with App Password (for email alerts)

### Step 1: Install Dependencies

```bash
# Install required Python packages
pip install streamlit plotly requests

# Or using conda
conda install -c conda-forge streamlit plotly requests
```

### Step 2: Configure the System

1. **Copy the template configuration**:
   ```bash
   cp config.template.json config.json
   ```

2. **Edit `config.json`** with your credentials:
   ```json
   {
     "device_name": "Your Device Name",
     "api_key": "YOUR_THINGSPEAK_API_KEY",
     "data_file": "data.csv",
     "update_interval": 20,
     "temperature_limit": 22,
     "humidity_limit": 45,
     "co2_limit": 1000,
     "email": {
       "enabled": true,
       "smtp_server": "smtp.gmail.com",
       "smtp_port": 587,
       "sender_email": "your-email@gmail.com",
       "sender_password": "your-app-password",
       "recipient_email": "recipient@example.com"
     }
   }
   ```

### Step 3: Prepare Data File

Ensure `data.csv` exists with sensor readings:
```csv
400,22,40
450,23,42
500,24,45
...
```

Format: `CO2_ppm,Temperature_celsius,Humidity_percent`

### Step 4: Initialize Row Tracker

Create an empty tracker file (or let the system create it):
```bash
echo "0" > row_tracker.txt
```

---

## ⚙️ Configuration

### Threshold Settings

| Parameter | Default | Description |
|-----------|---------|-------------|
| `temperature_limit` | 22°C | Temperature warning threshold |
| `humidity_limit` | 45% | Humidity warning threshold |
| `co2_limit` | 1000 ppm | CO₂ warning threshold |
| `update_interval` | 20 seconds | Time between readings |

### Email Configuration

To enable email alerts:

1. **Enable 2-Step Verification** on your Gmail account
2. **Generate App Password**:
   - Go to Google Account Settings → Security
   - Select "App passwords"
   - Generate password for "Mail"
3. **Update config.json**:
   - Set `email.enabled` to `true`
   - Add your Gmail address as `sender_email`
   - Add the 16-character app password as `sender_password`

### ThingSpeak Setup

1. Create free account at [ThingSpeak.com](https://thingspeak.com)
2. Create a new channel with 3 fields:
   - Field 1: CO₂ Level
   - Field 2: Temperature
   - Field 3: Humidity
3. Copy the "Write API Key"
4. Add to `config.json` as `api_key`

---

## 🎮 Usage

### Starting the System

**Option 1: Using the automated script (Easiest)**
```bash
# Run the setup and launch script
./setup_and_run.sh
```

**Option 2: Run manually**
```bash
# Run the main application
python3 main_csv.py
```

The automated script (`setup_and_run.sh`) performs the following:
1. ✅ Verifies you're in the correct directory
2. ✅ Checks Python installation
3. ✅ Installs required packages automatically
4. ✅ Creates/verifies configuration file
5. ✅ Initializes or checks row tracker
6. ✅ Validates data.csv exists
7. ✅ Launches the application

This will:
1. ✅ Load configuration
2. ✅ Start CSV sensor reading thread
3. ✅ Launch web dashboard at `http://localhost:8505`
4. ✅ Begin processing data every 20 seconds

### Accessing the Dashboard

Open your web browser and navigate to:
```
http://localhost:8505
```

The dashboard will automatically refresh every 2 seconds to show the latest readings.

### Stopping the System

Press `Ctrl+C` in the terminal to stop both threads gracefully.

### Restarting from Beginning

To restart from the first row:
```bash
echo "0" > row_tracker.txt
python3 main_csv.py
```

---

## 📊 Dashboard Features

### Main Components

#### 1. Title Bar
- 🌡️ IoT Environmental Monitoring Dashboard
- Professional gradient background
- System branding

#### 2. Row Progress Indicator
- Shows: "Reading row 5 of 25"
- Tracks progress through dataset
- Updates in real-time

#### 3. Metric Cards (Left Column)
Three cards displaying current readings:
- **CO₂ Level** - Shows ppm with status indicator
- **Temperature** - Shows °C with status indicator
- **Humidity** - Shows % with status indicator

Status Indicators:
- 🟢 **Normal** - Value below threshold
- 🟡 **Warning** - Value at threshold
- 🔴 **Critical** - Value significantly above threshold

#### 4. Gauge Visualization (Right Column)
Three separate gauges with:
- **Color-coded zones**: Green (safe), Orange (warning), Red (danger)
- **Threshold markers**: Orange line showing warning limit
- **Delta values**: Shows deviation from threshold
- **Appropriate scales**: 
  - CO₂: 0-1500 ppm
  - Temperature: 0-40°C
  - Humidity: 0-100%

#### 5. Footer
- ⏱️ Update interval: 20 seconds
- 📧 Email alerts: Enabled/Disabled
- 🕐 Last updated timestamp

---

## 🔄 How It Works

### Data Flow

1. **Initialization**
   - System reads `config.json` for settings
   - Loads last position from `row_tracker.txt`
   - Creates `current_state.json` if not exists

2. **Data Reading Loop** (Thread 1)
   ```
   Every 20 seconds:
   ├─ Read current row index from row_tracker.txt
   ├─ Read corresponding row from data.csv
   ├─ Parse CO₂, Temperature, Humidity values
   ├─ Display readings in terminal
   ├─ Check threshold violations
   ├─ Send email alert if threshold exceeded
   ├─ Upload data to ThingSpeak
   ├─ Save to current_state.json
   ├─ Increment row index in row_tracker.txt
   └─ Wait 20 seconds, repeat
   ```

3. **Dashboard Loop** (Thread 2)
   ```
   Every 2 seconds:
   ├─ Read current_state.json
   ├─ Load configuration from config.json
   ├─ Update metric cards with latest values
   ├─ Update gauge charts
   ├─ Refresh row progress indicator
   └─ Auto-refresh page
   ```

### Multi-Threading Design

The system uses two concurrent threads:

**Thread 1: Data Processor** (`csv_device.py`)
- Runs continuously in background
- Independent of dashboard
- Handles all data I/O operations
- Manages alerts and API calls

**Thread 2: Web Dashboard** (`streamlit_dashboard.py`)
- Runs Streamlit web server
- Reads shared state from JSON
- Displays real-time visualization
- No direct CSV access

**Communication**: Threads communicate through `current_state.json` file

---

## ⚠️ Threshold Monitoring

### Threshold Logic

Each metric has configurable thresholds with three zones:

#### CO₂ Level
- **🟢 Safe**: 0 - 1000 ppm
- **🟡 Warning**: 1000 - 1200 ppm
- **🔴 Critical**: > 1200 ppm

#### Temperature
- **🟢 Safe**: < 22°C
- **🟡 Warning**: 22 - 25°C
- **🔴 Critical**: > 25°C

#### Humidity
- **🟢 Safe**: < 45%
- **🟡 Warning**: 45 - 55%
- **🔴 Critical**: > 55%

### Alert Triggering

Alerts are triggered when:
1. Current reading exceeds configured threshold
2. Status changes from "Normal" to "Warning"
3. Email is enabled in configuration

### Alert Content

Email alerts include:
- ⚠️ Warning header
- Device name
- Exceeded metric name and value
- Threshold value
- Timestamp
- All current readings

---

## 📧 Email Alerts

### Configuration

```json
"email": {
  "enabled": true,
  "smtp_server": "smtp.gmail.com",
  "smtp_port": 587,
  "sender_email": "your-email@gmail.com",
  "sender_password": "your-app-password",
  "recipient_email": "recipient@example.com"
}
```

### Alert Trigger Conditions

Emails are sent when ANY of these conditions are met:
- Temperature > `temperature_limit`
- Humidity > `humidity_limit`
- CO₂ > `co2_limit`

### Sample Email

```
Subject: ⚠️ Alert: High Temperature Detected - Main Office Sensor

⚠️ ENVIRONMENTAL ALERT ⚠️

Device: Main Office Sensor
Time: 2025-11-06 14:30:45

THRESHOLD EXCEEDED:
Temperature: 24°C (Limit: 22°C)

Current Readings:
- CO₂ Level: 450 ppm
- Temperature: 24°C ⚠️
- Humidity: 42%

Please check the environmental conditions immediately.
```

### Troubleshooting Email

If emails aren't working:
1. ✅ Verify Gmail 2-Step Verification is enabled
2. ✅ Use App Password, not regular password
3. ✅ Check `email.enabled` is `true` in config.json
4. ✅ Verify SMTP server and port are correct
5. ✅ Check terminal for error messages

---

## 🌐 API Integration

### ThingSpeak IoT Platform

**Purpose**: Cloud storage and analytics for sensor data

**Configuration**:
- Channel ID: Auto-assigned by ThingSpeak
- Write API Key: Required in `config.json`

**Data Upload Format**:
```
https://api.thingspeak.com/update?api_key=YOUR_KEY
&field1=CO2_VALUE
&field2=TEMP_VALUE
&field3=HUMIDITY_VALUE
```

**Features**:
- Automatic data backup to cloud
- Historical data visualization
- Public/Private channel options
- MATLAB analytics integration
- Mobile app access

**Viewing Your Data**:
1. Log in to ThingSpeak
2. Navigate to "Channels" → "My Channels"
3. Select your channel
4. View real-time graphs and historical data

---

## 🧪 Testing & Validation

### Manual Testing

1. **Verify Data Reading**:
   ```bash
   python3 main_csv.py
   # Check terminal for "Reading row X of 25" messages
   ```

2. **Check Dashboard**:
   - Open `http://localhost:8505`
   - Verify gauges show correct values
   - Confirm auto-refresh works (2-second intervals)

3. **Test Threshold Alerts**:
   - Modify `data.csv` with values exceeding thresholds
   - Verify email is received
   - Check dashboard shows warning status

4. **Validate Row Tracking**:
   - Stop system after processing 5 rows
   - Check `row_tracker.txt` shows "5"
   - Restart system
   - Verify it resumes from row 6

### Expected Behavior

- ✅ System processes one row every 20 seconds
- ✅ Dashboard updates every 2 seconds
- ✅ Emails sent only when thresholds exceeded
- ✅ Original CSV data remains intact
- ✅ Row tracker increments correctly
- ✅ ThingSpeak receives data (check channel graphs)

---

## 🐛 Troubleshooting

### Common Issues

**Issue**: "Module not found" errors
```
Solution: Install missing packages
pip install streamlit plotly requests
```

**Issue**: Dashboard doesn't update
```
Solution: Check if current_state.json exists and is being updated
ls -la current_state.json
cat current_state.json
```

**Issue**: Email alerts not sending
```
Solution: 
1. Verify email.enabled = true
2. Check app password (not regular password)
3. Look for SMTP errors in terminal
```

**Issue**: "File not found: data.csv"
```
Solution: Ensure data.csv is in same directory as main_csv.py
```

**Issue**: System reads same row repeatedly
```
Solution: Check row_tracker.txt permissions
chmod 644 row_tracker.txt
```

**Issue**: ThingSpeak returns error
```
Solution: Verify API key is correct in config.json
Check rate limits (15 second minimum between updates)
```

---

## 📈 Future Enhancements

Potential improvements for the project:

1. **Database Integration** - Store historical data in SQLite/PostgreSQL
2. **Real Sensor Support** - Interface with actual IoT hardware (Arduino, Raspberry Pi)
3. **Advanced Analytics** - Add trend analysis, predictions, anomaly detection
4. **Mobile App** - Native iOS/Android application
5. **Multiple Sensors** - Support for multiple monitoring locations
6. **Data Export** - CSV/Excel export functionality
7. **User Authentication** - Login system for dashboard access
8. **Configurable Dashboard** - Drag-and-drop widget customization
9. **SMS Alerts** - Twilio integration for text notifications
10. **Historical Graphs** - Time-series visualization of past data

---

## 👥 Contributors

- **Your Name** - Project Developer
- **Mentor Name** - Project Advisor

---

## 📄 License

This project is created for educational purposes as part of [Your Institution/Course Name].

---

## 📞 Support

For questions or issues:
- Check the troubleshooting section above
- Review terminal output for error messages
- Verify all configuration files are correct
- Ensure all dependencies are installed

---

## 🙏 Acknowledgments

- ThingSpeak IoT Platform for cloud data storage
- Streamlit framework for rapid dashboard development
- Plotly for interactive visualizations
- Python community for excellent libraries

---

**Last Updated**: November 6, 2025  
**Version**: 1.0  
**Python Version**: 3.x  
**Status**: Production Ready ✅
