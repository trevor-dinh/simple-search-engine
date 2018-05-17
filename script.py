from tokenize_document import TokenizeDocument
from reduce_index import ReduceIndex
from Document.get_document import read_json, make_document
import os
from posting import Posting
from time import time
from add_index_to_db import CONNECTION_STRING, connect_to_database, add_to_db


if __name__ == "__main__":
    print(CONNECTION_STRING)
    times = [time()]
    bookkeeping_path = os.path.join(os.getcwd(), 'WEBPAGES_RAW', "bookkeeping.json")
    docs = make_document(read_json(bookkeeping_path), 100)
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
    for term in red_index.reduced_terms:
        print(term, red_index.reduced_terms[term])
    # td1 = TokenizeDocument(sample_path1)
    # td2 = TokenizeDocument(sample_path2)
    #
    # td1.parse()
    # td1.print_tokens()
    # print("-----")
    # print(td1.text)
    # print("-----")
    # td2.parse()
    # td2.print_tokens()
    # red_index = ReduceIndex([td1, td2])
    #
    # red_index.reduce()
    # print(red_index.reduced_terms)
    # mr.calc_tf_idf()
    # for term, list_posting in mr.reduced_terms.items()[:1]:
    #     print term, list_posting
    #     for p in list_posting:
    #         print(str(p.doc_id))