import tweepy
import json
import pandas as pd

# Access credentials obtained from https://apps.twitter.com/app/14516752/keys
consumer_key = 'aMi2tyW2jE3zG2EUkf0GOg8uQ'
consumer_secret = 'uRpLY2In02z50zL18W736iDWkgRmo18quSSbpfecPxBVSHZ0pW'
access_token = '30427118-DEcNQWA4QUlKfTjAfR635Oa4qWoTWrd5jSERn37Sd'
access_token_secret = 'Q5ynHitpqZfY3QCZVcGAzv8qG1pIucrwMLs46ygBoC4FJ'

# Modify file path as required
file_path = '/Users/manojkarthick/Documents/Spring-18/CMPT-733/Project/influencers-project/data/influencer_list.csv'

# Number of tweets needed from the user 
num_items = 500

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
    
    print("Operating on twitter handle:{}".format(twitter_handle))

    user_profile = api.get_user(screen_name = '@' + twitter_handle)._json

    file_location = 'twitter-data/{}'.format(twitter_handle)
    with open(file_location, 'w') as f:
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
    
    print("Finished reading {} tweets for twitter handle:{}".format(num_items, twitter_handle))

    result_list = [twitter_handle, user_profile['id_str'], user_profile['screen_name'], user_profile['name'],
                       user_profile['location'], user_profile['description'], user_profile['followers_count'], 
                       user_profile['statuses_count'], user_profile['verified'], file_location]
    
    print("Finished reading user information for twitter handle:{}".format(twitter_handle))

    outdf.loc[index] = result_list

    print("DONE for user:{}".format(index))

print("Writing out result for all users into CSV...")

outdf.to_csv('twitter_influencers_details.csv', sep=';', index=False)