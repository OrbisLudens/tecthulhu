#!/usr/bin/env python
#
# Title:      Control Orbis Ludens Motor with Raspberry Pi GPIO
# Author:     Martin Brenner
#
# One of two Motor Relays is switched on in one of two direction using the pins PINOPEN and PINCLOSE (active LOW)
# Motor Relay status is signalled with pins PINOPENING and PINCLOSING
# Relays will turn themselves OFF if an end switch is reached (and also turn the Motor off).
# Relays are a bit delayed after turning them ON, so immediate status will be LOW if they were just turned on.
import time
import RPi.GPIO as GPIO

class tmotor:

    def __init__(self, pinopen, pinclose, pinopening, pinclosing):
        # setup GPIO pins
        self.PINOPEN = pinopen
        self.PINCLOSE = pinclose
        self.PINOPENING = pinopening
        self.PINCLOSING = pinclosing
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(True)
        print "init motor control"
        GPIO.setup(self.PINOPEN,GPIO.OUT)
        GPIO.output(self.PINOPEN,GPIO.HIGH)
        GPIO.setup(self.PINCLOSE,GPIO.OUT)
        GPIO.output(self.PINCLOSE,GPIO.HIGH)
        GPIO.setup(self.PINOPENING,GPIO.IN)
        GPIO.setup(self.PINCLOSING,GPIO.IN)
        # initialize control variables
        self.opening = False
        self.closing = False
        self.openstarttime = -1
	self.closestarttime = -1
        self.MAXOPENTIME = 3
        self.MAXCLOSETIME = 3

    def stopsphere(self):
        # turn motor off immediately
        print "stopping"
        self.openstarttime = -1
        self.opening = False
        self.closestarttime = -1
        self.closing = False
        GPIO.output(self.PINOPEN, GPIO.HIGH)
        GPIO.output(self.PINCLOSE, GPIO.HIGH)

    def opensphere(self):
        print "start opening"
        self.openstarttime = time.time()
        self.opening = True
        GPIO.output(self.PINCLOSE, GPIO.HIGH)
        GPIO.output(self.PINOPEN, GPIO.LOW)

    def closesphere(self):
        print "start closing"
        self.closestarttime = time.time()
        self.closing = True
        GPIO.output(self.PINOPEN, GPIO.HIGH)
        GPIO.output(self.PINCLOSE, GPIO.LOW)

    def checkstatus(self):
        print "IN",GPIO.input(self.PINOPENING),GPIO.input(self.PINCLOSING)
        if self.opening:
           print "opening time since start=", time.time() - self.openstarttime
           if time.time() - self.openstarttime > self.MAXOPENTIME:
              self.stopsphere()
        if self.closing:
           print "closing time since start=", time.time() - self.closestarttime
           if time.time() - self.closestarttime > self.MAXCLOSETIME:
              self.stopsphere()
        

    def main(self):
        #test the motor control
        self.stopsphere()
	time.sleep(1.0)
	self.closesphere()
        while True:
            self.checkstatus()
            time.sleep(1.0)

if __name__ =='__main__':
        motor = tmotor(23, 24, 25, 26)
        motor.main()

