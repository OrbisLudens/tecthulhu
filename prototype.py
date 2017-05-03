#!/usr/bin/env python
# a prototype portal simulator

import time, sys
from ws2801 import ws2801 
from tlc5947 import tlc5947
#LEDs=ws2801() # Set the name of our module 
LEDs=tlc5947(23) # Set the name of our module 
NUMBER_OF_PIXELS=8 # Set the number of pixels
ledpixels = [0] * NUMBER_OF_PIXELS # set up the pixel array

print "XLAT=",LEDs.LAT

L0COLOR = [0,0,0]
L1COLOR = [255,255,0]
L2COLOR = [255,100,0]
L3COLOR = [255,30,0]
L4COLOR = [255,0,0]
L5COLOR = [255,0,30]
L6COLOR = [255,0,100]
L7COLOR = [255,0,255]
L8COLOR = [100,0,255]
RCOLORS = [L0COLOR,L1COLOR,L2COLOR,L3COLOR,L4COLOR,L5COLOR,L6COLOR,L7COLOR,L8COLOR]

def setresonator(index, level, energy) :
	print "resonator", index, level, energy
	r = RCOLORS[level][0] * energy / 8000
	g = RCOLORS[level][1] * energy / 8000
	b = RCOLORS[level][2] * energy / 8000
	LEDs.setpixelcolor(ledpixels, index, LEDs.Color(r, g, b))
	
FNCOLOR = [100,100,100]
FECOLOR = [0,255,0]
FRCOLOR = [0,0,255]
FCOLORS = [FNCOLOR,FECOLOR,FRCOLOR]

def setfaction(faction, energy) :
	r = FCOLORS[faction][0] * energy / 100
	g = FCOLORS[faction][1] * energy / 100
	b = FCOLORS[faction][2] * energy / 100
	LEDs.setpixelcolor(ledpixels, 8, LEDs.Color(r, g, b))
	LEDs.setpixelcolor(ledpixels, 9, LEDs.Color(r, g, b))
	LEDs.setpixelcolor(ledpixels, 10, LEDs.Color(r, g, b))
	LEDs.setpixelcolor(ledpixels, 11, LEDs.Color(r, g, b))


try: 
	LEDs.cls(ledpixels)
	time.sleep(0.5)

	#setfaction(0,100)
	#LEDs.writestrip(ledpixels)
	#time.sleep(1)

	#setfaction(1,100)

	for i in range(0, 8):
		setresonator(0, i+1, 8000)
		LEDs.writestrip(ledpixels)
      		time.sleep(0.5)


	LEDs.cls(ledpixels)
	time.sleep(0.5)

except KeyboardInterrupt:
	LEDs.cls(ledpixels) 
	sys.exit(0)
