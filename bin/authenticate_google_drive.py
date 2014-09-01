#!/usr/bin/env python

import httplib2
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from ConfigParser import SafeConfigParser
import sys

settings = SafeConfigParser(allow_no_value=True)
settings.read('settings.conf')

conf = {section : dict(settings.items(section)) for section in settings.sections()}

httpfix = httplib2.Http(disable_ssl_certificate_validation=True)
flow = flow_from_clientsecrets(conf['Google Drive']['client_secrets'],
                               conf['Google Drive']['oauth_scope'],
                               conf['Google Drive']['redirect_uri'])
authorize_url = flow.step1_get_authorize_url()
print("Go to the following link in your browser: \n{}".format(authorize_url))
code = raw_input('Enter verification code: ').strip()
credentials = flow.step2_exchange(code,httpfix)
storage = Storage(conf['Google Drive']['credentials'])
storage.put(credentials)
print("Initialization successful.  Ready to access Google Drive with readonly permissions")
sys.exit()
