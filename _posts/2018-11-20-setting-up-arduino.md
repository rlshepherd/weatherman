---
layout: post
title:  "Getting Started with Arduino"
date:   2018-11-20 00:47:35 -0800
categories: arduino weatherman update hardware
---

The first step in setting up our weather station was getting some hardware. Having never touched
an arduino or raspberry-pi before, this was the most exciting part.

## Planning

[Fritzing](http://www.fritzing.org) is an open source tool for documenting
electronics prototypes especially popular in the arduino community. I found
a [similar project](http://fritzing.org/projects/digital-thermometer-with-dht11/)
to use as a starting point. You can see a copy of the diagram here:

![Diagram](/weatherman/assets/diagram.png)

## Equipment

A bit of research led to a simple list of basic equipment to get started: 

1. Arduino
2. DHT11 Temperature and Humidity Sensor
3. Some electrical components and tools (e.g. cables, breadboard)

I also had to have these items shipped to Manila, where I was working at the time.
Luckily I found this really nice site [Makerlab Electronics](www.makerlab-electronics.com)
which carried everything I needed to get started.

Later on, back in Taipei, there were plently of parts and expertise available at [Guanghua Digital Plaza](https://en.wikipedia.org/wiki/Guang_Hua_Digital_Plaza).

## Assembly and Drive Code

Following great tutorials from [Circuit Basics](http://www.circuitbasics.com/how-to-set-up-the-dht11-humidity-sensor-on-an-arduino/) and on [Simple Circuits](https://simple-circuit.com/arduino-dht11-sensor-lcd-proteus/), I was able to get up an running in no time.

![Complete Circuit](/weatherman/assets/arduinocircuit.png)

Here is the final code which writes the sensor output to both the LCD display
and the arduino's serial port (which we will need in the next step).:

```c

#include <dht.h>
#include <LiquidCrystal.h>

LiquidCrystal lcd(12, 11, 5, 4, 3, 2);

dht DHT;

#define DHT11_PIN 7

void setup(){
  lcd.begin(16, 2);
  Serial.begin(9600);

}

void loop()
{
  int chk = DHT.read11(DHT11_PIN);
  Serial.print("Temperature = ");
  Serial.println(DHT.temperature);
  Serial.print("Humidity = ");
  Serial.println(DHT.humidity);
  lcd.setCursor(0,0); 
  lcd.print("Temp: ");
  lcd.print(DHT.temperature);
  lcd.print((char)223);
  lcd.print("C");
  lcd.setCursor(0,1);
  lcd.print("Humidity: ");
  lcd.print(DHT.humidity);
  lcd.print("%");
  delay(2000);
}

```

In the following posts we'll add a raspberry-pi to host a database and webserver.
