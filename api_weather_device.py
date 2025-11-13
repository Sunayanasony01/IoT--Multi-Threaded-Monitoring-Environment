import requests
import time
import json
import os
import smtplib
from email.message import EmailMessage
from datetime import datetime

class WeatherSensor:
    """
    Live weather sensor class that fetches real-time data from WeatherAPI.com
    
    This replaces CSV-based data with actual live weather data:
    - Current Weather: temperature and humidity
    - Air Quality: CO2, PM2.5, PM10, etc.
    
    WeatherAPI.com advantages:
    - Instant activation (no 15-minute wait!)
    - More reliable
    - Better free tier
    - Includes air quality data
    """
    
    def __init__(self, name, api_key, interval, weather_api_key, city, country_code="IN"):
        self.name = name
        self.api_key = api_key  # ThingSpeak API key
        self.interval = interval
        self.weather_api_key = weather_api_key  # WeatherAPI.com API key
        self.city = city
        self.country_code = country_code
        
        # WeatherAPI.com endpoint (includes both weather AND air quality!)
        self.weather_url = f"http://api.weatherapi.com/v1/current.json?key={weather_api_key}&q={city},{country_code}&aqi=yes"
        
        print(f" Weather Sensor '{self.name}' initialized for {self.city}, {self.country_code}")
        print(f"📡 Fetching live data from WeatherAPI.com")
        print(f"Debug - API URL: {self.weather_url}")

    def fetch_live_weather_data(self):
        """
        Fetch real-time weather data from WeatherAPI.com
        
        Returns:
            tuple: (temperature, humidity, co2_equivalent) or (None, None, None) on error
        """
        try:
            # Fetch current weather data (includes air quality!)
            response = requests.get(self.weather_url, timeout=10)
            
            if response.status_code != 200:
                print(f"[{self.name}]  Weather API returned status code {response.status_code}")
                if response.status_code == 403:
                    print(f"[{self.name}]  API key may be invalid or not activated yet")
                return None, None, None
            
            data = response.json()
            
            # Extract temperature and humidity
            temp = data['current']['temp_c']
            humidity = data['current']['humidity']
            
            # Extract air quality data
            co2_equivalent = 400  # Default baseline
            
            if 'air_quality' in data['current']:
                aqi_data = data['current']['air_quality']
                
                # WeatherAPI provides US EPA standard AQI
                us_epa_index = aqi_data.get('us-epa-index', 1)
                
                # Also has CO (Carbon Monoxide in μg/m3)
                co = aqi_data.get('co', 0)
                
                # Convert EPA AQI to CO2 equivalent
                # EPA Index: 1=Good, 2=Moderate, 3=Unhealthy for Sensitive, 4=Unhealthy, 5=Very Unhealthy, 6=Hazardous
                aqi_to_co2 = {
                    1: 400,   # Good air quality → baseline CO2
                    2: 600,   # Moderate
                    3: 800,   # Unhealthy for sensitive groups
                    4: 1000,  # Unhealthy
                    5: 1200,  # Very Unhealthy
                    6: 1400   # Hazardous
                }
                co2_equivalent = aqi_to_co2.get(us_epa_index, 400)
                
                # Adjust based on actual CO measurement if available
                if co > 0:
                    # CO is in μg/m³, use it to refine CO2 estimate
                    co2_from_co = 400 + (co / 10)
                    co2_equivalent = max(co2_equivalent, min(1500, co2_from_co))
                
                print(f"[{self.name}] Air Quality Index: {us_epa_index} → CO₂ Equivalent: {co2_equivalent:.0f} ppm")
            else:
                print(f"[{self.name}]  Air quality data not available, using baseline CO₂")
            
            print(f"[{self.name}] Live data fetched: {temp}°C, {humidity}%, ~{co2_equivalent:.0f} ppm CO₂")
            
            return temp, humidity, co2_equivalent
            
        except requests.exceptions.Timeout:
            print(f"[{self.name}]  API request timed out")
            return None, None, None
        except requests.exceptions.RequestException as e:
            print(f"[{self.name}]  Network error: {e}")
            return None, None, None
        except KeyError as e:
            print(f"[{self.name}]  Unexpected API response format: {e}")
            return None, None, None
        except Exception as e:
            print(f"[{self.name}]  Error fetching weather data: {e}")
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
            print(f"[{self.name}]   Email alert sent to {email_cfg.get('to_addr')}")
            return True
        except Exception as e:
            print(f"[{self.name}]    Failed to send email: {e}")
            return False

    def _send_to_thingspeak(self, co2, temp, humidity):
        """Upload data to ThingSpeak IoT platform"""
        try:
            url = f"https://api.thingspeak.com/update?api_key={self.api_key}&field1={co2:.1f}&field2={temp:.1f}&field3={humidity:.1f}"
            response = requests.get(url, timeout=10)
            if response.status_code == 200 and response.text != '0':
                print(f"[{self.name}]    ThingSpeak updated (Entry ID: {response.text})")
                return True
            else:
                print(f"[{self.name}]    ThingSpeak update failed (Response: {response.text})")
                return False
        except Exception as e:
            print(f"[{self.name}]    ThingSpeak error: {e}")
            return False

    def run_simulation(self):
        """
        Main loop: Fetch live weather data at regular intervals and process it
        """
        print(f"[{self.name}]   Starting live weather monitoring...")
        print(f"[{self.name}]   Location: {self.city}, {self.country_code}")
        print(f"[{self.name}]    Update interval: {self.interval} seconds")
        print(f"[{self.name}]   {'='*60}\n")
        
        iteration = 0
        
        try:
            while True:
                iteration += 1
                print(f"\n{'='*60}")
                print(f"[{self.name}]   DATA FETCH #{iteration} - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                print(f"{'='*60}")
                
                # Fetch live data from API
                temp, humidity, co2_equivalent = self.fetch_live_weather_data()
                
                if temp is None or humidity is None or co2_equivalent is None:
                    print(f"[{self.name}]    Failed to fetch data. Retrying in {self.interval} seconds...")
                    time.sleep(self.interval)
                    continue
                
                # Load configuration for thresholds
                cfg = None
                try:
                    with open('config.json', 'r') as f:
                        cfg = json.load(f)
                except Exception as e:
                    print(f"[{self.name}]    Could not load config: {e}")
                
                temp_limit = cfg.get('temperature_limit') if cfg else None
                humid_limit = cfg.get('humidity_limit') if cfg else None
                co2_limit = cfg.get('co2_limit', 1000) if cfg else 1000
                email_cfg = cfg.get('email') if cfg else None
                
                # Check thresholds
                status = "Normal"
                warnings = []
                
                if co2_limit is not None and co2_equivalent > float(co2_limit):
                    warnings.append(f"High CO2: {co2_equivalent:.0f} ppm > {co2_limit} ppm")
                if temp_limit is not None and temp > float(temp_limit):
                    warnings.append(f"High Temperature: {temp}°C > {temp_limit}°C")
                if humid_limit is not None and humidity > float(humid_limit):
                    warnings.append(f"High Humidity: {humidity}% > {humid_limit}%")
                
                if warnings:
                    status = "WARNING"
                
                # Display live dashboard in terminal
                print(f"\n{'─'*60}")
                print(f"   LIVE ENVIRONMENTAL MONITORING DASHBOARD")
                print(f"{'─'*60}")
                print(f"   Location     : {self.city}, {self.country_code}")
                print(f"   CO2 Level    : {co2_equivalent:.0f} ppm")
                print(f"   Temperature  : {temp}°C")
                print(f"   Humidity     : {humidity}%")
                print(f"   Status       : {status}")
                if warnings:
                    print(f"{'─'*60}")
                    print("   ALERTS:")
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
                        'data_source': 'WeatherAPI.com'
                    }
                    with open('current_state.json', 'w') as f:
                        json.dump(state, f, indent=2)
                    print(f"[{self.name}]   State saved for web dashboard")
                except Exception as e:
                    print(f"[{self.name}]   Failed to save state: {e}")
                
                # Send email alerts if thresholds exceeded
                if warnings and email_cfg and email_cfg.get('enabled'):
                    subject = f"Environmental Alert from {self.name}"
                    body = f"""
ENVIRONMENTAL THRESHOLD EXCEEDED

Device: {self.name}
Location: {self.city}, {self.country_code}
Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Data Source: WeatherAPI.com

Current Readings:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CO2 Level (AQI-based):  {co2_equivalent:.0f} ppm
Temperature:            {temp}°C
Humidity:               {humidity}%

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
                print(f"\n[{self.name}]   Waiting {self.interval} seconds until next update...")
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
