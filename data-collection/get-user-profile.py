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
screen_name = 'MKBHD'

user_profile = api.get_user(screen_name = '@' + screen_name)._json
user = dict()

# Extracting the following information
user['id_str'] = user_profile['id_str']
user['screen_name'] = user_profile['screen_name']
user['name'] = user_profile['name']
user['location'] = user_profile['location'] 
user['description'] = user_profile['description']
user['followers_count'] = user_profile['followers_count']
user['statuses_count'] = user_profile['statuses_count']
user['verified'] = user_profile['verified']

with open('twitter-data/{}-profile'.format(screen_name), 'w') as f:
    f.write(json.dumps(user))