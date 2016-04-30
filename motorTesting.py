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
import timeit

inputB = 7
ENABLE =  
HLFB = 

# Try to use BOARD instead of BCM.
# This is because BCM can break between revisions of the Rasp Pi
GPIO.setmode(GPIO.BOARD)


# PWM output to control speed of the motor.
GPIO.setup(inputB, GPIO.OUT)
# ENABLE pin. high to have feedback and low for no feedback?
GPIO.setup(ENABLE, GPIO.OUT)
# High Level FeedBack from the motor.
GPIO.setup(HLFB, GPIO.IN) 

p = GPIO.PWM(inputB, 50)	# Create a PWM object at pin inputB set at 20 Hz.
p.start(50)	# Start the PWM at 50% duty cycle, which should not be moving.

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
	p.ChangeDutyCycle(50)

except KeyboardInterrupt:
	start = timeit.timeit()
	p.stop()
	string = 'Keyboard Interrupt'
	
finally:
	p.stop()
	GPIO.output(ENABLE, GPIO.LOW)
	GPIO.cleanup()
	print 'GPIO Pins Cleaned.'
#Endtry
end = timeit.timeit()

print 'Time elapsed after ', string, ' is: ', end - start




