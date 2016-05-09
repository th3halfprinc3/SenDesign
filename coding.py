#!/usr/bin/pytho


########################################################################################
'''
NOTES:



SPI ports
	DO NOT US GPIO.setup() ON ANY OF THESE SPI PINS!!!!!!!!!!
	SPICLK = 23
	SPIMISO = 21
	SPIMOSI = 19
	SPICS = 24

ADC
0.00322 accuracy

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



NOTE THAT ALL POSITIVE DEGREES REPRESENTS A COUNTER CLOCKWISE MOTION

Extension yields a decreasing voltage
flexion yields an increasing voltage

AT THE POT SHAFT
X ( deg )		Y ( Volts )
3600		-->	3.3	full counter clockwise
0			-->	1.65
-3600		-->	0.0	full clockwise
360		-->	0.33
90			-->	0.0825
1			-->	0.000917

AT THE KNEE, a displacement of x degrees yields a change of y volts
X ( deg )		Y ( Volts )
90			-->	0.33
50			-->	0.183
40			-->	0.147
30			-->	0.111	
1			-->	0.0037


0.0037V change is a 1 degree change at the knee.
A change in 0.33V is a displacement of 90 degrees at the knee.
This is okay because the resolution of the ADC is 0.0032V.

VOLTAGE ASSOCIATED WITH THE POSITION OF THE KNEE
X ( deg )		Y ( Volts )
0			-->	1.32
90			-->	1.65
120		-->	1.761
130		-->	1.797
140		-->	1.833
'''



########################################################################################




print '\nImporting libraries...'
import RPi.GPIO as GPIO
from time import sleep
import timeit
import time
import spidev
from numpy import matrix
from numpy import zeros



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
			totCount += 1
		
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
		GPIO.output(ENABLE1, GPIO.LOW)
		GPIO.output(ENABLE2, GPIO.LOW)
		pwmControl1.stop()
		pwmControl2.stop()
		print 'Feedback and control disabled after button press.'
	#Endtry

	finally:
		GPIO.output(ENABLE1, GPIO.LOW)
		GPIO.output(ENABLE2, GPIO.LOW)
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

	try:
		while True:
			progChoice = raw_input('Which exercise would you like to do, extension or flexion? ').lower().strip()

			if( progChoice == 'debug'):
				break
			elif( progChoice == 'flex' or progChoice == 'ext' or progChoice == 'extension' or progChoice == 'flexion' ):

				print '''You have chosen %s, is this correct? ''' %( progChoice )
				rpt = raw_input().lower().strip()
	
				if ( rpt == 'yes' ):
					break
				elif ( rpt == 'no'):
					pass
				else:
					print "Please Enter 'yes' or 'no'."
				#End if
	
			else:
				print "Please enter 'flex', 'flexion', 'ext', or 'extension'."
			#End if
		#End while

	
		pauseTime = 0.02
	
		print 'Please position the brace at 90 degrees.'
	
	
		dV = 0.0037
		vol = 1.32
		l = 141
		A = zeros(shape = (1, l))
	
		# No need to include 2 rows, since the index is also the angle!
		for i in range(0, l):
			A[0, i] = vol
			vol += dV
		#End for
	
		sleep(3)
	
	
		'''
		Flexion:
		We want to start at 90 deg (or specified starting position), x(0) = pi/2 = 90 deg
		The Aflex variable will be used to indicate when to send a high ENABLE
		signal to start the motor. The PWM (5 - 48% DC) should slowly ramp up to 60
		deg/s. The voltage from the pot will be used to determine the distance the
		brace has travelled. If the distance travelled + 90 deg is within a
		mathematically sound percent error value, then a low ENABLE signal should be
		sent to disable the motor so the user can move their knee freely.
		'''
		
		# 3.3v is 5 turns = 5*360 deg counter clockwise and 0V is 5*360 deg
		# clockwise. 1.6V is centered and at 90 degrees if it is
		# assembled this way. 90 deg advance is 0.0825V. So if the voltage is 1.6
		# or greater, then the 
		

		'''
		# how much has it changed since the last read?
		pot_adjust = abs(trim_pot - last_read)
	
	
		if ( pot_adjust > tolerance ):
			trim_pot_changed = True
		'''

		# Volts/bit constant
		voltBit = 3.3/1024
	
		# Initial analog voltage should be close to 1.65V
		anaVol = voltBit * readADC( 0 )	# Read from channel 0 on the ADC
	
		# Since the brace will start near 90 degrees
		curPos = (np.abs(A - anaVol)).argmin()
	
	
		'''
		Extension:
		We want to start at 90 deg (or specified starting position), x(0) =
		pi/2 = 90 deg. The Aext variable will be used to indicate when to send
		a high ENABLE signal to start the motor. The PWM (52 - 95% DC) should
		be slowly ramped up to 60 deg/s,	or immediately to this value. The pot
		will be used to determine how much distance the brace has travelled.
		If the distance travelled + 90deg is within 2 or 3	degrees (or use a
		percent error value, which would be more mathematically sound!) of
		Pext, then send a low ENABLE signal. This will stop the motor and
		allow the knee to move freely.
		'''

		speed = 60	# deg/s

		if( progChoice == 'ext' or progChoice == 'extension' ):

			# Ensure that the motor is NOT enabled.
			GPIO.output(ENABLE1, GPIO.LOW)
			GPIO.output(ENABLE2, GPIO.LOW)

			# Do nothing while the angle is less than the active value
			while curPos > Aext:
				lastVol = curVol
				curVol = voltBit * readADC( adcNum )
				print 'Analog voltage = ', curVol

				if( curVol > 1.761 or curVol < 1.32 ):
					print 'The analog voltage is out of range! Exiting.'
					exit()	# Brace is out of ROM, 0 - 120
				else:
					pass
				#End if

				# Gets the voltage in the table A that is closest to the analog
				# voltage and returns its index and thus the degrees
				curPos = (numpy.abs(A - curVol)).argmin()
				print 'Current Position = ', curPos
				
				if( curPos > 118 or curPos < 2 ):
					print 'The position of the brace is approaching the extent of the intended ROM! Exiting.'
					exit()
				else:
					pass
				#End if
			#End while
							
			# Enable the motor.
			GPIO.output(ENABLE1, GPIO.HIGH)
			GPIO.output(ENABLE2, GPIO.HIGH)
			print 'Engaging Control and Feedback.'

			while curPos > Pext:
	
				# Reads the feedack signal and determinses the Duty Cycle
				DC = readPWM(HLFB)
				print 'Duty Cycle from HLFB = ', DC

				lastVol = curVol

				# This gives me the voltage, now associate it with a position!
				curVol = voltBit * readADC( adcNum )
				print 'Analog voltage = ', curVol
				
				if( curVol > 1.761 or curVol < 1.32 ):
					print 'The analog voltage is out of range! Exiting.'
					exit()	# Brace is out of ROM, 0 - 120
				else:
					pass
				#End if

				curPos = (numpy.abs(A - curVol)).argmin()
				print 'Current Position = ', curPos

				if( curPos > 118 or curPos < 2 ):
					print 'The position of the brace is approaching the extent of the intended ROM! Exiting.'
					GPIO.output(ENABLE1, GPIO.LOW)
					GPIO.output(ENABLE2, GPIO.LOW)
					exit()
				else:
					pass
				#End if

				pwmControl1.ChangeDutyCycle(5)		# 60 deg/s counter clockwise
				pwmControl2.ChangeDutyCycle(95)		# 60 deg/s clockwise
			#Endwhile

	
		elif( progChoice == 'flex' or progChoice == 'flexion' ):

			# Ensure that the motor is NOT enabled.
			GPIO.output(ENABLE1, GPIO.LOW)
			GPIO.output(ENABLE2, GPIO.LOW)
			
			# Do nothing while the angle is less than the active value
			while ang < Aflex:

				curVol = voltBit * readADC( adcNum )
				print 'Analog voltage = ', curVol

				if( curVol > 1.761 or curVol < 1.32 ):
					print 'The analog voltage is out of range! Exiting.'
					exit()	# Brace is out of ROM, 0 - 120
				else:
					pass
				#End if

				# Gets the voltage in the table A that is closest to the analog
				# voltage and returns its index and thus the degrees
				curPos = (numpy.abs(A - curVol)).argmin()
				print 'Current Position = ', curPos
				
				if( curPos > 118 or curPos < 2 ):
					print 'The position of the brace is approaching the extent of the intended ROM! Exiting.'
					GPIO.output(ENABLE1, GPIO.LOW)
					GPIO.output(ENABLE2, GPIO.LOW)
					exit()
				else:
					pass
				#End if
			#Endwhile
	
			GPIO.output(ENABLE1, GPIO.HIGH)
			GPIO.output(ENABLE2, GPIO.HIGH)

			while ang < Pflex:

				# Reads the feedack signal and determinses the Duty Cycle
				DC = readPWM(HLFB)
				print 'Duty Cycle from HLFB = ', DC
	
				# This gives me the voltage, now associate it with a position!
				curVol = voltBit * readADC( adcNum )
				print 'Analog voltage = ', curVol
				
				if( curVol > 1.761 or curVol < 1.32 ):
					print 'The analog voltage is out of range! Exiting.'
					exit()	# Brace is out of ROM, 0 - 120
				else:
					pass
				#End if

				curPos = (numpy.abs(A - curVol)).argmin()
				print 'Current Position = ', curPos

				if( curPos > 118 or curPos < 2 ):
					print 'The position of the brace is approaching the extent of the intended ROM! Exiting.'
					GPIO.output(ENABLE1, GPIO.LOW)
					GPIO.output(ENABLE2, GPIO.LOW)
					exit()
				else:
					pass
				#End if

				pwmControl1.ChangeDutyCycle(95)		# 60 deg/s clockwise
				pwmControl2.ChangeDutyCycle(5)		# 60 deg/s counter clockwise
			#Endwhile

		else:	# Debugging
			print 'Clockwise'
			for i in range(52, 101):
				pwmControl1.ChangeDutyCycle(i)
				pwmControl2.ChangeDutyCycle(100-i)
				sleep(pauseTime)
			#Endfor
				
			print 'Counter Clockwise'
			for i in range(49):
				pwmControl1.ChangeDutyCycle(100-i)
				pwmControl2.ChangeDutyCycle(i)
				sleep(pauseTime)
			#Endfor
		#Endif

		print 'Disabling motor...'
		GPIO.output(ENABLE1, GPIO.LOW)
		GPIO.output(ENABLE2, GPIO.LOW)

		print 'Stopping PWMs...'
		pwmControl1.ChangeDutyCycle(50)
		pwmControl2.ChangeDutyCycle(50)
		pwmControl1.stop()
		pwmControl2.stop()

		print 'Cleaning GPIO pins...'
		GPIO.cleanup()
		string = 'completion'
		startK = timeit.timeit()

	except KeyboardInterrupt:
		startK = timeit.timeit()
		GPIO.output(ENABLE1, GPIO.LOW)
		GPIO.output(ENABLE2, GPIO.LOW)
		string = 'keyboard interrupt'
	
	finally:
		GPIO.output(ENABLE1, GPIO.LOW)
		GPIO.output(ENABLE2, GPIO.LOW)
		pwmControl1.stop()
		pwmControl2.stop()
		print 'Feedback and control disabled after error.'
		GPIO.cleanup()#Endtry
	
		endK = timeit.timeit()
		totalTime = abs(1000*(endK - startK))
		print 'Time elapsed after ', string,' is: ', totalTime, 'ms.'

		exit()
	#Endtry
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
			Aext = int(raw_input("\nPatients active ROM, extension (degrees): "))
			Aflex = int(raw_input("\nPatients active ROM, flexion (degrees): "))
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
			Pext = int(raw_input("\nPatients passive ROM, extension (degrees): "))
			Pflex = int(raw_input("\nPatients passive ROM, flexion (degrees): "))
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
		print '''Torque is within the supported range. The device will support the
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
	
	# motor pins, BCM
	inputB1 = 19
	ENABLE1 = 20
	HLFB1 = 17

	inputB2 = 26
	ENABLE2 = 21
	HLFB2 = 18

	button = 23
	print '\nInitializing and setting up the motor...\n'

	# Try to use BOARD instead of BCM.
	# This is because BCM can break between revisions of the Rasp Pi
	GPIO.setmode(GPIO.BCM)
	
	# PWM output to control speed of the motor.
	GPIO.setup(inputB1, GPIO.OUT)
	GPIO.setup(inputB2, GPIO.OUT)
	
	# ENABLE pin. high to have feedback and low for no feedback?
	GPIO.setup(ENABLE1, GPIO.OUT)
	GPIO.setup(ENABLE2, GPIO.OUT)

	# High Level FeedBack from the motor.
	GPIO.setup(HLFB1, GPIO.IN) 
	GPIO.setup(HLFB2, GPIO.IN) 
	
	# GPIO 23 set up as an input for a pull up detection. Pin 23 will go to GND
	# when pressed and enables us to achieve edge detection.
	GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_UP)
	
	# 50% duty cyle(dc) +- 1 will be 0 velocity.
	# 0 - 48% dc results in a clockwise(cw) rotation.
	# 52 - 100% dc results in a counter-clockwise(ccw) rotation.
	pwmControl1 = GPIO.PWM(inputB1, 50)	# Create a PWM object at pin inputB1 set at 50 Hz.
	pwmControl2 = GPIO.PWM(inputB2, 50)	# Create a PWM object at pin inputB2 set at 50 Hz.
	pwmControl1.start(50)	# Start a PWM at 50% duty cycle
	pwmControl2.start(50)	# Start another PWM at 50% duty cycle
	
	# The GPIO.add_event_detect() line sets things up so that when a rising edge
	# is detected on port 23, regardless of what is happening elsewhere in the
	# program, the funciton 'buttonPress' will be run. This will even happen
	# while the program waits for something else in the program.
	GPIO.add_event_detect(button, GPIO.RISING, callback=buttonPress)

	controlSystem()


#Endif

########################################################################################
