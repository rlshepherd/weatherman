---
layout: post
title:  "Keeping Track with Raspberry Pi"
date:   2018-12-15 00:47:35 -0800
categories: arduino weatherman update hardware
---

Following up on the last post, weatherman was able to take sensor readings
on temperature and humidity as well as print those reading to the serial port.

In this post, we want to start keeping track of those readings so we can build
a historical weather record of our neighborhood. 

## Equipment

A raspberry pi is very well suited to solving our storage problem. It has plently of
computing power for running some simple processes and expandable storage via SD cards.

With that in mind our part list for this step is:
1. Raspberry Pi 3
2. 32G Micro SD Card
3. Peripherals (mouse, keyboard, monitor, usb cables)

After setting up the Pi using the [great online documenatation](https://projects.raspberrypi.org/en/projects/raspberry-pi-getting-started), 
you can immediately start powering the arduino from one of the Pi's USB ports:

![Raspberry Pi](/weatherman/assets/picircuit.png)

## Data Transfer

Getting data out of the arduino and into the pi is very straightforward using
python's serial library:

```python
from time import sleep
import serial

ser = serial.Serial("/dev/ttyACM0",9600)

while True:
  sleep(2)
  serialreader = ser.readline()
  print(serialreader)
```

This simple script is enough to get started:

![Data Transfer](/weatherman/assets/serialreader.png)

## Database

For the data persistence and data layers, I wanted to keep it light weight and simple.
So I choose [SQLite](https://sqlite.org/index.html) (though SQLite is suprisingly powerful and underestimated.)
and the [peewee framework](http://docs.peewee-orm.com/en/latest/) for python.

Here is a simple weather reading model using peewee:

```python
from peewee import *

database = SqliteDatabase('weather.db')

class BaseModel(Model):
    class Meta:
    database = database

class Weather(BaseModel):
    id = AutoField(unique = True, primary_key = True)
    datetime = DateTimeField()
    temperature = FloatField()
    humidity = FloatField()
```

## Connecting the pieces

After creating a database and model, a python script can be used to tranform
and save the reading coming from the arduino over the serial port.

Because the data coming from the arduino is raw text, this script also handles
parsing and validation.

```python
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
```

## Automation

Now the pi can take over. I set the crontab to execute the script every 5 minutes (better too much than too little?). Instead of calling the script directly, crontab calls a bash script which invokes the python script via it's virtual environment. This is a nice technique if you want to manage multiple python environments on a single pi:

```bash
/usr/local/bin/pipenv run python3 serialreader.py
```

## Summary

Okay, now we have a complete data recording and storage system set up. The only problem is all that data is stuck on the pi! The next post will remedy this by adding an API layer and exposing it on the public internet.