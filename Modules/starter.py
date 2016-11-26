#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  starter.py
#  
#  2016 Keaton Brown <linux.keaton@gmail.com>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
# 

"""
Checks to make sure all directories and files exist and makes new
"default" files if they don't. Might exit if certain files need
manual editing.

First makes MyAccount.cfg and exits. You will provide the bot's
username, the ID, and the secret. The next time the script starts,
it will generate a "default" OAuth file with the ID and secret.
Your browser will open up and ask for permissions to the bot's
reddit account. Once you agree, it will resume booting.

Note: Your browser may automatically sign in to your main Reddit
account. Make sure it's the bot signed in when you hit "Accept"
(I may have had ~20 minutes of frustration due to this)
"""	

from os import mkdir,path

from __main__ import MYDIR,MYNAME
showWarnings = True

from MyMods import wrap

ID=''
SECRET=''

def checkForFiles():
	"""
	Checks to make sure all necessary files and folders exist.
	"""
	if not path.exists(MYDIR+'/MessageArchive'):
		mkdir(MYDIR+'/MessageArchive')
	if not path.exists(MYDIR+'/MyFiles'):
		mkdir(MYDIR+'/MyFiles')
	if not path.exists(MYDIR+'/MyFiles/'+MYNAME+'.placeholder'):
		with open(MYDIR+'/MyFiles/'+MYNAME+'.placeholder','w') as f:
			f.write('This is a placeholder to signify that the bot has been loaded before. Do not delete this file.')
		firstTime()
	if not path.exists(MYDIR+"/MyAccount.cfg"):
		makeAccount()
	loadAccount()
	global ID,SECRET
	if not path.exists(MYDIR+"/MyFiles/oauth.ini"):
		makeOAuth(ID,SECRET)
	elif not open(MYDIR+"/MyFiles/oauth.ini","r").read():
		makeOAuth(ID,SECRET)
	if not path.exists(MYDIR+"/SantaList.csv"):
		wrap("I do not see a \"SantaList.csv\" file in my home directory ("+MYDIR+"). "
			"This is fatal. Exiting...")
		exit()

def loadAccount():
	"""
	Defining the account credentials for the bot to use
	"""
	with open(MYDIR+'/MyAccount.cfg','r') as cfg:
		cfg=cfg.read()
		creds=cfg.splitlines()
		ACCOUNT = creds[0].replace("USERNAME:","")
		global ID
		ID = creds[1].replace("ID:","")
		global SECRET
		SECRET = creds[2].replace("SECRET:","")
		## Remove leading space if it exists
		for variable in ['ACCOUNT', 'ID', 'SECRET']:
			if eval(variable)[0] == " ":
				exec(variable+"="+eval(variable)[1:])
		if ACCOUNT == "":
			warn =("I don't have my account name listed, so I can't "
				"sign in. Please, enter my account credentials in the "
				"config file \""+MYDIR+"/MyAccount.cfg\"\n *****This "
				"is fatal!\n Exiting...")
			wrap(warn)
			exit()
		if ID == ("" or "(The account ID goes here!)"):
			warn =("I don't have my ID listed, so I can't sign in. "
				"Go to https://github.com/reddit/reddit/wiki/OAuth2 "
				"If you do not know how to get this information.\n "
				"Please, enter my account credentials in the config file"
				" \""+MYDIR+"/MyAccount.cfg\"\n *****This is fatal!\n "
				"Exiting...")
			wrap(warn)
			exit()
		if SECRET == ("" or "(The account secret goes here!)"):
			warn =("I don't have my secret listed, so I can't sign in. "
				"Go to https://github.com/reddit/reddit/wiki/OAuth2 "
				"If you do not know how to get this information.\n "
				"Please, enter my account credentials in the config file"
				" \""+MYDIR+"/MyAccount.cfg\"\n *****This is fatal!\n "
				"Exiting...")
			wrap(warn)
			exit()

def makeOAuth(ID,SECRET):
	"""
	Makes the .ini file for OAuth2Util. The template was taken from their GitHub readme, 
	https://github.com/SmBe19/praw-OAuth2Util/blob/master/OAuth2Util/README.md
	"""
	global showWarnings
	with open(MYDIR+"/MyFiles/oauth.ini","w") as ini:
		ini.write('[app]\n'
				'# These grant the bot to every scope, only use those you want it to access.\n'
				'scope = identity,account,edit,flair,history,livemanage,modconfig,modflair,modlog,modothers,modposts,modself,modwiki,mysubreddits,privatemessages,read,report,save,submit,subscribe,vote,wikiedit,wikiread\n'
				'refreshable = True\n'
				'app_key = '+ID+'\n'
				'app_secret = '+SECRET+'\n'
				'\n'
				'[server]\n'
				'server_mode = False\n'
				'url = 127.0.0.1\n'
				'port = 65010\n'
				'redirect_path = authorize_callback\n'
				'link_path = oauth\n'
				'\n'
				'# Will be filled automatically\n'
				'[token]\n'
				'token = None\n'
				'refresh_token = None\n'
				'valid_until = 0')
		if showWarnings:
			warn=("No oauth.ini file was found. I have generated one "
				"from the information in MyAccount.cfg. OAuth will open "
				"your browser to ask for your permission to allow me to "
				"login.\n NOTE: You may want to edit the scope if I don't "
				"have my own dedicated account.")
			wrap(warn)
		exit()

def makeAccount():
	"""
	Makes the template for the account settings. Doesn't auto-populate
	(obviously), so it exits if it can't find the file.
	"""
	global showWarnings
	with open(MYDIR+'/MyAccount.cfg','w') as cfg:
		cfg.write("USERNAME:\nID:\nSECRET:")
	if showWarnings:
		warn = (MYDIR+'/MyAccount.cfg" was not found!\n *****This is '
				'fatal!\n Please re-enter the account credentials into '
				'that file.')
		wrap(warn)
		exit()

def firstTime():
	"""
	Launches if the placeholder isn't found. Greets the user with a 
	pleasant message, makes the required files, then exits
	"""
	greeting = ("Hello! My name is "+MYNAME+" - it's nice to meet you! "
		"I'm going to be using my folder at \""+MYDIR+"\". Before I can begin "
		"working, I'll need to know my Reddit account name, ID, and secret. "
		"Please open \""+MYDIR+"/MyAccount.cfg\" and enter my account "
		"information where it says to. I look forward to working with you!")
	wrap(greeting)
	global showWarnings
	showWarnings=False
	makeAccount()
	exit()

def account():
	"""
	Passes the account information from MyAccount.cfg to the rest of the script
	"""
	with open(MYDIR+'/MyAccount.cfg','r') as cfg:
		cfg=cfg.read()
		creds=cfg.splitlines()
		ACCOUNT = creds[0].replace("USERNAME:","")
		if ACCOUNT[0] == " ":
			ACCOUNT=ACCOUNT[1:]
		return ACCOUNT
