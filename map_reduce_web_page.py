from parse_web_page import ParseWebPage
from posting import Posting
from collections import defaultdict
from retrieval_math import tf_idf


class MapReduceWebPage(object):
    def __init__(self, docs=None):
        self.docs = docs
        self.reduced_terms = defaultdict(list)

    def merge_new_docs(self, *args):
        if type(args[0]) in (list, tuple):
            return self.reduce_terms(args[0])
        return self.reduce_terms(args)

    def reduce_terms(self, *args):
        docs = args if args else self.docs
        for web_page in docs:
            for token, frequency in web_page.tokens_freq.items():
                posting = Posting(web_page.doc_id,
                                  freq=frequency,
                                  occ=web_page.tokens_occ[token])
                self.reduced_terms[token].append(posting)
        return self.reduced_terms

    def calc_tf_idf(self):
        for term, list_postings in self.reduced_terms.items():
            for i, posting in enumerate(list_postings):
                posting.tf_idf = tf_idf(posting.freq,
                                        len(self.docs),
                                        len(list_postings))
                # print("HERE: {}".format(posting.tf_idf))
        return self.reduced_terms


