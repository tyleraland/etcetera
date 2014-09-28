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
from scripts.feeds.rescuetime_feed import fetch_rescuetime

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

def main(argv):
    settings = SafeConfigParser(allow_no_value=True)
    settings.read('settings.conf')

    #### SMS #### 
#    sms_feed = fetch_sms(dict(settings.items('Google Drive')))
#    csv2sqlite(dict(settings.items('Default')), 'sms', sms_feed)

    #### Twitter ####
    settings.read(os.path.join('secrets','twitter_secrets.conf'))
    twitter_feed = fetch_twitter(dict(settings.items('Twitter')))
    csv2sqlite(dict(settings.items('Default')), 'Twitter', twitter_feed)

    #### Fitbit ####
    settings.read(os.path.join('secrets','fitbit_secrets.conf'))
    fitbit_feed = fetch_fitbit(dict(settings.items('fitbit')))
    csv2sqlite(dict(settings.items('Default')), 'fitbit_intraday_steps', fitbit_feed)

    ### RescueTime ###
#    settings.read(os.path.join('secrets','rescuetime_secrets.conf'))
#    rescuetime_feed = fetch_rescuetime(dict(settings.items('rescuetime')))
#    csv2sqlite(dict(settings.items('Default')), 'rescuetime', rescuetime_feed)
