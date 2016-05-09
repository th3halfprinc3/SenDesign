from time import sleep

def funcFor():
	try:
		for i in range(100):
			print 'The response time is: ', i
		#Endfor
	except KeyboardInterrupt:
		print 'Keyboard Interrupt.'
		sleep(3)
#EndfuncFor

if __name__ == '__main__':
	funcFor()
#Endif


