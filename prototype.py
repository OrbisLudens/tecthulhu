#!/usr/bin/env python
# a prototype portal simulator

import time, sys
#from ws2801 import ws2801 
from tlc5947 import tlc5947

# LEDs=ws2801() # Set the name of our module 
LEDs=tlc5947(19) # Set the name of our module 
# For Orbis Ludens we have 16 available channels (2 tlc5947)
# channels 0-7: Resonators
# channel 8-11: Mods
# channel 12: Faction Status
# channel 13: Sphere Illumination?
# channel 14: Mission Day LEDs ('R'), Mission Banners ('G')
NUMBER_OF_PIXELS=16 # Set the number of pixels
ledpixels = [0] * NUMBER_OF_PIXELS # set up the pixel array

from mixer import tsound
audio = tsound()

from restclient import restclient
client = restclient()

#print "XLAT=",LEDs.LAT

ENERGYL = [0,1,2,4,8,16,32,64,128,256,256,512,1000,2000,4000,8000]

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
	#print "resonator", index, level, energy
	r = RCOLORS[level][0] * energy / 8000
	g = RCOLORS[level][1] * energy / 8000
	b = RCOLORS[level][2] * energy / 8000
	LEDs.setpixelcolor(ledpixels, index, LEDs.Color(r, g, b))
	
FNCOLOR = [100,100,100]
FECOLOR = [0,255,0]
FRCOLOR = [0,0,255]
FCOLORS = [FNCOLOR,FECOLOR,FRCOLOR]

def setfaction(faction, energy) :
	if faction == 0:
		energy = 100
	print "Factionenergy", energy
	r = FCOLORS[faction][0] * energy / 100
	g = FCOLORS[faction][1] * energy / 100
	b = FCOLORS[faction][2] * energy / 100
	LEDs.setpixelcolor(ledpixels, 8, LEDs.Color(r, g, b))
	LEDs.setpixelcolor(ledpixels, 9, LEDs.Color(r, g, b))
	LEDs.setpixelcolor(ledpixels, 10, LEDs.Color(r, g, b))
	LEDs.setpixelcolor(ledpixels, 11, LEDs.Color(r, g, b))
	LEDs.setpixelcolor(ledpixels, 12, LEDs.Color(r, g, b))
	LEDs.setpixelcolor(ledpixels, 13, LEDs.Color(r, g, b))
	LEDs.setpixelcolor(ledpixels, 14, LEDs.Color(r, g, b))
	LEDs.setpixelcolor(ledpixels, 15, LEDs.Color(r, g, b))


try: 
	LEDs.cls(ledpixels)
	time.sleep(0.5)

	#setfaction(0,100)
	#LEDs.writestrip(ledpixels)
	#time.sleep(1)

	#setfaction(1,100)

	#LEDs.setpixelcolor(ledpixels, 0, LEDs.Color(0,0,255))
	#LEDs.writestrip(ledpixels)
	#time.sleep(2)

	resdict = {'N':0,'NE':1,'E':2,'SE':3,'S':4,'SW':5,'W':6,'NW':7}

	oldfaction = 0
	oldhealth = 0
	oldreslevel = [0] * 8
	oldreshealth = [0] * 8
	oldinitialized = False

        while True:
		reslevel = [0] * 8
		reshealth = [0] * 8

		data = client.getjson()
		if data != 0:
			print data

			if 'result' in data:
                            mainkey = 'result'
				
			    factionname = data[mainkey]['controllingFaction']
			    if factionname == "Enlightened":
				faction = 1
			    elif factionname == "Resistance":
				faction = 2
			    else:
				faction = 0
			    health = int(data[mainkey]['health'])
			    setfaction(faction, health)

			    dres = data[mainkey]['resonators']
                            if dres is None:
                                print "no resonators"
                            else:
			        for r in range(0, len(dres)):
				    position = resdict[dres[r]['position']]
				    reslevel[position] = int(dres[r]['level'])
				    reshealth[position] = int(dres[r]['health'])

			        for r in range(0, 8):
				    setresonator(r, reslevel[r], reshealth[r]*10)
				    print r,reslevel[r],reshealth[r]
                            dmods = data[mainkey]['mods']
                            if dmods is None:
                                print "no mods"
                            else:
                                for m in range(0, len(dmods)):
                                    mtype = dmods[m]['type']
                                    mrare = dmods[m]['rarity']
                                    slot = dmods[m]['slot']
                                    print m,mtype,mrare,slot


		LEDs.writestrip(ledpixels)
		# if old values have been initialized, compare to old values
		if oldinitialized:
			if faction == oldfaction:
				isdeploy = False
				for r in range(0, 8):
					if reslevel[r] > oldreslevel[r]:
						isdeploy = True
				if isdeploy:
					audio.deploy()
					
		else:
			oldinitialized = True
			
		# copy current to old
		oldfaction = faction
		oldhealth = health
		for r in range(0, 8):
			oldreslevel[r] = reslevel[r]
			oldreshealth[r] = reshealth[r]

		time.sleep(1)


	LEDs.cls(ledpixels)
	time.sleep(0.5)

except KeyboardInterrupt:
	LEDs.cls(ledpixels) 
	sys.exit(0)
