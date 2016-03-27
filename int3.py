#!/usr/bin/python

'''
WHEN TYPING ON RASPBERRY PI BE AWARE OF INCORRECT KEY MAPPINGS
'''


'''
WHY WERE THE PINS 17, 23 AND 34 SPECIFICALLY CHOSEN?
These pins were chosen because they have ground pins beside them.
Therefore if they are configured to have internal pull-up resistors,
they can be connected to switches wired to simple 2-pin female connectors,
i.e. a switch or button between pins 9 & 11, 14 & 16, and 18 & 20.
'''


import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

# GPIO 23 & 17 set up as inputs. Pulled up to avoid false detection.
# Both ports are wired to connect to GND on button press.
# So we'll be setting up falling edge detection for both.
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# GPIO 24 set up as an input, pulled down, connected to 3V3 on button
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Now we'll define two threaded callback functions
# These will run in another thread when our events are detected.
def my_callback(channel):
	print "Falling edge detected on 17"

def my_callback2(channel):
	print "Falling edge detected on 23"

print '''Make sure you have a button connected so that when pressed
it will connect GPIO port 23 (pin 16) to GND (pin 6).
You will also need a second button connected so that when pressed 
it will connect GPIO port 24 (pin 18) to 3V3 (pin 1).
You will also need a third button connected so that when pressed 
it will connect GPIO port 17 (pin ) to 3V3 (pin 14).'''

raw_input("Press Enter when ready!")


# When a falling edge is detected on port 17, regardless of whatever
# else is happening in the program, the function my_callback will be run.
GPIO.add_event_detect(17, GPIO.FALLING, callback = my_callback, bouncetime = 300)

# When a falling edge is detected on port 23, regardless of whatever
# else is happening in the program, the function my_callback2 will be run.
# 'bouncetime = 300'is to debounce the switch, (the switch is so small and
# moves so fast that it actually bounces when it hits the contact pin. =o) 
GPIO.add_event_detect(23, GPIO.FALLING, callback = my_callback2, bouncetime = 300)

try:
	print 'Waiting for rising edge on port 24'
	GPIO.wait_for_edge(24, GPIO.RISING)
	print 'Rising edge detected on port 24. Here endeth the third lesson.'
except KeyboardInterrupt:
	GPIO.cleanup()		# Clean up GPIO on CTRL+C exit

GPIO.cleanup() 		# Clean up GPIO on normal exit
