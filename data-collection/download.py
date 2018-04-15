# Image downloader
import logging
import requests
import pandas as pd
from os import listdir
from os.path import isfile, join
import os

LOG_FILENAME = 'instagram_downloader_log.out'
logging.basicConfig(
    filename=LOG_FILENAME,
    level=logging.ERROR,
)

path = 'instagram-data'
instagram_files = [f for f in listdir(path) if isfile(join(path, f)) and (not f.startswith('.'))]

counter = 0
for instagram_file in instagram_files:
    file_name = join(path, instagram_file)
    df = pd.read_json(file_name, lines=True)
    directory = 'instagram-images/{}'.format(instagram_file)
    if not os.path.exists(directory):
    	os.makedirs(directory)
    for index, row in df.iterrows():
        image_url = row['image_thumbnail']
        response = requests.get(image_url, stream=True)
        if not response.ok:
            logging.error('Response {};Influencer:{};URL:{}'.format(
            response, instagram_file, image_url))
        else:
            with open('instagram-images/{}/{}_{}.jpg'.format(instagram_file, instagram_file, index), 'wb') as handle:
                for block in response.iter_content(1024):
                    if not block:
                        break
                    handle.write(block)
            # logging.debug('SUCCESS;Influencer:{};URL:{};index:{}'.format(
            # response, instagram_file, image_url, index))
    print("Done for: {}".format(instagram_file))