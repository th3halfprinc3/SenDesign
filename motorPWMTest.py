#!/usr/bin/python

'''
The motor feedback cable has 4 outputs:

HLFB - High Level Feedback
	- GREEN = HLFB+
	- RED = HLFB-

Input A - First input
	- WHITE = Input A+
	- BROWN = Input A-

Input B - Second input
	- BLACK = Input B+
	- YELLOW = Input B-

Enable - The enable line of the motor, tells it whether to make an action or
not.
	- BLUE = Enable+
	- ORANGE = Enable-

	IMPORTANT:
	!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
	If we want this to work with the minimum Logic Level, 5V, then we must
	supply the enable line with 5V. For constant use, supply enable with 5V,
	to stop the motor make the enable signal 0V.
	!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
'''


# Using PWM with RPi.GPIO library requires the version RPi.GPIO 0.5.2a or later

import RPi.GPIO as GPIO	# always needed to interface with the GPIO pins, and makes it easier
from time import sleep


##############################################
# Function to decrease the speed of the motor and to limit it to a "real"
# speed.
def decSpeed(curSpeed):
	newSpeed = curSpeed - 1
	if ( newSpeed < 0 ):
		newSpeed = 0
	#Endif
	motor.ChangeDutyCycle(newSpeed)
	return newSpeed
##############################################


##############################################
# Function to increase the speed of the motor and to limit how fast it can
# go
def incSpeed(curSpeed):
	newSpeed = curSpeed + 1
	if ( newSpeed > 90 ):
		newSpeed = 90
	#Endif
	motor.ChangeDutyCycle(newSpeed)
	return newSpeed
##############################################


##############################################
# Function to stop the motor and change it's direction.
def flipDir():
	motor.ChangeDutyCyle(0)
	GPIO.output(mot1, (not GPIO.input(mot1)) )
	GPIO.output(mot2, (not GPIO.input(mot2)) )
	print 'Changing direction!'
	sleep(1)
	return 0
##############################################


# MAIN FUNCTION

GPIO.setmode(GPIO.BOARD)	# Either BCM or BOARD can be used. I use BOARD, because BCM can break over Rasp Pi board revisions

#mot1 = 16
pwmPin = 7
#mot2 = 22

# Setup some output pins on the GPIO board
G#PIO.setup(mot1, GPIO.OUT)
G#PIO.setup(mot2, GPIO.OUT)
GPIO.setup(pwmPin, GPIO.OUT)

motor = GPIO.PWM(pwmPin, 50)	# Create object motor for PWM on port 22 at 50hz

motor.start(0)	# start the motor with a 0 percent duty cycle (off)

print 'Press CTRL+C at anytime to exit.'

# now the fun starts, we'll vary the duty cycle to increase and decrease the
# speed of the motor.

pause_time = 0.02	# you can change this to slow down/speed up
# use is to make the program sleep for x amount of sleep.

try:
	while True:
		for i in range(0,101):	# 101 becuase it stops when it finishes 100
			motor.ChangeDutyCycle(i)
			sleep(pause_time)
		#Endfor

		for i in range(100,-1,-1):	# from 100 to zero in steps of -1
			motor.ChangeDutyCycle(i)
			sleep(pause_time)
		#Endfor
	#Endwhile
	motor.ChangeDutyCycle(0)

except KeyboardInterrupt:
	motor.stop()	# Stop the motor PWM output

finally:
	motor.stop()	# Stop the motor PWM output
	GPIO.cleanup()	# clean up GPIO on CTRL+C exit
	print 'GPIO Pins Cleaned'
#Endtry


