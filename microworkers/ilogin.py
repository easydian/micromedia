#encoding: utf-8

"""
src: https://github.com/llqbll/web_login/blob/master/login.py
tiny modification
"""

import os
import urllib
import urllib2
import cookielib
from gzip import GzipFile
from StringIO import StringIO
import zlib
import base64
import re
import json
import binascii
import time
from rootcfg import ROOTDIR

class ContentEncodingProcessor(urllib2.BaseHandler):
    """A handler to add gzip capabilities to urllib2 requests """

    # add headers to requests
    def http_request(self, req):

        req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.22 (KHTML, like Gecko) Chrome/25.0.1364.152 Safari/537.22')
        req.add_header("Accept-Encoding", "gzip, deflate")
        return req

    # decode
    def http_response(self, req, resp):
        old_resp = resp
        # gzip
        if resp.headers.get("content-encoding") == "gzip":
            gz = GzipFile(
                    fileobj=StringIO(resp.read()),
                    mode="r"
                )
            resp = urllib2.addinfourl(gz, old_resp.headers, old_resp.url, old_resp.code)
            resp.msg = old_resp.msg
        # deflate
        if resp.headers.get("content-encoding") == "deflate":
            gz = StringIO( deflate(resp.read()) )
            resp = urllib2.addinfourl(gz, old_resp.headers, old_resp.url, old_resp.code)  # 'class to add info() and
            resp.msg = old_resp.msg
        return resp

# deflate support
def deflate(data):   # zlib only provides the zlib compress format, not the deflate format;
    try:               # so on top of all there's this workaround:
        return zlib.decompress(data, -zlib.MAX_WBITS)
    except zlib.error:
        return zlib.decompress(data)

class ilogin(object):

    encoding_support = ContentEncodingProcessor
    def __init__(self,username,pwd):#初始化urllib2，引入cookie
        self.uname = username
        self.passwd = pwd
        cookie_file = ROOTDIR+'/cfg/'+self.task+'/'+username+".dat"
        self.cookie_file = cookie_file
        #httpHandler = urllib2.HTTPHandler(debuglevel=1)
        #httpsHandler = urllib2.HTTPSHandler(debuglevel=1)
        self.cookie_jar = cookielib.MozillaCookieJar()
        cookie_support = urllib2.HTTPCookieProcessor(self.cookie_jar)
        self.opener = urllib2.build_opener(cookie_support, self.encoding_support,urllib2.HTTPHandler)
        urllib2.install_opener(self.opener)#设置 urllib2 的全局 opener
       
    def get_html(self,url):
        isopen = True
        count = 0
        while isopen:
            try:
                result = self.opener.open(url).read()
                isopen = False
            except:
                isopen = True
                count += 1
                if count > 5:
                   isopen = False 
                else:
                   time.sleep(0.5)
        return result

    def do_login(self):#RSA加密直接登录
        return 0

    def login(self):#使用cookie登录,可以解决验证码问题
        if os.path.exists(self.cookie_file):
            try:
                print "cookie login..."
                cookie_load = self.cookie_jar.load(self.cookie_file,ignore_discard=True, ignore_expires=True)
                return 1
            except cookielib.LoadError:
                print 'Loading cookies error'
                return self.do_login()#cookie过期使用RSA加密登录
        else:
            print "cookie file isnot exist"
            return self.do_login()