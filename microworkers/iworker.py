
import urllib2
import simplejson as json
import setting
import time

class iworker(object):
	def __init__(self):
		self.name = ""
		self.server_url = setting.SERVER_URL
		self.task = ""
		self.mul = False
		self.type = setting.TYPE_ROSTER
		self.inteval = setting.KEEPALIVE_INTEVAL
		pass

	def get_tasks(self):
		#worker name must be unique
		if(self.name == "" or self.server_url == "" or self.task == ""):
			return

		querys = {"name":self.name, "prefer":self.task, "type":self.type}
		data = urllib.urlencode(querys)

		req = urllib2.Request(self.server_url,data)
		response = urllib2.urlopen(req)
        http_code = response.getcode()
		if(http_code == 200):
			context = json.dumps(response.read())
			vjson = jsom.loads(context)
			if(vjson["type"] == self.task):
				return vjson["roster"]
			else:
				print "error: only exptext task: "+ self.name
				return ""
		else:
			print "error: failed to get task"
			return ""

	def init_request(self):
		roster = get_tasks()
		if(roster == ""):
			return
        if(!self.mul):
            iheader = get_headers()

		for one in roster:
			if(self.mul):
				iheader = get_headers()
		    request = urllib2.Request(url,headers=iheader)
		    response = urllib2.urlopen(request)
		    http_code = response.getcode()
		    if(http_code == 200):
		    	context = parse(response.read())
		    	yield Gfilter.filter_roster(context)
		    else:
		    	time.sleep(10)
    
    def get_headers(self):
    	#
    	return headers

    def parse(self):

    	pass

    def sync_result(self):
    	items = init_request()
    	for item in items:
    		midresult = item.next()
    		print mifresult
    	pass



        