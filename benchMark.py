import mainTest1
from time import sleep

if __name__ == '__main__':
	try:
		while True:
			mainTest1.funcFor()
		#Endwhile
	finally:
		sleep(3)
		print 'Consistent CTRL-C'
	#Endtry
#Endif
		

