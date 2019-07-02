import requests
import json
import re
try:
	import urllib.parse as urlparse
except:
	import urlparse

def subscribe(channel_id,session):
		xsrf = (re.findall("XSRF_TOKEN\W*(.*)=", session.get("https://www.youtube.com/channel/%s" % channel_id).content , re.IGNORECASE)[0]).split('"')[0]
		data = [
		  ('sej', '{"clickTrackingParams":"","commandMetadata":{"webCommandMetadata":{"url":"/service_ajax","sendPost":true}},"subscribeEndpoint":{"channelIds":["'+channel_id+'"],"params":"EgIIAg%3D%3D"}}'),
		  ('session_token', xsrf+"=="),
		]
		response = session.post('https://www.youtube.com/service_ajax?name=subscribeEndpoint', data=data)
		check_state = json.loads(response.content)['code']
		if check_state == "SUCCESS":
			return 1
		else:
			return 0

def like(video_id,session):
	xsrf = (re.findall("XSRF_TOKEN\W*(.*)=", session.get("https://youtube.com/watch?v=%s" % video_id).content , re.IGNORECASE)[0]).split('"')[0]
	data = [
	  ('sej', '{"clickTrackingParams":"","commandMetadata":{"webCommandMetadata":{"url":"/service_ajax","sendPost":true}},"likeEndpoint":{"status":"LIKE","target":{"videoId":"'+video_id+'"}}}'),
	  ('session_token',xsrf + "=="),
	]
	response = session.post('https://www.youtube.com/service_ajax?name=likeEndpoint', data=data)
	if "Added to Liked videos" in response.content:
		return 1
	else:
		return 0