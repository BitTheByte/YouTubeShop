from selenium import webdriver
import requests
import urllib
import time
import json
import re
try:
	import execption
except:
	import lib.execption as execption


class Botgaurd(object):
	def server_start(self):
		print("[CORE]: Handing off botguard.js execution to chrome")
		self.browser = webdriver.Chrome(executable_path=r"lib\\chromedriver.exe")
		self.browser.get("https://accounts.google.com/signin/v2/identifier?flowName=GlifWebSignIn&flowEntry=ServiceLogin")
		return self.browser

	def server_shutdown(self):
		print("[CORE]: shutting down chrome ..  please wait")
		self.browser.quit()


class GAuth(object):
	def set_botguard_server(self,browser):
		self.browser = browser

	def __botguard_generate_token(self,binary):
		if len(binary) == 0: return ""

		binary = binary[0].decode("unicode-escape")
		for _ in range(30):
			token = self.browser.execute_script("""
				try{
					return botguard.bg("%s").invoke()
				}catch(err){
					return -1;
				}
				""" % binary)
			if token != -1:
				#print("[CORE]: botguard.js :: " + token)
				return token
			time.sleep(0.5)
		else:
			return ""

	def __init__(self,email,password):
		self.email = email
		self.password = password
		self.session = requests.Session()
		self.session.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
	
	def __g_token(self):
		self.session.get('https://accounts.google.com/ServiceLogin?hl=en&passive=true&continue=https://www.google.com/')
		headers = {
		    'x-same-domain': '1',
		    'origin': 'https://accounts.google.com',
		    'accept-encoding': 'gzip, deflate, br',
		    'accept-language': 'en-US,en;q=0.9,ar;q=0.8',
		    'google-accounts-xsrf': '1',
		    'content-type': 'application/x-www-form-urlencoded;charset=UTF-8',
		    'accept': '*/*',
		    'referer': 'https://accounts.google.com/signin/v2/identifier?hl=en&passive=true&continue=https%3A%2F%2Fwww.google.com.eg%2F&flowName=GlifWebSignIn&flowEntry=ServiceLogin',
		    'authority': 'accounts.google.com',
		    'dnt': '1',
		}

		data = {
		  'continue': 'https://www.google.com/',
		  'hl': 'en',
		  'f.req': '["{email}","",[],null,"EG",null,null,2,false,true,[null,null,[2,1,null,1,"https://accounts.google.com/ServiceLogin?hl=en&passive=true&continue=https%3A%2F%2Fwww.google.com.eg%2F",null,[],4,[],"GlifWebSignIn"],1,[null,null,[],null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,[],null,null,null,[],[]],null,null,null,true],"{email}"]'.format(email=self.email),
		  'cookiesDisabled': 'false',
		  'deviceinfo': '[null,null,null,[],null,"EG",null,null,[],"GlifWebSignIn",null,[null,null,[],null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,[],null,null,null,[],[]]]',
		  'gmscoreversion': 'undefined',
		  'checkConnection': 'youtube:365:1',
		  'checkedDomains': 'youtube',
		  'pstMsg': '1',
		}

		response = self.session.post('https://accounts.google.com/_/signin/sl/lookup?hl=en&_reqid=144088&rt=j', headers=headers, data=data)
		
		return json.loads((response.content).replace(")]}'",""))[0][0][2]

	def ServiceLogin(self,name,return_url):
		headers = {
		    'authority': 'accounts.google.com',
		    'upgrade-insecure-requests': '1',
		    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
		    'accept-encoding': 'gzip, deflate, br',
		    'accept-language': 'en-US,en;q=0.9'
		}
		params = (
		    ('passive', 'true'),
		    ('continue', return_url),
		    ('hl', 'en'),
		    ('uilel', '3'),
		    ('service', name),
		)
		service_session = self.Glogin()["session"]
		service_session.get('https://accounts.google.com/ServiceLogin', headers=headers, params=params)
		return service_session

	def Glogin(self):
		botguard_token = self.__botguard_generate_token(re.findall(r'&quot;(eLC.*?)&quot;',self.session.get("https://accounts.google.com/signin").text))
		
		headers = {
		   'authority': 'accounts.google.com',
		   'pragma': 'no-cache',
		   'cache-control': 'no-cache',
		   'x-same-domain': '1',
		   'origin': 'https://accounts.google.com',
		   'google-accounts-xsrf': '1',
		   'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36',
		   'dnt': '1',
		   'content-type': 'application/x-www-form-urlencoded;charset=UTF-8',
		   'accept': '*/*',
		   'sec-fetch-site': 'same-origin',
		   'sec-fetch-mode': 'cors',
		   'referer': 'https://accounts.google.com/signin/v2/sl/pwd?hl=en&passive=true&continue=https%3A%2F%2Fwww.google.com%2F%3Fgws_rd%3Dssl&flowName=GlifWebSignIn&flowEntry=ServiceLogin&cid=1&navigationDirection=forward',
		   'accept-encoding': 'gzip, deflate, br',
		   'accept-language': 'en-US,en;q=0.9,ar;q=0.8',
		   'cookie': '1P_JAR=2019-12-15-16',
		}

		data = {
		  'continue': 'https://www.google.com/?gws_rd=ssl',
		  'hl': 'en',
		  'f.req': '["{token}",null,1,null,[1,null,null,null,["{password}",null,true]],[null,null,[2,1,null,1,"https://accounts.google.com/ServiceLogin?hl=en&passive=true&continue=https%3A%2F%2Fwww.google.com%2F%3Fgws_rd%3Dssl",null,[],4,[],"GlifWebSignIn",null,[]],1,[null,null,[],null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,[],null,null,null,[],[]],null,null,null,true,null,null,null,null,"{email}"]]'.format(
		  	token=self.__g_token(),
		  	email=self.email,
		  	password=self.password
		   ),
		  'bgRequest': '["identifier","{}"]'.format(botguard_token),
		  'cookiesDisabled': 'false',
		  'deviceinfo': '[null,null,null,[],null,"EG",null,null,[],"GlifWebSignIn",null,[null,null,[],null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,[],null,null,null,[],[]]]',
		  'gmscoreversion': 'undefined',
		  'checkConnection': 'youtube:520:1',
		  'checkedDomains': 'youtube',
		  'pstMsg': '1',
		}

		response = self.session.post('https://accounts.google.com/_/signin/sl/challenge', headers=headers, data=data, verify=False)

		if "CheckCookie" in response.content:
			return ({"status":1,"session":self.session})

		if "INCORRECT_ANSWER_ENTERED" in response.content or "LOGIN_CHALLENGE" in response.content:
			raise execption.LoginFailed()

		raise execption.LoginFailed()