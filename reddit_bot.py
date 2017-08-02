from error_handler import *
from google_handler import *
from myconfig import *
from pick_winners import *
from reddit_handler import *

def Run_It():
	entries = Get_Spreadsheet()
	Backup_Spreadsheet(entries)
	linkLocations = Get_Domains_From_Post()
	ref_contest_winners = Pick_Winners(entries)
	Handle_Reddit(linkLocations, ref_contest_winners)
	Delete_Old_Entries(len(entries))
