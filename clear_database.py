from pymongo import MongoClient
from pprint import pprint
import urllib
from add_index_to_db import CONNECTION_STRING

if __name__ == '__main__':
	client = MongoClient(CONNECTION_STRING)
	db = client.invertedIndexDB
	db.drop_collection('indices')

