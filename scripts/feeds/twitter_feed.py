import twitter
import json
import calendar
from itertools import imap

months = dict((month,num) for num,month in enumerate(calendar.month_abbr))

def clean_row(status):
    datetime = status.AsDict()['created_at'].split()
    date = [datetime[-1], months[datetime[1]], datetime[2]]
    date = '-'.join([str(date[0])] + ['0' + str(d) if len(str(d)) < 2 else str(d) for d in date[1:]])
    time = datetime[3]
    tz = datetime[-2]
    return (date, time, tz, status.AsDict()['text'])

def fetch_twitter(conf):
    api = twitter.Api(consumer_key=conf['consumer_key'],
                      consumer_secret=conf['consumer_secret'],
                      access_token_key=conf['access_token_key'],
                      access_token_secret=conf['access_token_secret'])

    # Returns list of last 20 twitter statuses
    timeline = api.GetUserTimeline()
    return imap(clean_row, timeline)
