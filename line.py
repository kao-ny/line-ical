# -*- coding: utf-8 -*-
import urllib2
from icalendar import Calendar
import datetime
import json
import pprint
import requests

# Download ics calendar
url = 'https://example.com/calendar.ics'  # TODO: Update!
PathandTitle = '/tmp/snct.ics'
response = urllib2.urlopen(url)
inputCal = response.read()


today = datetime.date.today()
# for debug
#today = datetime.date(2017,4,26)
nextday = today + datetime.timedelta(days=1)

todaySchedules = [ ]
nextdaySchedules = [ ]

cal = Calendar.from_string(inputCal)
body = ""
for ev in cal.walk():
    if ev.name == 'VEVENT':
        start_dt = ev.decoded("dtstart")
        end_dt = ev.decoded("dtend")
        summary = ev['summary'].encode('utf-8')
        # print "{start} - {end} : {summary}".format(start=start_dt.strftime("%Y/%m/%d %H:%M"), end=end_dt.strftime("%Y/%m/%d %H:%M"), summary=summary)

        start_date = datetime.date(int(start_dt.strftime("%Y")),int(start_dt.strftime("%m")),int(start_dt.strftime("%d")))
        end_date = datetime.date(int(end_dt.strftime("%Y")), int(end_dt.strftime("%m")),int(end_dt.strftime("%d")))

        end_date -= datetime.timedelta(days=1)
        if start_date<=today:
            if today<=end_date:
                todaySchedules.append("{start} - {end} : {summary}".format(start=start_dt.strftime("%Y/%m/%d %H:%M"), end=end_dt.strftime("%Y/%m/%d %H:%M"), summary=summary))


        if start_date<=nextday:
            if nextday<=end_date:
                nextdaySchedules.append("{start} - {end} : {summary}".format(start=start_dt.strftime("%Y/%m/%d %H:%M"), end=end_dt.strftime("%Y/%m/%d %H:%M"), summary=summary))

textTodaySchedule = ''
for todaySchedule in todaySchedules:
    textTodaySchedule += todaySchedule + '\n'

textNextdaySchedule = ''
for nextdaySchedule in nextdaySchedules:
    textNextdaySchedule += nextdaySchedule + '\n'

message = '【今日の予定】\n'+str(textTodaySchedule)+'\n【明日の予定】\n'+str(textNextdaySchedule)

lineApiUrl = 'https://api.line.me/v2/bot/message/push'
# TODO: Update!
authKey = 'Update_Your_LINE_bot_auth_key'
groupID = 'Update_Your_LINE_group_ID'

mes = [
    {
        'type':'text',
        'text':str(message),
    }
]

# tmp = json.dumps({'to':str(groupID),'messages':mes})

response = requests.post(
    str(lineApiUrl),
    str(json.dumps({'to':str(groupID),'messages':mes})),
    headers={"Content-Type":"application/json", "Authorization":"Bearer {"+str(authKey)+"}",}
)
pprint.pprint(response.json())
