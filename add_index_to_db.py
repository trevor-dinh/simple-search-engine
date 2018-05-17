from pymongo import MongoClient
from pprint import pprint
import urllib
from tokenize_document import TokenizeDocument
from reduce_index import ReduceIndex
import os
USERNAME = "***REMOVED***"
PASSWORD = "***REMOVED***"
CONNECTION_STRING =  ***REMOVED***.format(
    urllib.quote(USERNAME), urllib.quote(PASSWORD))
if __name__ == '__main__':
    client = MongoClient(CONNECTION_STRING)
    db = client.invertedIndexDB
    sample_path1 = os.path.join(os.getcwd(), 'WEBPAGES_RAW', '0', '6')
    sample_path2 = os.path.join(os.getcwd(), 'WEBPAGES_RAW', '0', '7')
    td1 = TokenizeDocument(sample_path1)
    td2 = TokenizeDocument(sample_path2)

    td1.parse()
    td1.print_tokens()
    td2.parse()
    td2.print_tokens()
    mr = ReduceIndex([td1, td2])

    mr.reduce()
    mr.calc_tf_idf()
    print("Adding to database")
    for term, list_posting in mr.reduced_terms.items():
        doc_objects = []
        for posting_object in list_posting:

            

            doc = {"freq" : posting_object.freq,
            "document" : str(posting_object.doc_id),
            "occurences" : posting_object.occ,
            "tf-idf" : posting_object.tf_idf
            }
            doc_objects.append(doc)

        term = {"token": term,
        "posting": doc_objects
        

        }
        db.indices.insert_one(term)
    print("Finished")

