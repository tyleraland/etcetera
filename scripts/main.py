"""
Parses settings.conf and provides top-level script
"""

from ConfigParser import SafeConfigParser
import httplib2
import os
import mimetypes

from scripts.feeds.twitterfeed import twitter_fetch

# This is also in bin/authenticate_ ...
OAUTH_SCOPE = 'https://www.googleapis.com/auth/drive.file'
REDIRECT_URI = 'urn:ietf:wg:oauth:2.0:oob'
# os.environ['REQUESTS_CA_BUNDLE']

credfile = '.credfile'

def main(argv):
    conf = SafeConfigParser(allow_no_value=True)
    conf.read('settings.conf')
    # https://developers.google.com/drive/web/auth/web-client
    
    twitter_fetch(None)
