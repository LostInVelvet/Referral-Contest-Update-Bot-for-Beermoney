This is a bot made for /r/beermoney on reddit. It will automatically choose winners for their referral contest.

# Current Bugs
* None that I know of!

# Future Updates
* Add the ability to deny users based on their account age and activity.

# Instructions
1. Create a Reddit App.
    * Go Here: https://www.reddit.com/prefs/apps
    * Fill in the name and description with whatever you want.
    * Select "Script".
    * Set the redirect uri to http://127.0.0.1

2. Copy the Code and Secret and put them into myconfig.py
    * The code goes under reddit_client_id
    * The secret goes under reddit_client_secret
    * Fill in the reddit_username and the reddit_password fields for the account that will be editing the posts.

3. Setup a Google App
    * Go here: https://console.developers.google.com/start/api?id=sheets.googleapis.com
    * If this is your first app, agree to the ToS and then go back to the link above.
    * Click "Continue".
    * Click "Go to credientials".
    * Fill in the credentials with the following information:
        * Which API are you using? - Google Sheets API
        * Where will you be calling the API from? - Web Server
        * What data will you be accessing? - Application data
        * Are you using Google App Engine or Google Compute Engine? - No
        * Service account name - (Fill it in with whatever you like)
        * Role - Project -> Editor
        * Key Type - JSON
    * After hitting continue, a file will be downloaded. Rename this file to "keyfile.json" and move it to the bot's folder.

4. Create the form, the spreadsheet, and share it with the account that was just made.
    * Go here to create a new form: https://docs.google.com/forms/
    * Once the form is finalized, create the spreadsheet
        * Click on the "Responses" tab at the top.
        * Click on the green square with the two lines through it.
        * Name the spreadsheet whatever you want, then click "Create"
    * Share the form with the new account you made.
        * To get the email, open up keyfile.json
        * Search for "client_email" and copy the email after that, without the quotes.
        * On the spreadsheet page, go to File -> Share. Paste the email in there and hit "Send". You may get a notice that the email was undeliverable - just ignore it.
        
5. Edit myconfig with the spreadsheet info.
    * google_spreadsheet_id = The long string of characters after https://docs.google.com/spreadsheets/d/ and before "/edit"
    * google_sheet_id = The string of numbers after "#gid=" (If this doesn't show up, click on the sheet tab at the bottom left of the page)

6. Run these commands on the server from the terminal (Linux only)
    * sudo apt-get python pip
    * sudo pip install praw
    
7. Setup cron to automate the task
    * Type into terminal: crontab -e
        * If this is the first time running this, it will ask what editor you want to choose. I recommend selecting nano.
    * Go to the bottom of the document and type this in: 0 \*/6 * * * python /FILE-LOCATION/reddit-bot.py
        * This will run a script every 6 hours to check if it is time to update the post. You can change this value if you want, but I recommend leaving it at every 6 hours (or decreasing it to every 1 or 2 hours)
        * To save the file: Ctrl + X then Y and then Enter to save
    * Restart cron to be safe
        * sudo /etc/init.d/cron restart
