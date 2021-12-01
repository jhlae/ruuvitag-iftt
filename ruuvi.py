from ruuvitag_sensor.ruuvitag import RuuviTag
import requests
import json
from decouple import config
from datetime import datetime

FIREBASE_URL = config('FIREBASE_URL')
IFTT_KEY = config('IFTT_KEY')

sensor = RuuviTag('RUUVITAG_MAC_ADDRESS')

# Current date and timestamp
now = datetime.now()
timestamp = datetime.timestamp(now)

# Update state from RuuviTag
state = sensor.update()

# Get latest sensor state
state = sensor.state

# Prepare JSON, send headers and data to IFTT's custom trigger
if(state):
  temp = str(state["temperature"])
  headers = {
    'Content-type': 'application/json',
  }

data = json.dumps(state)
response = requests.put(FIREBASE_URL, headers=headers, data=data)
x = requests.get('https://maker.ifttt.com/trigger/ruuvi_temperature_updated/with/key/'+IFTT_KEY+'&value1='+temp)

print(response)
print(timestamp)
print(x.status_code)
