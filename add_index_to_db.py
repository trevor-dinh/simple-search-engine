from pymongo import MongoClient
import json
import urllib
import sys
import datetime
USERNAME = "***REMOVED***"
PASSWORD = "***REMOVED***"
CONNECTION_STRING = ("mongodb+srv://{}:{}"
                     "@cluster0-ujza5.mongodb.net"
                     "/test?retryWrites=true").format(
    urllib.quote(USERNAME), urllib.quote(PASSWORD))
DEBUG = True

def dump_to_json_file(inverted_index, file_name):
    open(file_name, 'w').close()
    with open(file_name, 'w') as f:
        json.dump(inverted_index, f)

def convert_to_json_objects(map_reduced_index):
    '''takes a dict of reduced doc_terms and converts it into a list of JSON objects
    where each object is defined as
    {"term": <key>, "posting_list": posting list of term}
    '''
    json_objects = []
    for k in map_reduced_index.iterkeys():
        json_objects.append({"term" : k, "posting_list": map_reduced_index[k]})
    return json_objects




def connect_to_main_database(connection_string):
    client = MongoClient(connection_string)
    db = client.invertedIndexDB
    return db


def add_to_db(map_reduced_index, db_connection):
    if DEBUG:
        print(datetime.datetime.now(), ": Adding to database")
    for term in map_reduced_index.reduced_terms:
        try:
            doc_objects = []
            for posting_object in map_reduced_index.reduced_terms[term]:
                doc = {"freq": posting_object.freq,
                       "document": str(posting_object.doc_id),
                       "occurences": posting_object.occ,
                       "tf-idf": posting_object.tf_idf
                       }
                doc_objects.append(doc)

            term = {"token": term,
                    "posting": doc_objects
                    }
            db_connection.indices.insert_one(term)
        except Exception as ex:
            template = ("An exception of type {0} occurred"
                        "at term {} with posting list of size {}")
            message = template.format(
                type(ex).__name__, term, sys.getsizeof(
                    map_reduced_index.reduced_terms[term]))
            print message
    print("Finished")


if __name__ == '__main__':
    print(CONNECTION_STRING)
