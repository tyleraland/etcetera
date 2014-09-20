"""
Parses settings.conf and provides top-level script
"""

from ConfigParser import SafeConfigParser
import sqlite3
import os
import json

from datetime import datetime

from scripts.feeds.sms_feed import fetch_sms
from scripts.feeds.twitter_feed import fetch_twitter
from scripts.feeds.fitbit_feed import fetch_fitbit

def csv2sqlite(conf, table, rows):

    con = sqlite3.connect(conf['database'])
    cur = con.cursor()

    con.text_factory = str
    for row in rows:
        # We want to use sqlite's facilities to build our statement string, but that
        # requires knowing how many fields our inserted string will have.  We perform
        # an initial string formatting to insert the proper number of variables
        statement = "insert or replace into {} values ({})".format(
            table, ','.join(['?' for field in row])
        )
        cur.execute(statement, row)
    con.commit()

def raw2csv(kind, data):
    if kind == 'twitter':
        js = open(data, 'r')
        js.readline()     # Remove useless header
        tweets = json.loads(js.read())
        for tweet in tweets:
            text = tweet['text'].lower()
            time = tweet['created_at']
            time = time.split()
            time = time[0].split('-') + time[1].split(':')
            time = [int(e) for e in time]
            dt = datetime(*time)
            print(text, time)
            break
            
def main(argv):
    settings = SafeConfigParser(allow_no_value=True)
    settings.read('settings.conf')

    #### SMS #### 
#    sms_feed = fetch_sms(dict(settings.items('Google Drive')))
#    csv2sqlite(dict(settings.items('Default')), 'sms', sms_feed)

    #### Twitter ####
#    settings.read(os.path.join('secrets','twitter_secrets.conf'))
#    twitter_feed = fetch_twitter(dict(settings.items('Twitter')))
#    csv2sqlite(dict(settings.items('Default')), 'Twitter', twitter_feed)

    #### Fitbit ####
#    settings.read(os.path.join('secrets','fitbit_secrets.conf'))
#    fitbit_feed = fetch_fitbit(dict(settings.items('fitbit')))
#    csv2sqlite(dict(settings.items('Default')), 'Fitbit_intraday_steps', fitbit_feed)
