#!/usr/bin/python

import gaugette.rotary_encoder
import gaugette.switch
from time import sleep

A_PIN = 7
B_PIN = 9
SW_PIN = 8

# This should be using threads for the encoder!!!
encoder = gaugette.rotary_encoder.RotaryEncoder.Worker(A_PIN, B_PIN)
encoder.delay = 0.2
print 'starting'
encoder.start()	# This will not block the main thread
sleep(1)
print 'stopping'
encoder.stop()
encoder.join()
pring 'stopped'
sleep(1)

# This is not using threads! Find out which one is faster.
encoder = gaugette.rotary_encoder.RotaryEncoder(A_PIN, B_PIN)



switch = gaugette.switch.Switch(SW_PIN)
last_state = None

while True:
	delta = encoder.get_delta()
	if delta != 0
		print "rotate %d" %delta
	
	sw_state = switch.get_state()
	if sw_state != last_state()
		print "switch %d" %sw_state
		last_state = sw_state

# Catch any ports that weren't cleaned!
GPIO.cleanup()


