from time import sleep
import coding

if __name__ == '__main__':
	

	coding.controlSystem()
#Endif




runTot = 0
for i in range(1,len(total)):
	runTot += total[i]*(1e3)
avgTime = runTot/len(total)	# ms

print 'The average time is: ',avgTime,'ms'


# ALTERNATIVELY
#timeit.timeit(function, number = 1000)

