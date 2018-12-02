/*
read.c

Read from a DHT11 temp & humidity sensor.
Display data on a LCD display.
And print data to serial port.

based on these tutorial:
http://www.circuitbasics.com/how-to-set-up-the-dht11-humidity-sensor-on-an-arduino/
https://electronicsprojectshub.com/setup-dht11-sensor-with-arduino/

Requires DHTLib:
http://www.circuitbasics.com/wp-content/uploads/2015/10/DHTLib.zip

*/

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

