from lib.multi import Threader
from lib.auth import GAuth
import lib.execption as err
import lib.action as YT
import lib.cli as cli
import threading
import signal

cli.banner()
action             = cli.ask_action()
threader           = Threader(cli.ask_threads())
accounts_path      = cli.ask_accounts_file()
action_path        = cli.ask_action_file()
lock               = threading.Lock()
login_successful   = 0
login_failed       = 0
action_successful  = 0
action_faild       = 0


def Login(email,password):
	global login_successful
	global login_failed
	with lock:
		try:
			google = GAuth(email, password)
			status = google.ServiceLogin('youtube','https://www.youtube.com/signin?app=desktop&next=%2F&hl=en&action_handle_signin=true')
			login_successful += 1
			return status
		except err.LoginFailed:
			login_failed += 1
			return -1

def Like(email,password,video_id):
	global action_successful
	global action_faild
	session = Login(email, password)
	with lock:
		if session == -1:
			cli.debug("Like: [%s:%s]:UNAUTH -> %s:0" %(email,password,video_id) )
			action_faild += 1
		else:
			status = YT.like(video_id, session)
			if status == 1 : action_successful += 1
			else: action_faild += 1
			cli.debug("Like: [%s:%s]:LOGGED -> %s:%i" %(email,password,video_id,status) )

def Subscribe(email,password,channel_id):
	global action_successful
	global action_faild
	session = Login(email, password)
	with lock:
		if session == -1:
			cli.debug("Sub: [%s:%s]:UNAUTH -> %s:0" %(email,password,channel_id) )
			action_faild += 1
		else:
			status = YT.subscribe(channel_id, session)
			if status == 1 : action_successful += 1
			else: action_faild += 1
			cli.debug("Sub: [%s:%s]:LOGGED -> %s:%i" %(email,password,channel_id,status) )	

def signal_handler(sig, frame):
	cli.debug_mode = 1
	cli.show_status(login_successful, login_failed, action_successful, action_faild)
signal.signal(signal.SIGINT, signal_handler)
cli.menu_msg()

for yt_id in cli.read_action_file(action_path):
	for credentials in cli.read_acounts_file(accounts_path):
		if action == "l":
			threader.put(Like,[credentials[0],credentials[1],yt_id])
		elif action == "s":
			threader.put(Subscribe,[credentials[0],credentials[1],yt_id])
threader.finish_all()