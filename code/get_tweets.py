import tweepy
import pandas
import jsonpickle



# Variables that contains the credentials to access Twitter API
ACCESS_TOKEN = 'your_access_token'
ACCESS_SECRET = 'your_access_secret'
CONSUMER_KEY = 'your_consumer_key'
CONSUMER_SECRET = 'your_consumer_secret'


# Setup access to API
def connect_to_twitter_OAuth():
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

    api = tweepy.API(auth)
    return api


def get_tweets(filepath, api, query, max_tweets=1000000, lang='pt'):
    tweetCount = 0

    # Open file and save tweets
    with open(filepath, 'w') as f:

        # Send the query
        for tweet in tweepy.Cursor(api.search,
                                   q=query,
                                   lang=lang).items(max_tweets):

            # Convert to JSON format
            f.write(jsonpickle.encode(tweet._json, unpicklable=False) + '\n')
            tweetCount += 1

        # Display how many tweets we have collected
        print("Downloaded {0} tweets".format(tweetCount))


query = '#covid OR #covid19 OR #corona AND ' \
        '#k12 OR #k-12 OR'
        '#remotelearning OR #distancelearning OR' \
        '#remoteteaching OR #distanceteaching' 

# Create API object
api = connect_to_twitter_OAuth()
