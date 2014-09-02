import httplib2
import os
import mimetypes
import csv
import calendar

from apiclient.discovery import build
from apiclient.http import MediaFileUpload
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
from apiclient import errors
from oauth2client.file import Storage
from itertools import imap

months = dict((month,num) for num,month in enumerate(calendar.month_name))

last = ''
def clean_row(row):
    global last
    ls = row[0].translate(None,',').split(' ')
    text = row[1]
    month = str(months[ls[0]]) # E.g., 'September' -> '9'
    month = '0' + month if len(month) == 1 else month # '9' -> '09'
    day = ls[1]
    year = ls[2]
    hour = ls[4].split(':')[0] # E.g. '1' from '1:23AM'
    hour = '0' + hour if len(hour) == 1 else hour
    minute = ls[4][-4:-2] # E.g. '23' from '1:23AM'
    second = '00'
    datetimestring = '-'.join([year, month, day])
    datetimestring += ' '
    datetimestring += ':'.join([hour, minute, second])
    # We don't actually track seconds, but we don't want duplicate-timestamped entries
    # If this entry is the same as the previous one (except for second) then increment
    if datetimestring[:-2] == last[:-2]:
        second = str(int(last[-2:]) + 1)
        second = '0' + second if len(second) == 1 else second
        datetimestring = datetimestring[:-2] + second
    last = datetimestring
    return("'" + datetimestring + "'," + "'" + text + "'")
                
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
    return(imap(clean_row, reader))
