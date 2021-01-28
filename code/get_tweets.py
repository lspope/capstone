import tweepy
import json
import pandas as pd
import re
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

query_list = [
    'k-12 remote',
    'k-12 distance',
    'k-12 (online OR on-line)',
    'k-12 virtual',
    'k-12 hybrid',
    'teach remote learn',
    'teach distance learn',
    'teach (on-line OR online) learn',
    'teach virtual learn',
    'teach hybrid learn',
    '(kid OR child) remote learn',
    '(kid OR child) distance learn',
    '(kid OR child) (on-line OR online) learn',
    '(kid OR child) virtual learn',
    '(kid OR child) hybrid learn'
]

query_operators = ' -filter:retweets'


def get_mongo_client(host='localhost', port=27017):
    mongo_client = MongoClient(host=host, port=port)
    return mongo_client


def get_twitter_collection(mongo_client):
    capstone_db = mongo_client['capstone_db']
    twitter_collection = capstone_db['queried_tweets_before_jan_14']
    return twitter_collection


def get_twitter_api(filepath):
    with open(filepath) as f:
        d = json.load(f)
        auth = tweepy.OAuthHandler(consumer_key=d['consumer_key'],
                                   consumer_secret=d['consumer_secret'])
        auth.set_access_token(d['access_token'], d['access_token_secret'])

    api = tweepy.API(auth,
                     retry_count=5,
                     retry_delay=10,
                     retry_errors=set([401, 404, 500, 503]),
                     wait_on_rate_limit=True,
                     wait_on_rate_limit_notify=True)
    return api


def get_desired_attributes(tweet):
    id_str = tweet.id_str
    content = tweet.full_text
    if tweet.truncated:
        content = tweet.extended_tweet.full_text

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


def get_tweets(api, query):

    for tweet in tweepy.Cursor(api.search,
                               tweet_mode='extended',
                               q=query,
                               lang='en',
                               result_type='mixed',
                               before='2021-01-14',
                               include_rt=False,
                               timeout=999999).items(2000):

        if tweet.user.location:
            print(f'{tweet.user.screen_name}:{tweet.user.location}:{tweet.full_text}')
            user_loc_str = str(tweet.user.location).upper()
            found_usa_state = re.search(usa_states_regex, user_loc_str) or re.search(
                usa_states_fullname_regex, user_loc_str)
            if found_usa_state:
                if hasattr(tweet, 'retweeted_status'):
                    print('Not storing Retweets')
                else:
                    print(user_loc_str)
                    twitter_collection.insert(get_desired_attributes(tweet))


if __name__ == "__main__":
    fp = '/home/user/.ssh/twitter_app_capstone.json'

    mongo_client = get_mongo_client()
    twitter_collection = get_twitter_collection(mongo_client=mongo_client)
    original_count = twitter_collection.count_documents({})

    api = get_twitter_api(filepath=fp)

    for item in query_list:
        get_tweets(api=api, query=item+query_operators)

    new_count = twitter_collection.count_documents({})
    print(f"added {new_count-original_count}")
