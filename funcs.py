#!/usr/bin/env python
# Written by Limor "Ladyada" Fried for Adafruit Industries, (c) 2015
# This code is released into the public domain

import time
from timeit import timeit
import os
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
DEBUG = 1

def readPWM(pinNum):
	startpwm = timeit.timeit()
	
	highCount = 0
	totCount = 0
	cur = GPIO.input(pinNum)
	while True:
		prev = cur
		cur = GPIO.input(pinNum)
		if ( cur == 1 ):	# The gpio pin is high, increment high count
			highCount += 1
		
		elif ( prev == 1 and cur == 0 ):		# Period has ended, now determine DC.
			dutyCycle = highCount/totCount
		
		else:
			totCount += 1

		#End if
	#End while
	

	endpwm = timeit.timeit()
	totalTime = abs(1000*(endpwm - startpwm))	# Convert sec to ms
	print 'PWM took %.3f microseconds.' %(totalTime)

	return dutyCycle
#End readPWM	


# read SPI data from MCP3008 chip, 8 possible adc's (0 thru 7)
def readADC(adcnum, clockpin, mosipin, misopin, cspin):
	if ((adcnum > 7) or (adcnum < 0)):
		return -1
	#End if

	GPIO.output(cspin, True)

	GPIO.output(clockpin, False)	# start clock low
	GPIO.output(cspin, False)		# bring CS low

	commandout = adcnum
	commandout |= 0x18  # start bit + single-ended bit
	commandout <<= 3    # we only need to send 5 bits here
	for i in range(5):
		if (commandout & 0x80):
			GPIO.output(mosipin, True)
		else:
			GPIO.output(mosipin, False)
		#End if

		commandout <<= 1
		GPIO.output(clockpin, True)
		GPIO.output(clockpin, False)

		adcout = 0
		# read in one empty bit, one null bit and 10 ADC bits
		for i in range(12):
			GPIO.output(clockpin, True)
			GPIO.output(clockpin, False)
			adcout <<= 1
			if (GPIO.input(misopin)):
				adcout |= 0x1
			#End if
		#End for
	#End for

	GPIO.output(cspin, True)

	adcout >>= 1       # first bit is 'null' so drop it

	print 'adcout = ', adcout

	return adcout
#End readADC

# change these as desired - they're the pins connected from the
# SPI port on the ADC to the Cobbler

# These particular pins are from the actual pi and from my pi GPIO image.
SPICLK = 23
SPIMISO = 21
SPIMOSI = 19
SPICS = 24


# set up the SPI interface pins
GPIO.setup(SPIMOSI, GPIO.OUT)
GPIO.setup(SPIMISO, GPIO.IN)
GPIO.setup(SPICLK, GPIO.OUT)
GPIO.setup(SPICS, GPIO.OUT)

# I have a 5k linear pot, could this be an issue?????
# 10k trim pot connected to adc #0
potentiometer_adc = 0;

last_read = 0		# this keeps track of the last potentiometer value
tolerance = 1		# to keep from being jittery we'll only change
						# volume when the pot has moved more than 5 'counts'
try:
	while True:
		# we'll assume that the pot didn't move
		trim_pot_changed = False

		# read the analog pin
		trim_pot = readADC(potentiometer_adc, SPICLK, SPIMOSI, SPIMISO, SPICS)
		# how much has it changed since the last read?
		pot_adjust = abs(trim_pot - last_read)

		if DEBUG:
			print "trim_pot:", trim_pot
			print "pot_adjust:", pot_adjust
			print "last_read", last_read
		#End if

		if ( pot_adjust > tolerance ):
			trim_pot_changed = True
		#End if

		if DEBUG:
			print "trim_pot_changed", trim_pot_changed
		#End if

		if ( trim_pot_changed ):
			set_volume = trim_pot / 10.24		# convert 10bit adc0 (0-1024) trim
														# pot read into 0-100 volume level
			set_volume = round(set_volume)	# round out decimal value
			set_volume = int(set_volume)		# cast volume as integer
	
			print 'Volume = {volume}%' .format(volume = set_volume)
			set_vol_cmd = 'sudo amixer cset numid=1 -- {volume}% > /dev/null' .format(volume = set_volume)
			os.system(set_vol_cmd)  # set volume
	
			if DEBUG:
				print "set_volume", set_volume
				print "tri_pot_changed", set_volume
			#End if
	
			# save the potentiometer reading for the next loop
			last_read = trim_pot
		#End if
	
		# hang out and do nothing for a half second
		time.sleep(0.5)
	#End while

except KeyboardInterrupt:
	GPIO.cleanup()
	print "pins cleaned"
