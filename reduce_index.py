from tokenize_document import TokenizeDocument
from posting import Posting
from collections import defaultdict
from retrieval_math import tf_idf

import pandas as pd
import numpy as np


class ReduceIndex(object):
    def __init__(self, tok_docs=None):
        self.tok_docs = tok_docs
        self.reduced_terms = None
        self.doc_terms = defaultdict(dict)

    def merge_new_docs(self, *args):
        if type(args[0]) in (list, tuple):
            return self.reduce(args[0])
        return self.reduce(args)

    def reduce(self):
        red_terms_dict = defaultdict(list)
        for tok_doc in self.tok_docs:
            for token, frequency in tok_doc.tokens_freq.items():
                posting = Posting(tok_doc.document.doc_id,
                                  freq=frequency,
                                  occ=tok_doc.tokens_occ[token])
                #print(posting.__dict__)
                red_terms_dict[token].append(posting.__dict__)
        self.reduced_terms = red_terms_dict
        return self.reduced_terms

    def calc_tf_idf(self):
        for term, list_postings in self.reduced_terms.items():
            for posting in list_postings:
                posting["tf_idf"] = tf_idf(posting["freq"],
                                           len(self.tok_docs),
                                           len(list_postings))
                self.doc_terms[posting["doc_id"]][term] = posting["tf_idf"]
        return self.reduced_terms

    def champion_list(self):
        for term, list_postings in self.reduced_terms.items():
            self.reduced_terms[term] = sorted(list_postings,
                                              key=lambda p: -p["tf_idf"])
        return self.reduced_terms

    def tf_idf_champion_list(self):
        for term, list_postings in self.reduced_terms.items():
            for posting in list_postings:
                posting["tf_idf"] = tf_idf(posting["freq"],
                                           len(self.tok_docs),
                                           len(list_postings))
                self.doc_terms[posting["doc_id"]][term] = posting["tf_idf"]
            self.reduced_terms[term] = sorted(list_postings,
                                              key=lambda p: -p["tf_idf"])
        return self.reduced_terms
