from parse_web_page import ParseWebPage
from map_reduce_web_page import MapReduceWebPage
import os


if __name__ == "__main__":
    ## set current working directory
    os.chdir("/Users/***REMOVED******REMOVED***/Documents/UCI17-18/INF141/Assignments/simple-search-engine")
    parsed = ParseWebPage("/Users/***REMOVED******REMOVED***/Documents/UCI17-18/INF141/Assignments/simple-search-engine/WEBPAGES_RAW/0/6")
    parsed.parse()
    parsed.print_tokens(5)
    print("-----")
    parsed2 = ParseWebPage("/Users/***REMOVED******REMOVED***/Documents/UCI17-18/INF141/Assignments/simple-search-engine/WEBPAGES_RAW/0/7")
    parsed2.parse()
    parsed2.print_tokens(5)

    mr = MapReduceWebPage([parsed, parsed2])
    mr.reduce_terms()
    mr.calc_tf_idf()
    for term, list_posting in mr.reduced_terms.items():
        print(term)
        print(list_posting)
