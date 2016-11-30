# About

Implementing python twitter API wrapper "python-twitter" to get a user's tweets, mentions and hashtags to store it in a csv file.
Also, implementing nltk vader to get sentiments of every tweet.

# Installation

Run the following command with root privileges to install all dependencies

pip install -r requirements.txt

Then you will be needing to install nltk's data

In the python interpreter, run the following command

>> import nltk

>> nltk.download()

# Run the Code

python tweet.py

& to get sentiment score csv's

python tweet_sentiment.py

You will get three different csv files containing tweets by user, tweets mentioning the user and tweets containing hashtag of user. And three more when you run the sentiment analysis code.
