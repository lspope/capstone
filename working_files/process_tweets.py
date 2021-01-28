from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from textblob import TextBlob


 # Get the VADER sentiments
analyzer = SentimentIntensityAnalyzer()



def get_vader_sentiment(analyzer, tweet):
    tweet = tweet.replace('#','')  # we want things like #fail to be included in text
    vader_scores = analyzer.polarity_scores(tweet)
    
    compound_score = vader_scores['compound']
    vader_sentiment = None
    # using thresholds from VADER developers/researchers
    if (compound_score >= 0.05):
        vader_sentiment = 'positive'
    elif (compound_score < 0.05 and compound_score > -0.05):
        vader_sentiment = 'neutral'
    elif (compound_score <= -0.05):
        vader_sentiment = 'negative'
    return vader_sentiment


def get_text_blob_sentiment_(tweet):
    polarity = TextBlob(tweet).sentiment.polarity
    subjectivity = TextBlob(tweet).sentiment.subjectivity  # get this to help with filtering?
    # The polarity score is a float within the range [-1.0, 1.0]. 
    textblob_sentiment = None
    if (polarity > 0):
        textblob_sentiment = 'positive'
    elif (polarity == 0):
        textblob_sentiment = 'neutral'
    elif (polarity < 0):
        textblob_sentiment = 'negative'
    return textblob_sentiment    


def remove_pattern(input_txt, pattern):
    r = re.findall(pattern, input_txt)
    for i in r:
        input_txt = re.sub(i, '', input_txt)        
    return input_txt


def clean_tweet_one(tweet):
    # remove twitter Return handles (RT @xxx:)
    tweet = np.vectorize(remove_pattern)(tweet, "RT @[\w]*:") 
    
    # remove twitter handles (@xxx)
    tweet = np.vectorize(remove_pattern)(tweet, "@[\w]*")
    
    # remove URL links (httpxxx)
    tweet = np.vectorize(remove_pattern)(tweet, "https?://[A-Za-z0-9./]*")
    
    # remove special characters, numbers, punctuations (except for #)
    tweet = np.core.defchararray.replace(tweet, '[^a-zA-Z]','')
    
    return tweet


def clean_tweet(tweet):
    ''' Clean up the tweet text '''

    # remove hyperlinks
    # to remove links that start with HTTP/HTTPS inthe tweet
    url_regex =  "https?://[A-Za-z0-9./]*"
  
    tweet = re.sub(r'https?://[A-Za-z0-9./]*', '', tweet, flags=re.MULTILINE)
    # remove special characters, numbers, punctuations (except for #)
    twees = np.core.defchararray.replace(tweet, '[^a-zA-Z]', " ")
   
    return tweet