"""
Shows basic usage of the Google Calendar API. Creates a Google Calendar API
service object and outputs a list of the next 10 events on the user's calendar.
"""
#picking 3 random dates listen to the preference?(maybe not)
#send text at the end would be great!!!twilio
#and fourquare location 
from __future__ import print_function
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import datetime
import json
import pprint
import os


# Setup the Calendar API
SCOPES = 'https://www.googleapis.com/auth/calendar'
store = file.Storage('credentials.json')

flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
creds = tools.run_flow(flow, store)

creds = store.get()

# if not creds or creds.invalid:
#     flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
#     creds = tools.run_flow(flow, store)
service = build('calendar', 'v3', http=creds.authorize(Http()))

# Call the Calendar API
now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
#print('Getting the upcoming 10 events')
events_result = service.events().list(calendarId='primary', timeMin=now,
                                      maxResults=40, singleEvents=True,
                                      orderBy='startTime').execute()
events = events_result.get('items', [])

if (os.stat("events.json").st_size == 0):
	items = []
else:
	infile = open('events.json','r')
	items = json.load(infile)
	infile.close()


if not events:
    print('No upcoming events found.')
for event in events:
    start = event['start'].get('dateTime', event['start'].get('date'))
    end = event['end'].get('dateTime', event['start'].get('date'))
    location = event.get('location')
    print(event['summary'],start,end,location)
    item = {
        'title' : event['summary'],
    	'start' : start,
        'end' : end,
        'location' : location
    }
    items.append(item)
    #print(item)
    #json.dump(str(events['summary']), outfile, indent=2)


outfile = open('events.json','w')
json.dump(items, outfile, indent=2)
outfile.close()
