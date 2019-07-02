from __future__ import print_function
import colorama 
import os

try:
    input = raw_input
except NameError:
    pass
debug_mode = 0
colorama.init(autoreset=True)

def banner():
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
>>> [Version] : 12.8.2v                                   <<<
>>> +++++++++++++++++++++++++++++++++++++++++++++++++++++ <<<
[#] Editing this banner doesn't make you a programmer :)
"""
	print(banner)

def debug(t):
	if debug_mode != 0:
		print("{C0}[DEBUG-MODE] {C1}{text}\n".format(
				C0=colorama.Fore.LIGHTRED_EX,
				C1=colorama.Fore.LIGHTBLACK_EX,
				text=t
			),end='')

def error(t):
	print("{C0}[E] {C1}{text}".format(
			C0=colorama.Fore.RED,
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
		if not threads.isdigit():
			error("Please enter a vaild intger")
		else:
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
		if (action.lower()).strip() != "l" and (action.lower()).strip() != 's':
			error("Please choose a valid option")
		else:
			return action.lower()

def read_acounts_file(path):
	file = open(path,"r").readlines()
	for line in file:
		email,password = line.strip().split(":")
		yield (email,password)

def read_action_file(path):
	file = open(path,"r").readlines()
	for line in file:
		token = line.strip()
		yield token

def show_status(login,failed,succ1,fail1):
	os.system("cls")
	banner()
	print(colorama.Fore.LIGHTBLACK_EX+"[!] Welcome to debug mode press [CTRL+C] again to update the counters")
	print("{C0}[{C1}*{C0}] {C2}Successful logins: {C3}{text}".format(
			C0=colorama.Fore.BLUE,
			C1=colorama.Fore.RED,
			C2=colorama.Fore.WHITE,
			C3=colorama.Fore.CYAN,
			text=login
		))
	print("{C0}[{C1}*{C0}] {C2}Failed logins: {C3}{text}".format(
			C0=colorama.Fore.BLUE,
			C1=colorama.Fore.RED,
			C2=colorama.Fore.WHITE,
			C3=colorama.Fore.CYAN,
			text=failed
		))
	print("{C0}[{C1}*{C0}] {C2}Successful actions: {C3}{text}".format(
			C0=colorama.Fore.BLUE,
			C1=colorama.Fore.RED,
			C2=colorama.Fore.WHITE,
			C3=colorama.Fore.CYAN,
			text=succ1
		))
	print("{C0}[{C1}*{C0}] {C2}Failed actions: {C3}{text}\n".format(
			C0=colorama.Fore.BLUE,
			C1=colorama.Fore.RED,
			C2=colorama.Fore.WHITE,
			C3=colorama.Fore.CYAN,
			text=fail1
		))

def menu_msg():
	input("{C0}[{C1}*{C0}] {C2}Press enter to start .. ".format(
			C0=colorama.Fore.BLUE,
			C1=colorama.Fore.RED,
			C2=colorama.Fore.WHITE
		))

	print("{C0}[!] Working.. Press {C1}[CTRL + C]{C0} to access the debug mode.".format(
			C0=colorama.Fore.CYAN,
			C1=colorama.Fore.YELLOW
		))