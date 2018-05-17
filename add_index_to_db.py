from pymongo import MongoClient
from pprint import pprint
import urllib
from tokenize_document import TokenizeDocument
from reduce_index import ReduceIndex
import os
import datetime
USERNAME = "***REMOVED***"
PASSWORD = "***REMOVED***"
CONNECTION_STRING =  ***REMOVED***.format(
    urllib.quote(USERNAME), urllib.quote(PASSWORD))
DEBUG = True
def connect_to_main_database(connection_string):
    client = MongoClient(connection_string)
    db = client.invertedIndexDB
    return db

def add_to_db(map_reduced_index, db_connection):
    if DEBUG:
        print(datetime.datetime.now(), ": Adding to database")
    for term in map_reduced_index:
        if DEBUG:
            print(term)
        doc_objects = []
        for posting_object in map_reduced_index[term]:
            doc = {"freq" : posting_object.freq,
            "document" : str(posting_object.doc_id),
            "occurences" : posting_object.occ,
            "tf-idf" : posting_object.tf_idf
            }
            doc_objects.append(doc)

        term = {"token": term,
        "posting": doc_objects
        

        }
        db_connection.indices.insert_one(term)
    print("Finished")

