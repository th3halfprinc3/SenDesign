#!/usr/bin/python

import spidev
import time
import RPi.GPIO as GPIO

spi = spidev.SpiDev()
spi.open(0, 0)


# change these as desired - they're the pins connected from the
# SPI port on the ADC to the Cobbler

def readadc(adcnum):
	if adcnum > 7 or adcnum < 0:
		return -1
	r = spi.xfer2([1, 8 + adcnum << 4, 0])
	adcout = ((r[1] & 3) << 8) + r[2]
	return adcout

while True:
	value = readadc(0)
	volts = (value * 3.3) / 1024
	print ("%4d/2024 => %5.3f V" % (value, volts))
	time.sleep(0.5)
