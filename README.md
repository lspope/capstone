
# WIP ALERT -- COVID-19 K-12 Learning Sentiment Classifer -- WIP ALERT

## Capstone Project
### Flatiron Online Data Science Bootcamp

Prepared and presented by: [Leah Pope](https://www.linkedin.com/in/leahspope/)

Presentation: [Coming Soon](CapstoneProject_LeahPope.pdf)

Blog: [Coming Soon](https://leahspope7.medium.com)

![education_during_covid_image](images/thomas-park-6MePtA9EVDA-unsplash.jpg)

# Introduction
COVID-19 has impacted the world in a multitude of ways, some of the most striking and wide-reaching effects in the United States occurred within K-12 education. 

For my capstone project, I want to explore the question "What is the public sentiment in the US on K-12 learning during the COVID-19 pandemic?".

Using data collected from Twitter, Natural Language Processing, and Supervised Machine Learning, I created a text classifier to predict the sentiment (Positive, Negative, or Neutral) of Tweets on this topic.

I performed exploratory data analysis to uncover trends by US region. I also conducted Unsupervised Machine Learning to detect topics in the tweets.

I created my project with the following Stakeholders in mind, educational entities and personnel (school boards, superintendents, school administrators and educators) as well as companies (i.e., education technology, internet providers) and organization (i.e., non-profits, academic researchers) seeking to support K-12 students as the US navigates the COVID-19 pandemic.


# Data Description and Preparation
The data used in this project was collected from Twitter using [Tweepy](https://github.com/tweepy). The data is from both an external data source and data the I collected myself.  The exernal data is from Kaggle [Tweets about distance learning] (https://www.kaggle.com/barishasdemir/tweets-about-distance-learning).  A total of 38,392 tweets were collected. 

Positive, Negative, and Neutral sentiment scores on the Tweets were obtained with a hybrid approach of using [VADER](https://github.com/cjhutto/vaderSentiment) and [Text Blob](https://github.com/sloria/textblob) sentiment tools with some (limited) human labeling. 

See the [Data Prep Notebook](./code/data_cleaning_and_eda.ipynb) for additional information on data collection and preparation. 


# Sentiment Classifer Modeling
I experimented with multiple classification models, used the weighted F1 score as the performance metric, and ultimately selected LinearSVC. I performed hyperparameter tuning using GridSearchCV to train the final model with the following performance.
* Weighted F1 score of 0.94 
* Positive class F1 score of 0.97 
* Neutral class F1 score of 0.90
* Negative class F1 score of 0.83

### [Experimentation Notebook](./code/modeling.ipynb)
### [Final Model Notebook](./code/modeling.ipynb)



# EDA Questions Explored
I performed exploratory data analysis on various sentiment breakdowns. I also performed exploratory data analysis on the corpus using Topic Modeling.

### Question 1: What is the general sentiment breakdown for the collected Tweets?
### Question 2: What is the Breakdown of Tweets by US Geographic Region and by State in each Region?
### Question 3: What is the Sentiment Breakdown of Tweets by US Geographic Region and by State in each Region?
### [EDA Notebook](./code/eda.ipynb)

### Question 4: What are the Topics for Positive, Negative, and Neutral Tweets in the US, in the Southeast Region, and in the state of Alabama?
### [EDA Notebook](./code/corpus_eda.ipynb)



# Recommendations
My recommendations are for both technical and non-technical stakeholders.

### Recommendation 1
* Audience: Data Scientists seeking to expand this work
* The collected data has a class imbalance issue with 73.9% of the data labeled as Positive. Make sure any hyperparameter tuning uses the 'balanced' class_weight for LinearSVC or any other classification algorithm you may choose to experiment with. If class_weight 'balanced' is not an option, consider using RandomOverSampling to address the imbalance.

### Recommendation 2
* Audience: Data Scientists seeking to expand this work
* Topic Modeling complements the Sentiment Classifer and provides contextual insight into the words and terms that people are using in the various Positive, Negative or Neutral Tweets.  I recommend using Topic Modeling instead of Word Clouds based on frequent words/terms to provide a more organized method of presenting contextual insight

### Recommendation 3
* Audience: Educational entities
* NOTE:CHOSE A SINGLE ONE FROM THE EDA SECTION



# Future Work
* Create a dashboard/app that would allow the user to select specific Regions and/or States for Topic Modeling. Also allow for setting the desired number of topics and top word count. 
* Create a dashboard/app to classify tweets from the live Twitter stream. Allow the user to stream for Tweets for the entire United States,or selected US region(s) or selected US state(s).
* Continue to collect Tweets over a longer timespan and update model.
* Improve the regex code to detect a 'likely' United States location from the Tweet User-provided Location string.


# For More Information
* Review the non-technical presentation [Coming Soon](CapstoneProject_LeahPope.pdf)
* Contact the author [Leah Pope](https://www.linkedin.com/in/leahspope/)


# Repository Structure
```
--code
----get_tweets.py
----read_twitter_stream.py
----extract_tweets_to_df.py
----data_prep.ipnyb
----eda.ipynb
----corpus_eda.ipynb (topic modeling on the tweet corpus)
----modeling_playground.ipynb  (experimentation on different modeling options)
----modeling.ipynb (final sentiment classifier modeling)
--data (dir for all data files ingested/generated)
--images (dir for images)
```
