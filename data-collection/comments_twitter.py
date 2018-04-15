import twarc
import json
import os
import threading
import tweepy
import json
import pandas as pd

# Access credentials obtained from https://apps.twitter.com/app/14516752/keys
from time import sleep
consumer_key = 'aMi2tyW2jE3zG2EUkf0GOg8uQ'
consumer_secret = 'uRpLY2In02z50zL18W736iDWkgRmo18quSSbpfecPxBVSHZ0pW'
access_token = '30427118-DEcNQWA4QUlKfTjAfR635Oa4qWoTWrd5jSERn37Sd'
access_token_secret = 'Q5ynHitpqZfY3QCZVcGAzv8qG1pIucrwMLs46ygBoC4FJ'
file_path = 'influencer_list.csv'
num_items = 100

# OAuth process, using the keys and tokens
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# Creation of the actual interface, using authentication
api = tweepy.API(auth)

columns = ['tw_handle','tw_id_str','tw_screen_name','tw_name','tw_location','tw_description','tw_followers_count',
		   'tw_statuses_count','tw_verified','tw_tweets_file']
outdf = pd.DataFrame(columns=columns)

# Reading CSV file containing influencers' profile URLs
df = pd.read_csv(file_path, sep=',')
for index, row in df.iterrows():
	influencer = row['Influencer']
	print("Working on: {}".format(influencer))
	category = row['Category']
	twitter_url = row['Twitter']
	splits = twitter_url.split('/')
	if twitter_url:
		if twitter_url.endswith('/'):
			twitter_handle = splits[-2]
		else:
			twitter_handle = splits[-1]
	else:
		twitter_handle = None
	
	user_profile = api.get_user(screen_name = '@' + twitter_handle)._json

	file_location = 'twitter-data-comments/{}'.format(twitter_handle)
	os.makedirs(file_location)
	for status in tweepy.Cursor(api.user_timeline, screen_name='@' + twitter_handle).items(num_items):
		tweet = status._json
		id_str = tweet['id_str']
		name = twitter_handle
		# os.system("twarc replies {} > twitter-data-comments/{}/{}.jsonl".format(id_str, twitter_handle, id_str))
		replies = list()
		with open('twitter-data-comments/{}/{}.jsonl'.format(twitter_handle, id_str), 'a') as f:
			for twt in tweepy.Cursor(api.search,q='to:'+name,result_type='recent').items(100):
				if hasattr(twt, 'in_reply_to_status_id_str'):
					json.dump(twt._json, f)
					f.write('\n')
	sleep(30)
