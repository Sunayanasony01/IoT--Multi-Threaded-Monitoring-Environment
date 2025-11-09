import json
import threading
import time
from api_weather_device import WeatherSensor  # Import our new weather sensor class

print("╔════════════════════════════════════════════════════════════╗")
print("║     🌤️  LIVE WEATHER-BASED IoT MONITORING SYSTEM          ║")
print("║     Real-time data from OpenWeatherMap API                 ║")
print("╚════════════════════════════════════════════════════════════╝\n")

# Load the config file
try:
    with open('config.json', 'r') as f:
        config = json.load(f)
except FileNotFoundError:
    print("❌ ERROR: config.json not found.")
    print("\n💡 Please create config.json from config.api.template.json:")
    print("   cp config.api.template.json config.json")
    print("   Then edit config.json with your API keys\n")
    exit(1)

# Validate required fields
weather_api = config.get('weather_api')
if not weather_api or not weather_api.get('api_key') or weather_api.get('api_key') == 'YOUR_OPENWEATHERMAP_API_KEY':
    print("❌ ERROR: OpenWeatherMap API key not configured!")
    print("\n📝 Setup Instructions:")
    print("   1. Get FREE API key from: https://home.openweathermap.org/users/sign_up")
    print("   2. Add your API key to config.json under 'weather_api.api_key'")
    print("   3. Set your city in 'weather_api.city' (e.g., 'Bangalore')")
    print("   4. Set country code in 'weather_api.country_code' (e.g., 'IN' for India)\n")
    exit(1)

# Create the weather sensor object
print("🔧 Initializing weather sensor...")
sensor_device = WeatherSensor(
    name=config['device_name'],
    api_key=config['api_key'],  # ThingSpeak API key
    interval=config['update_interval'],
    weather_api_key=weather_api['api_key'],
    city=weather_api.get('city', 'Bangalore'),
    country_code=weather_api.get('country_code', 'IN')
)

# Start the sensor in a background thread
print("\n🚀 Launching weather monitoring thread...")
thread = threading.Thread(target=sensor_device.run_simulation, daemon=True)
thread.start()

print("\n╔════════════════════════════════════════════════════════════╗")
print("║  ✅ SYSTEM IS LIVE                                         ║")
print("║                                                            ║")
print("║  📊 Dashboard: http://localhost:8505                       ║")
print("║  🛑 Stop: Press CTRL+C                                     ║")
print("║                                                            ║")
print("║  The system is now fetching live weather data from        ║")
print("║  OpenWeatherMap every few seconds and displaying it       ║")
print("║  on the Streamlit dashboard.                              ║")
print("╚════════════════════════════════════════════════════════════╝\n")

# Keep the main script alive
try:
    while thread.is_alive():
        time.sleep(1)
except KeyboardInterrupt:
    print("\n\n╔════════════════════════════════════════════════════════════╗")
    print("║  🛑 System stopped by user. Goodbye!                       ║")
    print("╚════════════════════════════════════════════════════════════╝\n")
