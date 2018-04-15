import pandas as pd
import os

import google.oauth2.credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow

# The CLIENT_SECRETS_FILE variable specifies the name of a file that contains
# the OAuth 2.0 information for this application, including its client_id and
# client_secret.
CLIENT_SECRETS_FILE = "client_secret.json"

# This OAuth 2.0 access scope allows for full read/write access to the
# authenticated user's account and requires requests to use an SSL connection.
SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'

def get_authenticated_service():
  flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
  credentials = flow.run_console()
  return build(API_SERVICE_NAME, API_VERSION, credentials = credentials)

def get_channel_information(service, **kwargs):
  results = service.channels().list(
    **kwargs
  ).execute()
  
  return (results['items'][0]['id'],
        results['items'][0]['snippet']['title'],
        results['items'][0]['statistics']['viewCount'],
        results['items'][0]['statistics']['commentCount'],
        results['items'][0]['statistics']['subscriberCount'],
        results['items'][0]['statistics']['videoCount'])

df = pd.read_csv('influencer_list.csv')

columns = ['tw_handle','yt_url','yt_title', 'yt_channel_id','yt_user_id','yt_subscriber_count',
           'yt_view_count','yt_video_count']
outdf = pd.DataFrame(columns=columns)

def get_last_part(url):
    splits = url.split('/')
    if url:
        if url.endswith('/'):
            last_part = splits[-2]
        else:
            last_part = splits[-1]
    else:
        last_part = None    
    return last_part

for index, row in df.iterrows():
    twitter_url = row['Twitter']
    tw_handle = get_last_part(twitter_url)
    youtube_url = row['Youtube']
    yt_url = youtube_url
    if 'channel' in youtube_url:
        yt_channel_id = get_last_part(yt_url)
        result = get_channel_information(service,
          part='snippet,contentDetails,statistics',
          id=yt_channel_id)
    elif 'user' in youtube_url:
        yt_user_id = get_last_part(yt_url)
        result = get_channel_information(service,
          part='snippet,contentDetails,statistics',
          forUsername=yt_user_id)
    else:
        yt_channel_id = None
        yt_user_id = None
    
    yt_channel_id = result[0]
    yt_title = result[1]
    yt_view_count = result[2]
    yt_comment_count = result[3]
    yt_subscriber_count = result[4]
    yt_video_count = result[5]
    
    result_list = [tw_handle, yt_url, yt_title, yt_channel_id, yt_user_id, yt_subscriber_count, 
                   yt_view_count, yt_video_count]
    outdf.loc[index] = result_list

outdf.to_csv('youtube_influencers_details.csv', sep=';', index=False)