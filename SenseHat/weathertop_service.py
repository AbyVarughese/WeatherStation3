import json
import time
 
from datetime import datetime
# Use Flask framework
from flask import Flask
from sense_hat import SenseHat

 

__version__ = '0.1'

 

app = Flask(__name__)

 
# default page is just status as well as /status page
@app.route('/', methods=['GET'])
@app.route('/status', methods=['GET'])
def status():
  return ({'status': 'ok', 'appversion': __version__, 'utcnow': datetime.utcnow().isoformat()+'Z'}, 200)

 
# on /senshat page we return senory data in the same format used by weather api
@app.route('/sensehat', methods=['GET'])
def sensehat_values():
  sense = SenseHat()
  humidity = sense.get_humidity()
  temph = sense.get_temperature_from_humidity()
  tempp = sense.get_temperature_from_pressure()
  pressure = sense.get_pressure()
  #return ({'humidity': humidity, 'temph': temph, 'tempp': tempp, 'pressure': pressure}, 200)
  return ({'dt': int(time.time()), 'weather': [{'id': 804}], 'wind': {'speed': 0, 'deg': 0}, 'main': {'temp': round(temph,2), 'pressure': int(pressure)}}, 200)

 

#main app starts web server
if __name__ == '__main__':
  print(' > Starting server')
  try:
    app.run(host='0.0.0.0', port=8082)
  finally:
    print(' > Server shut down')