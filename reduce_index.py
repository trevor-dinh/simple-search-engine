from tokenize_document import TokenizeDocument
from posting import Posting
from collections import defaultdict
from retrieval_math import tf_idf

import pandas as pd


class ReduceIndex(object):
    def __init__(self, tok_docs=None):
        self.tok_docs = tok_docs
        self.reduced_terms = None

    def merge_new_docs(self, *args):
        if type(args[0]) in (list, tuple):
            return self.reduce(args[0])
        return self.reduce(args)

    def reduce(self, *args):
        docs = args if args else self.tok_docs
        red_terms_dict = defaultdict(list)
        for tok_doc in docs:
            for token, frequency in tok_doc.tokens_freq.items():
                posting = Posting(tok_doc.document.doc_id,
                                  freq=frequency,
                                  occ=tok_doc.tokens_occ[token])
                red_terms_dict[token].append(posting)
        self.reduced_terms = red_terms_dict
        # self.reduced_terms = pd.DataFrame(red_terms_dict)
        return self.reduced_terms

    def calc_tf_idf(self):
        for term, list_postings in self.reduced_terms.items():
            for i, posting in enumerate(list_postings):
                posting.tf_idf = tf_idf(posting.freq,
                                        len(self.tok_docs),
                                        len(list_postings))
        return self.reduced_terms


