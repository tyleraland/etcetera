import twitter
import json
import calendar
from itertools import imap
from datetime import datetime
from pytz import timezone

months = dict((month,num) for num,month in enumerate(calendar.month_abbr))

def clean_row(status):
    now = status.AsDict()['created_at'].split()
    hms = [int(hms) for hms in now[3].split(':')]
    dt = datetime(int(now[5]), int(months[now[1]]), int(now[2]),
         hms[0], hms[1], hms[2])
    datetimestring = dt.strftime('%Y-%m-%d %H:%M:%S')
    return([datetimestring, 
            str(status.AsDict()['text'])
           ])

def fetch_twitter(conf):
    api = twitter.Api(consumer_key=conf['consumer_key'],
                      consumer_secret=conf['consumer_secret'],
                      access_token_key=conf['access_token_key'],
                      access_token_secret=conf['access_token_secret'])

    # Returns list of last 20 twitter statuses
    timeline = api.GetUserTimeline()
    return imap(clean_row, timeline)
