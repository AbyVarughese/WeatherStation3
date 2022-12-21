import os
import json
import requests

from sense_hat import SenseHat

script_dir = os.path.abspath(os.path.dirname( __file__ ))

with open(f"{script_dir}/config.json") as f:
  config = json.load(f)
  f.close()

try:
  sense = SenseHat()
  humidity = sense.get_humidity()
  temph = sense.get_temperature_from_humidity()
except:
  requests.post(config['ntfy_url'], data=f"❌ There was an error loading sensory data".encode(encoding='utf-8'))
  exit(1)

response = requests.get(config['weather_api'])
if not (response.status_code == 200 and 'application/json' in response.headers.get('Content-Type','')):
  requests.post(config['ntfy_url'], data=f"❌ There was an error loading data from weather api".encode(encoding='utf-8'))
  exit(1)

weather_data = response.json()
message = f"Weather is currently {weather_data['weather'][0]['description']} with temperature of {weather_data['main']['temp']} C and {weather_data['main']['humidity']}% humidity.\n\nYour SenseHat readings show temperature of {round(temph, 2)} C and {round(humidity, 2)}% humidity."
requests.post(config['ntfy_url'], data=message.encode(encoding='utf-8'))