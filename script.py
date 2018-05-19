from tokenize_document import TokenizeDocument
from reduce_index import ReduceIndex
from Document.get_document import read_json, make_document
import os, sys
from posting import Posting
from time import time
from add_index_to_db import CONNECTION_STRING, connect_to_main_database, add_to_db
import pickle, json


if __name__ == "__main__":
    times = [time()]
    bookkeeping_path = os.path.join(os.getcwd(), 'WEBPAGES_RAW', "bookkeeping.json")
    docs = make_document(read_json(bookkeeping_path))
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
    # for k,v in red_index.reduced_terms.items():
    # 	print(k,v)
    # 	break
    open("milestone1.txt",'w').close()
    m1_queries = ["Irvine", "Mondego", "Informatics"]
    with open("milestone1.txt", "w") as f:
        f.write("Number of documents in corpus: {}\n".format(len(td_list)))
        f.write("Number of terms in index: {}\n".format(len(red_index.reduced_terms)))
        f.write("Size of index on disk: {}\n".format(sys.getsizeof(red_index.reduced_terms)))
        for q in m1_queries:
            f.write("\n\n{}\n".format(q))
            for i in red_index.reduced_terms[q][:10]:
                #print(type(i))
                p = "Posting({})".format(", ".join(
                    '{}:{}'.format(k,v) for k,v in i.items()))
                f.write(p)
    with open('index.json', 'w') as fp:
        json.dump(red_index.reduced_terms, fp)

    #m1_queries = ["Irvine", "Mondego", "Informatics"]
    # print("Number of documents in corpus: {}".format(len(td_list)))
    # print("Number of terms in index: {}".format(len(red_index.reduced_terms)))
    # print("Size of index on disk: {}".format(sys.getsizeof(red_index.reduced_terms)))

    # for q in m1_queries:
    # 	print("\n\n\n{}".format(q))
    # 	for i in red_index.reduced_terms[q][:10]:
    # 		print(i)


    # db = connect_to_main_database(CONNECTION_STRING)
    # add_to_db(red_index, db)

    #for printing terms
    # for term in red_index.reduced_terms:
    #     print(term)
    