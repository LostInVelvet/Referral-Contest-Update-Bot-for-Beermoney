from check_winner import *
from error_handler import *
from get_domain import *
from myconfig import *
from operator import itemgetter
from random import randint
from reddit_handler import REDDIT
from urlparse import urlparse
import httplib
import praw
import urllib2
import sys

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
#                      Check If The Winner Has A Ref Link
def Check_For_Ref_Link(winner, entries, site):
	for url in winner:
		domain = Get_Domain_From_Url(url)
		
		if(domain != False):
			if(domain.lower() == site.lower()):
				fixedUrl = Fix_Url(url, domain)
			
				if(fixedUrl != False):
					return fixedUrl

	return False
#                  End of Check If The Winner Has A Ref Link
# ----------------------------------------------------------------------------



# ----------------------------------------------------------------------------
#                                Count Entries
def Count_Entries(entries):
	numEntries = 0
	
	for i in entries:
		if isinstance(i, list):
			numEntries = numEntries + 1	
	
	return numEntries

#                             End of Count Entries
# ----------------------------------------------------------------------------



# ----------------------------------------------------------------------------
#                                 Fix The Url
def Fix_Url(txt, domain):
	# Find the start of the url
	linkStartIndex = txt.index(domain)

	refLink = txt[linkStartIndex:]
	
	# Check if there's whitespace after it.
	if refLink.find(" ") != -1:
		linkEndIndex = refLink.index(" ")
		refLink = refLink[:linkEndIndex]
	
	url = "http://" + refLink		
	
	if(Url_Works(url)==True):
		return url
	else:
		return False
	
	return url
#                              End of Fix The Url
# ----------------------------------------------------------------------------



# ----------------------------------------------------------------------------
#                                 Pick Winners
def Pick_Winners(entries):
	numSites = len(sites_with_refs)
	numEntries = Count_Entries(entries)
	contestWinners = []
	maxTries = 100;
	invalidWinners = []
	
	for site in sites_with_refs:
		tries = 0
		
		while tries <= maxTries:
			if(tries == maxTries):
				msg = "Error finding winner for the site: " + site + ".\n\n"
				msg += ">" + str(maxTries) + " tries were attempted, but no valid winner was found. Last week's winner has been left there instead. Please check the spreadsheet to see if there were any valid entries." 
				Send_Error_Message(REDDIT, msg)
				contestWinners.append([False, site])
				break;

			num = randint(0, numEntries-1)
			winner = entries[num]
			
			canWinReturn = Check_If_User_Can_Win(winner[0], REDDIT)
			userValid = canWinReturn[0]
			
			if(userValid):
				timesWon = 0
				for sublist in contestWinners:
					if(sublist[0] == winner[0]):
						timesWon += 1
				
				if timesWon < 2:
					refLink = Check_For_Ref_Link(winner[1:], entries, site)
					
					if refLink != False:
						contestWinners.append([winner[0], refLink])
						break
			else:
				invalidWinners.append(canWinReturn[1])
			tries += 1
			
			
	blankLine = "\n\n&nbsp;\n\n"
	bold = "**"
	msg = ""
	nl = "\n\n"
	usr = "/u/"
	reason = [	"Users whos account does not exist or are shadowbanned:",
				"Users who are banned from participating:",
				"Users whos accounts are not old enough:",
				"Users who don't have enough posts:",
				"Users who do not have recent posts:",
			 ]
	
	invalidWinners = sorted(invalidWinners, key=itemgetter(1))
	lastReason = -1;
	
	if(invalidWinners != []):
		for entry in invalidWinners:
			if(lastReason != entry[1]):
				if(lastReason != -1):
					msg += blankLine
				msg += bold + reason[entry[1]] + bold
				lastReason = entry[1]
				
			msg += nl + usr + entry[0]
		
		msg_to_send = "Hey, it's your bot here. I handle the referral link contest. I found some invalid potential this week:" + blankLine + msg + blankLine + "My associated subreddit: /r/beermoney"
		REDDIT.redditor(message_user).message("Invalid Potential Winners Found", msg_to_send)
			
	return contestWinners
#                             End of Pick Winners
# ----------------------------------------------------------------------------



# ----------------------------------------------------------------------------
#                            Check If The URL Works                          
def Url_Works(url):
	try:
		parsedUrl = urlparse(url)
	except Exception:
		sys.exc_clear()
		return False

	if(parsedUrl.netloc != ''):
		try:
			# Certain websites block scraper requests. To get around this, we'll pretend to be Mozilla
			l = urllib2.Request(url, headers={'User-Agent': "Mozilla/5.0"})
			r = urllib2.urlopen(l, timeout = 10)
			if(r.code != 404):
				return True
		except urllib2.HTTPError as e:
			print e.code
		except urllib2.URLError as e:
			print e.args
		except httplib.HTTPException as e:
			print "HTTPException"
		except Exception:
			sys.exc_clear()
			return False
			
	return False
#                        End of Check If The URL Works
# ----------------------------------------------------------------------------
