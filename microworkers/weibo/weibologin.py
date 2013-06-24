#encoding: utf-8

from ilogin import ilogin
import base64
import re
import json
import binascii
import urllib
import urllib2
import rsa

class weibo_login(ilogin):
    def __init__(self,username,pwd):
        self.task = "weibo" #must be declared before super __init__
        super(weibo_login,self).__init__(username,pwd)

    def __get_login_data(self):
        login_data = {
            'entry': 'weibo',
            'gateway': '1',
            'from': '',
            'savestate': '7',
            'userticket': '1',
            'ssosimplelogin': '1',
            'vsnf': '1',
            'vsnval': '',
            'su': '',
            'service': 'miniblog',
            'servertime': '',
            'nonce': '',
            'pwencode': 'rsa2',
            'sp': '',
            'rsakv':'1330428213',
            'encoding': 'UTF-8',
            'url': 'http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack',
            'returntype': 'META'
        }
        servertime_url = 'http://login.sina.com.cn/sso/prelogin.php?entry=sso&callback=sinaSSOController.preloginCallBack&su=&rsakt=mod&client=ssologin.js(v1.4.4)'
        login_url = 'http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.4)'
        return login_data, servertime_url, login_url
    
    def __get_rsa_mat(self,data):
        p = re.compile('\((.*)\)')
        try:
            json_data = p.search(data).group(1)
            data = json.loads(json_data)
            servertime = str(data['servertime'])
            nonce = data['nonce'].encode('UTF-8')
            pubkey = data['pubkey'].encode('UTF-8')
            rsakv = data['rsakv'].encode('UTF-8')
            return servertime, nonce, pubkey, rsakv
        except:
            print 'Get severtime and pubkey error!'
            return 0, 0, 0, 0
        
    def __get_rsa_username_pwd(self,pubkey,servertime,nonce):
        uname = urllib.quote(self.uname) #url格式编码
        uname = base64.encodestring(uname)[:-1] #base64加密username
        
        rsaPublickey = int(pubkey, 16)
        key = rsa.PublicKey(rsaPublickey, 65537) #创建公钥
        message = servertime + '\t' + nonce + '\n' + self.passwd #拼接明文 js加密文件中得到
        passwd = rsa.encrypt(message, key) #加密
        passwd = binascii.b2a_hex(passwd) #将加密信息转换为16进制
        
        return uname, passwd
    
    def __real_login(self,content):
        p = re.compile('location\.replace\(\"(.*?)\"\)')
        login_url = p.search(content).group(1)
        result = self.get_html(login_url)
        try:
            p = re.compile('\((.*)\)')
            json_data = p.search(result).group(1)
            data = json.loads(json_data)
            result = str(data['result'])
            #print result
            if result == 'True':
                print 'RSA Login success!'
                print self.cookie_file
                self.cookie_jar.save(self.cookie_file,ignore_discard=True, ignore_expires=True)
                return 1
            else:
                print 'ID is down!'#账号登录错误次数太多,已有验证码要求
                return 0
        except:
            print '登录方式变了，重新研究吧！'
            return 0
    
    def do_login(self):
        login_data,servertime_url, login_url = self.__get_login_data()
        data = self.get_html(servertime_url)
        servertime, nonce, pubkey, rsakv  = self.__get_rsa_mat(data)
        if servertime == 0:
            return 0

        uname, passwd = self.__get_rsa_username_pwd(pubkey, servertime, nonce)
        
        login_data['servertime'] = servertime
        login_data['nonce'] = nonce
        login_data['su'] = uname
        login_data['sp'] = passwd
        login_data['rsakv'] = rsakv
        login_data = urllib.urlencode(login_data)
   
        req_login  = urllib2.Request(
            url = login_url,
            data = login_data
        )
        result = self.get_html(req_login)
   
        return self.__real_login(result)

if __name__ == "__main__":

    username = 'wangjun0125@gmail.com'
    pwd = '08162004'
    login = weibo_login(username,pwd)
    login_status = login.login()

    if login_status:
        url = 'http://www.weibo.com/u/1230502365?wvr=5&'
        text = login.get_html(url)
        print text