#!/usr/bin/python

# Create a PWM instance
#p = GPIO.PWM(channel,frequency)
# Start the PWM
#p.start(dc)	# where dc is the duty cycle (0.0 <= dc <= 100.0)

# To change the frequency
#p.ChangeDutyCycle(dc)	# Where (0.0 <= dc <= 100.0)

# To stop the PWM
#p.stop()

# Note that PWM will also stop if the instance variable 'p' goes out of
# scope.

import RPi.GPIO as GPIO
from time import sleep

pwmPin = 7

# Try to use BOARD instead of BCM.
# This is because BCM can break between revisions of the Rasp Pi
GPIO.setmode(GPIO.BOARD)
GPIO.setup(pwmPin, GPIO.OUT)

p = GPIO.PWM(pwmPin, 20)	# Create a PWM object at pin pwmPin set at 20 Hz.
p.start(0)	# Start the PWM at 0% duty cycle.

print 'Press CTRL-C to stop the program at any time.'

pauseTime = 1#0.02

try:
	while True:
		for i in range(100):
			p.ChangeDutyCycle(i)
			sleep(pauseTime)
		#Endfor

		for i in range(100):
			p.ChangeDutyCycle(100-i)
			sleep(pauseTime)
		#Endfor
	#Endwhile
	p.ChangeDutyCycle(0)

except KeyboardInterrupt:
	p.stop()

finally:
	p.stop()
	GPIO.cleanup()
	print 'GPIO Pins Cleaned.'
#Endtry





