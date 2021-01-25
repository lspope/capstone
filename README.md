
# Learning During COVID - Sentiment Classifer


Flatiron Online Data Science Bootcamp __Capstone Project__

Prepared and presented by: [Leah Pope](https://www.linkedin.com/in/leahspope/)

Presentation: [Coming Soon](CapstoneProject_LeahPope.pdf)

Blog: [Coming Soon](https://leahspope7.medium.com)

![education_during_covid_image](images/thomas-park-6MePtA9EVDA-unsplash.jpg)


# Introduction
COVID-19 has impacted the world in a multitude of ways. Some of the most striking and wide-reaching effects in the United States occurred within K-12 education. My Data Science Capstone Project explores the question "What is the public sentiment in the United States on K-12 learning during the COVID-19 pandemic?".

Using data collected from Twitter, Natural Language Processing, and Supervised Machine Learning, I created a text classifier to predict the sentiment (Positive, Negative, or Neutral) of Tweets on this topic.

I performed exploratory data analysis to uncover sentiment and engagement trends. I also conducted Unsupervised Machine Learning to identify topics within the Positive, Negative, and Neutral tweets.

I created this project with the following Stakeholders in mind, educational entities and personnel (i.e., school boards, superintendents, school administrators and educators) as well as companies (i.e., education technology, internet providers) and organization (i.e., non-profits, academic researchers) seeking to support K-12 students as the US navigates the COVID-19 pandemic.



# Data Description and Preparation
I collected data from Twitter using [Tweepy](https://github.com/tweepy) and used previously collected Twitter data from the [Tweets about distance learning](https://www.kaggle.com/barishasdemir/tweets-about-distance-learning) dataset shared on Kaggle.  After combining the two datasets and filtering out non-US locations, a total of 30,599 Tweets were used. 

Positive, Negative, and Neutral sentiment labels for the Tweets were obtained using a hybrid approach combining the [VADER](https://github.com/cjhutto/vaderSentiment) and [Text Blob](https://github.com/sloria/textblob) sentiment tools with (limited) human labeling. 

See the [Data Prep Notebook](./code/data_prep.ipynb) for additional information on data collection and preparation. 



# Sentiment Classifer Modeling
In the [Model Experimentation Notebook](./code/model_playground.ipynb), I trained three different multiclass classifers (RandomForest, SGDClassifier, and LinearSCV).  I used weighted F1 score as the performance metric, and ultimately selected the LinearSVC model for further tuning.

In the [Final Model Notebook](./code/modeling.ipynb), I performed hyperparameter tuning using GridSearchCV, resulting in a multiclass classifer with the following performance:
* Weighted F1 score of __0.94__ 
* Positive class F1 score of 0.97 
* Neutral class F1 score of 0.90
* Negative class F1 score of 0.83



# EDA Questions Explored
I performed [EDA](./code/eda.ipynb) on various sentiment breakdowns (see Questions 1,2, and 3). I also performed [Corpus EDA](./code/corpus_eda.ipynb) using Unsupervised Learning (LatentDirichletAllocation) to perform Topic Modeling (see Question 4).

#### Question 1: What is the general sentiment breakdown for the collected Tweets?
#### Question 2: What is the Breakdown of Tweets by US Geographic Region and by State in each Region?
#### Question 3: What is the Sentiment Breakdown of Tweets by US Geographic Region and by State in each Region?
#### Question 4: What are the Topics for Positive, Negative, and Neutral Tweets in the US, in the Southeast Region, and in the state of Alabama?



# Recommendations
My recommendations are for the Education-focused Stakeholders identified in the Introduction and for Data Scientists seeking to expand upon this work.

### Recommendation 1
* Audience: Education-focused Stakeholders
* The number of Positive sentiment Tweets is substainally higher than the other sentiment classes in every State, in every Region. This initial analysis suggests that Twitter is being used across the US to communicate positive information and statements on Education during COVID. I recommend that Stakeholders explore the [Topic Modeling analysis](./code/corpus_eda.ipynb) of these Positive Tweets for additional insight. 

### Recommendation 2
* Audience: Audience: Education-focused Stakeholders
* EDA on the breakdown of Tweets by State in each Region identified two areas of concern. 
    * ___2 of the 5__ Regions have a 'leading' State that far exceeds the others in number of Tweets. The leading state in the _West_ and _Southwest_ Regions have more than __twice__ the number of Tweets of the 'next-in-line' State I Recommend that Education-focused Stakeholders take into consideration that these Regions may be over-representing the 'leading' state. Region/State population analysis is most likely required.
    * __3 of the 5__ Regions had States that provided > 1% of Tweets for the Region. This occured in the _West_ (Montana, Alaska, and Wyoming), _Northeast_ (Delaware), and _Midwest_ (North and South Dakota). I recommend that Stakeholders take into consideration that these States, in particular, may be under-represented in the Region. State population analysis is most likely required.

### Recommendation 3
* Audience: Data Scientists seeking to expand this work
* The collected data has a class imbalance issue with 73.9% of the data labeled as Positive. Make sure any hyperparameter tuning uses the 'balanced' class_weight for LinearSVC or any other classification algorithm you may choose to experiment with. If class_weight 'balanced' is not an option, consider using RandomOverSampling to address the imbalance.



# Future Work
* Create a dashboard/app that would allow the user to select specific Regions and/or States for Topic Modeling. Also allow for setting the desired number of topics and top word count. 
* Create a dashboard/app to classify Tweets from the live Twitter stream. Allow the user to stream for Tweets for the entire United States, or selected US Region(s) or selected US State(s).
* Continue to collect Tweets over a longer timespan and update model.
* Improve the regex code used to detect a 'likely' United States location from the Tweet User-provided Location string.



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
