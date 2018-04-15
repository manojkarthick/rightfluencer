import json
from os import listdir
from os.path import isfile, join
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
def get_handle(twitter_url):
	splits=twitter_url.split('/')

	if twitter_url:
		if twitter_url.endswith('/'):
			twitter_handle = splits[-2]
		else:
			twitter_handle = splits[-1]
	else:
		twitter_handle = None
	return twitter_handle

# Change the below three variables accordingly.
db = client.influencers_db
collection = db.influencers_list_collection

file_name = '/Users/manojkarthick/Documents/Spring-18/CMPT-733/Project-733/influencers-project/data/influencer_list.csv'
fp = open(file_name, 'r')
inf_list = [line for line in fp.readlines()]
for data in inf_list:
	line = data.split(',')

	my_dict = dict()
	my_dict['name'] = line[0]
	my_dict['category'] = line[1]
	my_dict['tw_handle'] = get_handle(line[2])
	my_dict['twitter_url'] = line[2]
	my_dict['facebook_url'] = line[3]
	my_dict['instagram_url'] = line[4]
	my_dict['youtube_url'] = line[5]

	result = collection.insert_one(my_dict)
	print(result)