from myconfig import *
from operator import itemgetter
import praw

# ----------------------------------------------------------------------------
#                                    Login

REDDIT = praw.Reddit(	client_id=reddit_client_id,
						client_secret = reddit_client_secret,
						user_agent = reddit_user_agent,
						username = reddit_username,
						password = reddit_password)
							
#                                 End of Login
# ----------------------------------------------------------------------------



# ----------------------------------------------------------------------------
#                     Check If There Are Multiple Entries
def Check_For_Multiple_Entries(entries):
	duplicates = []
	numDups = 0
	
	
	for i in range(len(sites_with_refs)):

		entries = sorted(entries, key=itemgetter(i))
		indices = []
	
		for index, value in enumerate(entries):
			
			
			if(index > 0):
				if(value[i] == entries[index-1][i]):
					duplicates.append([entries[index-1], value])
					
					# If the values are the same, delete the duplicate entry.
					if(value == entries[index-1]):
						indices.append(index-1)
						numDups += 1
										
							
					# If the values aren't the same, delete both of them.
					else:
						indices.append(index-1)
						indices.append(index)
						numDups = 0
				else:
					# If the user has more than 3 entries, delete the original entry as well
					if(numDups >= 3):
						indices.append(index-1)
					numDups = 0
					
		
		# Remove any duplicates from indices[]
		for indIndex, x in enumerate(indices):
			if(indIndex > 0):
				if(indices[indIndex] == indices[indIndex-1]):
					del indices[indIndex]

		# Delete all the duplicates we found in this pass
		for i in reversed(indices):
			del entries[i]


	msgContent = [[], [], []]
	
	for dup in duplicates:
		# If usernames match
		if(dup[0][0] == dup[1][0]):
			# If the content is the same
			if(dup[0] == dup[1]):
				msgContent[0].append(dup[0][0])
			# Else if the content is different
			else:
				msgContent[1].append([dup[0], dup[1]])
				
		# Else if the usernames don't match
		else:
			msgContent[2].append([dup[0], dup[1]])



	# Format it nicely for sending in a reddit message
	bar = " | "
	blankLine = "\n\n&nbsp;\n\n"
	bold = "**"
	cnt = 1
	msg = ""
	nl = "\n\n"
	oneLine = "\n"
	solidLine = "\n\n------\n\n"
	tableFormat = ":--|:--"
	usr = "/u/"
	reason = [	"Users who had multiple of the same entry:",
				"Usernames that were used multiple times but the ref links don't match up:",
				"Duplicate ref links found with different usernames:"
			 ]
	
	for msgIndex, msgContentSection in enumerate(msgContent):
		if(msgContentSection != []):
			msg += bold + reason[msgIndex] + bold + nl
			
			for entryIndex, entry in enumerate(msgContentSection):
				if(msgIndex == 0):
					if(entryIndex + 1 < len(msgContentSection) and entry == msgContentSection[entryIndex+1]):
						cnt += 1
					else:
						msg += nl + usr + str(entry)
						
						if(cnt > 1):
							msg += " had " + str(cnt) + " entries."
						cnt = 1
					
				else:
					for x, field in enumerate(entry[0]):
						if(x == 0):
							msg += usr + entry[0][x] + bar + usr + entry[1][x] + oneLine
							msg += tableFormat + oneLine
						else:
							msg += entry[0][x] + bar + entry[1][x] + oneLine
				
						
				if(msgIndex > 0 and entryIndex < len(entry)):
					msg += blankLine
			
			msg += blankLine


	# Message the contents
	error_msg = "Hey, it's your bot here. I handle the referral link contest. I found some duplicate entries this week:" + blankLine + msg + "My associated subreddit: /r/beermoney"
	REDDIT.redditor(message_user).message("Duplicate Entries Found", error_msg)


	return entries
		
#                 End of  Check If There Are Multiple Entries
# ----------------------------------------------------------------------------
