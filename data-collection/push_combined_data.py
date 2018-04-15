import pandas as pd
from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.influencers_db
collection = db.combined_collection

df = pd.read_csv('combined_influencers_details.csv', sep=';')
records = df.to_dict(orient='records')

result = collection.insert_many(records)