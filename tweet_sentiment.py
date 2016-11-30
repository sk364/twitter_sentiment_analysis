import twitter
import csv
import json
import requests
import ast
import re
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk import tokenize

#-------------------------------------------------------#

def compute_sentiment_score(data):
	' Returns the average sentiment score of all sentences in the tweet '

	sentences = tokenize.sent_tokenize(data)

	sid = SentimentIntensityAnalyzer()

	compounds = 0.0000
	for sentence in sentences:
		ss = sid.polarity_scores(sentence)
		compounds += ss['compound']

	avg_comp = (compounds*100)/len(sentences)

	if avg_comp >= 60:
		return 2

	elif avg_comp >= 20:
		return 1

	elif avg_comp <= -60:
		return -2

	elif avg_comp <= -20:
		return -1

	else:
		return 0

#-------------------------------------------------------#

def filter_tweets(tweets):
	' Filters the status for specific target values from all tweets '
	
	utweets = []

	for twt in tweets:
		twt = twt.AsDict()
		utwt = {}

		sentiment_score = compute_sentiment_score(twt['text'])

		utwt['date_of_twt'] = twt['created_at'].encode('utf-8')
		utwt['id'] = twt['id_str'].encode('utf-8')
		utwt['text'] = twt['text'].encode('utf-8')
		utwt['lang'] = twt['lang'].encode('utf-8')

		# filter source
		utwt['source'] = (re.sub('<[^>]*>', '', twt['source'])).encode('utf-8')

		utwt['retweet_status'] = False
		# doubt
		utwt['reply_to_name'] = ''.encode('utf-8')
		utwt['reply_to_id'] = ''.encode('utf-8')

		utwt['sentiment_score'] = sentiment_score

		utweets.append(utwt)

	return utweets

#-------------------------------------------------------#

def get_name_tweets(uname):
	' Returns all tweets by specified user. If user name not provided, then an empty list is returned '
	
	utweets = []
	
	if uname:	
		user_tweets = api.GetUserTimeline(screen_name=uname)

		utweets = filter_tweets(user_tweets)

	return utweets

#-------------------------------------------------------#

def get_hashtag_tweets(search_tag):
	' Returns all statuses containing specified hashtag. If search hashtag is not provided, then an empty list is returned '

	hashtag_tweets = []

	if search_tag:
		t_tweets = api.GetSearch(raw_query='q=%23'+search_tag)

		hashtag_tweets = filter_tweets(t_tweets)

	return hashtag_tweets

#-------------------------------------------------------#

def get_mention_tweets(uname):
	' Returns all mentions of specified user. If user name not provided, then an empty list is returned '
	
	mention_tweets = []

	if uname:
		m_tweets = api.GetSearch(raw_query='q=%40'+uname)

		mention_tweets = filter_tweets(m_tweets)

	return mention_tweets

#-------------------------------------------------------#

def create_csv(uname, tweets, ftype=''):
	' Creates a csv file '

	f = open(ftype+'realDonaldTrump_sentiment_analysis.csv', 'w')
	writer = csv.writer(f)

	writer.writerow([
		'Name', 'Twitter Handle', 'Total Tweets', 'Total Followings', 'Total Followers', 'User ID', 'User Verified', 'User Location',
		'User Description', 'Date of Tweet', 'Tweet ID', 'Tweet Text', 'Tweet Language', 'Tweet Source', 'Tweet Retweet Status',
		'Tweet Reply To Name', 'Tweet Reply To ID', 'Sentiment Score'
	])
	
	user_info = api.GetUser(screen_name=uname).AsDict()

        name = user_info['name'].encode('utf-8')
        twitter_handle = uname.encode('utf-8')
        total_twt = user_info['statuses_count']
        total_followings = user_info['friends_count']
        total_followers = user_info['followers_count']
        user_id = uname.encode('utf-8')
        verified = user_info['verified']
        location = user_info['location'].encode('utf-8')
        desc = user_info['description'].encode('utf-8')

	for twt in tweets:
		writer.writerow([
			name, twitter_handle, total_twt, total_followings, total_followers, user_id, verified, location, desc,
			twt['date_of_twt'], twt['id'], twt['text'], twt['lang'], twt['source'], twt['retweet_status'], twt['reply_to_name'],
			twt['reply_to_id'], twt['sentiment_score']
		])

#-------------------------------------------------------#

if __name__=='__main__':
	# initialize twitter api
	with open('config.json') as f:
		config = json.load(f)

	api = twitter.Api(consumer_key=config['consumer_key'], consumer_secret=config['consumer_secret'],
			      access_token_key=config['access_token_key'], access_token_secret=config['access_token_secret'])

	# set screen name
	screen_name = 'realDonaldTrump'

	# get all tweets
	user_tweets = get_name_tweets(screen_name)
	hash_tweets = get_hashtag_tweets(screen_name)
	mention_tweets = get_mention_tweets(screen_name)

	# create the required csv files
	create_csv(screen_name, user_tweets)
	create_csv(screen_name, hash_tweets, ftype='#')
	create_csv(screen_name, mention_tweets, ftype='@')
