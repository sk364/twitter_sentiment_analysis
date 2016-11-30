import csv
import json
import re
import time
import twitter

#-------------------------------------------------------#


def filter_tweets(tweets):
    ''' Filters the status for specific target values from all statuses '''

    utweets = []

    for twt in tweets:
        twt = twt.AsDict()
        utwt = {}

        utwt['date_of_twt'] = twt['created_at'].encode('utf-8')
        utwt['id'] = twt['id_str'].encode('utf-8')
        utwt['text'] = twt['text'].encode('utf-8')
        utwt['lang'] = twt['lang'].encode('utf-8')

        # filter source
        utwt['source'] = (re.sub('<[^>]*>', '', twt['source'])).encode('utf-8')
        utwt['retweet_status'] = False

        utwt['reply_to_name'] = ''.encode('utf-8')
        utwt['reply_to_id'] = ''.encode('utf-8')
        if twt['user_mentions']:
            utwt['reply_to_name'] = twt['user_mentions'][
                0]['screen_name'].encode('utf-8')
            utwt['reply_to_id'] = twt['user_mentions'][0]['id']

        utweets.append(utwt)

    return utweets

#-------------------------------------------------------#


def get_name_tweets(uname):
    ''' Returns all tweets by specified user. If user name not provided, then an empty list is returned '''

    utweets = []
    lis = []

    first_twt_id = [twt.AsDict()['id']
                    for twt in api.GetUserTimeline(screen_name=uname, count=1)]
    lis.append(first_twt_id[0])

    if uname:
        for i in xrange(16):
            user_tweets = api.GetUserTimeline(
                screen_name=uname, count=200, include_rts=False, max_id=lis[-1])

            for twt in user_tweets:
                utweets.append(twt)
                lis.append(twt.AsDict()['id'])

        utweets = filter_tweets(utweets)

    return utweets

#-------------------------------------------------------#


def get_hashtag_tweets(search_tag):
    ''' Returns all statuses containing specified hashtag. If search hashtag is not provided, then an empty list is returned '''

    hashtag_tweets = []
    lis = []

    first_twt_id = [twt.AsDict()['id'] for twt in api.GetSearch(
        raw_query='q=%23' + search_tag, count=1)]
    lis.append(first_twt_id[0])

    if search_tag:
        for i in xrange(16):
            t_tweets = api.GetSearch(
                raw_query='q=%23' + search_tag, count=200, max_id=lis[-1])

            for twt in t_tweets:
                hashtag_tweets.append(twt)
                lis.append(twt.AsDict()['id'])

        hashtag_tweets = filter_tweets(hashtag_tweets)

    return hashtag_tweets

#-------------------------------------------------------#


def get_mention_tweets(uname):
    ''' Returns all mentions of specified user. If user name not provided, then an empty list is returned '''

    mention_tweets = []
    lis = []

    first_twt_id = [twt.AsDict()['id']
                    for twt in api.GetSearch(raw_query='q=%40' + uname, count=1)]
    lis.append(first_twt_id[0])

    if uname:
        for i in xrange(16):
            m_tweets = api.GetSearch(
                raw_query='q=%40' + uname, count=200, max_id=lis[-1])

            for twt in m_tweets:
                mention_tweets.append(twt)
                lis.append(twt.AsDict()['id'])

        mention_tweets = filter_tweets(mention_tweets)

    return mention_tweets

#-------------------------------------------------------#


def create_csv(uname, tweets, ftype=''):
    ' Creates a csv file '

    f = open(ftype + 'realDonaldTrump.csv', 'w')
    writer = csv.writer(f)

    writer.writerow([
        'Name', 'Twitter Handle', 'Total Tweets', 'Total Followings', 'Total Followers', 'User ID', 'User Verified', 'User Location',
        'User Description', 'Date of Tweet', 'Tweet ID', 'Tweet Text', 'Tweet Language', 'Tweet Source', 'Tweet Retweet Status',
        'Tweet Reply To Name', 'Tweet Reply To ID'
    ])

    user_info = api.GetUser(screen_name=uname).AsDict()

    name = user_info['name'].encode('utf-8')
    twitter_handle = uname.encode('utf-8')
    total_twt = user_info['statuses_count']
    total_followings = user_info['friends_count']
    total_followers = user_info['followers_count']
    user_id = user_info['id']
    verified = user_info['verified']
    location = user_info['location'].encode('utf-8')
    desc = user_info['description'].encode('utf-8')

    for twt in tweets:
        writer.writerow([
            name, twitter_handle, total_twt, total_followings, total_followers, user_id, verified, location, desc,
            twt['date_of_twt'], twt['id'], twt['text'], twt['lang'], twt[
                'source'], twt['retweet_status'], twt['reply_to_name'],
            twt['reply_to_id']
        ])

#-------------------------------------------------------#

if __name__ == '__main__':
    # initialize twitter api
    with open('config.json') as f:
        config = json.load(f)

    api = twitter.Api(consumer_key=config['consumer_key'], consumer_secret=config['consumer_secret'],
                      access_token_key=config['access_token_key'], access_token_secret=config['access_token_secret'])

    screen_name = 'realDonaldTrump'

    user_tweets = get_name_tweets(screen_name)
    create_csv(screen_name, user_tweets)
    print "realDonaldTrump.csv created!"

    hash_tweets = get_hashtag_tweets(screen_name)
    create_csv(screen_name, hash_tweets, ftype='#')
    print "#realDonaldTrump.csv created!"

    mention_tweets = get_mention_tweets(screen_name)
    create_csv(screen_name, mention_tweets, ftype='@')
    print "@realDonaldTrump.csv created!"
