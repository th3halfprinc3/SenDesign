#!/usr/bin/python

import threading
import time
'''
# import from a file or files, the data needed?
#from foobar import alice, bob, charles

for mod in [alice, bob, charles]:
	# mod is an object that represents a module
	worker = getattr(mod, 'do_work')
	# worker now is a reerence to the function like alice.do_work
	t = threading.Thread(target = worker, args = [data])
	# uncomment following line if you don't want to block the program
	# until thread finishes on termination
	#t.daemon = True
	t.start()
'''

exitFlag = 0

class myThread(threading.Thread):
	def __init__(self, threadID, name, counter):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.name = name
		self.counter = counter
	def run(self):
		print 'Starting ',self.name
		print_time(self.name, self.counter, 5)
		print 'Exiting ',self.name

def print_time(threadName, delay, counter):
	while counter:
		if exitFlag:
			threadName.exit()
		
		
