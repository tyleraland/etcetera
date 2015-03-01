import csv
import calendar
import itertools
import dropbox

from datetime import datetime
from pytz import timezone

months = dict((month,num) for num,month in enumerate(calendar.month_name))

def clean_row(call_type, row):
    ls = row[0].translate(None,',').split(' ')
    phone_number = row[1]
    contact_name = row[2]
    if call_type == 'outgoing_calls' or call_type == 'received_calls':
        duration = row[3]
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

    # Assuming that datetime is already in UTC
    datestring = dt.strftime("%Y-%m-%d")
    timestring = dt.strftime("%H:%M:%S")
    datetimestring = ' '.join([datestring,timestring])
    clean_row = [str(datetimestring),
                 str(phone_number),
                 str(contact_name)]
    if call_type == 'outgoing_calls' or call_type == 'received_calls':
        clean_row.append(int(duration))
    return clean_row

def fetch_calls(call_type, conf):
    assert(call_type in ['outgoing_calls', 'received_calls', 'missed_calls'])

    client = dropbox.client.DropboxClient(conf['access_token'])

    filepaths = [f['path'] for f in client.metadata(conf[call_type])['contents']]

    all_rows = []
    # There may be multiple files in this direcotyr; max file size is 2MB
    for filepath in filepaths:
        handle = client.get_file(filepath)
        content = handle.read()
        rows = [row for row in csv.reader(content.split(' \n'), delimiter=',', quotechar='"')]
        rows = [clean_row(call_type, row) for row in rows]
        all_rows.extend(rows)
    return(all_rows)
