from tokenize_document import TokenizeDocument
from reduce_index import ReduceIndex
from Document.get_document import read_json, make_document
import os, sys
from posting import Posting
from time import time
from add_index_to_db import dump_to_json_file, convert_to_json_objects
import pickle, json

def chunk(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]

if __name__ == "__main__":
    times = [time()]
    bookkeeping_path = os.path.join(os.getcwd(), 'WEBPAGES_RAW', "bookkeeping.json")
    docs = make_document(read_json(bookkeeping_path), 5)
    print(len(docs))
    times.append(time())
    print("(1 / 4) Made Documents")
    td_list = [TokenizeDocument(doc) for doc in docs]
    for i, td in enumerate(td_list):
        if i and i % 1000 == 0:
            print(i)
        td.parse()
    times.append(time())
    print("(2 / 4) Tokenized Documents")
    red_index = ReduceIndex(td_list)
    red_index.reduce()
    times.append(time())
    print("(3 / 4) Reduced Index\n")
    red_index.calc_tf_idf()
    times.append(time())
    print("(4 / 4) TF IDF Calculated")
    times.append(time())
    for i in range(len(times) - 1):
        sub = times[i + 1] - times[i]
        print("Section {} took {} seconds.".format(i + 1, round(sub, 3)))
    print("This process took {} seconds".format(round(times[-1] - times[0], 3)))
    start = time()
    document_list = convert_to_json_objects(red_index.reduced_terms)
    dump_to_json_file(document_list, 'index.json')
    print("Time to dump to index.json was {} seconds".format(time() - start))
