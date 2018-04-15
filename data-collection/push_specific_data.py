import json
from os import listdir
from os.path import isfile, join
from pymongo import MongoClient

client = MongoClient('localhost', 27017)

def dump_data(path):    
    files = [f for f in listdir(path) if isfile(join(path, f))]
    if '.DS_Store' in files:
        files.remove('.DS_Store')

    for f in files:
        file_name = join(path, f)
        fp = open(file_name, 'r')
        twitter_data = [line for line in fp.readlines()]
        for data in twitter_data:
            json_data = json.loads(data)
            collection.insert_one(json_data)


# Change the below three variables accordingly.
db = client.influencers_db
collection = db.instagram_collection
path = '/Users/manojkarthick/Documents/Spring-18/CMPT-733/Project/instagram-data/'

dump_data(path)