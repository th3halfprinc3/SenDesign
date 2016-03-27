#!/usr/bin/python

import time
total = []
for i in range(10):
	t0 = time.time()
	print "I'm timing you"
	t1 = time.time()
	total.append(t1-t0)
	print total[i]
print "done"

runTot = 0
for i in range(1,len(total)):
	runTot += total[i]*(1e3)
avgTime = runTot/len(total)	# ms

print 'The average time is: ',avgTime,'ms'


# ALTERNATIVELY
#timeit.timeit(function, number = 1000)
