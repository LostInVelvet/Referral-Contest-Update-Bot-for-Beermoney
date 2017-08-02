from check_winner import *
from error_handler import *
from get_domain import *
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
			
			timesWon = 0
			for sublist in contestWinners:
				if(sublist[0] == winner[0]):
					timesWon += 1
			
			if timesWon < 2:
				user = Check_If_User_Can_Win(winner[0])
				refLink = Check_For_Ref_Link(winner[1:], entries, site)
				
				if refLink != False:
					contestWinners.append([winner[0], refLink])
					break
			tries += 1
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
