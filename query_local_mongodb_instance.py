from pymongo import MongoClient
import os
from Document.get_document import read_json
MONGODB_CONNECTION_STRING = 'mongodb://{}:{}@***REDACTED***/invertedIndex'

if __name__ == '__main__':
    bookkeeping_path = os.path.join(
        os.getcwd(), 'WEBPAGES_RAW', "bookkeeping.json")
    lookup = read_json(bookkeeping_path)
    client = MongoClient(
        MONGODB_CONNECTION_STRING.format("***REDACTED***", "***REDACTED***"))
    db = client.invertedIndex
    all_docs = db.terms
    while True:
        query = raw_input(
            "Input query here, otherwise enter ':wq' to QUIT: ").lower()
        query_object = all_docs.find_one({"term": query})
        print(query == ":wq")
        if query == ":wq":
            break
        if query_object is not None:
            postings = query_object['posting_list']
            sorted_docs = sorted(
                postings, key=lambda x: x['tf_idf'], reverse=True)
            for i, d in enumerate(sorted_docs[:10]):
                print("{}: {}".format(i, lookup[d['doc_id']]))
                print(d)
                print("\n")
    print("Thanks for querying")
    client.close()
