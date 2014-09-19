#!/usr/bin/env python

import fitbit
import IPython

def fetch_fitbit(conf):
    fb = fitbit.Fitbit(conf['consumer_key'],
                                 conf['consumer_secret'],
                                 resource_owner_key=conf['oauth_token'],
                                 resource_owner_secret=conf['oauth_token_secret'])


    profile = fb.user_profile_get()

    # Year-month-day
    day_to_fetch = '2014-09-14'
    url = '{}/{}/user/{}/activities/steps/date/{}/1d.json'.format(fb.API_ENDPOINT,
                                                                  fb.API_VERSION,
                                                                  '-',
                                                                  day_to_fetch)
    # Steps every 1 minute
    result = fb.make_request(url=url)
    print(result['activities-steps'][0]['dateTime'])
    print(result['activities-steps'][0]['value']) # Total steps that day
    assert( len(result['activities-steps-intraday']['dataset']) == 1440 )
    assert( result['activities-steps-intraday']['datasetType'] == 'minute')
#    IPython.embed() 
