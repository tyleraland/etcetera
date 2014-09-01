#!/usr/bin/env python

import httplib2
import mimetypes
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
import sys

OAUTH_SCOPE = 'https://www.googleapis.com/auth/drive.readonly'
REDIRECT_URI = 'urn:ietf:wg:oauth:2.0:oob'

credfile = '.credfile'

httpfix = httplib2.Http(disable_ssl_certificate_validation=True)
flow = flow_from_clientsecrets('client_secrets.json', OAUTH_SCOPE, REDIRECT_URI)
authorize_url = flow.step1_get_authorize_url()
print 'Go to the following link in your browser: \n' + authorize_url
code = raw_input('Enter verification code: ').strip()
credentials = flow.step2_exchange(code,httpfix)
storage = Storage(credfile)
storage.put(credentials)
print "All finished initializing, run again using -f or --file to upload a file."
sys.exit()
