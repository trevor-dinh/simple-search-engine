from tokenize_document import TokenizeDocument
from reduce_index import ReduceIndex
from Document.get_document import read_json, make_document
import os
from posting import Posting
from time import time


class InvertIndex(object):
    def __init__(self):
        self.times = [time()]
        self.sections = {
            0: "Load Json",
            1: "Make Documents",
            2: "Tokenized Documents",
            3: "Reduced Index",
            4: "TF IDF Calculated"
        }

    def main(self):
        bookkeeping_path = os.path.join(os.getcwd(),
                                        'WEBPAGES_RAW',
                                        "bookkeeping.json")

        docs = make_document(read_json(bookkeeping_path), 10000)
        self.times.append(time())
        print("(1 / 4) Made Documents")
        td_list = [TokenizeDocument(doc) for doc in docs]
        for i, td in enumerate(td_list):
            if i and i % 1000 == 0:
                print(i)
            td.parse()
        self.times.append(time())
        print("(2 / 4) Tokenized Documents")
        red_index = ReduceIndex(td_list)
        red_index.reduce()
        self.times.append(time())
        print("(3 / 4) Reduced Index\n")
        red_index.calc_tf_idf()
        self.times.append(time())
        print("(4 / 4) TF IDF Calculated")
        self.times.append(time())
        for i in range(len(self.times) - 1):
            sub = self.times[i + 1] - self.times[i]
            print("Section {} took {} seconds.".format(i + 1, round(sub, 3)))
        print("This process took {} seconds.".format(
            round(self.times[-1] - self.times[0], 3)))
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