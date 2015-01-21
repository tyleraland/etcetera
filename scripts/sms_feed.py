import httplib2
import csv
import calendar
import itertools

from apiclient.discovery import build
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from datetime import datetime
from pytz import timezone

months = dict((month,num) for num,month in enumerate(calendar.month_name))

def clean_row(row):
    direction = row[0]
    ls = row[1].translate(None,',').split(' ')
    number = row[2]
    contact_name = row[3]
    text = row[4]
    month = months[ls[0]] # E.g., 'September' -> '9'
    day = int(ls[1])
    year = int(ls[2])
    hour = int(ls[4].split(':')[0]) # E.g. '1' from '1:23AM'
    minute = int(ls[4][-4:-2]) # E.g. '23' from '1:23AM'
    if ls[4][-2:] == 'AM' or hour == 12:
        pass
    elif ls[4][-2:] == 'PM':
        hour += 12
    else:
        raise Exception("Must be AM or PM")
    second = 0
    dt = datetime(year, month, day, hour, minute, second)

    datestring = dt.strftime("%Y-%m-%d")
    timestring = dt.strftime("%H:%M:%S")
    datetimestring = ' '.join([datestring,timestring])
    return [str(field) for field in [datetimestring,
                                     direction,
                                     number,
                                     contact_name,
                                     text]]

def fetch_sms(conf):
    # https://developers.google.com/drive/web/auth/web-client

    storage = Storage(conf['credentials'])
    creds = storage.get()
    flow = flow_from_clientsecrets(conf['client_secrets'], conf['oauth_scope'])

    #Create an httplib2.Http object and authorize it with our credentials
    http = httplib2.Http()
    http = creds.authorize(http)
    drive_service = build('drive', 'v2', http=http)


    readers = {}
    for sms_type in ['sms_received','sms_sent']:
        params = {'q': 'title="{}"'.format(conf[sms_type])}
        files = drive_service.files().list(**params).execute()
        results = []
        results.extend(files['items'])

        # Gotcha: you deleted the spreadsheet, but didn't empty the trash
        assert(1==len(results))

        # Drive will kindly insert double-quotes if they are already present in a field
        url = results[0]['exportLinks']['text/csv']
        resp, content = drive_service._http.request(url)
        if resp.status != 200:
            print("An error occured: {}".format(resp))
            return None
        readers[sms_type] = csv.reader(content.split('\n'), delimiter=',', quotechar='"')

    return(itertools.chain(
                itertools.imap(clean_row, readers['sms_received']),
                itertools.imap(clean_row, readers['sms_sent'])))
