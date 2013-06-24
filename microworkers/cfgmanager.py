
import simplejson as json
import "./utils/filelock"

class cfgmanager(object):
	def  __init__(self):
		self.path = "./cookie.json"
		pass

	def  get_cfg(self):
		with FileLock(self.path, timeout=3) as lock:
		    f = file(self.path)
            self.content = json.load(f)

    def get_cookie(self,type):

    def get_useragent(self)
		



