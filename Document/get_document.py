import os
import json

from document import Document
from doc_id import DocID
from doc_url import DocURL
# for using bookkeeping.json


def read_json(file_name):
    with open(file_name) as json_data:
        json_dict = json.load(json_data)
    return json_dict


def make_document(json_dict, count=None):
    doc_list = []
    for doc_id, doc_url in json_dict.items()[:count]:
        doc_list.append(Document(DocID(doc_id), DocURL(doc_url)))
    return doc_list

# for iterating over WEBPAGES_RAW


def get_docs_in_dir(doc_dir):
    return [os.path.join(doc_dir, doc) for doc in os.listdir(doc_dir)]


def get_all_docs(directory):
    all_docs = []
    for sub_dir in os.listdir(directory):
        sub_dir = os.path.join(directory, sub_dir)
        if os.path.isdir(sub_dir):
            all_docs.append(get_docs_in_dir(sub_dir))
    return all_docs


if __name__ == "__main__":
    # get_docs_in_dir("/Users/***REMOVED******REMOVED***/Documents/UCI17-18/INF141/Assignments/simple-search-engine/WEBPAGES_RAW/0")
    # for d in get_all_docs("/Users/***REMOVED******REMOVED***/Documents/UCI17-18/INF141/Assignments/simple-search-engine/WEBPAGES_RAW"):
    #     print(d)
    json_dict = read_json("/Users/***REMOVED******REMOVED***/Documents/UCI17-18/INF141/Assignments/simple-search-engine/WEBPAGES_RAW/bookkeeping.json")
    for doc in make_document(json_dict, 10):
        print(doc)
    #
    # for k, v in read_json("/Users/***REMOVED******REMOVED***/Documents/UCI17-18/INF141/Assignments/simple-search-engine/WEBPAGES_RAW/bookkeeping.json").items():
    #     print("{}: {}".format(k, v))
