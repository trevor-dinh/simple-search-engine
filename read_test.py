from pymongo import MongoClient
from pprint import pprint
import urllib
from add_index_to_db import CONNECTION_STRING

if __name__ == '__main__':
    client = MongoClient(CONNECTION_STRING)
    db = client.invertedIndexDB
    collection = db.indices
    cursor = collection.find({})
    print(collection.count())
    #Source: https://stackoverflow.com/a/34598654
    # for document in cursor:  
    #     pprint(document)
    print(collection.find_one({"token" : "irvine"})) 


    #Source: http://api.mongodb.com/python/current/tutorial.html#getting-a-single-document-with-find-one

