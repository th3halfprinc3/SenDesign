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
import warnings


# Takes care of RuntimeWarning's
#warnings.simplefilter('error',RuntimeWarning)

# Catch any uncleaned GPIO pins
GPIO.cleanup()

# Try to use BOARD instead of BCM.
# This is because BCM can break between revisions of the Rasp Pi
GPIO.setmode(GPIO.BOARD)
GPIO.setup(12,GPIO.OUT)

p = GPIO.PWM(12,0.5)
p.start(1)
input('Press return to stop:')	# use raw_input for Python 2
p.stop()
GPIO.cleanup()


