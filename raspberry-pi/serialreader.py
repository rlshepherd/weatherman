from time import sleep
from datetime import datetime
import re
import logging

import serial

from models.weather import Weather, database

logging.basicConfig(filename='weatherman.log', level=logging.INFO)

def extract_value(reading, search_pattern = '[0-9]{2}'):
    """Get the numerical value from a string formatted arduino serial port write.
        
    Parameters:
    reading [str] - A string in the format b'Temperature: 24.00'
 
    Returns:
    [float] - reading value
    """
    r = re.search(search_pattern, reading)
    if r:
        found = r.group()
        return(found)
    else:
        raise ValueError('reading missing properly formatted numerical value.') 

# definition of a complete reading
temperature_pattern = re.compile("^b'Temperature")
humidity_pattern = re.compile("^b'Humidity")

# create a new record
weather = Weather()

# connect to the sensor
ser = serial.Serial("/dev/ttyACM0",9600)

# wait for a full reading from the sensor
t = False
h = False

logging.info('Taking reading at {}'.format(str(datetime.now)))

while not t or not h:
  sleep(2)
  reading = str(ser.readline())
  if temperature_pattern.match(reading):
      weather.temperature = extract_value(reading)
      t = True
      logging.info('Arduino : {}'.format(reading))
      logging.info('Extracted temperature value : {}'.format(weather.temperature))
  elif humidity_pattern.match(reading):
      weather.humidity = extract_value(reading)
      h = True
      logging.info('Arduino : {}'.format(reading))
      logging.info('Extract humidity value : {}'.format(weather.humidity))

weather.datetime = datetime.now()

# save record
weather.save() 
logging.info('Saved to {}: {}'.format(database, weather.__dict__))
