

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


# Try to use BOARD instead of BCM.
# This is because BCM can break between revisions of the Rasp Pi
GPIO.setmode(GPIO.BOARD)

def buttonPress(channel):
	startb = timeit.timeit()
	try:
		pwmControl.stop()
#		GPIO.output(ENABLE, GPIO.LOW)
		print 'Feedback disabled.'
	#Endtry

	finally:
		GPIO.cleanup()
		endb = timeit.timeit()
		totalTime = abs(1000*(endb - startb))
		print 'Response time after button press is: ', totalTime, 'ms.'
#		exit(0)
	#Endfinally

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

PERCENT ERROR BETWEEN COMMANDED SPEED AND OUTPUT SPEED IS ABOUT 6 - 7 %

ENABLE HIGH AND PWM OFF RESULTS IN A SHAFT THAT IMPEDES MOTION.

'''

inputB = 7
ENABLE = 40 
HLFB = 12
button = 16


# PWM output to control speed of the motor.
GPIO.setup(inputB, GPIO.OUT)

# ENABLE pin. high to have feedback and low for no feedback?
GPIO.setup(ENABLE, GPIO.OUT)

# High Level FeedBack from the motor.
GPIO.setup(HLFB, GPIO.IN) 

# GPIO 23 set up as an input for a pull up detection. Pin 23 will go to GND
# when pressed and enables us to achieve edge detection.
GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# 50% duty cyle(dc) +- 1 will be 0 velocity.
# 0 - 48% dc results in a clockwise(cw) rotation.
# 52 - 100% dc results in a counter-clockwise(ccw) rotation.
pwmControl = GPIO.PWM(inputB, 50)	# Create a PWM object at pin inputB set at 50 Hz.
pwmControl.start(50)	# Start the PWM at 50% duty cycle

print 'Press CTRL-C to stop the program at any time.'

# The GPIO.add_event_detect() line sets things up so that when a rising edge
# is detected on port 23, regardless of what is happening elsewhere in the
# program, the funciton 'buttonPress' will be run. This will even happen
# while the program waits for something else in the program.
GPIO.add_event_detect(button, GPIO.RISING, callback=buttonPress)

GPIO.output(ENABLE, GPIO.HIGH)
print 'Feedback enabled.'

pauseTime = 0.1
j = 2
try:
	while True:
		if j == 1:

			i = 0
			print 'Clockwise'
			while i <= 100:
				pwmControl.ChangeDutyCycle(95)
				sleep(pauseTime)
				i += 1
			#Endwhile

			i = 0
			print 'Counter Clockwise'
			while i <= 100:
				pwmControl.ChangeDutyCycle(5)
				sleep(pauseTime)
				i += 1
			#Endwhile

		elif j == 2:
			while True:
				pwmControl.ChangeDutyCycle(95)
				sleep(pauseTime)
			#Endwhile

		else:
			print 'Clockwise'
			for i in range(52, 101):
				pwmControl.ChangeDutyCycle(i)
				sleep(pauseTime)
			#Endfor
			
			print 'Counter Clockwise'
			for i in range(49):
				pwmControl.ChangeDutyCycle(i)
				sleep(pauseTime)
			#Endfor
		#Endif
	#Endwhile
	pwmControlChangeDutyCycle(50)

except KeyboardInterrupt:
	startK = timeit.timeit()
	pwmControl.stop()
	GPIO.output(ENABLE, GPIO.LOW)

finally:
	pwmControl.stop()
	print 'Feedback disabled.'
	GPIO.cleanup()
#Endtry
endK = timeit.timeit()
totalTime = abs(1000*(endK - startK))
print 'Time elapsed after keyboard interrupt is: ', totalTime, 'ms.'



