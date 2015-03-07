#!/usr/bin/env python

import fitbit
import IPython
from pytz import timezone
from datetime import datetime, timedelta
from itertools import imap, chain, repeat

def clean_row(date, tz, row):
    yr,mo,dy = [int(ymd) for ymd in date.split('-')]
    hr,mn,sc = [int(hms) for hms in row['time'].split(':')]

    # Never create datetime with timezone by using tzinfo
    # https://stackoverflow.com/questions/24856643/unexpected-results-converting-timezones-in-python
    dt = datetime(yr,mo,dy,hr,mn,sc)
    dt = tz.localize(dt)                # Insert timezone information into datetime object
    dt = dt.astimezone(timezone('UTC')) # Convert to UTC
    steps = int(row['value'])
    datetimestring = dt.strftime('%Y-%m-%d %H:%M:%S')

    return [datetimestring, steps]

def fetch_day(fb, daystring):
    url = '{}/{}/user/{}/activities/steps/date/{}/1d.json'.format(fb.API_ENDPOINT,
                                                              fb.API_VERSION,
                                                              '-',
                                                              daystring)
    now = datetime.now()
    tz = timezone(fb.user_profile_get()['user']['timezone'])

    # Steps every 1 minute
    result = fb.make_request(url=url)
    assert(len(result['activities-steps-intraday']['dataset']) <= 1440 )
    assert(result['activities-steps-intraday']['datasetType'] == 'minute')
    date = result['activities-steps'][0]['dateTime']

    # Process every "row" in this day's dataset
    return(imap(clean_row,
                repeat(date),
                repeat(tz),
                result['activities-steps-intraday']['dataset']))

def fetch_fitbit(conf):
    fb = fitbit.Fitbit(conf['consumer_key'],
                       conf['consumer_secret'],
                       resource_owner_key=conf['oauth_token'],
                       resource_owner_secret=conf['oauth_token_secret'])

    today = datetime.now()
    days = [(today - timedelta(days=i)).strftime('%Y-%m-%d')
            for i in range(1, 1+int(conf['day_span']))]

    # chain.from_iterable is flattening multiple iterators into a single stream
    # each imap applies fetch_day(fb, day) for each day in days
    # each fetch_day returns an iterator that returns 1440 rows; one for each minute of the day
    return chain.from_iterable(imap(fetch_day, repeat(fb), days))
