import glob
import ntpath
import os
import json

from pymongo import MongoClient
from bson import Binary, Code

DATABASENAME = 'mongo_db'
TEST = False

client = MongoClient('localhost', 27017)
if not TEST:
	db = client[DATABASENAME]



files = ['business.json','checkin.json','review.json','tip.json','user.json']
def add_2D_location(json):
    if 'longitude' in json and 'latitude' in json:
        loc = [json['longitude'],json['latitude']]
        json['loc'] = loc
    return json
for file in files:
	name,ext  = file.split('.')
	collection_name = 'yelp.'+name
	print(collection_name)

	if not TEST:
		collection = db[collection_name]
	if not TEST:
		result = collection.delete_many({})
	f = open(file)
	for line in f:
		line = add_2D_location(json.loads(line))
		if not TEST:
			collection.insert(line)
    
