#!/usr/bin/python

# Using PWM with RPi.GPIO library requires the version RPi.GPIO 0.5.2a or later

import RPi.GPIO as GPIO	# always needed with RPi.GPIO, and makes it easier
from time import sleep

GPIO.setmode(GPIO.BOARD)	# Either BCM or BOARD can be used. I use BOARD, because BCM can break over Rasp Pi board revisions

GPIO.setup(25, GPIO.OUT)	# Set GPIO 25 as output for white LED
GPIO.setup(24, GPIO.OUT)	# Set GPIO 24 as output for red LED

white = GPIO.PWM(25,100)	# Create object white for PWM on port 25 at 100hz
red = GPIO.PWM(25,100)	# Create object red for PWM on port 24 at 100hz

white.start(0)	# start white LED on 0 percent duty cycle (off)
red.start(100)	# red fully on 100% duty cycle

# now the fun starts, we'll vary the duty cycle to dim/brighten the LEDs,
# so one is bright while the other is dim.

pause_time = 0.02	# you can change this to slow down/speed up

try:
	while True:
		for i in range(0,101):	# 101 becuase it stops when it finishes 100
			white.ChangeDutyCycle(i)
			red.ChangeDutyCycle(100-i)
			sleep(pause_time)
		
		for i in range(100,-1,-1)	# from 100 to zero in steps of -1
			white.ChangeDutyCycle(i)
			red.ChangeDutyCycle(100-i)
			sleep(pause_time)

except KeyboardInterrupt:
	white.stop()	# Stop the white PWM output
	red.stop()		# Stop the red PWM output
	GPIO.cleanup()	# clean up GPIO on CTRL+C exit

