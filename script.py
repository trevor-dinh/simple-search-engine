from tokenize_document import TokenizeDocument
from reduce_index import ReduceIndex
from Document.get_document import read_json, make_document
import os
from posting import Posting


if __name__ == "__main__":
    bookkeeping_path = os.path.join(os.getcwd(), 'WEBPAGES_RAW', "bookkeeping.json")
    docs = make_document(read_json(bookkeeping_path), 10)
    print("(1 / 3) Made Documents")
    td_list = [TokenizeDocument(doc) for doc in docs]
    for td in td_list:
        print(td)
        td.parse()
    print("(2 / 3) Tokenized Documents")
    red_index = ReduceIndex(td_list)
    red_index.reduce()
    print("(3 / 3) Reduced Index\n")
    print(red_index.reduced_terms)
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