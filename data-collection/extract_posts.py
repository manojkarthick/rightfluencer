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
        
df = pd.read_csv('influencer_list.csv')
for index, row in df.iterrows():
    influencer = row['Influencer']
    category = row['Category']
    
    twitter_url = row['Twitter']
    twitter_handle = get_handle(twitter_url)
    
    instagram_url = row['Instagram']
    
    if instagram_url != 'null':
        instagram_handle = get_handle(instagram_url)
        json_location = 'instagram_data/{}/{}/{}.json'.format(category.lower(), instagram_handle, instagram_handle)

        f = open(json_location, 'r')
        items = json.load(f)
        f.close()
        
        outfile_location = 'instagram-data/{}'.format(twitter_handle)
        with open(outfile_location, 'w') as insta_file:
            for item in items:
                post = dict()

                post['twitter_handle'] = twitter_handle
                post['instagram_handle'] = instagram_handle

                try:
                    post['likes'] = item['edge_media_preview_like']['count']
                except (KeyError, IndexError) as err:
                    post['likes'] = None

                try:
                    post['comments'] = item['edge_media_to_comment']['count']
                except (KeyError, IndexError) as err:
                    post['comments'] = None

                try:
                    post['hashtags'] = item['tags']
                except (KeyError, IndexError) as err:
                    post['hashtags'] = None

                try:
                    post['caption'] = item['edge_media_to_caption']['edges'][0]['node']['text']
                except (KeyError, IndexError) as err:
                    post['caption'] = None

                try:
                    post['timestamp'] = item['taken_at_timestamp']
                except (KeyError, IndexError) as err:
                    post['timestamp'] = None

                try:
                    post['image_thumbnail'] = item['thumbnail_src']
                except (KeyError, IndexError) as err:
                    post['image_thumbnail'] = None
                
                insta_file.write(json.dumps(post))
                insta_file.write('\n')