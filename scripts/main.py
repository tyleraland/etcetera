"""
Parses settings.conf and provides top-level script
"""

from ConfigParser import SafeConfigParser
import sqlite3
import os

from scripts.feeds.twitter import twitter_fetch

def csv2sqlite(conf, rows):
    con = sqlite3.connect(conf['database'])
    cur = con.cursor()
    cur.execute("CREATE table if not exists Twitter(datetime TEXT unique, content TEXT)")

    for row in rows:
        cur.execute("insert or replace into Twitter values({})".format(row))
    con.commit()

def main(argv):
    settings = SafeConfigParser(allow_no_value=True)
    settings.read('settings.conf')

    reader = twitter_fetch(dict(settings.items('Google Drive')))
    csv2sqlite(dict(settings.items('Default')), reader)
