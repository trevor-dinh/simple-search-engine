from tokenize_document import TokenizeDocument
from reduce_index import ReduceIndex
import os


if __name__ == "__main__":
    ## set current working directory
    os.chdir("/Users/***REMOVED******REMOVED***/Documents/UCI17-18/INF141/Assignments/simple-search-engine")
    sample_path1 = os.path.join(os.getcwd(), 'WEBPAGES_RAW', '0', '6')
    sample_path2 = os.path.join(os.getcwd(), 'WEBPAGES_RAW', '0', '7')
    # print("-----")
    # parsed2 = TokenizeDocument("/Users/***REMOVED******REMOVED***/Documents/UCI17-18/INF141/Assignments/simple-search-engine/WEBPAGES_RAW/0/7")
    # parsed2.parse()
    # parsed2.print_tokens(5)
    #
    # mr = ReduceIndex([parsed, parsed2])
    # mr.reduce_terms()
    # mr.calc_tf_idf()
    # for term, list_posting in mr.reduced_terms.items():
    #     print(term)
    #     print(list_posting)
