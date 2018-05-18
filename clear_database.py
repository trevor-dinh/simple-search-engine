from pymongo import MongoClient
from pprint import pprint
import urllib
import json
from add_index_to_db import CONNECTION_STRING, connect_to_main_database
DEBUG = True
def drop_database(db_connection, collection_to_delete):
    if DEBUG:
        print("Clearing primary replica set of data, thanks Thanos")
    db_connection.drop_collection(collection_to_delete)
    if DEBUG:
        print("Done")




if __name__ == '__main__':
    client = MongoClient(CONNECTION_STRING)
    db = client.buisness
    db.drop_collection('reviews')
    #db = client.invertedIndexDB
    #db.drop_collection('indices')

