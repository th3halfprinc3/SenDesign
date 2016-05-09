import time
import coding

if __name__ == '__main__':
	response = []
	try:
		for i in range(100):
			coding.controlSystem()

			

			totTime = 1000*abs(end - start)
			response[i] = totTime
		#End for
	finally:
		sleep(2)
		print 'finally clause: '
	#End try
	
	tot = 0
	for i in range(1,len(response)):
		tot += total[i]*(1e3)
	avgTime = tot/len(total)	# ms
	
	print 'The average time is: ',avgTime,'ms'
#Endif



# ALTERNATIVELY
#timeit.timeit(function, number = 1000)



