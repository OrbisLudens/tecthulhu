#!/usr/bin/env python
#
# Title:      TLC5947 SPI control class for Raspberry Pi
# Author:     Martin Brenner
#
# Hardware: Adafruit TLC5947 24 12bit channel PWM controller CLOCK=SCLK; Data=MOSI, GND=RpiGND, LAT=GPIO23

import RPi.GPIO as GPIO, time, os, sys

class tlc5947:

 # import RPi.GPIO as GPIO, time, os
 NUMBER_OF_PIXELS=8 # set number of pixels in your strip
 DEBUG = 1
 LAT = 19 # The Latch control to transfer shift register into display register
 GPIO.setmode(GPIO.BCM)
 GPIO.setwarnings(False)

 ledpixels = [0] * NUMBER_OF_PIXELS

 print "LAT=",LAT

 def __init__(self, lat):
	self.LAT = lat
	GPIO.setup(self.LAT,GPIO.OUT)
	
 def writestrip(self, pixels):
	spidev = file("/dev/spidev0.0", "w")
	for i in range(len(pixels)-2, -2, -2):
		# Each 2 pixels share 1 byte for a total of 9 bytes
		spidev.write(chr((pixels[i+1] >> 16) & 0xFF))
		spidev.write(chr((((pixels[i+1] >> 8) & 0xFF) >> 4) & 0x0F))
		spidev.write(chr((((pixels[i+1] >> 8) & 0xFF) << 4) & 0xF0))
		spidev.write(chr(pixels[i+1] & 0xFF))
		spidev.write(chr((((pixels[i] >> 16) & 0xFF) >> 4) & 0x0F))
		spidev.write(chr((((pixels[i] >> 16) & 0xFF) << 4) & 0xF0))
		spidev.write(chr((pixels[i] >> 8 ) & 0xFF))
		spidev.write(chr(((pixels[i] & 0xFF) >> 4) & 0x0F))
		spidev.write(chr(((pixels[i] & 0xFF) << 4) & 0xF0))
	spidev.close()
	print "SLAT=",self.LAT
	GPIO.output(self.LAT,GPIO.HIGH)
	time.sleep(0.1)
	GPIO.output(self.LAT,GPIO.LOW)
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
        LEDs=tlc5947()
        LEDs.main()
