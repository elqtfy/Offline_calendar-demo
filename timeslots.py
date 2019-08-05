#time_slots.py
from datetime import datetime, timedelta
import json
import random
from pprint import pprint
from twilio.rest import Client

infile = open('events.json','r')
events = json.load(infile)

appointments = []

for event in events:
    title = event.get('title')
    dateS, start = event['start'].split('T',1)
    start = start.split('-',1)[0]
    dateE, end = event['end'].split('T',1)
    end = end.split('-',1)[0]
    location = event['location']
    #print(title,date,start,end,location)
    #print dateS, start,dateE, end
    A = datetime(int(dateS.split('-')[0]),
        int(dateS.split('-')[1]),
        int(dateS.split('-')[2]),
        int(start.split(':')[0]),
        int(start.split(':')[1]))
    # appointments.append(A)
    B = datetime(int(dateE.split('-')[0]),
        int(dateE.split('-')[1]),
        int(dateE.split('-')[2]),
        int(end.split(':')[0]),
        int(end.split(':')[1]))
    #print A,B,B-A
    # appointments.append(B)
    appointments.append((A,B))
pprint(appointments)

hours = (datetime(datetime.now().year, datetime.now().month, datetime.now().day, datetime.now().hour),
        datetime(datetime.now().year, datetime.now().month, datetime.now().day+7, datetime.now().hour))
# print hours

def get_slots(hours, appointments, duration=timedelta(hours=4)):
    slots = sorted([(hours[0], hours[0])] + appointments + [(hours[1], hours[1])])
    possiblelist = []
    for start, end in ((slots[i][1], slots[i+1][0]) for i in range(len(slots)-1)):
        # assert start <= end, "Cannot attend all appointments"
        while start + duration <= end:
            A = "{:%m-%d, %H:%M} - {:%H:%M}".format(start, start + duration)
            possiblelist.append(A)
            start += duration
    #pprint(possiblelist)
    # pprint(random.sample(set(possiblelist),3))
    return random.sample(set(possiblelist),3)

with open('creds.json','r') as infile:
    creds = json.load(infile)

def send(message):
    sid = creds['twilio_sid']
    token = creds['twilio_token']

    client = Client(sid, token)
    numbers = [
        creds['twilio_realnum']
    ]


    for number in numbers:
        message = client.messages.create(
            to=number,
            from_=creds['twilio_accnum'],
            body=message
        )

if __name__ == "__main__":
    dates = get_slots(hours, appointments)
    msg_txt = '''Hello dear, Offline arranged a hangout for you!\nvote for these potential dates.\n1: '''+dates[0]+'\n2: '+dates[1]+'\n3: '+dates[2]+'\nor you can send NO if anything does not work for you.'
    print msg_txt
    send(msg_txt)