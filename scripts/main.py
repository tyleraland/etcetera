"""
Parses settings.conf and provides top-level script
"""

from ConfigParser import SafeConfigParser
import httplib2
import os

from scripts.feeds.twitter import twitter_fetch

def main(argv):
    settings = SafeConfigParser(allow_no_value=True)
    settings.read('settings.conf')

    conf = {section : dict(settings.items(section)) for section in settings.sections()}

    twitter_fetch(dict((k,conf['Google Drive'][k]) for k in ['oauth_scope',
                                                             'credentials',
                                                             'client_secrets'])) 
