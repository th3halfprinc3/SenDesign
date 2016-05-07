#!/usr/bin/python

import timeit


'''
Extension:
We want to start at 90 deg (or specified starting position), x(0) = pi/2 = 90 deg
The Aext variable will be used to indicate when to send a high ENABLE signal
to start the motor. The PWM (52 - 95% DC) should be slowly ramped up to 60 deg/s,
or immediately to this value. The pot will be used to determine how much distance
the brace has travelled. If the distance travelled + 90deg is within 2 or 3
degrees (or use a percent error value, which would be more mathematically sound!)
of Pext, then send a low ENABLE signal. This will stop the motor and allow the
knee to move freely.

Flexion:
We want to start at 90 deg (or specified starting position), x(0) = pi/2 = 90 deg
The Aflex variable will be used to indicate when to send a high ENABLE
signal to start the motor. The PWM (5 - 48% DC) should slowly ramp up to 60
deg/s. The voltage from the pot will be used to determine the distance the
brace has travelled. If the distance travelled + 90 deg is within a
mathematically sound percent error value, then a low ENABLE signal should be
sent to disable the motor so the user can move their knee freely.
'''



def control(progNum, Aext, Aflex, Pext, Pflex):

	x0 = 90
	if ( progNum == 1 ):	# Extension
	
		#readPot()
		# ...
		# distTrav = 
	
		# If we have reached the end of the patients active ROM, engage motor.
		if ( (distTrav - x0) <= Aext and not(Pext >= (distTrav - x0)) ):
			GPIO.output(ENABLE, HIGH)	# Send a high enable signal to engage motor
			controlSystem()
		else:
			pass
		#End if
	elif ( progNum == 2 ):	# Flexion
		#readPot()
		# ...
		# distTrav = 
		if (  ):
#End 
	
	



if __name__ == '__main__':
	main()
#End if
