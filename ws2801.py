#!/usr/bin/env python
#
# Title:      WS2801 SPI control class for Raspberry Pi
# Author:     AndyPi (http://andypi.co.uk/)
# Based on:   Adafruit https://raw.githubusercontent.com/adafruit/Adafruit-Raspberry-Pi-Python-Code/master/Adafruit_LEDpixels/Adafruit_LEDpixels.py
#
# Hardware: WS2801 pixels, CLOCK=RPi23; Data=RPi19, GND=RpiGND, +5v=Rpi+5v

import RPi.GPIO as GPIO, time, os, sys

class ws2801:

 # import RPi.GPIO as GPIO, time, os
 NUMBER_OF_PIXELS=16 # set number of pixels in your strip
 DEBUG = 1
 GPIO.setmode(GPIO.BCM)

 ledpixels = [0] * NUMBER_OF_PIXELS

 def writestrip(self, pixels):
	spidev = file("/dev/spidev0.0", "w")
	for i in range(len(pixels)):
		spidev.write(chr((pixels[i]>>16) & 0xFF))
		spidev.write(chr((pixels[i]>>8) & 0xFF))
		spidev.write(chr(pixels[i] & 0xFF))
	spidev.close()
	time.sleep(0.002)

 def Color(self, r, g, b):
	return ((r & 0xFF) << 16) | ((g & 0xFF) << 8) | (b & 0xFF)

 def setpixelcolor(self, pixels, n, r, g, b):
	if (n >= len(pixels)):
		return
	pixels[n] = self.Color(r,g,b)

 def setpixelcolor(self, pixels, n, c):
	if (n >= len(pixels)):
		return
	pixels[n] = c

 def colorwipe(self, pixels, c, delay):
	for i in range(len(pixels)):
		self.setpixelcolor(pixels, i, c)
		self.writestrip(pixels)
		time.sleep(delay)		

 def Wheel(self, WheelPos):
	if (WheelPos < 85):
   		return self.Color(WheelPos * 3, 255 - WheelPos * 3, 0)
	elif (WheelPos < 170):
   		WheelPos -= 85;
   		return self.Color(255 - WheelPos * 3, 0, WheelPos * 3)
	else:
		WheelPos -= 170;
		return self.Color(0, WheelPos * 3, 255 - WheelPos * 3)

 def rainbowCycle(self, pixels, wait):
	for j in range(256): # one cycle of all 256 colors in the wheel
    	   for i in range(len(pixels)):
 # tricky math! we use each pixel as a fraction of the full 96-color wheel
 # (thats the i / strip.numPixels() part)
 # Then add in j which makes the colors go around per pixel
 # the % 96 is to make the wheel cycle around
      		self.setpixelcolor(pixels, i, self.Wheel( ((i * 256 / len(pixels)) + j) % 256) )
	   self.writestrip(pixels)
	   time.sleep(wait)
 
 def cls(self, pixels):
          for i in range(len(pixels)):
                self.setpixelcolor(pixels, i, self.Color(0,0,0))
                self.writestrip(pixels)


 def main(self):
   try:  
    self.colorwipe(self.ledpixels, self.Color(255, 0, 0), 0.05)
    self.colorwipe(self.ledpixels, self.Color(0, 255, 0), 0.05)
    self.colorwipe(self.ledpixels, self.Color(0, 0, 255), 0.05)
    self.rainbowCycle(self.ledpixels, 0.00)
    self.cls(self.ledpixels)
   
   except KeyboardInterrupt:
        self.cls(self.ledpixels)
        sys.exit(0)



if  __name__ =='__main__':
        LEDs=ws2801()
        LEDs.main()
