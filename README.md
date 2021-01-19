
# WIP ALERT -- COVID-19 K-12 Learning Sentiment Classifer -- WIP ALERT

## Capstone Project
### Flatiron Online Data Science Bootcamp

Prepared and presented by: [Leah Pope](https://www.linkedin.com/in/leahspope/)

Presentation: [Coming Soon](CapstoneProject_LeahPope.pdf)

Blog: [Coming Soon](https://leahspope7.medium.com)

![tweeting](images/thomas-park-6MePtA9EVDA-unsplash.jpg)


# Introduction

COVID-19 has impacted the world in a multitude of ways, some of the most striking and visible effects in the United States occurred within K-12 education. 

For my capstone project, I want to explore the question "What is the public sentiment in the U.S. on K-12 learning during the COVID-19 pandemic?", Using data collected from Twitter, Natural Language Processing, and Supervised Machine Learning, I created a text classifier to predict the sentiment (positive/negative) of Tweets on this topic.

(EDA Goals:) I performed exploratory data analysis to uncover trends by U.S. region. I also conducted Unsupervised Machine Learning to detect specific topics in the Positive and Negative Tweets.

The Primary Stakeholders for my project are educational entities (school boards, superintendents, school administrators and educators) as well as companies (i.e., education technology, internet providers) and organizations (i.e., non-profits, academic researchers) seeking to support students engaged in remote learning. 


# Data Description
The data used in this project was collected from Twitter using [Tweepy](https://github.com/tweepy). A total of X tweets were collected, covering the dates X to Y and using the search filters X, Y, and Z.  Positive and Negative sentiment scores on the tweets were obtained with a hybrid approach of using [VADER](https://github.com/cjhutto/vaderSentiment) and [Text Blob](https://github.com/sloria/textblob) sentiment tools and human labeling. 


# EDA Questions Explored
### Question 1:
### Question 2: 
### Question 3: 
#### [Notebook](./code/data_cleaning_and_eda.ipynb)


# Binary Sentiment Classifer Modeling
### Creating binary sentiment classifiers 
#### [Notebook](./code/modeling.ipynb)


# Conclusions
## Binary Classifer - winning model
* Description: X Score of __0.XX__

More details go here.

If multiple, show breakdown of all considered Models and scores:
* 1 - 0.X
* 2 - 0.X  


# Stakeholder Recommendations
After analyzing X, I can make the following Stakeholder Recommendations:

Recommendation 1 
* 1

Recommendation 2
* 1

Recommendation 3
* 3


# Next Steps/Future Work
Futher analysis into the following areas could yield additional insights.

* Item 1
* Item 2


# For More Information
* Review the non-technical presentation [Coming Soon](CapstoneProject_LeahPope.pdf)
* Contact the author [Leah Pope](https://www.linkedin.com/in/leahspope/)


# Repository Structure
```
--code
----twitter_data_pull
-------X
----data_cleaning_and_eda.ipynb
----modeling.ipynb 
--data
----X
--images (dir for images)
```
