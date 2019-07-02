import requests
import json
import urllib
try:
	import execption
except:
	import lib.execption as execption

class GAuth(object):
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
		headers = {
		    'Host': 'accounts.google.com',
		    'Connection': 'close',
		    'Accept-Encoding': 'gzip, deflate',
		    'accept': '*/*',
		    'origin': 'https://accounts.google.com',
		    'authority': 'accounts.google.com',
		    'accept-language': 'en-US,en;q=0.9,ar;q=0.8',
		    'x-same-domain': '1',
		    'dnt': '1',
		    'referer': 'https://accounts.google.com/signin/v2/sl/pwd?hl=en&passive=true&continue=https%3A%2F%2Fwww.google.com.eg%2F&flowName=GlifWebSignIn&flowEntry=ServiceLogin&cid=1&navigationDirection=forward',
		    'google-accounts-xsrf': '1',
		    'content-type': 'application/x-www-form-urlencoded;charset=UTF-8',
		}

		# Request has problem encoding this.
		data = 'continue=https%3A%2F%2Fwww.google.com%2F%3Fgws_rd%3Dssl&hl=en&f.req=%5B%22{}%22%2Cnull%2C1%2Cnull%2C%5B1%2Cnull%2Cnull%2Cnull%2C%5B%22{}%22%2Cnull%2Ctrue%5D%5D%2C%5Bnull%2Cnull%2C%5B2%2C1%2Cnull%2C1%2C%22https%3A%2F%2Faccounts.google.com%2FServiceLogin%3Fhl%3Den%26passive%3Dtrue%26continue%3Dhttps%253A%252F%252Fwww.google.com%252F%253Fgws_rd%253Dssl%22%2Cnull%2C%5B%5D%2C4%2C%5B%5D%2C%22GlifWebSignIn%22%5D%2C1%2C%5Bnull%2Cnull%2C%5B%5D%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2C%5B%5D%2Cnull%2Cnull%2Cnull%2C%5B%5D%2C%5B%5D%5D%2Cnull%2Cnull%2Cnull%2Ctrue%5D%5D&bgRequest=%5B%22identifier%22%2C%22%22%5D&bghash=&azt=&cookiesDisabled=false&deviceinfo=%5Bnull%2Cnull%2Cnull%2C%5B%5D%2Cnull%2C%22EG%22%2Cnull%2Cnull%2C%5B%5D%2C%22GlifWebSignIn%22%2Cnull%2C%5Bnull%2Cnull%2C%5B%5D%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2C%5B%5D%2Cnull%2Cnull%2Cnull%2C%5B%5D%2C%5B%5D%5D%5D&gmscoreversion=undefined&checkConnection=youtube%3A395%3A1&checkedDomains=youtube&pstMsg=1&'
		data = data.format(self.__g_token(),urllib.quote(self.password))

		response = self.session.post('https://accounts.google.com/_/signin/sl/challenge', headers=headers, data=data, verify=False)

		if "CheckCookie" in response.content:
			return ({"status":1,"session":self.session})

		if "INCORRECT_ANSWER_ENTERED" in response.content:
			raise execption.LoginFailed()

		raise execption.LoginFailed()