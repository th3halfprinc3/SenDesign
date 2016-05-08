#!/usr/bin/pytho


########################################################################################
'''
NOTES:

	SPICLK = 23
	SPIMISO = 21
	SPIMOSI = 19
	SPICS = 24
ADC
	* SPICLK
		- ORANGE		GPIO Pin 23
	* SPIMISO	---	DOUT
		- YELLOW		GPIO Pin 21
	* SPIMOSI	---	DIN
		- BLUE		GPIO Pin 19
	* SPICS		---	CS
		- VIOLET		GPIO Pin 24

Button
	- GPIO Pin 16
	- GND

HLFB	---	green
	- GREEN		GPIO Pin 12
	- RED			GND
INPUT B	---	white
	- BLK			GPIO Pin 7
	- YELLOW		GND
ENABLE	---	blue
	- BLUE		GPIO Pin 40
	- ORANGE		GND

PERCENT ERROR BETWEEN COMMANDED SPEED AND OUTPUT SPEED IS ABOUT 6 - 7 %

ENABLE HIGH AND PWM OFF RESULTS IN A SHAFT THAT IMPEDES MOTION.

'''
########################################################################################




print '\nImporting libraries...'
import RPi.GPIO as GPIO
from time import sleep
import timeit
import time
import os
import spidev



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

'''




def readADC(adcnum):
	if adcnum > 7 or adcnum < 0:
		return -1
	r = spi.xfer2([1, 8 + adcnum << 4, 0])
	adcout = ((r[1] & 3) << 8) + r[2]
	return adcout



def readPWM(pinNum):
	startpwm = timeit.timeit()	# Time the pwm for now
	
	highCount = 0
	totCount = 0
	cur = GPIO.input(pinNum)
	while True:
		prev = cur
		cur = GPIO.input(pinNum)
		if ( cur == 1 ):	# The gpio pin is high, increment high count
			highCount += 1
			totCoutn += 1
		
		elif ( prev == 1 and cur == 0 ):		# Period has ended, now determine DC.
			totCount += 1
			dutyCycle = highCount/totCount
			break

		else:
			totCount += 1

		#End if
	#End while
	

	endpwm = timeit.timeit()
	totalTime = abs(1000*(endpwm - startpwm))	# Convert sec to ms
	print 'PWM took %.3f microseconds.' %(totalTime)

	return dutyCycle
#End readPWM	



# Define any functions necesary
def buttonPress(channel):
	startb = timeit.timeit()
	try:
		GPIO.output(ENABLE, GPIO.LOW)
		pwmControl.stop()
		print 'Feedback and control disabled.'
	#Endtry

	finally:
		GPIO.output(ENABLE, GPIO.LOW)
		GPIO.cleanup()
		endb = timeit.timeit()
		totalTime = abs(1000*(endb - startb))
		print 'Response time after button press is: ', totalTime, 'ms.'
		exit(0)
	#Endfinally
#EndbuttonPress



"""
RUN THE CONTROL SYSTEM
1. Wait for movement
	a) Upon movement obtain position
"""
def controlSystem():
	print 'Initiating control...\n'
	# Enable feedback from the motor.
	GPIO.output(ENABLE, GPIO.HIGH)
	print 'Feedback enabled.'
	
	pauseTime = 0.02
	adcNum = 0
	j = 1
	try:
		while True:
			
			#readPWM()
			#readADC()

			if j == 1:
	
				i = 0
				print 'Clockwise'
				while i <= 100:
					# This gives me the voltage, now associate it with a position!
					anaVol =(3.3/1024) * readADC( adcNum )

					print 'Analog voltage = ', anaVol

					pwmControl.ChangeDutyCycle(95)	# 60 deg/s clockwise
					sleep(pauseTime)
					i += 1
				#Endwhile
	
				i = 0
				print 'Counter Clockwise'
				while i <= 100:
					# This gives me the voltage, now associate it with a position!
					anaVol =(3.3/1024) * readADC( adcNum )

					print 'Analog voltage = ', anaVol
					pwmControl.ChangeDutyCycle(5)		# 60 deg/s ccw
					sleep(pauseTime)
					i += 1
				#Endwhile
	
			elif j == 10:
				while True:
					# This gives me the voltage, now associate it with a position!
					anaVol =(3.3/1024) * readADC( adcNum )

					print 'Analog voltage = ', anaVol

					pwmControl.ChangeDutyCycle(95)
					sleep(pauseTime)
				#Endwhile
	
			else:
				print 'Clockwise'
				for i in range(52, 101):
					# This gives me the voltage, now associate it with a position!
					anaVol =(3.3/1024) * readADC( adcNum )

					print 'Analog voltage = ', anaVol

					pwmControl.ChangeDutyCycle(i)
					sleep(pauseTime)
				#Endfor
				
				print 'Counter Clockwise'
				for i in range(49):
					# This gives me the voltage, now associate it with a position!
					anaVol =(3.3/1024) * readADC( adcNum )

					print 'Analog voltage = ', anaVol

					pwmControl.ChangeDutyCycle(i)
					sleep(pauseTime)
				#Endfor
			#Endif
		#Endwhile
		pwmControlChangeDutyCycle(50)
	
	except KeyboardInterrupt:
		startK = timeit.timeit()
		GPIO.output(ENABLE, GPIO.LOW)
	
	finally:
		GPIO.output(ENABLE, GPIO.LOW)
		pwmControl.stop()
		print 'Feedback and control disabled.'
		GPIO.cleanup()#Endtry
		exit()
	#Endtry
	
	endK = timeit.timeit()
	totalTime = abs(1000*(endK - startK))
	print 'Time elapsed after keyboard interrupt is: ', totalTime, 'ms.'

#EndcontrolSystem



"""
PARAMETER CALCULATIONS 
1. Calculate maximum torque required to lift the patient's shank
2. Proceed
"""
def getAndCalcParameters():
	get = True
	while( get ):
		# Ask the user for height in inches and weight in lbs
		height = float(raw_input("\nPatients height (inches): "))

		while ( height < 60 or height > 73 ):
			print 'The patients height is outisde the intended range.'
			choice = raw_input('\nWould you like to continue, exit or repeat? ').lower().strip()
			if ( choice == 'continue' ):
				break
			elif ( choice == 'exit' ):
				print 'Exiting program.'
				exit()
			elif ( choice == 'repeat' ):
				height = float(raw_input("\nPatients height (inches): "))
			else:
				print 'Please enter one of the following: \'continue\' or \'exit\' or \'repeat\''
			#Endif
		#Endwhile

		print 'Checking height...'
		if ( height > 80 or height < 54 ):
			print 'Patients height is to small or too large!'
			exit()
		else:
			print 'Within operational height range.'
		#Endif

		weight = float(raw_input("\nPatients weight (lbs): "))

		while ( weight < 110 or weight > 193 ):
			print 'The patients weight is outisde the intended range.'
			choice = raw_input('\nWould you like to continue, exit or repeat? ').lower().strip()
			if ( choice == 'continue' ):
				break
			elif ( choice == 'exit' ):
				print 'Exiting program.'
				exit()
			elif ( choice == 'repeat' ):
				weight = float(raw_input("\nPatients weight (lbs): "))
			else:
				print 'Please enter one of the following: \'continue\' or \'exit\' or \'repeat\''
			#Endif
		#Endwhile
	
		print 'Checking weight...'
		if ( weight > 230 or weight < 100 ):
			print 'Patients weight is too small or too large!'
			exit()
		else:
			print 'Within operational weight range.'
		#Endif

		# ROM in degrees. Flexion should be higher, i.e. 130 and extension should be
		# lower, i.e. 0
		Aext = int(raw_input("\nPatients active ROM, extension (degrees): "))
		Aflex = int(raw_input("\nPatients active ROM, flexion (degrees): "))

		wCount = 1
		while (  not(0 < Aext < 50) or not(95 < Aflex < 150) ):
			print 'Active ROM not entered correctly.'
			if ( wCount >= 3 ):
				exit("\nValues were repeatedly entered incorrectly!")
			else:
				wCount+=1
			#Endif

			print '''\nRange of motion is either reversed or entered incorrectly!
Extension and flexion should be close to 0 and 130 respectively.'''
			Aext = int(raw_input("\nPatients ROM, extension (degrees): "))
			Aflex = int(raw_input("\nPatients ROM, flexion (degrees): "))
		#Endwhile

		Pext = int(raw_input("\nPatients passive ROM, extension (degrees): "))
		Pflex = int(raw_input("\nPatients passive ROM, flexion (degrees): "))
	
		while( not(0 < Pext < 50) or not(95 < Pflex < 150) ):
			print 'Passive ROM not entered correctly.'
			if ( wCount >= 3 ):
				exit("\nValues were repeatedly entered incorrectly!")
			else:
				wCount+=1
			#Endif

			print '''\nRange of motion is either reversed or entered incorrectly!
Extension and flexion should be close to 0 and 130 respectively.'''
			Pext = int(raw_input("\nPatients ROM, extension (degrees): "))
			Pflex = int(raw_input("\nPatients ROM, flexion (degrees): "))
		#Endwhile

		print '''\nThe patients information entered:
Height (inches) \t = \t%d
Weight (lbs) \t\t = \t%d
Acive ROM (degrees) \t = \t%d - %d
Passive ROM (degrees) \t = \t%d - %d''' %(height, weight, Aext, Aflex, Pext, Pflex)

		rpt = True
		while rpt:
			# Strip the answer of all whitespace and convert their answer to
			# lowercase.
			repeat = raw_input('\nAre these the correct inputs? ( y or n ): ').lower().strip()
			if ( (repeat == 'y') or (repeat == 'yes') ):
				print 'Continuing.'
				get = False
				rpt = False
			elif ( (repeat == 'n') or (repeat == 'no') ):
				print 'Repeating.'
				rpt = False
			else:
				print 'Please enter one of the following: \'y\' or \'yes\' or \'n\' or \'no\''
				rpt = True
			#Endif
		#Endwhile
	#Endwhilei


	print '\nCalculating parameters...\n'
	# 1 lb = 0.453591 kg
	# Gravity approximated to 9.81 m/s^2
	# 1 inch = 0.0254 m
	weight = (weight*0.453592)*9.81	# N
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

	print 'Maximum torque required: %.2f' %( moment )
	
	if ( moment < 16 and moment != 0):
		print '''Torque is within the supported range. The device sill support the
full weight of the patients leg at full extension.\n'''
	elif ( moment == 0 ):
		print 'Parameters were not entered correctly!'
		exit()
	else:
		print '''Torque is NOT within the supported range. The device will not be
able to support the full weight of the patients leg at full extension.\n'''
	
	
	print '''The patients information entered:
Height (m) \t\t = \t%.2f
Weight (N) \t\t = \t%.2f
Active ROM (degrees) \t = \t%d - %d
Passive ROM (degrees) \t = \t%d - %d''' %(height, weight, Aext, Aflex, Pext, Pflex)



			 # meters, Newtons,deg,  deg,  deg,  deg
	return ( height, weight, Aext, Aflex, Pext, Pflex )
#EndgetUserInput





########################################################################################












########################################################################################

# Run main if called.
if __name__ == '__main__':


	print '\nPress CTRL-C to stop the program at any time.'
	print '\nTaking user input...'
	height, weight, Aext, Aflex, Pext, Pflex = getAndCalcParameters()

	'''
	MOTOR INITIALIZATION & SETUP
	1. Initialize & setup pins for motor, rotary encoder and PWM.
	2. Initialize any constants necessary.
	'''
	
	# motor pins
	inputB = 7
	ENABLE = 40
	HLFB = 12
	button = 16
	print '\nInitializing and setting up the motor...\n'

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
	GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_UP)
	
	# 50% duty cyle(dc) +- 1 will be 0 velocity.
	# 0 - 48% dc results in a clockwise(cw) rotation.
	# 52 - 100% dc results in a counter-clockwise(ccw) rotation.
	pwmControl = GPIO.PWM(inputB, 50)	# Create a PWM object at pin inputB set at 50 Hz.
	pwmControl.start(50)	# Start the PWM at 50% duty cycle
	
	# The GPIO.add_event_detect() line sets things up so that when a rising edge
	# is detected on port 23, regardless of what is happening elsewhere in the
	# program, the funciton 'buttonPress' will be run. This will even happen
	# while the program waits for something else in the program.
	GPIO.add_event_detect(button, GPIO.RISING, callback=buttonPress)

	controlSystem()



	# read the analog pin
	trim_pot = readADC(potentiometer_adc, SPICLK, SPIMOSI, SPIMISO, SPICS)

	# how much has it changed since the last read?
	pot_adjust = abs(trim_pot - last_read)


	if ( pot_adjust > tolerance ):
		trim_pot_changed = True


#Endif

########################################################################################
#!/usr/bin/env python
# Written by Limor "Ladyada" Fried for Adafruit Industries, (c) 2015
# This code is released into the public domain







'''
while True:
	# we'll assume that the pot didn't move trim_pot_changed = False
	trim_pot_changed = False

		if DEBUG:
		print "trim_pot:", trim_pot
		print "pot_adjust:", pot_adjust
		print "last_read", last_read


	if DEBUG:
		print "trim_pot_changed", trim_pot_changed

	if ( trim_pot_changed ):
		set_volume = trim_pot / 10.24		# convert 10bit adc0 (0-1024) trim pot read
													# into 0-100 volume level
		set_volume = round(set_volume)	# round out decimal value
		set_volume = int(set_volume)		# cast volume as integer

		print 'Volume = {volume}%' .format(volume = set_volume)
		set_vol_cmd = 'sudo amixer cset numid=1 -- {volume}% > /dev/null' .format(volume = set_volume)
		os.system(set_vol_cmd)  # set volume

		# save the potentiometer reading for the next loop
		last_read = trim_pot

		# hang out and do nothing for a half second
		time.sleep(0.5)

'''

        
	
	


#!/usr/bin/python

