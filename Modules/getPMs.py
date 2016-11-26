#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  getPMs.py
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
Reads private messages sent to the bot, analyzes them, then responds accordingly.
The important parts of this code were derived from /u/RemindMeBotWrangler's remindmebot_search.py
https://github.com/SIlver--/remindmebot-reddit/blob/master/remindmebot_search.py
"""

from __main__ import MYDIR,reddit,PMLink,botFlair,SantaList
from MyMods import *

from re import search,finditer
from time import sleep,time
import praw

def readMail(mail):
	"""
	Gets unread messages, parses them for the correct syntax, then
	sends mail accordingly to the appropriate parties.
	"""
	Body = force_utf8(mail.body) ## Convert message to utf8 just in case
	sender = str(force_utf8(mail.author)) ## Same deal
	report = search('(?i)report:(.*)',Body)
	## Check if the report call was used.
	## Sends modmail with copy of message if yes
	if report:
		return reportMessage(report.group(1),Body,mail)
	try: # non-conformance error prevention at it's finest.
		direction = search('(?i)(to:|from:) santa.*',Body).group(1)
		message = Body[finditer('(?im)message:',Body).next().end():]
	except:
		ID = str(int(time()))[:-2]
		with open(MYDIR+'/MessageArchive/'+ID+'.txt','w') as msg:
			msg.write('from: /u/'+sender+"\n\n****\n"+Body)
		msg=("Hello /u/"+sender+"!\n\nI was unable to read your message. "
			"This means the formatting of your message was off somehow. "
			"The supplied links below have the proper formatting already "
			"set up, so try using one of those if you did not before. "
			"Message the /r/ClosetSanta mods if you feel there is a problem. "
			"Include this ID number in your message: "+ID+botFlair)
		mail.reply(msg)
		wrap("Non-conformant mail message detected. Saved as "+ID+".txt. /u/"+sender+" notified.")
		return False ## Skips the rest of this function
	if message[0] == ' ': ## Removes leading space if it exists
		message = message[1:]
	if sender not in (x[0] for x in SantaList):
		ID = str(int(time()))[:-2] ##Assigns unique ID based on epoch time
		with open(MYDIR+'/MessageArchive/'+ID+'.txt','w') as msg: ## Saves to unique file
			msg.write('from: /u/'+sender+"\n\n****\n"+message)
		msg=("Hello /u/"+sender+"!\n\nI was unable to find your account in my "
			"list of participants for this year's Closet Santa. This means you "
			"may be using the wrong account, or you may not have signed up. "
			"Message the /r/ClosetSanta mods if you feel there is a problem. "
			"Include this ID number in your message: "+ID+botFlair)
		mail.reply(msg)
		wrap("Message received from user not in SantaList.csv. Saved as "+ID+".txt. Maybe the SantaList.csv was updated and I need to be restarted?")
		return False
	recipient,anonMail = lookupRecipient(direction.lower(),mail) ## Find the recipient account and starts building the anonymous message
	anonMail = anonMail+message
	ID = str(int(time()))[:-2]
	with open(MYDIR+'/MessageArchive/'+ID+'.txt','w') as msg:
		msg.write('from: /u/'+sender+"\n\nto: /u/"+recipient+"\n\n****\n"+message)
	## Build message and add report link
	anonMail = "Hello /u/"+recipient+"!\n\n"+anonMail+"\n****\nIf you feel the need to report this message, [click here]("+PMLink+URLSyntax('Report:'+ID+"\n\nReason: ")+")"+botFlair
	reddit.send_message(recipient,"Closet Santa message",anonMail,captcha=None)
	sleep(1) ## Ensures a different ID for each message, although it's probably not necessary.
	return True

def reportMessage(ID,Body,mail):
	try:
		with open(MYDIR+"/MessageArchive/"+ID+".txt",'r') as msg:
			msg=msg.read()
			reason = Body[finditer('(?im)reason:',Body).next().end():]
			msg =("I have received a report about the following interaction:\n\n"+msg+
					"\n****\nThe recipient gave the following reason:"+str(reason))
			wrap(msg)
			reddit.send_message("/r/ClosetSanta","Reported interaction",msg,captcha=None)
			return True
	except: ## This means that they messed with the ID number, or the archived message was deleted.
		newID = str(int(time()))[:-2]
		with open(MYDIR+'/MessageArchive/'+newID+'.txt','w') as msg:
			msg.write('from: /u/'+str(force_utf8(mail.author))+"\n\n****\n"+Body)
		msg = "I received a report from /u/"+str(force_utf8(mail.author))+" about the message ID "+ID+", but that ID is not in my message archive. The full report message was saved as "+newID+".txt"
		reddit.send_message("/r/ClosetSanta","Reported interaction",msg,captcha=None)
		wrap("Non-conformant report message detected- Reported message not found. Report was saved as "+newID+".txt")
		return False

def lookupRecipient(direction,mail):
	sender = str(force_utf8(mail.author))
	if direction.lower() == "to:":
		#Look up user's Closet Santa (column 1 of csv)
		recipient = [santa for (user,santa) in SantaList if user == sender][0]
		anonMail = "You have received a message from your gift recipient!\n****\n"
		return recipient,anonMail
	else:
		#Look up user's recipient (column 0 of csv)
		recipient = [user for (user,santa) in SantaList if santa == sender][0]
		anonMail = "You have received a message from your Closet Santa!\n****\n"
		return recipient,anonMail
		
def getPMs():
	for mail in reddit.get_unread(unset_has_mail=True, update_user=True, limit=None):
		success = readMail(mail)
		if success:
			mail.reply('Your message was successfully sent!'+botFlair)
		mail.mark_as_read()
