import os
import json
import time
import requests
import traceback
from datetime import datetime
from sense_hat import SenseHat

script_dir = os.path.abspath(os.path.dirname( __file__ ))
data_file = f"{script_dir}/sensehat_data.csv"

#infinite main loop
while True:
  #read configuration
  with open(f"{script_dir}/config.json") as f:
    config = json.load(f)
    f.close()

  #current date and time
  ts = datetime.utcnow().isoformat()+'Z'
  try:
    #read values from sensehat
    sense = SenseHat()
    humidity = sense.get_humidity()
    temph = sense.get_temperature_from_humidity()
    tempp = sense.get_temperature_from_pressure()
    pressure = sense.get_pressure()

    is_new_file = not os.path.exists(data_file)
    with open(data_file, "a") as f:
      #write header if file does not exist
      if is_new_file:
        f.write("timestamp,humidity,temp_humidity,pressure,temp_pressure\n")

      #write sensory values into csv database
      f.write(f"{ts},{humidity},{temph},{pressure},{tempp}\n")
      f.close()

    #check thresholds and send notifications using ntfy.sh service
    if temph < config['temp_low']:
      requests.post(config['ntfy_url'], data=f"🥶 Temperature below threshold: {round(temph, 2)}".encode(encoding='utf-8'))

    if temph > config['temp_high']:
      requests.post(config['ntfy_url'], data=f"🥵 Temperature above threshold: {round(temph, 2)}".encode(encoding='utf-8'))

  except:
    #log excpetions into the file
    with open("errors.log", "a") as logfile:
      traceback.print_exc(file=logfile)
  finally:
    #wait 5 minutes (configurable) before the next run
    time.sleep(config['sleep_time'])
