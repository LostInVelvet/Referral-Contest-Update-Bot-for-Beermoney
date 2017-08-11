#from __future__ import print_function
from datetime import datetime
import praw
import time
import sys

# ----------------------------------------------------------------------------
#			    	 Check If The Winner Is Allowed To Win
def Check_If_User_Can_Win(winner, REDDIT):
	def User_Exists():
		try: 
			userCreated = REDDIT.redditor(winner).created_utc
		
		# If there's an error for any reason, we will take note of it and continue on.	
		except Exception as e:
#			print("Error in Check_If_User_Can_Win() -> User_Exists() : " + str(e), file=sys.stderr)
			pass
			return False
			
		return True

	def User_Is_Not_Banned():
		# Check if user is in banned_users.txt
		bannedUsersFile = open("banned_users.txt", "r")
		bannedUsersList = bannedUsersFile.read().splitlines()
		bannedUsersFile.close()
		
		for user in bannedUsersList:
			if(winner.lower() == user.lower()):
				return False
		
		
		# Check if user is banned by the subreddit
		for user in REDDIT.subreddit('beermoney').banned():
			if(user == winner):
				return False
		return True
	
	
	# User account must be at least 30 days old to participate
	def User_Account_Is_Aged():
		userCreated = REDDIT.redditor(winner).created_utc
		
		t = time.strftime("%x", time.localtime(userCreated))
		timeAccountCreated = datetime.strptime(str(t), "%x").date()
		currentTime = datetime.strptime(time.strftime("%x"), "%x").date()
		
		
		if((currentTime - timeAccountCreated).days > 30):
			return True
		else:
			return False
		
		
	# Check if the user has 20 posts	
	def User_Has_Enough_Posts():
		posts = 0
		
		# Get the recent comments
		for comment in REDDIT.redditor(winner).comments.new(limit=20):
			posts += 1
		
		# Get the recent submissions
		for submission in REDDIT.redditor(winner).submissions.new(limit=(20-posts)):
			posts += 1
			
		# Make sure there are 20.
		if(posts == 20):
			return True
		else:
			return False
			
	
	# Check if user has at least 2 posts in the last 2 weeks
	def User_Has_Recent_Posts():
		recentPosts = 0
		currentTime = datetime.strptime(time.strftime("%x"), "%x").date()
		
		
		for comment in REDDIT.redditor(winner).comments.new(limit=2):
			t = time.strftime("%x", time.localtime(comment.created))
			timeCreated = datetime.strptime(str(t), "%x").date()
			
			if((currentTime - timeCreated).days <= 14):
				recentPosts += 1
			else:
				break
				
				
		for submission in REDDIT.redditor(winner).submissions.new(limit=(2-recentPosts)):
			t = time.strftime("%x", time.localtime(submission.created))
			timeCreated = datetime.strptime(str(t), "%x").date()
			
			if((currentTime - timeCreated).days <= 14):
				recentPosts += 1
			else:
				break
		
		
		# Make sure there are 2 recent posts.
		if(recentPosts == 2):
			return True
		else:
			return False
		
	exists = User_Exists()
	if(exists):
		notBanned = User_Is_Not_Banned()
		
		if(notBanned):
			oldEnough = User_Account_Is_Aged()
			
			if(oldEnough):
				enoughPosts = User_Has_Enough_Posts()
				
				if(enoughPosts):
					recentPosts = User_Has_Recent_Posts()
					if(recentPosts == False):
						invalidWinner = [winner, 4]
				else:
					invalidWinner = [winner, 3]
			else:
				invalidWinner = [winner, 2]
		else:
			invalidWinner = [winner, 1]
	else:
		invalidWinner = [winner, 0]
		
	
	if(exists and notBanned and enoughPosts and recentPosts):
		print "valid"
		return [True, invalidWinner]
	else:
		print "invalid"
		return [False, invalidWinner]
	
#                End of Check If The Winner Is Allowed To Win
# ----------------------------------------------------------------------------
