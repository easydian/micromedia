
import threading
import time
import urllib2
import setting

class keepalive(threading.Thread):
	def __init__(self,name,inteval):
		self.name = name
		self.url  = setting.KEEPALIVE_URL_PREFIX + name
		self.thread_stop = False
		selt.inteval = inteval
		pass
    
    def run(self):
    	while(not self.thread_stop):
    		send_heartbeat()
    		print time.ctime() + ": send a heatbeat to scheduler"
    		time.sleep(self.inteval)
  
    #worker needs a feedback?
	def send_heartbeat():
		req = urllib2.Request(self.url)
		response = urllib2.urlopen(req)


