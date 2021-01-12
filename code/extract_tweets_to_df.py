import json
import pandas as pd
from pymongo import MongoClient
from datetime import datetime


def get_mongo_client(host='localhost', port=27017):
    mongo_client = MongoClient(host=host, port=port)
    return mongo_client

def get_twitter_collection(mongo_client):
    capstone_db = mongo_client['capstone_db']
    twitter_collection = capstone_db['tweets']
    return twitter_collection

def export_tweets_to_dataframe(twitter_collection, filename):
    df = pd.DataFrame(list(twitter_collection.find({})))  #select * from tweet_collection
    print(df.shape)
    df.to_csv(filename)

if __name__=="__main__":
    mongo_client = get_mongo_client()
    twitter_collection = get_twitter_collection(mongo_client=mongo_client)
    original_count = twitter_collection.count_documents({})

    current_count = twitter_collection.count_documents({})
    print(f'Fetching {current_count} tweets from MongoDb...collected from filtered Twitter Stream.')

    # Converting datetime object to string
    dateTimeObj = datetime.now()
    timestampStr = dateTimeObj.strftime('%d_%b_%Y_%H_%M')
    timestamped_filename = 'collected_tweets_' + timestampStr + '.csv'
    print(timestamped_filename)
    export_tweets_to_dataframe(twitter_collection=twitter_collection, filename=timestamped_filename)