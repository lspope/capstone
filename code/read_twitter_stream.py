import tweepy
import json
import pandas as pd
import re
import sys
from pymongo import MongoClient

usa_states_regex = ',\s{1}(A[KLRZ]|C[AOT]|D[CE]|FL|GA|HI|I[ADLN]|K[SY]|LA|M[ADEINOST]|N[CDEHJMVY]|O[HKR]|P[AR]|RI|S[CD]|T[NX]|UT|V[AIT]|W[AIVY])'

usa_states_fullname_regex = '(ALABAMA|ALASKA|ARIZONA|ARKANSAS|CALIFORNIA|'\
                            'COLORADO|CONNECTICUT|DELAWARE|FLORIDA|GEORGIA|HAWAII|'\
                            'IDAHO|ILLINOIS|INDIANA|IOWA|KANSAS|KENTUCKY|'\
                            'LOUISIANA|MAINE|MARYLAND|MASSACHUSETTS|MICHIGAN|'\
                            'MINNESOTA|MISSISSIPPI|MISSOURI|MONTANA|'\
                            'NEBRASKA|NEVADA|NEW\sHAMPSHIRE|NEWSJERSEY|'\
                            'NEW\sMEXICO|NEW\sYORK|NORTH\sCAROLINA|'\
                            'NORTH\sDAKOTA|OHIO|OKLAHOMA|OREGON|PENNSYLVANIA|'\
                            'RHODE\sISLAND|SOUTH\sCAROLINA|SOUTH\sDAKOTA|'\
                            'TENNESSEE|TEXAS|UTAH|VERMONT|VIRGINIA|'\
                            'WASHINGTON|WEST\sVIRGINIA|WISCONSIN|WYOMING|USA)'

track_terms = [
    'k-12 remote',
    #   'k-12 distance',
    #   'k-12 (on-line OR online)' ,
    #   'k-12 virtual',
    'k-12 hybrid',
    'k-12 in-person'
    #   'teach remote',
    #   'teach distance learn',
    #  'k-12 (on-line OR online)',
    #    'teach virtual learn',
    '(kid OR child) remote',
    #   '(kid OR child) distance learn',
    '(kid OR child) online (learn OR class OR school)',
    #    '(kid OR child) virtual learn',
    '(kid OR child) hybrid (learn OR class OR school)',
    '(kid OR child) in-person (class OR school)'
]


class MyStreamListener(tweepy.StreamListener):
    def __init__(self, api, twitter_collection, filter_retweets):
        super(MyStreamListener, self).__init__()
        self.api = api
        self.me = api.me()
        self.twitter_collection = twitter_collection
        self.filter_retweets = filter_retweets

    def on_error(self, status_code):
        print(str(status_code))
        print('Error detected')
        if status_code == 420:
            # returning False in on_data disconnects the stream
            print('420 - exceeded # attempts to connect to streaming API')
            return False

    def on_status(self, tweet):
        is_retweet = hasattr(tweet, 'retweeted_status')
        # If it is retweet check if we are filtering out retweets
        if is_retweet:
            if filter_retweets:
                print('Not storing retweets')
                return

        # Checking tweet for likely USA location
        is_usa_loc = self.get_is_usa_loc(tweet)
        if is_usa_loc:
            tweet_doc = self.get_desired_attributes(tweet)
            print(tweet_doc['user_loc'])
            print(tweet_doc['content'])
            # insert the tweet into collection
            twitter_collection.insert(tweet_doc)
        else:
            print('Could not determine USA location')

    def get_is_usa_loc(self, tweet):
        is_usa_loc = False
        if tweet.user.location:
            user_loc_str = str(tweet.user.location).upper()
            is_usa_loc = re.search(usa_states_regex, user_loc_str) or re.search(
                usa_states_fullname_regex, user_loc_str)
        return is_usa_loc

    def get_desired_attributes(self, tweet):
        id_str = tweet.id_str
        content = tweet.text
        if tweet.truncated:
            content = tweet.extended_tweet['full_text']

        user_loc = tweet.user.location
        user_screen_name = tweet.user.screen_name
        retweet_count = tweet.retweet_count
        fav_count = 0
        if hasattr(tweet, 'favorite_count'):
            fav_count = tweet.favorite_count

        created_at = tweet.created_at
        tweet_doc = {'id_str': id_str,
                     'content': content,
                     'user_loc': user_loc,
                     'user_screen_name': user_screen_name,
                     'retweet_count': retweet_count,
                     'fav_count': fav_count,
                     'created_at': created_at}
        return tweet_doc


def get_mongo_client(host='localhost', port=27017):
    mongo_client = MongoClient(host=host, port=port)
    return mongo_client


def get_twitter_collection(mongo_client):
    capstone_db = mongo_client['capstone_db']
    twitter_collection = capstone_db['streamed_tweets_starting_jan15']
    return twitter_collection


def get_twitter_api(filepath):
    with open(filepath) as f:
        d = json.load(f)
        # Getting read-only access to public information
        auth = tweepy.OAuthHandler(consumer_key=d['consumer_key'],
                                   consumer_secret=d['consumer_secret'])
        auth.set_access_token(d['access_token'], d['access_token_secret'])
    # prep for streaming
    api = tweepy.API(auth,
                     retry_count=5,
                     retry_delay=10,
                     retry_errors=set([401, 404, 500, 503]),
                     wait_on_rate_limit=True,
                     wait_on_rate_limit_notify=True)
    return api


if __name__ == "__main__":
    n = len(sys.argv)
    print('total args passed ', n)

    print("\nArguments passed:", end=" ")
    for i in range(1, n):
        print(sys.argv[i], end=" ")

    # get filter retweets flag
    filter_retweets = True
    if sys.argv[1]:
        param = sys.argv[1]
        if param == 'False':
            filter_retweets = False

    # get any track terms passed in command line
    track_terms_from_commandline = []
    for i in range(2, n):
        track_terms_from_commandline.append(sys.argv[i])

    print(track_terms_from_commandline)

    fp = '/home/user/.ssh/twitter_app_capstone.json'
    mongo_client = get_mongo_client()
    twitter_collection = get_twitter_collection(mongo_client=mongo_client)
    api = get_twitter_api(filepath=fp)

    # set the stream listener and GO!
    tweets_listener = MyStreamListener(api=api,
                                       twitter_collection=twitter_collection,
                                       filter_retweets=filter_retweets)
    stream = tweepy.Stream(api.auth, tweets_listener)
    try:
        print('Streaming has begun with filter_retweets set to ' +
              str(filter_retweets))
        track_terms_to_use = track_terms
        if n > 2:
            print('using track terms from command line')
            track_terms_to_use = track_terms_from_commandline

        stream.filter(track=track_terms_to_use, languages=['en'])
    except KeyboardInterrupt as e:
        print('Stopped')
    finally:
        print('Streaming is now done..')
        stream.disconnect()
