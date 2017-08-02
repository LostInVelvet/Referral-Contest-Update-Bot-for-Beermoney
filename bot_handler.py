#!/usr/bin/python
from datetime import datetime
from myconfig import *
from reddit_bot import *
import codecs
import time
import os
import sys

dir_path = os.path.dirname(os.path.abspath(__file__))
os.chdir(dir_path)

# Make sure we have an "Errors" folder, and make one if we don't
dirErrorFolder = "Errors"

try:
	os.makedirs(dirErrorFolder)
except OSError as exception:
	if exception.errno != errno.EEXIST:
		raise
		Send_Error_Message(REDDIT, "Error making Error Backup directory")

sys.stderr = open('Errors/CriticalErrors.txt', 'a')


date_format = "%m/%d/%Y"

file1 = open("last_updated.txt", "r")
l = file1.read()
t = time.strftime(date_format)

lastUpdated = datetime.strptime(l[0:10], date_format).date()
todaysDate = datetime.strptime(t, date_format).date()

# Only run the program if it's been more than 5 days and it's the scheduled day and time to run.
if(todaysDate - lastUpdated).days > 5:
	if(datetime.today().weekday() == day_to_update and datetime.today().hour >= time_to_update):
		Run_It()

	with codecs.open("last_updated.txt", 'w+', encoding='utf8') as f:
		f.write(t)
	f.close()

sys.stderr.close()
#sys.stderr = sys.__stderr__
