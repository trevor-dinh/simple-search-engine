from parse_web_page import ParseWebPage
from token_tuple import TokenTuple
from collections import defaultdict


class MapReduceWebPage(object):
    def __init(self, web_page_list):
        self.web_page_list = web_page_list
        self.reduced = defaultdict(set)

    def reduce_terms(self):
        reduced_terms = defaultdict(set)
        for web_page in self.web_page_list:
            for token, frequency in web_page.tokens.items():
                token_tuple = TokenTuple(web_page.doc_id, frequency)
                reduced_terms[token].add(token_tuple)
