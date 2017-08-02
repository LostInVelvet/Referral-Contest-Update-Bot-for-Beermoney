from myconfig import *

# ----------------------------------------------------------------------------
#							  Get Domain From Url

# This function returns the domain of the url if the domain is within the list of sites_with_refs
# It returns False if the there is not a valid link, or if the domain is not within the list of sites.
def Get_Domain_From_Url(url):
	if url.find("www.") != -1:
		domainStartIndex = url.index("www.") + 4
	elif url.find("://") != -1:
		domainStartIndex = url.index("://") + 3	
	else:
		return False

	if(url.find('.', domainStartIndex, len(url)) != -1):
		domainEndIndex = url.index('.', domainStartIndex)
	else:
		return False
	
	
	domain = url[domainStartIndex:domainEndIndex]


	if any(domain.lower() in i.lower() for i in sites_with_refs):
		return domain
	else:
		return False

#						  End of Get Domain From Url
# ----------------------------------------------------------------------------
