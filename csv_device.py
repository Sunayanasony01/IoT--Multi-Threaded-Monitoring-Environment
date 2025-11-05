import requests
import time
import csv
import os
import smtplib
from email.message import EmailMessage

class CsvSensor:
    
    def __init__(self, name, api_key, interval, csv_file):
        self.name = name
        self.api_key = api_key
        self.interval = interval
        self.csv_file = csv_file
        print(f"Device '{self.name}' created. Reading from '{self.csv_file}'.")

    def _send_email_alert(self, subject: str, body: str, email_cfg: dict):
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
            print(f"[{self.name}]   > Email alert sent to {email_cfg.get('to_addr')}")
            return True
        except Exception as e:
            print(f"[{self.name}]   > Failed to send email: {e}")
            return False

    # This is a "generator" function
    def _get_current_row_index(self):
        """Get the current row index from tracker file"""
        tracker_file = 'row_tracker.txt'
        try:
            if os.path.exists(tracker_file):
                with open(tracker_file, 'r') as f:
                    return int(f.read().strip())
            return 0
        except Exception:
            return 0
    
    def _update_row_index(self, index):
        """Update the row tracker file"""
        tracker_file = 'row_tracker.txt'
        try:
            with open(tracker_file, 'w') as f:
                f.write(str(index))
        except Exception as e:
            print(f"[{self.name}]   > Error updating tracker: {e}")
    
    def _read_data_from_csv(self):
        try:
            with open(self.csv_file, 'r') as file:
                csv_reader = csv.reader(file)
                # Read all rows including header
                rows = list(csv_reader)

            if not rows:
                return

            header = rows[0]
            for row in rows[1:]:
                # yield each data row as a list of strings
                yield row
                    
        except FileNotFoundError:
            print(f"[{self.name}]   > ERROR: Could not find file {self.csv_file}")
            return
        except Exception as e:
            print(f"[{self.name}]   > ERROR reading CSV: {e}")
            return

    # The main loop that reads and sends data
    def run_simulation(self):
        print(f"[{self.name}]   > Starting simulation...")
        # Read rows sequentially using a tracker file (no deletion)
        try:
            while True:
                # Get current row index
                current_index = self._get_current_row_index()
                
                # Read all rows from CSV
                try:
                    with open(self.csv_file, 'r') as file:
                        rows = list(csv.reader(file))
                except FileNotFoundError:
                    print(f"[{self.name}]   > ERROR: Could not find file {self.csv_file}")
                    break
                
                # Check if we have data rows (excluding header)
                data_rows = rows[1:] if len(rows) > 1 else []
                
                if not data_rows:
                    print(f"[{self.name}]   > No data rows in CSV. Exiting simulation.")
                    break
                
                # If we've processed all rows, loop back to start
                if current_index >= len(data_rows):
                    current_index = 0
                    self._update_row_index(0)
                    print(f"[{self.name}]   > Reached end of data. Starting from beginning...")
                
                # Get the current row to process
                current_row = data_rows[current_index]
                
                try:
                    co2_s, temp_s, humid_s = current_row[0], current_row[1], current_row[2]
                    co2 = float(co2_s)
                    temp = float(temp_s)
                    humid = float(humid_s)

                    # Dashboard display
                    status = "Normal"
                    warnings = []

                    # Read limits from config file if available
                    cfg = None
                    try:
                        import json
                        with open('config.json', 'r') as f:
                            cfg = json.load(f)
                    except Exception:
                        cfg = None

                    temp_limit = cfg.get('temperature_limit') if cfg else None
                    humid_limit = cfg.get('humidity_limit') if cfg else None
                    email_cfg = cfg.get('email') if cfg else None

                    if temp_limit is not None and temp > float(temp_limit):
                        warnings.append(f"⚠️ Warning: High Temperature ({temp} > {temp_limit})")
                    if humid_limit is not None and humid > float(humid_limit):
                        warnings.append(f"⚠️ Warning: High Humidity ({humid} > {humid_limit})")

                    if warnings:
                        status = "Warning"

                    # Print a simple terminal dashboard
                    print("\n=== DASHBOARD ===")
                    print(f"CO2: {co2} ppm")
                    print(f"Temperature: {temp} °C")
                    print(f"Humidity: {humid} %")
                    print(f"Status: {status}")
                    for w in warnings:
                        print(w)
                    print("=================\n")

                    # Save current state for web dashboard
                    try:
                        from datetime import datetime
                        state = {
                            'co2': co2,
                            'temperature': temp,
                            'humidity': humid,
                            'status': status,
                            'warnings': warnings,
                            'timestamp': datetime.now().isoformat()
                        }
                        with open('current_state.json', 'w') as f:
                            json.dump(state, f, indent=2)
                    except Exception as e:
                        print(f"[{self.name}]   > Failed to save state for web dashboard: {e}")

                    # If warning(s) and email enabled, send an alert
                    if warnings and email_cfg and email_cfg.get('enabled'):
                        subject = f"Alert from {self.name}: {', '.join(warnings)}"
                        body = f"Sensor reading exceeded threshold(s):\n\nCO2: {co2}\nTemperature: {temp}\nHumidity: {humid}\n\nDetails:\n" + "\n".join(warnings)
                        self._send_email_alert(subject, body, email_cfg)

                    # Optionally send to ThingSpeak (keep existing behavior)
                    try:
                        url = f"https://api.thingspeak.com/update?api_key={self.api_key}&field1={co2}&field2={temp}&field3={humid}"
                        response = requests.get(url, timeout=10)
                        if response.status_code == 200:
                            print(f"[{self.name}]   > Success (Entry ID: {response.text})")
                        else:
                            print(f"[{self.name}]   > Failed to send to ThingSpeak (code {response.status_code})")
                    except Exception as e:
                        print(f"[{self.name}]   > Error sending to ThingSpeak: {e}")

                    # Update the row tracker to move to next row (NO DELETION)
                    try:
                        next_index = current_index + 1
                        self._update_row_index(next_index)
                        print(f"[{self.name}]   > Row {current_index + 1} processed (kept in CSV, moving to next)")
                    except Exception as e:
                        print(f"[{self.name}]   > Failed to update row tracker: {e}")

                    # Wait specified interval
                    print(f"[{self.name}]   > Waiting {self.interval} seconds...\n")
                    time.sleep(self.interval)

                except KeyboardInterrupt:
                    print(f"[{self.name}]   > Simulation stopped by user.")
                    return
                except Exception as e:
                    print(f"[{self.name}]   > Error during loop processing row: {e}")
                    # Avoid tight error loop
                    time.sleep(self.interval)

        except Exception as e:
            print(f"[{self.name}]   > Fatal error in simulation loop: {e}")