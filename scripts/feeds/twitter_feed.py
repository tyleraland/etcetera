import twitter
import json

def fetch_twitter(conf):
    api = twitter.Api(consumer_key=conf['consumer_key'],
                      consumer_secret=conf['consumer_secret'],
                      access_token_key=conf['access_token_key'],
                      access_token_secret=conf['access_token_secret'])
    #print api.VerifyCredentials()

    # Returns list of last 20 twitter statuses
    timeline = api.GetUserTimeline()
    for status in timeline:
        print(status.AsDict()['text'])
        print(status.AsDict()['created_at'])
