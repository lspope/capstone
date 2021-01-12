import tweepy
import json
import pandas as pd
import re
from pymongo import MongoClient

usa_states_regex = '(?:(A[KLRZ]|C[AOT]|D[CE]|FL|GA|HI|I[ADLN]|K[SY]|LA|M[ADEINOST]|N[CDEHJMVY]|O[HKR]|P[AR]|RI|S[CD]|T[NX]|UT|V[AIT]|W[AIVY]|USA))'

usa_states_fullname_regex = '(ALABAMA|ALASKA|ARIZONA|ARKANSAS|CALIFORNIA|COLORADO|CONNECTICUT|DELAWARE|FLORIDA|GEORGIA|HAWAII|' \
                            'IDAHO|ILLINOIS|INDIANA|IOWA|KANSAS|KENTUCKY|LOUISIANA|MAINE|MARYLAND|MASSACHUSETTS|MICHIGAN|MINNESOTA|MISSISSIPPI|MISSOURI|MONTANA|'\
                            'NEBRASKA|NEVADA|NEW\sHAMPSHIRE|NEWSJERSEY|NEW\sMEXICO|NEW\sYORK|NORTH\sCAROLINA|NORTH\sDAKOTA|OHIO|OKLAHOMA|OREGON|PENNSYLVANIA|RHODE\sISLAND|'\
                            'SOUTH\sCAROLINA|SOUTH\sDAKOTA|TENNESSEE|TEXAS|UTAH|VERMONT|VIRGINIA|WASHINGTON|WEST\sVIRGINIA|WISCONSIN|WYOMING)'

track_terms = ['covid k12 remote', 'covid k-12 remote', 
    'covid k12 distance', 'covid k-12 distance', 
    'covid k12 online' , 'covid k-12 online' , 
    'covid k12 virtual', 'covid k-12 virtual', 
    'covid k12 hybrid', 'covid k-12 hybrid' ]


class MyStreamListener(tweepy.StreamListener):
    def __init__(self, api, twitter_collection):
        super(MyStreamListener, self).__init__()
        self.api = api
        self.me = api.me()
        self.twitter_collection = twitter_collection

    def on_status(self, tweet):
        print(f"{tweet.user.screen_name}:{tweet.user.location}:{tweet.text}")
        user_loc_str = str(tweet.user.location).upper()
        found_usa_state = re.search(usa_states_regex, user_loc_str) or re.search(usa_states_fullname_regex, user_loc_str)
        if found_usa_state:
            if hasattr(tweet, 'retweeted_status'):
                print('Not storing Retweets')
            else:
                print(user_loc_str)
                twitter_collection.insert(tweet._json)

    def on_error(self, status):
        print("Error detected")

def get_mongo_client(host='localhost', port=27017):
    mongo_client = MongoClient(host=host, port=port)
    return mongo_client

def get_twitter_collection(mongo_client):
    capstone_db = mongo_client['capstone_db']
    twitter_collection = capstone_db['tweets']
    twitter_collection.drop()
    return twitter_collection

def get_twitter_api(filepath):
    with open(filepath) as f:
        d = json.load(f)
        # OAuth 2 authentication for making API requests without the user context
        # Getting read-only access to public information
        auth = tweepy.OAuthHandler(consumer_key=d['consumer_key'], 
                                   consumer_secret=d['consumer_secret'])
        auth.set_access_token(d['access_token'], d['access_token_secret'])
    # prep for streaming
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    return api


if __name__=="__main__":
    fp = '/home/user/.ssh/twitter_app_capstone.json'
    mongo_client = get_mongo_client()
    twitter_collection = get_twitter_collection(mongo_client=mongo_client)
    api = get_twitter_api(filepath=fp)
    # set the stream listener and GO!
    tweets_listener = MyStreamListener(api=api, twitter_collection=twitter_collection)
    stream = tweepy.Stream(api.auth, tweets_listener)
    try:
        print('Streaming has begun...')
        #stream.filter(track=['covid k-12', 'covid k12', 'covid k-12 remote', 'covid k12 remote', 'covid k12 online', 'covid k-12 online'], languages=['en'])
        stream.filter(track=track_terms, languages=['en'])
    except KeyboardInterrupt as e:
        print('Stopped')
    finally:
        print('Streaming is now done..')
        stream.disconnect()