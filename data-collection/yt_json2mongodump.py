import csv
import os
from os import listdir
from os.path import join
import json
import re

# this program converts youtube API responses into a file in which each row is like a json
# response which we feed into MongoDB. 

# INPUT:: sample file content:
# Influencer, Category, Twitter, Facebook, Instagram, Youtube
# here we only use influencer name, category and Youtube channel/user id

# OUTPUT:: it creates as many files as the number of influencers in influencer_list.csv and put
# all of these files inside a folder called '<Influencer Name>'


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

def dumpyoutubejson(folder, jsonfilename):
	with open(join('export', jsonfilename), 'w') as output_file:
		for filename in os.listdir(folder):
			if filename.endswith('.json'):
					with open(join(folder, filename)) as json_data:
						data = json.load(json_data)
						data = data['items'][0]

						video_id = data.get('id')
						likes = data.get('statistics').get('likeCount')
						dislikes = data.get('statistics').get('dislikeCount')
						comments = data.get('statistics').get('commentCount')
						views = data.get('statistics').get('viewCount')
						title = data.get('snippet').get('title')
						description = data.get('snippet').get('description')
						tags = data.get('snippet').get('tags')
						publishat = data.get('snippet').get('publishedAt')
						cc_filename = re.sub('[^A-Za-z0-9]+', '', title).lower() + '_' + video_id
						my_dictionary = {
						'twitter_handle' : jsonfilename,
						'video_id' : video_id,
						'likes' : likes,
						'dislikes' : dislikes,
						'comments' : comments,
						'views' : views,
						'title' : title,
						'description' : description,
						'tags' : tags,
						'publishat' : publishat,
						'cc_filename' : cc_filename
						}
						# write row_dict to username.json file
						output_file.write(json.dumps(my_dictionary) + '\n')


def main():
	with open('influencer_list.csv') as csvfile:
	    readCSV = csv.reader(csvfile, delimiter=',')
	    for row in list(readCSV)[1:]:
	        influencer_name = row[0].replace(" ", "")
	        twitter_handle = row[2]
	        twitter_handle = get_handle(twitter_handle)
	        category = row[1]

	        if category == 'Travel': # we are doing it for TRAVEL category here, change it according to inputs
	        	if row[5] != 'null':
		        	dumpyoutubejson(influencer_name, twitter_handle)


if __name__ == "__main__":
    main()