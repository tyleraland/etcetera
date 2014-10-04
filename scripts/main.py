"""
Parses settings.conf and provides top-level script
"""

from ConfigParser import SafeConfigParser
import os

from scripts.db import dbcreate, dbinsert
from scripts.feeds.sms_feed import fetch_sms
#from scripts.feeds.gps_feed import fetch_gps
from scripts.feeds.twitter_feed import fetch_twitter
from scripts.feeds.fitbit_feed import fetch_fitbit
from scripts.feeds.rescuetime_feed import fetch_rescuetime

class config:
    def __init__(self, settings):
        self.settings = settings
    def section(self, section):
        return dict(self.settings.items(section))

def main(argv):
    settings = SafeConfigParser(allow_no_value=True)
    settings.read('settings.conf')
    conf = config(settings)
    #database = dict(settings.items('Default'))['database']
    database = conf.section('Default')['database']
    dbcreate(conf.section('Default'))

    ### GPS ###
#    gps_feed = fetch_gps(dict(settings.items('Google Drive')))
#    dbinsert(dict(settings.items('Default')), 'gps', gps_feed)
#    for g in gps_feed:
#        print(g)
    #csv2sqlite(dict(settings.items('Default')), 'gps', gps_feed)
    
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
#    csv2sqlite(dict(settings.items('Default')), 'fitbit_intraday_steps', fitbit_feed)

    ### RescueTime ###
#    settings.read(os.path.join('secrets','rescuetime_secrets.conf'))
#    rescuetime_feed = fetch_rescuetime(dict(settings.items('rescuetime')))
#    csv2sqlite(dict(settings.items('Default')), 'rescuetime', rescuetime_feed)

