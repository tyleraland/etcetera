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
from datetime import datetime
import itertools
from datetime import datetime
from pytz import timezone

months = dict((month,num) for num,month in enumerate(calendar.month_name))

def clean_row(row):
    ls = row[0].translate(None,',').split(' ')
    number = row[1]
    contact_name = row[2]
    text = row[3]
    month = months[ls[0]] # E.g., 'September' -> '9'
#    month = '0' + month if len(month) == 1 else month # '9' -> '09'
    day = int(ls[1])
    year = int(ls[2])
    hour = int(ls[4].split(':')[0]) # E.g. '1' from '1:23AM'
#    hour = '0' + hour if len(hour) == 1 else hour
    minute = int(ls[4][-4:-2]) # E.g. '23' from '1:23AM'
    second = 0
#    date = '-'.join([year, month, day])
#    time = ':'.join([hour, minute, second])
    dt = datetime(year, month, day, hour, minute, second)
    dt = timezone('US/Pacific').localize(dt)

    # timezone = 'PST'
#    fields = ["'" + field + "'" for field in [date, time, timezone, number,
#                                              contact_name, text]]
    print(dt)
    datetimestring = dt.strftime("%Y-%m-%d %H:%M:%S %Z%z")
    print(datetimestring)

#    dt = datetime.datetime(int(year), int(month), int(day),
#                           int(hour), int(minute), int(second))
#    dt = timezone('UTC').localize(dt)
#    print(dt)
#    dt = dt.astimezone(timezone('US/Pacific'))
#    print(dt)
    return None
#    return(','.join(fields))

def fetch_sms(conf):
    # https://developers.google.com/drive/web/auth/web-client

    storage = Storage(conf['credentials'])
    creds = storage.get()
    flow = flow_from_clientsecrets(conf['client_secrets'], conf['oauth_scope'])
    
    #Create an httplib2.Http object and authorize it with our credentials
    http = httplib2.Http()
    http = creds.authorize(http)
    drive_service = build('drive', 'v2', http=http)
    
    results = []

    # Received SMS messages
    params = {'q': 'title="{}"'.format(conf['sms_received'])}
    files = drive_service.files().list(**params).execute()
    results.extend(files['items'])

    assert(1==len(results))
    # Drive will kindly insert double-quotes if they are already present in a field
    url = results[0]['exportLinks']['text/csv']
    resp, content = drive_service._http.request(url)
    if resp.status != 200:
        print("An error occured: {}".format(resp))
        return None
    recv_reader = csv.reader(content.split('\n'), delimiter=',', quotechar='"')

    # Sent SMS messages
    params = {'q': 'title="{}"'.format(conf['sms_sent'])}
    files = drive_service.files().list(**params).execute()
    results.extend(files['items'])

    assert(2==len(results))
    # Drive will kindly insert double-quotes if they are already present in a field
    url = results[0]['exportLinks']['text/csv']
    resp, content = drive_service._http.request(url)
    if resp.status != 200:
        print("An error occured: {}".format(resp))
        return None
    sent_reader = csv.reader(content.split('\n'), delimiter=',', quotechar='"')

    return(itertools.chain(itertools.imap(clean_row, recv_reader),
                           itertools.imap(clean_row, sent_reader)))
