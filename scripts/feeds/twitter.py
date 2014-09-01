#!/usr/bin/env python

from ConfigParser import SafeConfigParser
import httplib2
import os
import mimetypes
import csv

from apiclient.discovery import build
from apiclient.http import MediaFileUpload
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
from apiclient import errors
from oauth2client.file import Storage

def twitter_fetch(conf):
    # https://developers.google.com/drive/web/auth/web-client

    storage = Storage(conf['credentials'])
    creds = storage.get()
    flow = flow_from_clientsecrets(conf['client_secrets'], conf['oauth_scope'])
    
    #Create an httplib2.Http object and authorize it with our credentials
    http = httplib2.Http()
    http = creds.authorize(http)
    
    drive_service = build('drive', 'v2', http=http)
    
    results = []
    params = {'q': 'title="Tweets by @AtumTal"'}
    files = drive_service.files().list(**params).execute()
    results.extend(files['items'])

    assert(1==len(results))
    # Drive will kindly insert double-quotes if they are already present in a field
    url = results[0]['exportLinks']['text/csv']
    resp, content = drive_service._http.request(url)
    if resp.status != 200:
        print("An error occured: {}".format(resp))
        return None
    reader = csv.reader(content.split('\n'), delimiter=',', quotechar='"')
    for l in reader:
        print(l)
