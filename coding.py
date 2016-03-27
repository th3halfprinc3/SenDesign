#!/usr/bin/python

# Import libraries and such
import time
import sys
import RPi.GPIO as GPIO
import gaugette.rotary_encoder
import gaugette.switch

# Define any functions necesary
"""
SETUP
1. Clean up any ports from the GPIO. ( just in case ).
2. Ensure data acquisition from the motor and rotary encoder is possible.
3. Initialize pins for motor, rotary encoder and PWM.
"""
# Clean up any GPIO pins that weren't cleaned!
GPIO.cleanup()

A_PIN = 7
B_PIN = 9
SW_PIN = 8

# Rotary Encoder setup
encoder = gaugette.rotary_encoder.RotaryEncoder.Worker(A_PIN,B_PIN)
encoder.delay = 0.2
encoder.start()	# This will not block the main thread!!!

# Switch initialization if a switch is needed
switch = gaugette.switch.Switch(SW_PIN)
last_state = None

# Rotary Encoder Thread??
while True:
	print 'entering encoder'
	delta = encoder.get_delta()
	if delta != 0:
		print 'rotate %d' %delta
	
	sw_state = switch.get_state()
	if sw_state != last_state:
		print 'switch %d' %sw_state
		last_state = sw_state

print 'outside encoder'


"""
USER INPUT
"""
height = 0
weight = 0
Aext = 0
Aflex = 0
Pext = 0
Pflex = 0

# Ask the user for height in inches and weight in lbs
height = float(raw_input("\nPatients height (inches): "))
weight = float(raw_input("\nPatients weight (lbs): "))

# ROM in degrees. Flexion should be higher, i.e. 130 and extension should be
# lower, i.e. 0
Aext = int(raw_input("\nPatients active ROM, extension (degrees): "))
Aflex = int(raw_input("\nPatients active ROM, flexion (degrees): "))
Pext = int(raw_input("\nPatients passive ROM, extension (degrees): "))
Pflex = int(raw_input("\nPatients passive ROM, flexion (degrees): "))


wCount = 1
# Test if the values were entered correctly.
while( not(0 < Aext < 50) or not(0 < Pext < 50) or not(100 < Aflex < 150) or not(100 < Pflex < 150) ):
	if ( wCount >= 3 ):
		sys.exit("\nValues were repeatedly entered incorrectly!")
	else:
		wCount+=1
	print '''\nRange of motion is either reversed or entered incorrectly!
Extension and flexion should be close to 0 and 130 respectively.'''
	ext = int(raw_input("\nPatients ROM, extension (degrees): "))
	flex = int(raw_input("\nPatients ROM, flexion (degrees): "))

print '''The patients information entered:
Height (inch) \t= %d
Weight (lb) \t= %d
ROM (degree) \t= %d - %d''' %(height,weight,ext,flex)


	

"""
INITIALIZATION
1. Initialize constants
2. Calculate maximum torque required to lift the patient's shank
3. Obtain position of the rotary encoder
4. Proceed
"""
# 1 lb = 0.453591 kg
# Gravity approximated to 9.81 m/s^2
# 1 inch = 0.0254 m
weight = (weight*0.453591)*9.81	# N
height = height*0.0254	# m

# Shank weight is ~ 4.6% of body weight
# Foot weight is ~ 1.3% of body weight
shankWeight = 0.046*weight	# N
footWeight = 0.013*weight	# N

# Length from knee to center of gravity (cog) of shank, ~ 10.8% of height
# Length from knee to cog of foot, ~ 25% of height
lenShank = 0.108*height	# m
lenFoot = 0.25*height	# m

# Moment generated about the knee, TORQUE
moment = shankWeight*lenShank + footWeight*lenFoot	# Nm

print '''The patients information entered:
Height (m) \t= %f
Weight (N) \t= %f
ROM (degree) \t= %d - %d''' %(height,weight,ext,flex)



# Get position and velocity of the motor, should be ~ 90 and 0 respectively
#theta = 
#thetaDot = 
'''
if (theta < 0 or theta > 150):
	sys.exit("Brace position is out of safe operating range!")
else:
	pass
'''

"""
RUN
1. Wait for movement
	a) Upon movement obtain position
"""
# Get position and velocity of the motor
#theta = 
#thetaDot = 

#while(

'''
CLEANUP OPERATIONS
'''
# Stop getting data from the rotary encoder.
encoder.stop()
# Join the encoder thread with the main thread.
encoder.join()
# Clean up any GPIO pins that were initialized.
GPIO.cleanup()

