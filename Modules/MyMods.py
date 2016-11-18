#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  MyMods.py
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
A collection of various, basic functions
"""

from time import strftime
from os import mkdir
from os.path import getmtime,dirname
try:
	mod='glob'
	from glob import glob
	mod='shutil'
	from shutil import rmtree
	mod='csv'
	import csv
except:
	print "Module '"+mod+"'not found!\nInstall the python module '"+mod+"' and try again."
	exit()

from __main__ import MYDIR

def loadArray(full_file_path):
	"""
	Opens a .csv and converts it to the array used by the bot
	"""
	with open(full_file_path,"r") as f:
		reader = csv.reader(f)
		SantaList = []
		removeHeader = reader.next()
		for row in reader:
			SantaList.append(row)
	return SantaList

def wrap(S,wide=50):
	"""
	Fancy console printing!
	Wraps a string to a certain width. Default is 50 characters.
	Breaks the lines at spaces.
	"""
	# Make a fancy box with the date and time the message was created
	breaker = ""
	timestamp = ""
	dateIn=False
	width=len(strftime("%a, %b %d; %X"))
	if width<wide:
		for i in range(wide):
			breaker=breaker+"*"
			if i == 0 or i == wide-1:
				timestamp=timestamp+"*"
			elif i<(wide-width)/2 or i>(wide-width)/2+width:
				timestamp=timestamp+" "
			elif not dateIn:
				timestamp=timestamp+strftime("%a, %b %d; %X")
				dateIn = True
			elif i==(wide-width)/2+width:
				timestamp=timestamp+" "
	else:
		timestamp=strftime("%a, %b %d; %X")
	# Actually wrap the string
	wrappedS = breaker+"\n"+timestamp+"\n"+breaker+"\n"
	if len(S)>wide-1:									# This could probably be more efficient...
		for line in S.splitlines():
			totallyDone = False
			while totallyDone==False:
				if len(line)>wide:
					if line[0] != ' ':
						line = ' '+line
					for i in range(0,wide+1):
						if i == wide:
							lineAdjust = line[:wide]+"\n "
							line = line[wide:]
						elif line[wide-i] == " ":
							lineAdjust = line[:wide-i]+"\n"
							line = line[wide-i:]
							break
					wrappedS = wrappedS + lineAdjust
				else:
					wrappedS = wrappedS + line+"\n"
					totallyDone=True
	else:
		wrappedS = wrappedS+S+"\n"
	print wrappedS

def URLSyntax(Name):
	"""
	Convert to URL-friendly syntax
	"""
	Name=Name.replace("%", "%25")
	Name=Name.replace("`", "%60")
	Name=Name.replace("@", "%40")
	Name=Name.replace("#", "%23")
	Name=Name.replace("$", "%24")
	Name=Name.replace(" ", "%20")
	Name=Name.replace("^", "%5E")
	Name=Name.replace("&", "%26")
	Name=Name.replace("=", "%3D")
	Name=Name.replace("+", "%2B")
	Name=Name.replace("[", "%5B")
	Name=Name.replace("{", "%7B")
	Name=Name.replace("]", "%5D")
	Name=Name.replace("}", "%7D")
	Name=Name.replace("\n","%0A")
	Name=Name.replace("\\","%5C")
	Name=Name.replace("|", "%7C")
	Name=Name.replace(";", "%3B")
	Name=Name.replace(":", "%3A")
	Name=Name.replace("'", "%27")
	Name=Name.replace(",", "%2C")
	Name=Name.replace("/", "%2F")
	Name=Name.replace("?", "%3F")
	return Name

"""
From Reddit's Code at
https://github.com/reddit/reddit/blob/master/r2/r2/lib/unicode.py
Brought to my attention by RemindMeBot
"""

def _force_unicode(text):
	if text == None:
		return u''
	if isinstance(text, unicode):
		return text
	try:
		text = unicode(text, 'utf-8')
	except UnicodeDecodeError:
		text = unicode(text, 'latin1')
	except TypeError:
		text = unicode(text)
	return text

def force_utf8(text):
	return str(_force_unicode(text).encode('utf8'))
