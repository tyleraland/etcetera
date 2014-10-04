import httplib2
import csv
import calendar
import itertools

from apiclient.discovery import build
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from datetime import datetime,timedelta
from pytz import timezone
from itertools import chain,imap
from tzwhere.tzwhere import tzwhere
import time

from xml.dom.minidom import parseString

months = dict((month,num) for num,month in enumerate(calendar.month_name))
namer = tzwhere()

def delocalize_time(timestring, latitude, longitude):
    # Given: a lat, long coordinate and timestamp in its local time
    # Result: the time converted to UTC
    tzname = namer.tzNameAt(float(latitude), float(longitude))
    tz = timezone(tzname)
    dt = datetime.strptime(timestring, "%Y-%m-%dT%H:%M:%SZ")
    dt = tz.localize(dt)
    dt = dt.astimezone(timezone('UTC'))
    time = dt.strftime('%Y-%m-%dT%H:%M:%S')
    return time
def fetch_gps(conf):
    # https://developers.google.com/drive/web/auth/web-client

    storage = Storage(conf['credentials'])
    creds = storage.get()
    flow = flow_from_clientsecrets(conf['client_secrets'], conf['oauth_scope'])
    
    #Create an httplib2.Http object and authorize it with our credentials
    http = httplib2.Http()
    http = creds.authorize(http)
    drive_service = build('drive', 'v2', http=http)

    params1 = {'q': 'title="{}"'.format(conf['gpslog_folder'])}
    results = drive_service.files().list(**params1).execute()
    assert(len(results['items']) == 1)
    parent_folder_id = results['items'][0]['id']
    params2 = {'q': "'{}' in parents".format(parent_folder_id)}
    results = drive_service.files().list(**params2).execute()
    
    urls = dict([(f['title'],f['downloadUrl']) for f in results['items']])

    # Use datetime.now(), grab YYYYMMDD, use settings.conf dayspan to calculate interval
    # then check if any files in that interval are available for download
    now = datetime.now()
    wishlist = [(now - timedelta(days=i)).strftime('%Y%m%d') + '.kml'
                for i in range(1,1+int(conf['day_span']))]
    xmls = []
    for name in wishlist:
        if name not in urls:
            continue
        resp, content = drive_service._http.request(urls[name])
        if resp.status != 200:
            raise Exception("An error occured: {}".format(resp))
        xmls.append(content)
        doc = parseString(content)
        for where,when in zip(doc.getElementsByTagName('gx:coord'), 
                              doc.getElementsByTagName('when')):
            coords = where.firstChild.data.split(' ')
            longitude = coords[0]
            latitude = coords[1]
            # Infer timezone from lat,long and convert local time to UTC
            datetimestring = delocalize_time(when.firstChild.data, latitude, longitude)
            yield [datetimestring, float(latitude), float(longitude)]
