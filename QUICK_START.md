# 🚀 Quick Setup Guide for Friends

## Super Simple 3-Step Setup

### Step 1: Get the Project
```bash
# Download or clone the project
cd A-Multi-Threaded-Environmental-Monitoring-System-main-2
```

### Step 2: Run the Magic Script
```bash
./setup_and_run.sh
```

### Step 3: Open Your Browser
```
http://localhost:8505
```

## That's It! 🎉

The script automatically handles:
- ✅ Installing packages (streamlit, plotly, requests)
- ✅ Setting up configuration
- ✅ Creating tracker files
- ✅ Launching the dashboard

---

## If the Script Doesn't Run

Make it executable first:
```bash
chmod +x setup_and_run.sh
./setup_and_run.sh
```

---

## Manual Setup (If You Want Control)

```bash
# 1. Install packages
pip install streamlit plotly requests

# 2. Copy config template
cp config.template.json config.json

# 3. Edit config.json (add your API key, disable email if you want)

# 4. Create tracker
echo "0" > row_tracker.txt

# 5. Run
python3 main_csv.py
```

---

## Common Questions

**Q: Do I need API keys?**
A: You need a ThingSpeak API key (free at thingspeak.com). Email is optional - you can disable it in config.json.

**Q: What if I get an error?**
A: Check that you have Python 3 installed (`python3 --version`)

**Q: How do I stop it?**
A: Press `Ctrl + C` in the terminal

**Q: How do I restart from the beginning?**
A: Run `echo "0" > row_tracker.txt` then start again

---

## Config.json Quick Template

Minimal config to get started (no email):
```json
{
  "device_name": "My Test Sensor",
  "api_key": "YOUR_THINGSPEAK_API_KEY_HERE",
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

Just replace `YOUR_THINGSPEAK_API_KEY_HERE` with your actual key!

---

**Need more help?** Check the full README.md for detailed documentation.
