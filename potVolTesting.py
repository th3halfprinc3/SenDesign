#!/usr/bin/python

import spidev
import time
import RPi.GPIO as GPIO
import numpy

spi = spidev.SpiDev()
spi.open(0, 0)

GPIO.setmode(GPIO.BOARD)


inputB1 = 26	# 37	BLACK
ENABLE1 = 21	# 40	BLUE
HLFB1 = 18		# 12	GREEN

GPIO.setup(inputB1, GPIO.OUT)

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
l = 120
A = numpy.zeros(shape=(1, l))
# j represents the angle of the pot
# i represents the angle of the knee
# vol is the voltage associated with the knee


for i in range(l):
	A[0, i] = vol
	vol += dV
#End for

#vol = 0
#dV = 0.000917

'''
for i in range(3600):
	with open( "potVoltAngle.txt", "a" ) as myfile:
		myfile.write( str(i-1800) + "," + str(vol) + "\n" )

	vol += dV
#End if
'''

try:
	while True:
		value = readadc(0)
		volts = (value * 3.3) / 1024
		pos = (numpy.abs(A - volts)).argmin()
	
		print ("%4d/1024 => %5.3f V => %5.3f degrees" % (value, volts, pos))
		time.sleep(0.5)

	#End while

except KeyboardInterrupt:
	GPIO.cleanup()
#End try
