#!/usr/bin/python
from apiclient.discovery import build
from myconfig import *
from oauth2client.service_account import ServiceAccountCredentials
import errno
import httplib2
import os
import pickle
import time

# Spreadsheet info
scopes = ['https://www.googleapis.com/auth/spreadsheets']
credentials = ServiceAccountCredentials.from_json_keyfile_name( 'keyfile.json', scopes)

spreadsheet_id = google_spreadsheet_id
range_name = "B2:Z"  # The A row of the automatically generated spreadsheet is for timestamps. The first column is for question titles. 

http = credentials.authorize(httplib2.Http())
discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?' 'version=v4')
service = build('sheets', 'v4', http=http, discoveryServiceUrl=discoveryUrl)



# ----------------------------------------------------------------------------
#							  Backup The Entries
def Backup_Spreadsheet(entries):
	dirEntriesFolder = "Entries"

	try:
		os.makedirs(dirEntriesFolder)
	except OSError as exception:
		if exception.errno != errno.EEXIST:
			raise
			Send_Error_Message(REDDIT, "Error making Entries Backup directory")

	todaysDate = time.strftime("%x")
	todaysDate = todaysDate.replace("/"  , "-")

	file1 = dirEntriesFolder + "/Spreadsheet-Backup-" + todaysDate
	with open(file1, 'w+') as f:
		pickle.dump(entries, f)
	
#						  End of Backup The Entries
# ----------------------------------------------------------------------------


	
# ----------------------------------------------------------------------------
#							   Get The Spreadsheet
def Get_Spreadsheet():
	formSheet = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range=range_name).execute()
	result = formSheet.values()[1]

	return result
#						   End of Get The Spreadsheet
# ----------------------------------------------------------------------------



# ----------------------------------------------------------------------------
#							   Delete Old Entries
def Delete_Old_Entries(numEntries):
	request = {
		"requests": [
			{
			  "deleteDimension": {
				"range": {
				  "sheetId": google_sheet_id,
				  "dimension": "ROWS",
				  "startIndex": 1,
				  "endIndex": numEntries+1
				}
			  }
			}
		  ],
	}

	request = service.spreadsheets().batchUpdate(spreadsheetId=spreadsheet_id, body=request)
	response = request.execute()
#						   End of Delete Old Entries
# ----------------------------------------------------------------------------
