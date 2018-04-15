from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
import csv
import json


def get_handle(url):
    splits = url.split('/')
    if url:
        if url.endswith('/'):
            handle = splits[-2]
        else:
            handle = splits[-1]
    else:
        handle = None    
    return handle
        
columns = ['tw_handle','ig_handle','ig_followers', 'ig_following', 'ig_posts', 'ig_thumbnail_url']
outdf = pd.DataFrame(columns=columns)

    
df = pd.read_csv('influencer_list.csv')
for index, row in df.iterrows():
    influencer = row['Influencer']
    category = row['Category']
    
    twitter_url = row['Twitter']
    twitter_handle = get_handle(twitter_url)
    
    instagram_url = row['Instagram']

    if instagram_url != 'null':
        instagram_handle = get_handle(instagram_url)
        
        response = requests.get(instagram_url)
        soup = BeautifulSoup(response.text, 'html.parser')

        metas = soup.find_all('meta')
        description = [ meta.attrs['content'] for meta in metas if 'name' in meta.attrs and meta.attrs['name'] == 'description' ][0]
        numbers = re.findall(r'\d+', description)

        followers = numbers[0]
        following = numbers[1]
        posts = numbers[2]

        thumbnail_url = soup.find("meta",  property="og:image")['content']

        result_list = [twitter_handle, instagram_handle, followers, following, posts, thumbnail_url]
        outdf.loc[index] = result_list

outdf.to_csv('instagram_influencers_details.csv', sep=';', index=False)