import time
import coding

if __name__ == '__main__':
	response = []
	for i in range(100):
		try:
			execfile('coding.py')
			print 'iteration ', i
		finally:
			time.sleep(2)
			print 'finally clause: '
		#End try
	#End for
#Endif





