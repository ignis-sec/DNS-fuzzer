import os
import sys
import re
import threading
from multiprocessing.pool import ThreadPool
import signal
import argparse

MAX_THREADS = 10
lock = threading.Lock()
nameserver = ''
verbose=False

#arguement setup
parser = argparse.ArgumentParser()
parser.add_argument("-t",type=int, help="Number of threads. Default is 10")
parser.add_argument("-n", help="Specific nameserver. Default is any")
parser.add_argument("-v", action='store_true',help="verbose")
parser.add_argument("wordlist", help="Wordlist to attempt from")
args = parser.parse_args()

#handling
wordlist = args.wordlist
if(args.t):
	MAX_THREADS = args.t

if(args.n):
	nameserver = args.n
if(args.v):
	verbose=True
#sigterm handle
def signal_handler(sig, frame):
        print('Terminating all pool workers.')
        pool.terminate()
        sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

#pool worker process #
def doLookup(line,counter):
	bTimeout = True
	lock.acquire()
	
	sys.stdout.write("\r" + str(counter) + " ")
	lock.release()
	while bTimeout==True:
	    output = os.popen("nslookup "+ line + ' ' + nameserver).read()
	    timeout = re.search("connection timed out; no servers could be reached", output)
	    if(timeout!=None):
	    	bTimeout=True
	    	print("\033[1;31mConnection timed out. Possibly thread number too high. Waiting and decreasing thread number\033[1;37m")
	    	time.sleep(1)
	    	MAX_THREADS=MAX_THREADS-1 # Not actually doing anything yet, need to resize pool in future
	    else:
	    	bTimeout=False

	x = re.search("(C|c)an't find", output)
	if x == None:#Name exists in dns server 
	    canon = re.search("(?<=canonical name = ).*",output)
	    if (canon==None):
	        canstr=''
	    else: #canonical name exists too.
	        canstr = canon.group(0)
	    #lock thread until io is finished
	    lock.acquire()
	    print("\r\033[1;37m" + str(counter) + " \033[1;32m" + line + (20-len(line))*' ' + canstr + "\033[1;37m")
	    if(verbose):
	    	print(output)
	    lock.release()
	return

fp = open(wordlist, "r")
line = fp.readline()
counter = 1
pool = ThreadPool(processes=MAX_THREADS)

while line:
    line = fp.readline()
    line = line.strip('\n')
    counter=counter+1
    pool.apply_async(doLookup, (line,counter))

pool.close()  # Done adding tasks.
pool.join()  # Wait for all tasks to complete.
