#!/usr/bin/env python

import fitbit
import IPython
import pytz
from datetime import datetime, timedelta
from itertools import imap, chain, repeat

def clean_row(date, timezone, row):
    return([' '.join([date, row['time']]),
            timezone, 
            row['value']
           ]) 

def fetch_day(fb, daystring):
    url = '{}/{}/user/{}/activities/steps/date/{}/1d.json'.format(fb.API_ENDPOINT,
                                                              fb.API_VERSION,
                                                              '-',
                                                              daystring)
    now = datetime.now()
    tz = pytz.timezone(fb.user_profile_get()['user']['timezone'])
    now = tz.localize(now)
    timezone = now.strftime('%Z%z')

    # Steps every 1 minute
    result = fb.make_request(url=url)
    assert(len(result['activities-steps-intraday']['dataset']) == 1440 )
    assert(result['activities-steps-intraday']['datasetType'] == 'minute')
    date = result['activities-steps'][0]['dateTime']

    # Process every "row" in this day's dataset
    return(imap(clean_row,
                repeat(date),
                repeat(timezone),
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
