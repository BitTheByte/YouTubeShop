import requests
import json
import re
import threading
import urlparse
import os
import glob
import platform

SUCCESS_LOGIN  = 0
FAILED_LOGIN   = 0
SUCCESS_ACTION = 0
FAILED_ACTION  = 0
Threadtimeout = 120
ThreadPoolSize = 10
storeThreads = []

from urllib3.exceptions import InsecureRequestWarning 
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

def threadManager(function,Funcargs,Startthreshold,Threadtimeout=5):
	if len(storeThreads) != Startthreshold:
		storeThreads.append(threading.Thread(target=function,args=tuple(Funcargs) ))
	if len(storeThreads) == Startthreshold:
		for metaThread in storeThreads:
			metaThread.start()
		for metaThread in storeThreads:
			metaThread.join(Threadtimeout)
		del storeThreads[::]

def G_identifier(email,SessionManager):
	while 1:
		try:
			params = (('hl', 'en'),('_reqid', '60794'),('rt', 'j'))
			headers = {
			    'x-same-domain': '1',
			    'origin': 'https://accounts.google.com',
			    'accept-encoding': 'gzip, deflate, br',
			    'accept-language': 'en-US,en;q=0.9,ar;q=0.8',
			    'google-accounts-xsrf': '1',
			    'cookie': 'GAPS=1:5anptsFCcX86o8zx79JaMKbjR6SUSg:i9ZZi85-G8eD7wsC; ',
			    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
			    'content-type': 'application/x-www-form-urlencoded;charset=UTF-8',
			    'accept': '*/*',
			    'referer': 'https://accounts.google.com/signin/v2/identifier?continue=https%3A%2F%2Fwww.youtube.com%2Fsignin%3Fhl%3Den%26app%3Ddesktop%26next%3D%252F%26action_handle_signin%3Dtrue&hl=en&service=youtube&passive=true&uilel=3&flowName=GlifWebSignIn&flowEntry=ServiceLogin',
			    'authority': 'accounts.google.com',
			    'dnt': '1'
			}
			data = [
			  ('continue', 'https://www.youtube.com/signin?hl=en&app=desktop&next=%2F&action_handle_signin=true'),
			  ('service', 'youtube'),
			  ('hl', 'en'),
			  ('f.req', '["{email}","",[],null,"EG",null,null,2,false,true,[null,null,[2,1,null,1,"https://accounts.google.com/ServiceLogin?continue=https%3A%2F%2Fwww.youtube.com%2Fsignin%3Fhl%3Den%26app%3Ddesktop%26next%3D%252F%26action_handle_signin%3Dtrue&hl=en&service=youtube&passive=true&uilel=3",null,[],4,[],"GlifWebSignIn"],1,[null,null,[]],null,null,null,true],"{email}"]'.format(email=email)),
			  ('cookiesDisabled', 'false'),
			  ('deviceinfo', '[null,null,null,[],null,"EG",null,null,[],"GlifWebSignIn",null,[null,null,[]]]'),
			  ('gmscoreversion', 'undefined'),
			  ('checkConnection', 'youtube:202:1'),
			  ('checkedDomains', 'youtube'),
			  ('pstMsg', '1')
			]
			response = SessionManager.post('https://accounts.google.com/_/signin/sl/lookup', headers=headers, params=params, data=data)
			return json.loads((response.content).replace(")]}'",""))[0][0][2]
		except Exception as e:
			print "[E] G_identifier:"+ str(e)
			pass
def login(identifier,password,SessionManager):
	while(1):
		try:
			params = (('hl', 'en'),('_reqid', '260794'),('rt', 'j'))
			headers = {
			    'x-same-domain': '1',
			    'origin': 'https://accounts.google.com',
			    'accept-encoding': 'gzip, deflate, br',
			    'accept-language': 'en-US,en;q=0.9,ar;q=0.8',
			    'google-accounts-xsrf': '1',
			    'cookie': 'GAPS=1:Q6gx2sQ34TRRxWUO3mC1_Be79xLYpA:akZ-LyOsSbAsOKOQ',
			    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
			    'content-type': 'application/x-www-form-urlencoded;charset=UTF-8',
			    'accept': '*/*',
			    'referer': 'https://accounts.google.com/signin/v2/sl/pwd?continue=https%3A%2F%2Fwww.youtube.com%2Fsignin%3Fhl%3Den%26app%3Ddesktop%26next%3D%252F%26action_handle_signin%3Dtrue&hl=en&service=youtube&passive=true&uilel=3&flowName=GlifWebSignIn&flowEntry=ServiceLogin&cid=1&navigationDirection=forward',
			    'authority': 'accounts.google.com',
			    'dnt': '1',
			}
			data = {
			  'continue': 'https://www.google.com/?gws_rd=ssl',
			  'hl': 'en',
			  'f.req': '["{}",null,1,null,[1,null,null,null,["{}",null,true]],[null,null,[2,1,null,1,"https://accounts.google.com/ServiceLogin?hl=en&passive=true&continue=https%3A%2F%2Fwww.google.com%2F%3Fgws_rd%3Dssl",null,[],4,[],"GlifWebSignIn"],1,[null,null,[],null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,[]],null,null,null,true]]'.format(identifier,password),
			  'bgRequest': '["identifier",""]',
			  'cookiesDisabled': 'false',
			  'deviceinfo': '[null,null,null,[],null,"EG",null,null,[],"GlifWebSignIn",null,[null,null,[],null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,[]]]',
			  'gmscoreversion': 'undefined',
			  'checkConnection': 'youtube:447:1',
			  'checkedDomains': 'youtube',
			  'pstMsg': '1',
			}

			response = SessionManager.post('https://accounts.google.com/_/signin/sl/challenge', headers=headers, params=params, data=data)
			login  = (response.content).replace(")]}'","")
			login =  json.loads(login)
			try:
				if "CheckCookie" in response:
					return 1
				if str(login[0][0][5][5]) == "INCORRECT_ANSWER_ENTERED":
					return 0
			except:
				return 1
		except Exception as e:
			print "[E] login:"+ str(e)
			pass
def YouTubeSubscribe(url,SessionManager):
	while(1):
		try:
			html = SessionManager.get(url).content
			session_token = (re.findall("XSRF_TOKEN\W*(.*)=", html , re.IGNORECASE)[0]).split('"')[0]
			id_yt = url.replace("https://www.youtube.com/channel/","")
			params = (('name', 'subscribeEndpoint'),)
			data = [
			  ('sej', '{"clickTrackingParams":"","commandMetadata":{"webCommandMetadata":{"url":"/service_ajax","sendPost":true}},"subscribeEndpoint":{"channelIds":["'+id_yt+'"],"params":"EgIIAg%3D%3D"}}'),
			  ('session_token', session_token+"=="),
			]
			response = SessionManager.post('https://www.youtube.com/service_ajax', params=params, data=data)
			check_state = json.loads(response.content)['code']
			if check_state == "SUCCESS":
				return 1
			else:
				return 0
		except Exception as e:
			print "[E] YouTubeSubscribe:"+ str(e)
			pass
def LoginYT(SessionManager):
	while(1):
		try:
			headers = {
			    'authority': 'accounts.google.com',
			    'upgrade-insecure-requests': '1',
			    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
			    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
			    'referer': 'https://www.youtube.com/',
			    'accept-encoding': 'gzip, deflate, br',
			    'accept-language': 'en-US,en;q=0.9'
			}
			params = (
			    ('passive', 'true'),
			    ('continue', 'https://www.youtube.com/signin?app=desktop&next=%2F&hl=en&action_handle_signin=true'),
			    ('hl', 'en'),
			    ('uilel', '3'),
			    ('service', 'youtube'),
			)
			SessionManager.get('https://accounts.google.com/ServiceLogin', headers=headers, params=params)
			return 1
		except Exception as e:
			print "[E] LoginYT:"+ str(e)
			pass
def YouTubeLike(url,SessionManager):
	while (1):
		try:
			vid_id = urlparse.parse_qs(urlparse.urlparse(url).query)['v'][0]
			html = SessionManager.get(url).content
			session_token = (re.findall("XSRF_TOKEN\W*(.*)=", html , re.IGNORECASE)[0]).split('"')[0]
			params = (('name', 'likeEndpoint'),)
			data = [
			  ('sej', '{"clickTrackingParams":"","commandMetadata":{"webCommandMetadata":{"url":"/service_ajax","sendPost":true}},"likeEndpoint":{"status":"LIKE","target":{"videoId":"'+vid_id+'"}}}'),
			  ('session_token',session_token+"=="),
			]
			response = SessionManager.post('https://www.youtube.com/service_ajax', params=params, data=data)

			check_state = json.loads(response.content)['code']
			if "SUCCESS" in str(check_state):
				return 1
			else:
				return 0

		except Exception as e:
			print "[E] YouTubeLike:"+ str(e)
			pass

def show_status(action="",channel_id="",live_count=""):
	if platform.system() == "Windows":
		os.system("cls")
	else:
		os.system("clear")
	banner = """
>>> ===================================================== <<<
>>> 	                                                  <<<
>>> 	  __   _______   ____  _   _  ___  ____           <<<
>>> 	  \ \ / |_   _| / ___|| | | |/ _ \|  _ \          <<<
>>> 	   \ V /  | |   \___ \| |_| | | | | |_) |         <<<
>>> 	    | |   | |    ___) |  _  | |_| |  __/          <<<
>>> 	    |_|   |_|   |____/|_| |_|\___/|_|             <<<
>>> 	                                                  <<<
>>> ===================================================== <<<
>>> [DEV] : BitTheByte (Ahmed Ezzat)                      <<<
>>> [GitHub] : https://www.github.com/bitthebyte          <<<
>>> [Version] : 8.1v                                      <<<
>>> +++++++++++++++++++++++++++++++++++++++++++++++++++++ <<<
[#] Editing this banner doesn't make you a programmer :)

"""
	if action == "START":
		print banner
	if action == "YT_SUB":
		s = "[+] Successful Logins   = {}\n[!] Failed Logins   	= {}\n[Channel ID : {}] Live subscribers count = {}\n"
		print banner
		print s.format(SUCCESS_LOGIN,FAILED_LOGIN,channel_id,live_count)
	if action == "YT_LIKE":
		s = "[+] Successful Logins = {}\n[+] Successful likes = {}\n[!] Failed Logins = {}\n[!] Failed likes = {}"
		print banner
		print s.format(SUCCESS_LOGIN,SUCCESS_ACTION,FAILED_LOGIN,FAILED_ACTION)


def YTGetSubCount(url):
	x = requests.get(url).content
	x = x.split("subscriber-count")
	x = x[1].split("</span>")
	x =  re.findall('title="(.*?)"',x[0])[0]
	return x

def main(email,password,action,YTUrl):
		global FAILED_LOGIN
		global SUCCESS_LOGIN
		global SUCCESS_ACTION
		global FAILED_ACTION

		SessionManager 	= requests.Session()
		identifier   	= G_identifier(email,SessionManager)
		logged 		= login(identifier,password,SessionManager)
		LoginYT(SessionManager)

		if not logged:
			FAILED_LOGIN += 1
			return "LOGIN_ERROR"
		else:
			SUCCESS_LOGIN += 1
		
		if action.upper() == "YT_SUB":
			try:
				if YouTubeSubscribe(YTUrl,SessionManager):
					SUCCESS_ACTION += 1
				else:
					FAILED_ACTION += 1
			except:
				return "ERR_YT_SUB"
			
		if action.upper() == "YT_LIKE":
			try:
				if YouTubeLike(YTUrl,SessionManager):
					SUCCESS_ACTION += 1
				else:
					FAILED_ACTION += 1
			except:
				return "ERR_YT_LIKE" 
while (1):
	try:
		show_status("START")
		action = ""
		while (1):
			action = raw_input("[*] Choose action (l = like , s = subscribe): ")
			if action == "l":
				action = "YT_LIKE"
				break
			if action == "s":
				action = "YT_SUB"
				break
			print "[!] Are you sure that's right ? "
		ThreadPoolSize_custom = raw_input("[*] Choose number of threads [default = {}] [press Enter to use defaults]: ".format(ThreadPoolSize))
		if ThreadPoolSize_custom != "":
			ThreadPoolSize = int(ThreadPoolSize_custom)
		os.chdir(".")
		for file in glob.glob("*.txt"):
		    print(" |_--> " + file)
		while (1):
			combo_file = raw_input("[*] Setect the name of your [Email:Password] Combo file: ")
			try:
				read_combo  = open(combo_file,"r").read()
				break
			except:
				print "[!] Check your [Email:Password] Combo file name !"
		while (1):
			ytfile = raw_input("[*] Setect the name of your [YouTube] Combo file: ")
			try:
				yt_combo  = open(ytfile,"r").read()
				break
			except:
				print "[!] Check your [YouTube] Combo file name !"
		raw_input("[+] All Done! , Press Enter to start .. ")
		for data in read_combo.split("\n"):
			if data == "":break
			email = data.split(":")[0]
			password = data.split(":")[1]
			for yturl in yt_combo.split("\n"):
				if yturl == "":break
				while(1):
					try:
						threadManager( main, [email,password,action ,yturl]  , ThreadPoolSize ,Threadtimeout)
						if action == "YT_SUB":
							live_count  = YTGetSubCount(yturl)
							channel_id = yturl.replace("https://www.youtube.com/channel/","").replace(" ","").replace("\n","")
							show_status(action,channel_id,live_count)
							break
						else:
							show_status(action)
							break
					except:
						pass
		break
	except Exception as e:
		open('loop_error.txt','w').write(str(e))
		pass
	except Exception as e:
		print "[!!!] Fatal Error : {}".format(e)
		open('error_log.txt','w').write(str(e))


print "[!] DONE"
raw_input("[!] Finished Press enter to exit")
