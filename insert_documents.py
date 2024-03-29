from tokenize_document import TokenizeDocument
from reduce_index import ReduceIndex
from document_vector import DocumentVector
from posting import Posting
from handle_db import HandleDB
from Document.get_document import read_json, make_document
import os
from time import time, time
from datetime import timedelta
import warnings


def insert_documents(number=None):
    warnings.filterwarnings("ignore", category=UserWarning, module='bs4')
    bookkeeping_path = os.path.join(os.getcwd(), 'WEBPAGES_RAW', "bookkeeping.json")

    times = [time()]
    docs = make_document(read_json(bookkeeping_path), number)
    times.append(time())
    print("(1 / 5) Made Documents. Tokenizing...")

    td_list = []
    for i, doc in enumerate(docs):
        td = TokenizeDocument(doc)
        td.parse()
        td_list.append(td)
        if i and not i % 1000:
            print("\t -> Tokenized {} Documents".format(i))
    times.append(time())
    print("(2 / 5) Tokenized Documents. Reducing...")

    red_index = ReduceIndex(td_list)
    red_index.reduce()
    times.append(time())
    print("(3 / 5) Reduced Index. Calculating...")

    red_index.calc_tf_idf()
    times.append(time())
    print("(4 / 5) TF IDF Calculated. Vectorizing...")

    dv_list = []
    for doc_id, terms in red_index.doc_terms.items():
        dv = DocumentVector(doc_id, terms, red_index.doc_metric[doc_id])
        dv.make_vector_frame()
        dv.normalize()
        check = dv.vector_frame[dv.vector_frame["tf_idf"] > 1]
        if not check.empty:
            print(check)
        dv_list.append({"doc_id": doc_id,
                        "term": dv.vector_frame["term"].values.tolist(),
                        "tf_idf": dv.vector_frame["tf_idf"].values.tolist()})

    times.append(time())
    print("(5 / 5) Vector Space created.")

    # db = HandleDB()
    #
    # db.database["reduced_terms"].drop()
    # db.database["term_count"].drop()
    # db.database["document_vector"].drop()
    #
    # db.insert_dict(red_index.reduced_terms,
    #                key="term",
    #                value="posting",
    #                collection="reduced_terms")
    # db.insert_dict(red_index.term_count,
    #                key="term",
    #                value="count",
    #                collection="term_count")
    # # print(dv_list)
    # db.insert_list(dv_list, collection="document_vector")

    times.append(time())

    for i in range(len(times) - 1):
        sub = times[i + 1] - times[i]
        print("Section {} took {} seconds.".format(i + 1, round(sub, 3)))
    seconds = round(times[-1] - times[0], 3)
    print("This process took {} seconds ({})".format(seconds,
                                                     timedelta(seconds=seconds)))