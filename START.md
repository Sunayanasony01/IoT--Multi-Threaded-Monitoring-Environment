# 🚀 Quick Start Guide

Get your IoT Environmental Monitoring System up and running in **5 minutes**!

---

## 📋 Prerequisites

- **Python 3.12+** installed (Anaconda recommended)
- **Internet connection** (for weather API)
- **Gmail account** (optional, for email alerts)

---

## 🎯 Step-by-Step Setup

### Step 1: Install Dependencies

```bash
pip install requests streamlit plotly
```

**Verify installation:**
```bash
python -c "import requests, streamlit, plotly; print('✅ All packages installed!')"
```

---

### Step 2: Get Your API Keys

#### 🌤️ WeatherAPI.com (Required)

1. Go to: https://www.weatherapi.com/signup.aspx
2. Sign up with your email (FREE, 1 million calls/month!)
3. Copy your API key from the dashboard
4. **Save it** - you'll need it in Step 3

**Example key format:** `08101473693f4bc9b50140331250911`

---

#### ☁️ ThingSpeak (Optional - for cloud backup)

1. Go to: https://thingspeak.com/
2. Sign up for a free account
3. Click **"New Channel"**
4. Add 3 fields:
   - Field 1: CO2
   - Field 2: Temperature
   - Field 3: Humidity
5. Go to **API Keys** tab
6. Copy **Write API Key**

---

#### 📧 Gmail App Password (Optional - for alerts)

1. Enable **2-Step Verification** on your Google account
2. Go to: https://myaccount.google.com/apppasswords
3. Select **"Mail"** and generate password
4. Copy the 16-character password (format: `xxxx xxxx xxxx xxxx`)

---

### Step 3: Configure the System

Open `config.json` and update these fields:

```json
{
  "device_name": "Live Weather Sensor - Bangalore",
  "api_key": "YOUR_THINGSPEAK_API_KEY",
  "update_interval": 20,
  "temperature_limit": 22,
  "humidity_limit": 45,
  "co2_limit": 1000,
  "weather_api": {
    "api_key": "YOUR_WEATHERAPI_KEY",      ← Add your WeatherAPI key here
    "city": "Bangalore",                   ← Change to your city
    "country_code": "IN"                   ← Change to your country code
  },
  "email": {
    "enabled": true,
    "smtp_server": "smtp.gmail.com",
    "smtp_port": 587,
    "from_addr": "your-email@gmail.com",   ← Your Gmail address
    "to_addr": "your-email@gmail.com",     ← Alert recipient email
    "username": "your-email@gmail.com",    ← Your Gmail address
    "password": "xxxx xxxx xxxx xxxx"      ← Gmail app password
  }
}
```

**Minimum required:**
- `weather_api.api_key` ✅ Required
- `weather_api.city` ✅ Required
- Everything else is optional!

---

### Step 4: Run the System

#### Terminal 1: Start Data Fetcher

```bash
python main_api.py
```

You should see:
```
╔════════════════════════════════════════════════════════════╗
║     🌤️  LIVE WEATHER-BASED IoT MONITORING SYSTEM          ║
╚════════════════════════════════════════════════════════════╝

🔧 Initializing weather sensor...
✅ Live data fetched: 23.2°C, 57%, ~600 ppm CO₂
```

**Keep this terminal running!** ⚠️

---

#### Terminal 2: Launch Dashboard

Open a **new terminal** and run:

```bash
streamlit run streamlit_dashboard.py --server.port 8505
```

Dashboard will open automatically, or visit: **http://localhost:8505**

---

## 🎉 You're Done!

Your system is now:
- ✅ Fetching live weather data every 20 seconds
- ✅ Displaying it on a beautiful dashboard
- ✅ Sending email alerts when thresholds exceeded
- ✅ Uploading data to ThingSpeak cloud (if configured)

---

## 🎨 What You'll See

### Dashboard Features:

1. **🌡️ Temperature Gauge**
   - Green zone: Safe (< 22°C)
   - Yellow zone: Warning
   - Red zone: Alert! (> 22°C)

2. **💧 Humidity Gauge**
   - Green: < 45%
   - Yellow: 45-60%
   - Red: > 60%

3. **💨 CO₂ Gauge**
   - Green: < 1000 ppm
   - Yellow: 1000-1500 ppm
   - Red: > 1500 ppm

4. **Auto-refresh** every 2 seconds!

---

## 🔧 Customization

### Change Your City

Edit `config.json`:
```json
"weather_api": {
  "city": "London",
  "country_code": "GB"
}
```

### Adjust Thresholds

```json
"temperature_limit": 25,    ← Alert when > 25°C
"humidity_limit": 60,       ← Alert when > 60%
"co2_limit": 1500          ← Alert when > 1500 ppm
```

### Change Update Interval

```json
"update_interval": 30       ← Fetch data every 30 seconds
```

---

## 🐛 Troubleshooting

### Problem: API 401 Error

**Solution:** Check your WeatherAPI key in `config.json`

Test it manually:
```bash
curl "http://api.weatherapi.com/v1/current.json?key=YOUR_KEY&q=Bangalore,IN&aqi=yes"
```

---

### Problem: Dashboard Not Updating

**Solutions:**
1. Make sure `main_api.py` is running in Terminal 1
2. Check if `current_state.json` file exists and is updating
3. Refresh your browser (F5)

---

### Problem: Email Not Sending

**Solutions:**
1. Use Gmail **App Password**, not your regular password!
2. Make sure 2-Step Verification is enabled
3. Set `"enabled": true` in email config
4. Check `from_addr`, `username`, and `password` are correct

---

### Problem: Import Error (requests, streamlit, etc.)

**Solution:** Use `python` instead of `python3`:
```bash
python main_api.py
```

If still failing, reinstall:
```bash
pip install --upgrade requests streamlit plotly
```

---

## 🌐 Alternative: CSV Simulation Mode

Don't want to use live API? Use CSV simulation:

```bash
# Terminal 1
python main_csv.py

# Terminal 2
streamlit run streamlit_dashboard.py --server.port 8505
```

This reads data from `data.csv` instead of the weather API.

---

## 🛑 How to Stop

1. **Stop Dashboard**: Go to Terminal 2, press `Ctrl+C`
2. **Stop Data Fetcher**: Go to Terminal 1, press `Ctrl+C`

---

## ⚡ Quick Command Reference

```bash
# Install packages
pip install requests streamlit plotly

# Run live weather mode
python main_api.py

# Run CSV simulation mode
python main_csv.py

# Launch dashboard
streamlit run streamlit_dashboard.py --server.port 8505

# Test API key
curl "http://api.weatherapi.com/v1/current.json?key=YOUR_KEY&q=Bangalore,IN&aqi=yes"

# Verify packages
python -c "import requests, streamlit, plotly; print('OK')"
```

---

## 📚 Next Steps

- Check **[README.md](README.md)** for complete documentation
- Customize thresholds in `config.json`
- Set up ThingSpeak cloud backup
- Configure email alerts
- Try different cities!

---

## 💡 Pro Tips

1. **Keep both terminals open** while system is running
2. Dashboard auto-refreshes - no need to manually reload
3. Email alerts only sent when thresholds exceeded
4. ThingSpeak keeps historical data for analysis
5. You can change city/thresholds anytime by editing `config.json`

---

## 🆘 Need Help?

**Common Questions:**

**Q: Can I use a different city?**  
A: Yes! Edit `weather_api.city` and `weather_api.country_code` in `config.json`

**Q: Do I need all the API keys?**  
A: No! Only WeatherAPI is required. ThingSpeak and Gmail are optional.

**Q: How often does it update?**  
A: Every 20 seconds (configurable via `update_interval`)

**Q: Can I run without internet?**  
A: Use CSV mode: `python main_csv.py`

**Q: Is it free?**  
A: Yes! WeatherAPI free tier gives 1 million calls/month.

---

**🎊 Enjoy your IoT monitoring system!**

Made with ❤️ for environmental monitoring
