from parse_web_page import ParseWebPage
from map_reduce_web_page import MapReduceWebPage
import os


if __name__ == "__main__":

    sample_path1 = os.path.join(os.getcwd(), 'WEBPAGES_RAW', '0', '6')
    sample_path2 = os.path.join(os.getcwd(), 'WEBPAGES_RAW', '0', '7')
    ## set current working directory
    #os.chdir("/Users/***REMOVED******REMOVED***/Documents/UCI17-18/INF141/Assignments/simple-search-engine")
    parsed = ParseWebPage(sample_path1)
    parsed.parse()
    parsed.print_tokens()
    print("-----")
    parsed2 = ParseWebPage(sample_path2)
    parsed2.parse()
    parsed2.print_tokens(5)

    mr = MapReduceWebPage([parsed, parsed2])
    mr.reduce_terms()
    mr.calc_tf_idf()
    for term, list_posting in mr.reduced_terms.items():
        print(term)
        print(list_posting)
