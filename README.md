# 🌡️ IoT Multi-Threaded Environmental Monitoring System# 🌡️ Multi-Threaded Environmental Monitoring System



A real-time IoT environmental monitoring system with **live weather API integration** and **CSV simulation modes**. Features multi-threaded architecture, interactive web dashboard, cloud data backup, and automated email alerts.A real-time IoT environmental monitoring system that reads sensor data from CSV files, displays live readings on an interactive web dashboard, monitors threshold violations, and sends automated email alerts.



---## 📋 Table of Contents

- [Quick Start Guide](#-quick-start-guide)

## ✨ Features- [Overview](#overview)

- [Features](#features)

- 🌤️ **Live Weather Data**: Real-time temperature, humidity, and air quality from WeatherAPI.com- [System Architecture](#system-architecture)

- 📊 **Interactive Dashboard**: Beautiful Streamlit web interface with color-coded gauge charts- [Technology Stack](#technology-stack)

- 🔄 **Multi-Threading**: Concurrent data fetching and dashboard updates- [Project Structure](#project-structure)

- ☁️ **Cloud Integration**: Automatic data backup to ThingSpeak IoT platform- [Installation & Setup](#installation--setup)

- 📧 **Email Alerts**: Automated Gmail notifications when thresholds are exceeded- [Configuration](#configuration)

- 📈 **Dual Modes**: Switch between live API data or CSV file simulation- [Usage](#usage)

- 🎨 **Visual Indicators**: Color-coded zones (green/yellow/red) for easy monitoring- [Dashboard Features](#dashboard-features)

- [How It Works](#how-it-works)

---- [Threshold Monitoring](#threshold-monitoring)

- [Email Alerts](#email-alerts)

## 🚀 Quick Start- [API Integration](#api-integration)



See **[START.md](START.md)** for the complete step-by-step guide!---



**TL;DR:**## 🚀 Quick Start Guide

```bash

# 1. Install dependencies**For someone forking/cloning this project for the first time:**

pip install requests streamlit plotly

### ⚡ Option 1: Automated Setup (Recommended)

# 2. Configure your API keys in config.json

Just run the setup script - it does everything for you!

# 3. Run the system

python main_api.py```bash

# Clone the repository

# 4. In a new terminal, launch dashboardgit clone <repository-url>

streamlit run streamlit_dashboard.py --server.port 8505cd A-Multi-Threaded-Environmental-Monitoring-System-main-2

```

# Run the automated setup script

Open browser: **http://localhost:8505**./setup_and_run.sh

```

---

The script will automatically:

## 📁 Project Structure- ✅ Check Python installation

- ✅ Install required packages (streamlit, plotly, requests)

```- ✅ Create config.json from template

IoT--Multi-Threaded-Monitoring-Environment/- ✅ Initialize row tracker

├── main_api.py                 # Entry point for live weather API mode- ✅ Validate data files

├── main_csv.py                 # Entry point for CSV simulation mode- ✅ Launch the dashboard at http://localhost:8505

├── api_weather_device.py       # Weather API sensor class

├── csv_device.py               # CSV simulator sensor class**That's it!** The system will start automatically. 🎉

├── streamlit_dashboard.py      # Web dashboard interface

├── config.json                 # Configuration file (API keys, thresholds)---

├── current_state.json          # Live data state (auto-generated)

├── data.csv                    # Sample sensor data for simulation### 🔧 Option 2: Manual Setup

├── setup_and_run.sh           # Automated setup script

├── README.md                   # This fileIf you prefer to set up manually:

└── START.md                    # Quick start guide

```#### Step 1: Clone the Repository

```bash

---# Clone the repository

git clone <repository-url>

## 🏗️ System Architecturecd A-Multi-Threaded-Environmental-Monitoring-System-main-2



```# Or if you downloaded as ZIP, extract and navigate to the folder

┌─────────────────────────────────────────────────────────────┐cd A-Multi-Threaded-Environmental-Monitoring-System-main-2

│                    LIVE API MODE                            │```

├─────────────────────────────────────────────────────────────┤

│                                                             │#### Step 2: Install Dependencies

│  Thread 1: Data Fetcher          Thread 2: Dashboard       │```bash

│  ┌─────────────────────┐         ┌─────────────────────┐  │# Option 1: Using pip

│  │  WeatherAPI.com     │         │   Streamlit Web     │  │pip install streamlit plotly requests

│  │  (every 20 sec)     │────────▶│   Dashboard         │  │

│  │                     │  JSON   │   (auto-refresh)    │  │# Option 2: Using conda (recommended)

│  │  • Fetch temp       │  file   │                     │  │conda install -c conda-forge streamlit plotly requests

│  │  • Fetch humidity   │         │  • Gauge charts     │  │```

│  │  • Fetch AQI        │         │  • Live updates     │  │

│  │  • Check thresholds │         │  • Color zones      │  │#### Step 3: Set Up Configuration

│  │  • Send alerts      │         │                     │  │```bash

│  │  • Upload to cloud  │         │                     │  │# Copy the template to create your config file

│  └─────────────────────┘         └─────────────────────┘  │cp config.template.json config.json

│         │                                                   │

│         ├──▶ Gmail SMTP (Email Alerts)                     │# Edit config.json with your details (use any text editor)

│         └──▶ ThingSpeak API (Cloud Backup)                 │# You need to add:

│                                                             │# - ThingSpeak API key (get free at thingspeak.com)

└─────────────────────────────────────────────────────────────┘# - Gmail credentials for alerts (optional - can disable)

``````



---**Minimal config.json to get started** (without email alerts):

```json

## ⚙️ Configuration{

  "device_name": "Test Sensor",

Edit `config.json` to customize your setup:  "api_key": "YOUR_THINGSPEAK_KEY",

  "data_file": "data.csv",

```json  "update_interval": 20,

{  "temperature_limit": 22,

  "device_name": "Live Weather Sensor - Bangalore",  "humidity_limit": 45,

  "api_key": "YOUR_THINGSPEAK_API_KEY",  "co2_limit": 1000,

  "update_interval": 20,  "email": {

  "temperature_limit": 22,    "enabled": false

  "humidity_limit": 45,  }

  "co2_limit": 1000,}

  "weather_api": {```

    "api_key": "YOUR_WEATHERAPI_KEY",

    "city": "Bangalore",#### Step 4: Initialize Tracker File

    "country_code": "IN"```bash

  },# Create the row tracker (starts from first row)

  "email": {echo "0" > row_tracker.txt

    "enabled": true,```

    "smtp_server": "smtp.gmail.com",

    "smtp_port": 587,#### Step 5: Run the Application

    "from_addr": "your-email@gmail.com",```bash

    "to_addr": "alert-email@gmail.com",# Start the system

    "username": "your-email@gmail.com",python3 main_csv.py

    "password": "your-app-password"```

  }

}#### Step 6: Access the Dashboard

```Open your browser and go to:

```

### 🔑 Getting API Keyshttp://localhost:8505

```

**WeatherAPI.com (Required for Live Mode):**

1. Go to https://www.weatherapi.com/signup.aspx**That's it!** 🎉 The system will start reading sensor data every 20 seconds and display it on the dashboard.

2. Sign up for free account (1M calls/month)

3. Copy your API key from dashboard---

4. Add to `config.json` → `weather_api.api_key`

### 📝 Quick Commands Reference

**ThingSpeak (Optional - Cloud Backup):**

1. Go to https://thingspeak.com/| Command | Purpose |

2. Create a free account|---------|---------|

3. Create a new channel with 3 fields (CO₂, Temp, Humidity)| `./setup_and_run.sh` | **🚀 Automated setup and run (easiest!)** |

4. Copy Write API Key| `python3 main_csv.py` | Start the monitoring system manually |

5. Add to `config.json` → `api_key`| `Ctrl + C` | Stop the system |

| `echo "0" > row_tracker.txt` | Reset to first row |

**Gmail App Password (Optional - Email Alerts):**| `cat current_state.json` | View current readings |

1. Enable 2-Step Verification on your Google account| `tail -f row_tracker.txt` | Monitor progress |

2. Go to https://myaccount.google.com/apppasswords| `chmod +x setup_and_run.sh` | Make setup script executable (if needed) |

3. Generate new app password for "Mail"

4. Add to `config.json` → `email.password`---



---## 🎯 Overview



## 📊 Dashboard FeaturesThis project simulates an IoT environmental monitoring system for indoor air quality management. It reads sensor data (CO₂, Temperature, Humidity) from a CSV file sequentially, processes each reading with configurable time intervals, displays the data on a modern web dashboard, and triggers alerts when values exceed predefined thresholds.



The Streamlit dashboard displays:**Use Case**: Office building environmental monitoring, smart home automation, data center climate control, greenhouse management.



- **Temperature Gauge**: Color-coded temperature monitoring---

  - 🟢 Green: Below threshold (safe)

  - 🟡 Yellow: Approaching threshold## ✨ Features

  - 🔴 Red: Above threshold (alert!)

### Core Functionality

- **Humidity Gauge**: Real-time humidity percentage- ✅ **Sequential CSV Data Processing** - Reads sensor data row-by-row with configurable intervals (default: 20 seconds)

  - 🟢 Green: Below 45%- ✅ **Non-Destructive Reading** - Preserves original CSV data using a position tracker system

  - 🟡 Yellow: 45-60%- ✅ **Real-Time Web Dashboard** - Interactive Streamlit-based UI with auto-refresh

  - 🔴 Red: Above 60%- ✅ **Multi-Threaded Architecture** - Concurrent data processing and web serving

- ✅ **Threshold Monitoring** - Automatic detection of abnormal readings

- **CO₂ Gauge**: Air quality monitoring (converted from AQI)- ✅ **Email Alerts** - SMTP-based notifications when thresholds are exceeded

  - 🟢 Green: Below 1000 ppm- ✅ **Cloud Integration** - Automatic data upload to ThingSpeak IoT platform

  - 🟡 Yellow: 1000-1500 ppm- ✅ **Professional Visualization** - Gauge charts with color-coded zones

  - 🔴 Red: Above 1500 ppm

### Dashboard Features

- **Real-time Updates**: Auto-refresh every 2 seconds- 🎯 **Real-Time Gauge Charts** - Separate gauges for each metric with appropriate scales

- **Live Alerts**: Visual warnings when thresholds exceeded- 📊 **Live Metric Cards** - Current readings with color-coded status indicators

- **Timestamp**: Last update time display- 🔔 **Alert Notifications** - Visual warnings when thresholds are exceeded

- 📍 **Row Progress Tracker** - Shows current position in dataset

---- ⏱️ **System Status Footer** - Displays update interval, email status, and timestamp

- 🎨 **Responsive Design** - Professional IoT dashboard styling

## 🔧 How It Works

---

### Live API Mode (`main_api.py`)

## 🏗️ System Architecture

1. **Initialization**: Loads config, validates API keys

2. **Background Thread**: Starts weather data fetcher```

3. **API Polling**: Fetches data from WeatherAPI.com every 20 seconds┌─────────────────────────────────────────────────────────────┐

4. **Data Processing**: │                     Main Application                         │

   - Extracts temperature, humidity, air quality│                    (main_csv.py)                             │

   - Converts AQI to CO₂ equivalent└────────────────────────┬────────────────────────────────────┘

   - Checks threshold violations                         │

5. **Alert System**: Sends email if thresholds exceeded                    ┌────▼────┐

6. **Cloud Backup**: Uploads to ThingSpeak                    │ Config  │

7. **State Update**: Saves to `current_state.json`                    │  Loader │

8. **Dashboard**: Streamlit reads state file and displays live gauges                    └────┬────┘

                         │

### CSV Simulation Mode (`main_csv.py`)        ┌────────────────┴────────────────┐

        │                                  │

- Reads sensor data from `data.csv` row by row   ┌────▼─────┐                    ┌──────▼────────┐

- Simulates real sensor readings   │  Thread 1│                    │   Thread 2    │

- Same dashboard, alerts, and cloud features   │CSV Sensor│                    │   Streamlit   │

- Useful for testing without API dependencies   │ Processor│                    │   Dashboard   │

   └────┬─────┘                    └──────┬────────┘

---        │                                  │

        │  ┌──────────────────────────┐   │

## 🎯 Threshold Monitoring        ├─►│   data.csv (Source)      │   │

        │  └──────────────────────────┘   │

The system monitors three key environmental parameters:        │                                  │

        │  ┌──────────────────────────┐   │

| Parameter | Default Threshold | Configured In |        ├─►│ row_tracker.txt (Index)  │   │

|-----------|------------------|---------------|        │  └──────────────────────────┘   │

| Temperature | 22°C | `temperature_limit` |        │                                  │

| Humidity | 45% | `humidity_limit` |        │  ┌──────────────────────────┐   │

| CO₂ Level | 1000 ppm | `co2_limit` |        ├─►│ current_state.json       │◄──┤

        │  │ (Shared State)           │   │

When any parameter exceeds its threshold:        │  └──────────────────────────┘   │

- 📧 Email alert sent (if enabled)        │                                  │

- 🔴 Dashboard shows red zone        │  ┌──────────────────────────┐   │

- ⚠️ Console warning logged        ├─►│ ThingSpeak API           │   │

- ☁️ Data uploaded to cloud for analysis        │  └──────────────────────────┘   │

        │                                  │

---        │  ┌──────────────────────────┐   │

        └─►│ SMTP Email Server        │   │

## 📧 Email Alerts           └──────────────────────────┘   │

                                           │

When thresholds are violated, the system sends detailed email alerts:                                    ┌──────▼────────┐

                                    │  Web Browser  │

**Subject:** `⚠️ Environmental Alert from [Device Name]`                                    │ (localhost:   │

                                    │     8505)     │

**Contains:**                                    └───────────────┘

- 🌡️ Current temperature vs threshold```

- 💧 Current humidity vs threshold

- 💨 Current CO₂ level vs threshold---

- ⏰ Timestamp of violation

- 📍 Location information## 🛠️ Technology Stack



**Setup:**### Backend

1. Use Gmail with 2-Step Verification- **Python 3.x** - Core programming language

2. Generate App Password (see Configuration section)- **Threading** - Concurrent execution of sensor reading and web dashboard

3. Add credentials to `config.json`- **CSV Module** - Data file handling

4. Set `email.enabled: true`- **SMTP (smtplib)** - Email alert system

- **Requests** - HTTP API calls to ThingSpeak

---

### Frontend

## 🌐 Two Operating Modes- **Streamlit** - Modern web dashboard framework

- **Plotly** - Interactive gauge chart visualizations

### 🌤️ Live Weather Mode (Recommended)- **Custom CSS** - Professional styling and layout

```bash

python main_api.py### APIs & Services

```- **ThingSpeak** - IoT data platform for cloud storage and analytics

- Real-time data from WeatherAPI.com- **Gmail SMTP** - Email notification delivery

- Actual weather conditions for your city

- Best for production/demo### Data Storage

- **CSV Files** - Sensor data storage

### 📊 CSV Simulation Mode- **JSON Files** - Configuration and state management

```bash- **Text Files** - Row position tracking

python main_csv.py

```---

- Reads from `data.csv` file

- Useful for testing/development## 📁 Project Structure

- No API key required

```

**Both modes** use the same dashboard!A-Multi-Threaded-Environmental-Monitoring-System/

│

---├── setup_and_run.sh            # 🚀 Automated setup and launch script

│

## 🛠️ Technology Stack├── main_csv.py                 # Main entry point - starts both threads

├── csv_device.py               # Core sensor reading and processing logic

- **Python 3.12+**├── streamlit_dashboard.py      # Web dashboard UI

- **Streamlit**: Web dashboard framework│

- **Plotly**: Interactive gauge visualizations├── config.json                 # System configuration (API keys, thresholds)

- **Requests**: HTTP API calls├── config.template.json        # Template for configuration setup

- **Threading**: Concurrent execution│

- **WeatherAPI.com**: Live weather data├── data.csv                    # Sensor data source (25 rows of readings)

- **ThingSpeak**: IoT cloud platform├── row_tracker.txt            # Tracks current row position

- **Gmail SMTP**: Email notifications├── current_state.json         # Shared state between threads

│

---└── README.md                   # This file

```

## 🐛 Troubleshooting

### File Descriptions

**Dashboard not updating?**

- Check if `main_api.py` or `main_csv.py` is running#### `setup_and_run.sh`

- Verify `current_state.json` is being updated- **Type**: Bash script

- Refresh browser page- **Purpose**: Automated setup and launch script

- **Features**:

**API returning 401 error?**  - Validates project directory and Python installation

- Verify API key in `config.json`  - Auto-installs required packages (streamlit, plotly, requests)

- Check if WeatherAPI key is active  - Creates config.json from template if needed

- Test with: `curl "http://api.weatherapi.com/v1/current.json?key=YOUR_KEY&q=Bangalore,IN&aqi=yes"`  - Initializes row_tracker.txt

  - Checks data.csv exists

**Email not sending?**  - Launches the monitoring system

- Verify Gmail app password (not regular password!)  - Provides colorful, user-friendly progress output

- Check 2-Step Verification is enabled- **Usage**: `./setup_and_run.sh`

- Ensure `email.enabled: true` in config- **Benefit**: One-command setup for new users



**Import errors (requests, streamlit, etc.)?**#### `main_csv.py`

- Use correct Python: `python main_api.py` (not `python3`)- Entry point for the application

- Install packages: `pip install requests streamlit plotly`- Loads configuration from `config.json`

- Creates `CsvSensor` instance

---- Starts sensor reading in a background thread

- Launches Streamlit dashboard on port 8505

## 📝 License

#### `csv_device.py`

This project is open source and available for educational purposes.- **Class**: `CsvSensor`

- **Key Methods**:

---  - `_get_current_row_index()` - Reads current position from tracker

  - `_update_row_index(index)` - Updates position in tracker

## 👥 Contributing  - `_read_data_from_csv()` - Reads specific row from CSV

  - `_send_to_thingspeak()` - Uploads data to cloud platform

Feel free to fork, modify, and create pull requests!  - `_send_email_alert()` - Sends SMTP email notifications

  - `run_simulation()` - Main loop that processes data every 20 seconds

**Possible Enhancements:**

- Add more weather parameters (wind speed, pressure, etc.)#### `streamlit_dashboard.py`

- Historical data graphs- **Functions**:

- Multiple location monitoring  - `load_config()` - Loads system configuration

- Mobile app integration  - `load_current_data()` - Reads latest sensor data

- Database storage (PostgreSQL, MongoDB)  - `get_row_info()` - Gets current row progress

- Docker containerization  - `create_enhanced_visualization()` - Creates gauge charts

- REST API endpoints  - `main()` - Dashboard layout and rendering



---#### `config.json`

- Contains all system settings:

## 🙏 Acknowledgments  - Device name and API credentials

  - Data file path and update interval

- **WeatherAPI.com**: Free weather data API  - Threshold values for alerts

- **ThingSpeak**: IoT cloud platform  - Email configuration (server, credentials, recipients)

- **Streamlit**: Amazing dashboard framework

- **Plotly**: Beautiful visualizations#### `data.csv`

- Contains 25 rows of sensor readings

---- Format: `CO2,Temperature,Humidity`

- Example: `400,22,40` (400 ppm CO₂, 22°C, 40% humidity)

**Made with ❤️ for IoT Environmental Monitoring**- Data is preserved (not deleted) during processing



Need help? Check **[START.md](START.md)** for detailed setup instructions!#### `row_tracker.txt`

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
