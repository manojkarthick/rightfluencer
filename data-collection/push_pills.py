import json
from os import listdir
from os.path import isfile, join
from pymongo import MongoClient

client = MongoClient('localhost', 27017)

db = client.influencers_db
collection = db.pills_collection

file_name = 'topic_pills'
fp = open(file_name, 'r')
pills_data = [line for line in fp.readlines()]
for data in pills_data:
    json_data = json.loads(data)
    result = collection.insert_one(json_data)
    print(result)