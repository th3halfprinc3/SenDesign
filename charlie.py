#!/usr/bin/python

import spidev
import time
import RPi.GPIO as GPIO
from numpy import matrix
from numpy import zeros

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

'''
NOTE THAT ALL POSITIVE DEGREES REPRESENTS A COUNTER CLOCKWISE MOTION

Extension yields a decreasing voltage
flexion yields an increasing voltage

AT THE POT SHAFT
X ( deg )		Y ( Volts )
3600		-->	3.3	full counter clockwise
0			-->	1.65
-3600		-->	0.0	full clockwise
360			-->	0.33
90			-->	0.0825
1			-->	0.000917

AT THE KNEE, a displacement of x degrees yields y volts
X ( deg )		Y ( Volts )
90			-->	0.33
50			-->	0.183
40			-->	0.147
1			-->	0.0037


0.0037V change is a 1 degree change at the knee.
A change in 0.33V is a displacement of 90 degrees at the knee.
This is okay because the resolution of the ADC is 0.0032V.

VOLTAGE ASSOCIATED WITH THE POSITION OF THE KNEE
X ( deg )		Y ( Volts )
0			-->	1.32
90			-->	1.65
130		-->	1.797
140		-->	1.833
'''


dV = 0.0037
vol = 1.32
l = 141
A = zeros(shape = (1, l))
for i in range(0, l):
	A[0, i] = vol
	vol += dV
#End for

try:
	while True:
		value = readadc(0)
		volts = (value * 3.3) / 1024
	

	
		print ("%4d/1024 => %5.3f V" % (value, volts))
		time.sleep(0.5)

	#End while

except KeyboardInterrupt:
	print 'The A matrix is: ', A

#End try
