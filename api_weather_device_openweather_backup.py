import requests
import time
import json
import os
import smtplib
from email.message import EmailMessage
from datetime import datetime

class WeatherSensor:
    """
    Live weather sensor class that fetches real-time data from OpenWeatherMap API
    
    This replaces CSV-based data with actual live weather data from external APIs:
    - Current Weather API: for temperature and humidity
    - Air Quality API: for CO2 equivalent (AQI/Air Quality Index)
    """
    
    def __init__(self, name, api_key, interval, weather_api_key, city, country_code="IN"):
        self.name = name
        self.api_key = api_key  # ThingSpeak API key
        self.interval = interval
        self.weather_api_key = weather_api_key  # OpenWeatherMap API key
        self.city = city
        self.country_code = country_code
        
        # OpenWeatherMap API endpoints
        self.weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={city},{country_code}&appid={weather_api_key}&units=metric"
        self.air_quality_url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={{lat}}&lon={{lon}}&appid={weather_api_key}"
        
        print(f"🌤️  Weather Sensor '{self.name}' initialized for {self.city}, {self.country_code}")
        print(f"📡 Fetching live data from OpenWeatherMap API")

    def fetch_live_weather_data(self):
        """
        Fetch real-time weather data from OpenWeatherMap API
        
        Returns:
            tuple: (temperature, humidity, co2_equivalent) or (None, None, None) on error
        """
        try:
            # Fetch current weather data
            response = requests.get(self.weather_url, timeout=10)
            
            if response.status_code != 200:
                print(f"[{self.name}] ⚠️  Weather API returned status code {response.status_code}")
                return None, None, None
            
            weather_data = response.json()
            
            # Extract temperature and humidity
            temp = weather_data['main']['temp']
            humidity = weather_data['main']['humidity']
            
            # Get coordinates for air quality API
            lat = weather_data['coord']['lat']
            lon = weather_data['coord']['lon']
            
            # Fetch air quality data (CO2 equivalent from AQI)
            air_quality_response = requests.get(
                self.air_quality_url.format(lat=lat, lon=lon), 
                timeout=10
            )
            
            co2_equivalent = 400  # Default baseline value
            aqi = 1  # Default good air quality
            
            if air_quality_response.status_code == 200:
                air_data = air_quality_response.json()
                
                # AQI (Air Quality Index): 1=Good, 2=Fair, 3=Moderate, 4=Poor, 5=Very Poor
                aqi = air_data['list'][0]['main']['aqi']
                
                # Get component concentrations (including CO, NO2, etc.)
                components = air_data['list'][0]['components']
                
                # Convert AQI to CO2 equivalent for monitoring
                # This is an approximation based on air quality
                aqi_to_co2 = {
                    1: 400,   # Good air quality → baseline CO2
                    2: 600,   # Fair
                    3: 800,   # Moderate
                    4: 1000,  # Poor
                    5: 1200   # Very Poor
                }
                co2_equivalent = aqi_to_co2.get(aqi, 400)
                
                # If CO data is available, use it to adjust
                if 'co' in components and components['co'] > 0:
                    # CO is in μg/m³, convert to rough CO2 equivalent
                    co_concentration = components['co']
                    co2_equivalent = max(co2_equivalent, min(1500, 400 + (co_concentration / 10)))
                
                print(f"[{self.name}] 🌍 Air Quality Index: {aqi} → CO₂ Equivalent: {co2_equivalent:.0f} ppm")
            
            print(f"[{self.name}] ✅ Live data fetched: {temp}°C, {humidity}%, ~{co2_equivalent:.0f} ppm CO₂")
            
            return temp, humidity, co2_equivalent
            
        except requests.exceptions.Timeout:
            print(f"[{self.name}] ⚠️  API request timed out")
            return None, None, None
        except requests.exceptions.RequestException as e:
            print(f"[{self.name}] ⚠️  Network error: {e}")
            return None, None, None
        except KeyError as e:
            print(f"[{self.name}] ⚠️  Unexpected API response format: {e}")
            return None, None, None
        except Exception as e:
            print(f"[{self.name}] ⚠️  Error fetching weather data: {e}")
            return None, None, None

    def _send_email_alert(self, subject: str, body: str, email_cfg: dict):
        """Send email alert when thresholds are exceeded"""
        if not email_cfg or not email_cfg.get('enabled'):
            return False

        try:
            msg = EmailMessage()
            msg['Subject'] = subject
            msg['From'] = email_cfg.get('from_addr')
            msg['To'] = email_cfg.get('to_addr')
            msg.set_content(body)

            server = smtplib.SMTP(email_cfg.get('smtp_server'), email_cfg.get('smtp_port'))
            if email_cfg.get('use_tls'):
                server.starttls()
            username = email_cfg.get('username')
            password = email_cfg.get('password')
            if username:
                server.login(username, password)
            server.send_message(msg)
            server.quit()
            print(f"[{self.name}]   📧 Email alert sent to {email_cfg.get('to_addr')}")
            return True
        except Exception as e:
            print(f"[{self.name}]   ⚠️  Failed to send email: {e}")
            return False

    def _send_to_thingspeak(self, co2, temp, humidity):
        """Upload data to ThingSpeak IoT platform"""
        try:
            url = f"https://api.thingspeak.com/update?api_key={self.api_key}&field1={co2:.1f}&field2={temp:.1f}&field3={humidity:.1f}"
            response = requests.get(url, timeout=10)
            if response.status_code == 200 and response.text != '0':
                print(f"[{self.name}]   ☁️  ThingSpeak updated (Entry ID: {response.text})")
                return True
            else:
                print(f"[{self.name}]   ⚠️  ThingSpeak update failed (Response: {response.text})")
                return False
        except Exception as e:
            print(f"[{self.name}]   ⚠️  ThingSpeak error: {e}")
            return False

    def run_simulation(self):
        """
        Main loop: Fetch live weather data at regular intervals and process it
        
        This replaces the CSV reading logic with live API calls
        """
        print(f"[{self.name}]   🚀 Starting live weather monitoring...")
        print(f"[{self.name}]   📍 Location: {self.city}, {self.country_code}")
        print(f"[{self.name}]   ⏱️  Update interval: {self.interval} seconds")
        print(f"[{self.name}]   {'='*60}\n")
        
        iteration = 0
        
        try:
            while True:
                iteration += 1
                print(f"\n{'='*60}")
                print(f"[{self.name}]   📊 DATA FETCH #{iteration} - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                print(f"{'='*60}")
                
                # Fetch live data from API
                temp, humidity, co2_equivalent = self.fetch_live_weather_data()
                
                if temp is None or humidity is None or co2_equivalent is None:
                    print(f"[{self.name}]   ⚠️  Failed to fetch data. Retrying in {self.interval} seconds...")
                    time.sleep(self.interval)
                    continue
                
                # Load configuration for thresholds
                cfg = None
                try:
                    with open('config.json', 'r') as f:
                        cfg = json.load(f)
                except Exception as e:
                    print(f"[{self.name}]   ⚠️  Could not load config: {e}")
                
                temp_limit = cfg.get('temperature_limit') if cfg else None
                humid_limit = cfg.get('humidity_limit') if cfg else None
                co2_limit = cfg.get('co2_limit', 1000) if cfg else 1000
                email_cfg = cfg.get('email') if cfg else None
                
                # Check thresholds
                status = "Normal"
                warnings = []
                
                if co2_limit is not None and co2_equivalent > float(co2_limit):
                    warnings.append(f"⚠️  High CO₂: {co2_equivalent:.0f} ppm > {co2_limit} ppm")
                if temp_limit is not None and temp > float(temp_limit):
                    warnings.append(f"⚠️  High Temperature: {temp}°C > {temp_limit}°C")
                if humid_limit is not None and humidity > float(humid_limit):
                    warnings.append(f"⚠️  High Humidity: {humidity}% > {humid_limit}%")
                
                if warnings:
                    status = "⚠️  WARNING"
                
                # Display live dashboard in terminal
                print(f"\n{'─'*60}")
                print(f"   🌡️  LIVE ENVIRONMENTAL MONITORING DASHBOARD")
                print(f"{'─'*60}")
                print(f"   📍 Location     : {self.city}, {self.country_code}")
                print(f"   💨 CO₂ Level    : {co2_equivalent:.0f} ppm")
                print(f"   🌡️  Temperature  : {temp}°C")
                print(f"   💧 Humidity     : {humidity}%")
                print(f"   📊 Status       : {status}")
                if warnings:
                    print(f"{'─'*60}")
                    print("   🚨 ALERTS:")
                    for w in warnings:
                        print(f"      {w}")
                print(f"{'─'*60}\n")
                
                # Save current state for web dashboard
                try:
                    state = {
                        'co2': round(co2_equivalent, 1),
                        'temperature': round(temp, 1),
                        'humidity': round(humidity, 1),
                        'status': status,
                        'warnings': warnings,
                        'timestamp': datetime.now().isoformat(),
                        'location': f"{self.city}, {self.country_code}",
                        'data_source': 'OpenWeatherMap API'
                    }
                    with open('current_state.json', 'w') as f:
                        json.dump(state, f, indent=2)
                    print(f"[{self.name}]   💾 State saved for web dashboard")
                except Exception as e:
                    print(f"[{self.name}]   ⚠️  Failed to save state: {e}")
                
                # Send email alerts if thresholds exceeded
                if warnings and email_cfg and email_cfg.get('enabled'):
                    subject = f"🚨 Environmental Alert from {self.name}"
                    body = f"""
⚠️  ENVIRONMENTAL THRESHOLD EXCEEDED ⚠️

Device: {self.name}
Location: {self.city}, {self.country_code}
Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Data Source: Live OpenWeatherMap API

Current Readings:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💨 CO₂ Level (AQI-based):  {co2_equivalent:.0f} ppm
🌡️  Temperature:           {temp}°C
💧 Humidity:              {humidity}%

Alerts:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{chr(10).join(warnings)}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Please check the environmental conditions immediately.

This is an automated alert from your IoT Environmental Monitoring System.
                    """
                    self._send_email_alert(subject, body, email_cfg)
                
                # Upload to ThingSpeak
                self._send_to_thingspeak(co2_equivalent, temp, humidity)
                
                # Wait for next update
                print(f"\n[{self.name}]   ⏳ Waiting {self.interval} seconds until next update...")
                print(f"{'='*60}\n")
                time.sleep(self.interval)
                
        except KeyboardInterrupt:
            print(f"\n\n{'='*60}")
            print(f"[{self.name}]   🛑 Monitoring stopped by user")
            print(f"{'='*60}\n")
            return
        except Exception as e:
            print(f"\n[{self.name}]   ❌ Fatal error: {e}")
            import traceback
            traceback.print_exc()
