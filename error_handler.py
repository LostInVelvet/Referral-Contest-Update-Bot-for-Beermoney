from myconfig import *
import codecs
import errno
import os
import time

# If something goes wrong for some reason, this will send a whisper to the /r/beermoney mods and to me.
def Send_Error_Message(REDDIT, msg):
	error_msg = "Hey, it's your bot here. I handle the referral link contest. I had this error message pop up:\n\n> " + msg + "\n\nMy associated subreddit: /r/beermoney"
	REDDIT.redditor(creator).message("Error Message Notification", error_msg)
	
	error_msg += "\n\nI have notified /u/" + creator + "If you don't hear back within a week, please send a friendly reminder about this error."
	REDDIT.redditor(message_user).message("Error Message Notification", error_msg)


	# Save the Errors to a file
	todaysDate = time.strftime("%x")
	todaysDate = todaysDate.replace("/"  , "-")

	file1 = "Errors/Error" + todaysDate
	with codecs.open(file1, 'a', encoding='utf8') as f:
		f.write(msg + "\n\n-------------------------------\n\n")
	f.close()

