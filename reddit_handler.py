from error_handler import *
from get_domain import *
from myconfig import *
import codecs
import errno
import os
import praw
import re
import time


# ----------------------------------------------------------------------------
#                                    Login

REDDIT = praw.Reddit(	client_id=reddit_client_id,
						client_secret = reddit_client_secret,
						user_agent = reddit_user_agent,
						username = reddit_username,
						password = reddit_password)
							
#                                 End of Login
# ----------------------------------------------------------------------------


commonBeermoneySites = REDDIT.submission(id=common_beermoney_id)
refContestWinners    = REDDIT.submission(id=ref_winners_id)
	
commonBeermoneySitesPost = commonBeermoneySites.selftext
refContestWinnersPost    = refContestWinners.selftext


# ----------------------------------------------------------------------------
#                                 Get Domains
def Get_Domains_From_Post():
	# Get the indices and domains of every the url in the post. Add them into an array.
	# Assumption: 	All urls start with "http". This will include https, but it will ignore anything starting with www.
	#             	For reddit purposes, all linked text should start with "http" in order to make clickable text
	linkLocations = []

	for i in re.finditer("http", commonBeermoneySitesPost):
		endBracketLocation = commonBeermoneySitesPost.index(')', i.start())
		url = commonBeermoneySitesPost[i.start():endBracketLocation]
		domain = Get_Domain_From_Url(url)
		
		if domain != False and any(domain.lower() == j.lower() for j in sites_with_refs):
			if not any(domain.lower() in k[2].lower() for k in linkLocations):
				linkLocations.append([i.start(), endBracketLocation, domain])

	return linkLocations

#                              End of Get Domains
# ----------------------------------------------------------------------------



# ----------------------------------------------------------------------------
#                                 Post Editor

def Handle_Reddit(linkLocations, ref_contest_winners):
	Make_Backups()

	# Recreate the posts.
	# Assumptions: 	All links are properly started with "http" or "https". Otherwise they will look weird on reddit.
	# 				All winners will be formatted as "Winner: /u/" in the referral link contest post.
	updatedBeermoneySitesPost = ""
	updatedRefContestWinnersPost = ""
	currentIndex = 0
	cnt = 0
	
	# Create the Common Beermoney Sites Post
	for link in linkLocations:
		contestWinner = ref_contest_winners[cnt]
		
		if(contestWinner[0] != False):
			updatedBeermoneySitesPost = updatedBeermoneySitesPost + commonBeermoneySitesPost[currentIndex:link[0]]
			contestWinnerLink = contestWinner[1]
			# Update winners list with user here.
			updatedBeermoneySitesPost = updatedBeermoneySitesPost + contestWinnerLink
			currentIndex = link[1]
			
		cnt = cnt + 1
		
	updatedBeermoneySitesPost = updatedBeermoneySitesPost + commonBeermoneySitesPost[currentIndex:]
	

	# Create the Referral Link Contest Post
	firstWinnerIndex = refContestWinnersPost.index("Winner: /u/")
	startOfWinners = refContestWinnersPost.rfind('\n', 0, firstWinnerIndex) + 1
	
	lastWinnerIndex = refContestWinnersPost.rfind("Winner: /u/")
	endOfWinners = refContestWinnersPost.find('\n', lastWinnerIndex) + 2	# The newline characters will be re-added later.
	
		# Keep the previous winners in case we come across a winner who can't be replaced
	previousWinners = refContestWinnersPost[startOfWinners:endOfWinners].split("\n\n")
	
	updatedRefContestWinnersPost = refContestWinnersPost[0:startOfWinners]
	
	for contestWinner in ref_contest_winners:
		if(contestWinner[0] != False):
			domain = Get_Domain_From_Url(contestWinner[1])
			updatedRefContestWinnersPost = updatedRefContestWinnersPost + domain.title() + " Winner: /u/" + contestWinner[0] + "\n\n"
		
		else:
			# In the event that a winner couldn't be chosen, the previous winner will remain the winner. Find out who won last time.
			prevWinner = ''
			for line in previousWinners:
				if contestWinner[1].lower() in line.lower():
					prevWinner = line
			
			updatedRefContestWinnersPost = updatedRefContestWinnersPost + prevWinner + "\n\n"
	
	updatedRefContestWinnersPost = updatedRefContestWinnersPost + refContestWinnersPost[endOfWinners:]
	

	# Post the updated posts
	commonBeermoneySites.edit(updatedBeermoneySitesPost)
	refContestWinners.edit(updatedRefContestWinnersPost)
				
#                              End of Post Editor
# ----------------------------------------------------------------------------



# ----------------------------------------------------------------------------
# 								 Make Backups
def Make_Backups():
	# Save the current posts as files.
	# Assumptions:  No other file will be in the folder with the same name. If for some reason it is there, it'll be overwriten.

	# Create the folders
	dirBackupFolder = "Beermoney-Posts-Backups"

	dirCommon = dirBackupFolder + "/" + "Common-Beermoney-Sites-Backups"
	dirRefs   = dirBackupFolder + "/" + "Referral-Contest-Backups"

	try:
		os.makedirs(dirBackupFolder)
	except OSError as exception:
		if exception.errno != errno.EEXIST:
			raise
			Send_Error_Message(REDDIT, "Error making Beermoney Posts Backups directory")

	try:
		os.makedirs(dirCommon)
	except OSError as exception:
		if exception.errno != errno.EEXIST:
			raise
			Send_Error_Message(REDDIT, "Error making Common Beermoney Sites Backups directory")

	try:
		os.makedirs(dirRefs)
	except OSError as exception:
		if exception.errno != errno.EEXIST:
			raise
			Send_Error_Message(REDDIT, "Error making Referral Contest Backups directory")

		# Save the files
	todaysDate = time.strftime("%x")
	todaysDate = todaysDate.replace("/"  , "-")

	file1 = dirCommon + "/" + "Common-Beermoney-Site-Post-" + todaysDate
	with codecs.open(file1, 'w+', encoding='utf8') as f:
		f.write(commonBeermoneySitesPost)
	f.close()

	file2 = dirRefs + "/" + "Referral-Contest-Post-" + todaysDate
	with codecs.open(file2, 'w+', encoding='utf8') as f2:
		f2.write(refContestWinnersPost)
	f2.close()

#							 End of Make Backups
# ----------------------------------------------------------------------------
