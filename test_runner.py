import shutil
import time
import json
from csv_device import CsvSensor

# Create a temporary copy of data.csv to avoid modifying the real data
orig = 'data.csv'
copy = 'data_test.csv'
shutil.copyfile(orig, copy)

# Load config and tweak for fast testing
with open('config.json', 'r') as f:
    cfg = json.load(f)

cfg['data_file'] = copy
cfg['update_interval'] = 2  # short interval for test
# keep email disabled for safety
cfg['email']['enabled'] = False

sensor = CsvSensor(name=cfg['device_name'], api_key=cfg['api_key'], interval=cfg['update_interval'], csv_file=cfg['data_file'])

try:
    sensor.run_simulation()
except KeyboardInterrupt:
    print('Test interrupted by user')

print('Test run complete. Remaining rows in', copy)
with open(copy, 'r') as f:
    print(f.read())
