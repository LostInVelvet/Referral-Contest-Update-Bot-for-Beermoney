# ----------------------------------------------------------------------------
#			    	 Check If The Winner Is Allowed To Win
def Check_If_User_Can_Win(winner):
	def User_Exists():
		return True
	def User_Has_Enough_Posts():
		return True
	def User_Has_Recent_Posts():
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
#		for user in REDDIT.subreddit('beermoney').banned():
#			if(user == winner):
#				return False
		return True

	exists = User_Exists()
	enoughPosts = User_Has_Enough_Posts()
	recentPosts = User_Has_Recent_Posts()
	notBanned = User_Is_Not_Banned()
	
	if(exists and enoughPosts and recentPosts and notBanned):
		return True
	else:
		return False

#                End of Check If The Winner Is Allowed To Win
# ----------------------------------------------------------------------------
