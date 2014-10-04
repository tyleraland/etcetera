import datetime

from rescuetime.api.service.Service import Service
from rescuetime.api.access.AnalyticApiKey import AnalyticApiKey
from rescuetime.api.model.ResponseData import ResponseData
from datetime import datetime, timedelta
from itertools import imap, chain

def clean_row(row):
    datetimestring = row[0].replace('T',' ') # Remove T from datetime
    return([datetimestring,
            row[1],   # Seconds spent
            row[3],   # Activity
            row[4],   # Category
            row[5]])  # Productivity score
def fetch_rescuetime(conf):

    now = datetime.now()
    targetdays = [(now - timedelta(days=i)).strftime('%Y-%m-%d')
                  for i in reversed(range(0, 1+int(conf['day_span'])))]

    rescuetime_service = Service()
    key = AnalyticApiKey(conf['api_key'], rescuetime_service)

    # https://www.rescuetime.com/apidoc
    for i,_ in enumerate(targetdays[:-1]):
        args = {
                'op': 'select',
                'vn': 0,
                'pv': 'interval',
                'rb': targetdays[i],
                're': targetdays[i+1],
                'resolution_time': 'minute'
               }
        response = ResponseData(key, **args)
        response.sync()

        # Row headers:
        # Date
        # Time spent (seconds)
        # Number of people
        # Activity
        # Category
        # Productivity weight
        if response.object['rows'] is not None:
            return(imap(clean_row,
                        response.object['rows']))
        else:
            raise Exception("rescuetime returned None")
