import json
import threading
import time  # <-- THIS IS THE LINE I FORGOT
from csv_device import CsvSensor  # Import our new CSV sensor class

print("--- CSV-Based IoT Simulation: STARTING ---")

# Load the config file
try:
    with open('config.json', 'r') as f:
        config = json.load(f)
except FileNotFoundError:
    print("ERROR: config.json not found. Exiting.")
    exit()

# 1. Create the sensor object from the config
sensor_device = CsvSensor(
    name=config['device_name'],
    api_key=config['api_key'],
    interval=config['update_interval'],
    csv_file=config['data_file']
)

# 2. We use threading so the main program doesn't freeze
# This is a key "high-level" concept
print("--- Launching device thread... ---")
thread = threading.Thread(target=sensor_device.run_simulation, daemon=True)
thread.start()

print("--- System is LIVE. Press CTRL+C to stop. ---")

# Keep the main script alive so we can see the output
try:
    while thread.is_alive():
        time.sleep(1)
except KeyboardInterrupt:
    print("\n--- Main thread stopping. Shutting down... ---")