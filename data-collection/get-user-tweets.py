import tweepy
import json

# Access credentials obtained from https://apps.twitter.com/app/14516752/keys
consumer_key = 'aMi2tyW2jE3zG2EUkf0GOg8uQ'
consumer_secret = 'uRpLY2In02z50zL18W736iDWkgRmo18quSSbpfecPxBVSHZ0pW'
access_token = '30427118-DEcNQWA4QUlKfTjAfR635Oa4qWoTWrd5jSERn37Sd'
access_token_secret = 'Q5ynHitpqZfY3QCZVcGAzv8qG1pIucrwMLs46ygBoC4FJ'

# OAuth process, using the keys and tokens
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# Creation of the actual interface, using authentication
api = tweepy.API(auth)
num_items = 5
twitter_handle = 'MKBHD'

# Information currently being extracted: text, entities/hashtags, user/screen_name, favourite_count, retweet_count
with open('twitter-data/{}'.format(twitter_handle), 'w') as f:
    for status in tweepy.Cursor(api.user_timeline, screen_name='@' + twitter_handle).items(num_items):
        tweet = status._json

        reqd = dict()
        reqd['screen_name'] = tweet['user']['screen_name']
        reqd['tweet_text'] = tweet['text']
        reqd['hashtags'] = tweet['entities']['hashtags']
        reqd['favorites'] = tweet['favorite_count']
        reqd['retweet_count'] = tweet['retweet_count']

        f.write(json.dumps(reqd))
        f.write('\n')