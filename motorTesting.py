

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


def buttonPress():
	startb = timeit.timeit()
	try:
		pwmOut.stop()
	#Endtry

	finally:
		GPIO.output(ENABLE, GPIO.LOW)
		GPIO.cleanup()
	#Endfinally

	endb = timeit.timeit()
	print 'Time elapsed after button press is: ', endb - startb
#EndbuttonPress




'''
HLFB
	- GREEN		GPIO Pin 12
	- RED			GND
INPUT B
	- BLK			GPIO Pin 7
	- YELLOW		GND
ENABLE
	- BLUE		GPIO Pin 40
	- ORANGE		GND
'''

inputB = 7
ENABLE = 40 
HLFB = 12
button = 23

# Try to use BOARD instead of BCM.
# This is because BCM can break between revisions of the Rasp Pi
GPIO.setmode(GPIO.BOARD)

# PWM output to control speed of the motor.
GPIO.setup(inputB, GPIO.OUT)

# ENABLE pin. high to have feedback and low for no feedback?
GPIO.setup(ENABLE, GPIO.OUT)

# High Level FeedBack from the motor.
GPIO.setup(HLFB, GPIO.IN) 

# GPIO 23 set up as an input for a pull up detection. Pin 23 will go to GND
# when pressed and enables us to achieve edge detection.
GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# 50% duty cyle(dc) +- 1 will be 0 velocity.
# 0 - 48% dc results in a clockwise(cw) rotation.
# 52 - 100% dc results in a counter-clockwise(ccw) rotation.
p = GPIO.PWM(inputB, 50)	# Create a PWM object at pin inputB set at 50 Hz.
p.start(50)	# Start the PWM at 50% duty cycle

print 'Press CTRL-C to stop the program at any time.'

# The GPIO.add_event_detect() line sets things up so that when a rising edge
# is detected on port 23, regardless of what is happening elsewhere in the
# program, the funciton 'buttonPress' will be run. This will even happen
# while the program waits for something else in the program.
GPIO.add_event_detect(button, GPIO.RISING, callback=buttonPress)

pauseTime = 1#0.02
try:
	while True:

		# Clockwise
		for i in range(52, 101):
			p.ChangeDutyCycle(i)
			sleep(pauseTime)
		#Endfor

		# Counter clockwise
		for i in range(49):
			p.ChangeDutyCycle(48-i)
			sleep(pauseTime)
		#Endfor
	#Endwhile
	p.ChangeDutyCycle(50)

except KeyboardInterrupt:
	startK = timeit.timeit()
	p.stop()
	
finally:
	p.stop()
	GPIO.output(ENABLE, GPIO.LOW)
	GPIO.cleanup()
	print 'GPIO Pins Cleaned.'
#Endtry
endK = timeit.timeit()

print 'Time elapsed after button press is: ', endK - startK




