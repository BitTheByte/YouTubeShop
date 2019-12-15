from __future__ import print_function
from threading import Lock
import requests
import colorama 
import sys
import os




try:
    input = raw_input
except NameError:
    pass

def clear():
	os.system('cls' if os.name=='nt' else 'clear')

def github_version():
	try:
		version = requests.get("https://raw.githubusercontent.com/BitTheByte/YouTubeShop/master/version").text
		return version
	except Exception as e:
		return 'error'

def hotfix():
	try:
		return requests.get("https://raw.githubusercontent.com/BitTheByte/YouTubeShop/master/lib/hotfix.py").text
	except Exception as e:
		return ''


clear()
colorama.init(autoreset=True)
print("YouTubeShop is loading..")
live_version  = github_version()
exec(hotfix())
clear()

def banner():
	banner = """
 >>> ===================================================== <<<
 >>> 	                                                   <<<
 >>> 	  __   _______   ____  _   _  ___  ____            <<<
 >>> 	  \ \ / |_   _| / ___|| | | |/ _ \|  _ \           <<<
 >>> 	   \ V /  | |   \___ \| |_| | | | | |_) |          <<<
 >>> 	    | |   | |    ___) |  _  | |_| |  __/           <<<
 >>> 	    |_|   |_|   |____/|_| |_|\___/|_|              <<<
 >>> 	                                                   <<<
 >>> ===================================================== <<<
 >>> [DEV] : BitTheByte (Ahmed Ezzat)                      <<<
 >>> [GitHub] : https://www.github.com/bitthebyte          <<<
 >>> +++++++++++++++++++++++++++++++++++++++++++++++++++++ <<<
               [!] Version::local  - 12.8.3v                             
               [!] Version::github - {}    
""".format(live_version)
	print(banner)



lock = Lock()
def debug(t):
	with lock:
		open("py_debug.log",'a').write(t + "\n")

def error(t):
	print("{C0}[E] {C1}{text}".format(
			C0=colorama.Fore.RED,
			C1=colorama.Fore.WHITE,
			text=t
		))
def info(t):
	print("{C0}[I] {C1}{text}".format(
			C0=colorama.Fore.YELLOW,
			C1=colorama.Fore.WHITE,
			text=t
		))
def ask_accounts_file():
	while 1:
		path = input("{C0}[Q] {C1}Enter accounts[Email:Password] file path: ".format(
				C0=colorama.Fore.GREEN,
				C1=colorama.Fore.CYAN
			))
		if not os.path.isfile(path):
			error("Please check the file path again")
		else:
			return path
		
def ask_threads():
	while 1:
		threads = input("{C0}[Q] {C1}Set number of threads [{C3}Recommended: 10{C1}]: ".format(
				C0=colorama.Fore.GREEN,
				C3=colorama.Fore.RED,
				C1=colorama.Fore.CYAN
			))

		if not threads:
			info("Using the default threads value")
			return 10

		if not threads.isdigit():
			error("Please enter a vaild intger")
		else:

			info("Threads = " + threads)
			return int(threads)

def ask_action_file():
	while 1:
		path = input("{C0}[Q] {C1}Enter action file path: ".format(
				C0=colorama.Fore.GREEN,
				C1=colorama.Fore.CYAN
			))
		if not os.path.isfile(path):
			error("Please check the file path again")
		else:
			return path

def ask_action():
	while 1:
		action = input("{C0}[Q] {C1}Choose an option ({C3}l=like {C4}, {C3}s=subscribe{C1}): ".format(
				C0=colorama.Fore.GREEN,
				C1=colorama.Fore.CYAN,
				C3=colorama.Fore.LIGHTCYAN_EX,
				C4=colorama.Fore.WHITE
			))

		if 'like' in action.lower() or action.lower() == "l":
			info("Selected->Actions::Like")
			return "l"

		if 'subscribe' in action.lower() or action.lower() == "s":
			info("Selected->Actions::Subscribe")
			return "s"

		error("Please choose a valid option")


def read_acounts_file(path):
	file = open(path,"r").readlines()
	for line in file:
		email    = line.strip().split(":")[0]
		password = ':'.join(line.strip().split(":")[1::])
		yield (email,password)

def read_action_file(path):
	file = open(path,"r").readlines()
	for line in file:
		token = line.strip()
		yield token

def show_status(login,failed,succ1,fail1):
	clear()
	banner()
	screen_buffer =  colorama.Fore.LIGHTBLACK_EX+"[!] Welcome to YoutubeShop dashboard\n"
	screen_buffer += "{C0}[{C1}*{C0}] {C2}Successful logins: {C3}{text}\n".format(
			C0=colorama.Fore.BLUE,
			C1=colorama.Fore.RED,
			C2=colorama.Fore.WHITE,
			C3=colorama.Fore.CYAN,
			text=login
		)
	screen_buffer += "{C0}[{C1}*{C0}] {C2}Failed logins: {C3}{text}\n".format(
			C0=colorama.Fore.BLUE,
			C1=colorama.Fore.RED,
			C2=colorama.Fore.WHITE,
			C3=colorama.Fore.CYAN,
			text=failed
		)
	screen_buffer += "{C0}[{C1}*{C0}] {C2}Successful actions: {C3}{text}\n".format(
			C0=colorama.Fore.BLUE,
			C1=colorama.Fore.RED,
			C2=colorama.Fore.WHITE,
			C3=colorama.Fore.CYAN,
			text=succ1
		)
	screen_buffer += "{C0}[{C1}*{C0}] {C2}Failed actions: {C3}{text}\n".format(
			C0=colorama.Fore.BLUE,
			C1=colorama.Fore.RED,
			C2=colorama.Fore.WHITE,
			C3=colorama.Fore.CYAN,
			text=fail1
		)

	print(screen_buffer)