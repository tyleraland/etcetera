import csv
import calendar
import itertools
import dropbox

from datetime import datetime,timedelta
from pytz import timezone
from itertools import chain,imap
from tzwhere.tzwhere import tzwhere
from os import path
import time

from xml.dom.minidom import parseString

months = dict((month,num) for num,month in enumerate(calendar.month_name))
namer = tzwhere()

def delocalize_time(timestring, latitude, longitude):
    # Given: a lat, long coordinate and timestamp in its local time
    # Result: the time converted to UTC
    tzname = namer.tzNameAt(float(latitude), float(longitude))
    try:
        tz = timezone(tzname)
    except AttributeError:
        return None
    dt = datetime.strptime(timestring, "%Y-%m-%dT%H:%M:%SZ")
    dt = tz.localize(dt)
    dt = dt.astimezone(timezone('UTC'))
    time = dt.strftime('%Y-%m-%dT%H:%M:%S')
    return time
def fetch_gps(conf):
    client = dropbox.client.DropboxClient(conf['access_token'])
    filepaths = [f['path'] for f in client.metadata(conf['gps'])['contents']]

    # Use datetime.now(), grab YYYYMMDD, use settings.conf dayspan to calculate interval
    # then check if any files in that interval are available for download
    now = datetime.now()
    wishlist = [(now - timedelta(days=i)).strftime('%Y%m%d') + '.kml'
                for i in range(1,1+int(conf['day_span']))]
    wishlist = [path.join(conf['gps'], w) for w in wishlist]
    xmls = []
    for name in wishlist:
        if name not in filepaths:
            continue
        handle = client.get_file(name)
        content = handle.read()
        xmls.append(content)
        doc = parseString(content)
        for where,when in zip(doc.getElementsByTagName('gx:coord'),
                              doc.getElementsByTagName('when')):
            coords = where.firstChild.data.split(' ')
            longitude = coords[0]
            latitude = coords[1]
            # Infer timezone from lat,long and convert local time to UTC
            datetimestring = delocalize_time(when.firstChild.data, latitude, longitude)
            if not datetimestring:
                continue
            yield [datetimestring, float(latitude), float(longitude)]
