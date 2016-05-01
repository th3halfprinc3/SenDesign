#!/usr/bin/python

'''
WHEN TYPING ON RASPBERRY PI B+ BE AWARE OF INCORRECT KEY MAPPINGS
'''

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)

button = 16
# GPIO 23 set up as input. It is pulled up to stop false signals.
GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_UP)

print '''Make sure you have a button connected so that when pressed
it will connect GPIO port 23 (pin 16) to GND (pin 6)'''

raw_input("Press Enter when ready!")

print "Waiting for falling edge on port 23."

# Now the program will do nothing until the signal on port 23
# starats to fall towards zero. This is why we used the pullup
# to keep the signal high and prevent a false interrupt.

print '''During this waiting time, your computer is not
wasting resources by polling for a button press.
Press your button when ready to initiate a flling edge interrupt.'''

try:
	GPIO.wait_for_edge(button, GPIO.FALLING)
	print '''
Falling edge detected. Now your program can continue with
whatever was waiting for a button press.'''
except KeyboardInterrupt:
	GPIO.cleanup()		# Clean up GPIO on CTRL+C exit
GPIO.cleanup() 		# Clean up GPIO on normal exit
