from tokenize_document import TokenizeDocument
from reduce_index import ReduceIndex
from Document.get_document import read_json, make_document
from document_vector import DocumentVector
import os
from time import time
from datetime import timedelta
import pickle, json
import warnings
from insert_documents import insert_documents
from retrieval_math import tf_idf
from handle_db import HandleDB
import pprint
from handle_query import Query

if __name__ == "__main__":
    q = "artificial intelligence"
    db = HandleDB()
    query = Query(q, db)
    pprint.pprint(query.handle())
    # insert_documents()
    # pprint.pprint(db.database["document_vector"].find_one({"doc_id": '57/494'}))

    # print(tf_idf(1, 36664, 46))
    # {u'doc_id': u'57/494',
    #  u'freq': 1,
    #  u'occ': [217],
    #  u'tf_idf': 2.9022630966637197}]
    # count = 46
    #36664