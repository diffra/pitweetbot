#!/usr/bin/python
import twitter
import time, datetime
import threading
import psutil
from emoji import emojize
import timeit
import random

api = twitter.Api(consumer_key='consumer_key',
                      consumer_secret='consumer_secret',
                      access_token_key='access_token',
                      access_token_secret='access_token_secret')

#print api.VerifyCredentials()
#status = api.PostUpdate("Testing pitweetbot.py")

def post_quote ( delay, counter ):
	while counter != 0:
		with open('quotes.txt') as f:
		   content = f.readlines()
		qnum=random.randint(0,465)
		#print "Quote number " + str(qnum)
		quote = content[qnum*3] + " " + content[qnum*3+1]
		#print quote
		tweets={}
		i=0
		while len(quote) > 140:
		        tweets[i]=quote[:140]
		        quote = quote[140:]
		        i += 1
		tweets[i] = quote
		
		while i > -1:
		        #print tweets[i],
			api.PostUpdate(tweets[i])
			i -= 1
		time.sleep(delay)

def post_load( delay, counter ):
	netdown = 0
	netup = 0
	while counter != 0:
		start=timeit.default_timer()
		cpuInUse = str( psutil.cpu_percent( interval=5 ) )
		memInUse = str( psutil.virtual_memory()[2])
		sdcInUse = str( psutil.disk_usage( '/' ).percent )
		hddInUse = str( psutil.disk_usage( '/media' ).percent )
		netdownps = str( ( ( psutil.net_io_counters( pernic=True )['eth0'].bytes_recv-netdown ) / delay ) / 1024 )
                netupps = str( ( ( psutil.net_io_counters( pernic=True )['eth0'].bytes_sent-netup ) / delay ) / 1024 )
		netdown = psutil.net_io_counters( pernic=True )['eth0'].bytes_recv
                netup = psutil.net_io_counters( pernic=True )['eth0'].bytes_sent
		temp = str(float(check_output(["/opt/vc/bin/vcgencmd", "measure_temp"])[5:9])*(9.0/5.0)+32)
		uptime = " ".join(str( datetime.timedelta( seconds=time.time()-psutil.boot_time() ) ).split()[:2])[:-1]
		#print emojize(":computer: %s% :signal_strength: %s% :floppy_disk: %s% :minidisk: %s% :arrow_down: %sK :arrow_up: %sK" % (cpuInUse, memInUse, sdcInUse, hddInUse, netdownps, netupps) )
		status_text=emojize(":computer: " + cpuInUse  + "%  :signal_strength: " + memInUse  + "%  :floppy_disk: " + sdcInUse  + "% (/) " +hddInUse  + "% (/media)  :arrow_down: " + netdownps  + "K  :arrow_up: " + netupps  + "K  :fire: " + temp + "F  :clock10: " + uptime)
		print status_text
		api.PostUpdate(status_text)
		counter -= 1
		stop=timeit.default_timer()
		print "sleeping " + str(delay-(stop-start)) + "seconds"
		time.sleep(delay-(stop-start))
threads=[]
t=threading.Thread( name='post_load', target=post_load, args=( 3600, -1 ) )
threads.append(t)
t.start()
q=threading.Thread( name='post_quote', target=post_quote, args=( 3*3615, -1) )
threads.append(q)
q.start()
