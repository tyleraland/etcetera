#!/usr/bin/env python

#import httplib2
#import pprint
#
#from apiclient.discovery import build
#from apiclient.http import MediaFileUpload
#from oauth2client.client import OAuth2WebServerFlow


from ConfigParser import SafeConfigParser
import httplib2
import os
import mimetypes

from apiclient.discovery import build
from apiclient.http import MediaFileUpload
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
from apiclient import errors
from oauth2client.file import Storage

# This is also in bin/authenticate_ ... and this is maybe the wrong value
OAUTH_SCOPE = 'https://www.googleapis.com/auth/drive.file'
REDIRECT_URI = 'urn:ietf:wg:oauth:2.0:oob'
# os.environ['REQUESTS_CA_BUNDLE']

credfile = '.credfile'

def twitter_fetch(args):

    conf = SafeConfigParser(allow_no_value=True)
    conf.read('settings.conf')
    # https://developers.google.com/drive/web/auth/web-client

    storage = Storage(credfile)
    creds = storage.get()
    flow = flow_from_clientsecrets('client_secrets.json', OAUTH_SCOPE, REDIRECT_URI)
    
    #Create an httplib2.Http object and authorize it with our credentials
    http = httplib2.Http()
    http = creds.authorize(http)
    
    drive_service = build('drive', 'v2', http=http)
    
#    # Retrieve a file

    results = []
    params = {'q': 'title="hello"'}
    files = drive_service.files().list(**params).execute()
    results.extend(files['items'])
    assert(1==len(results))
    url = results[0]['exportLinks']['text/plain']
    resp, content = drive_service._http.request(url)
    if resp.status != 200:
        print("An error occured: {}".format(resp))
        return None
    print("Content is as follows: ")
    print(content)


#    format,encoding = mimetypes.guess_type(arg)
#    #if format is None:
#    #        format = 'application/zip'
#    media_body = MediaFileUpload(arg, mimetype=format, resumable=True)
#    body = {
#            'title': filename,
#            'description': 'Backupfile from gbackup.py',
#            'mimeType': format
#    }
#    #file = drive_service.files().insert(body=body, media_body=media_body).execute()
#    file = drive_service.files().insert(body=body, media_body=media_body)
#    response = None
#    while response is None:
#            status, response = file.next_chunk()
#            if status:
#                    print "Uploaded %d%%." % int(status.progress() *100)
