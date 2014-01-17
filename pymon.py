#pymon.py
#A python script to check the status of a web page
#Joe McManus
#jospehmc@cmu.edu 

#Check to see if this is python3
import sys
import platform
if platform.python_version() < "3.0.0": 
        print("ERROR: Python 3.0 or greater is required for this to run. Sorry ")
        sys.exit()


import urllib.request
import re
import time
import smtplib
import socket
from email.mime.text import MIMEText


def msgHandler(message, exitCode):
	if exitCode != 0:
		currentTime=str(time.asctime(time.localtime(time.time())))
		print("ERROR: " + message + " " + currentTime )	
		msgText = "url: " + message + "\n" + "Script: " + sys.argv[0] + "\nMachine: " + socket.gethostname() 
		msg = MIMEText(msgText)
		msg['To'] = "joe@example.com"
		msg['From'] = "joe@example.com"
		msg['Subject'] = "ERROR: " + message + " " + currentTime
		try:
			server=smtplib.SMTP("smtp.example.com")
		except: 
			print("ERROR: Unable to connect to smtp server.")
			sys.exit()
		server.sendmail(msg['To'], msg['From'], msg.as_string())
		server.quit()
		sys.exit()
	else: 
		print("OK: " + message)
		
#Uncomment if you need to use a proxy
#proxy_handler = urllib.request.ProxyHandler({'https': 'https://proxy.foo.org:3128/'})
#proxy_auth_handler = urllib.request.ProxyBasicAuthHandler()

#Enter the URL you are monitoring
urlToWatch="http://www.google.com"

#Test to see if the server is responding
try: 
	fh = urllib.request.urlopen(urlToWatch) 
except:
	msgHandler( urlToWatch + " did not respond", 1)

#Look for a string in the first 5000 Characters
pageData = str(fh.read(5000))
searchString = "Lycos"

if pageData.find(searchString) != -1: 
	msgHandler("Page OK", 0)
else: 
	msgHandler(urlToWatch + " up but content not what is expected.", 1)
