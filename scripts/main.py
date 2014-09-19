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

def dbinit(conf):
    con = sqlite3.connect(conf['database'])
    cur = con.cursor()

    cur.execute("CREATE table if not exists Twitter(datetime TEXT unique, content TEXT)")

    con.commit()

def csv2sqlite(conf, rows):
    con = sqlite3.connect(conf['database'])
    cur = con.cursor()
    cur.execute("CREATE table if not exists Twitter(datetime TEXT unique, content TEXT)")

    for row in rows:
        cur.execute("insert or replace into Twitter values({})".format(row))
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

    #reader = twitter_fetch(dict(settings.items('Google Drive')))
    #csv2sqlite(dict(settings.items('Default')), reader)

    # Twitter
    #settings.read(os.path.join('secrets','twitter_secrets.conf'))
    #fetch_twitter(dict(settings.items('Twitter')))
