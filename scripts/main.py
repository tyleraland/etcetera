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

    #### NOTE ####
    # For SMS, this should send to sent and recv in different tables
    
    con = sqlite3.connect(conf['database'])
    cur = con.cursor()
    cur.execute("CREATE table if not exists Twitter(datetime TEXT unique, content TEXT)")
    cur.execute("CREATE table if not exists sms(date TEXT,\
                                                time TEXT,\
                                                timezone TEXT,\
                                                number TEXT,\
                                                contact_name TEXT,\
                                                message TEXT,\
                                                UNIQUE(date, time, message)\
                                                  on conflict replace);")
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

    #### Twitter ####
    #csv2sqlite(dict(settings.items('Default')), reader)
    #raw2csv(kind='twitter', data='/Users/tal/Downloads/tweets/data/js/tweets/2013_04.js')

    #settings.read(os.path.join('secrets','twitter_secrets.conf'))
    #twitter_feed = fetch_twitter(dict(settings.items('Twitter')))

    #### Fitbit ####
    settings.read(os.path.join('secrets','fitbit_secrets.conf'))
    fetch_fitbit(dict(settings.items('fitbit')))

    #### SMS #### 
#    sms_recv_feed = fetch_sms(dict(settings.items('Google Drive')), kind='recv')
#    sms_send_feed = fetch_sms(dict(settings.items('Google Drive')), kind='send')
#    csv2sqlite(dict(settings.items('Default')), 'sms', sms_feed)

#    for i in sms_feed:
#        print(i)
#        break
