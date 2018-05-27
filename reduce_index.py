from tokenize_document import TokenizeDocument
from posting import Posting
from collections import defaultdict
from retrieval_math import tf_idf

import pandas as pd
import numpy as np


def reduce_tok_doc(tok_doc, reduced_terms=None, documents=None):
    reduced_terms = defaultdict(list) if reduced_terms is None else reduced_terms
    for token, frequency in tok_doc.tokens_freq.items():
        posting = Posting(tok_doc.document.doc_id,
                          freq=frequency,
                          occ=tok_doc.tokens_occ[token])
        # print(posting.__dict__)
        reduced_terms[token].append(posting.__dict__)
    return reduced_terms


class ReduceIndex(object):
    def __init__(self, tok_docs=None):
        self.tok_docs = tok_docs
        self.reduced_terms = defaultdict(list)
        self.term_count = dict()
        # self.doc_terms = defaultdict(dict)
        self.doc_terms = defaultdict(list)
        self.doc_metric = defaultdict(list)

    def reduce(self):
        for tok_doc in self.tok_docs:
            for token, frequency in tok_doc.tokens_freq.items():
                posting = Posting(tok_doc.document.doc_id,
                                  freq=frequency,
                                  occ=tok_doc.tokens_occ[token])
                # print(posting.__dict__)
                self.reduced_terms[token].append(posting.__dict__)
        return self.reduced_terms

    # def merge_new_doc(self, tok_doc):
    #     new_reduced_terms = reduce_tok_doc(tok_doc)
    #     new_doc_terms = dict()
    #     for term, list_postings in new_reduced_terms.items():
    #         for posting in list_postings:
    #             posting["tf_idf"] = self._calc_single_tf_idf(posting, self.reduced_terms[term])
    #             new_doc_terms[term] = posting["tf_idf"]
    #     return new_doc_terms

    def calc_tf_idf(self, champion_list=True):
        for term, list_postings in self.reduced_terms.items():
            self.term_count[term] = len(list_postings)
            for posting in list_postings:
                posting["tf_idf"] = self._calc_single_tf_idf(posting,
                                                             self.term_count[term])
                # self.doc_terms[posting["doc_id"]][term] = posting["tf_idf"]
                self.doc_terms[posting["doc_id"]].append(term)
                self.doc_metric[posting["doc_id"]].append(posting["tf_idf"])
            if champion_list:
                self.reduced_terms[term] = sorted(list_postings,
                                                  key=lambda p: -p["tf_idf"])
        return self.reduced_terms

    # def champion_list(self):
    #     for term, list_postings in self.reduced_terms.items():
    #         self.reduced_terms[term] = sorted(list_postings,
    #                                           key=lambda p: -p["tf_idf"])
    #     return self.reduced_terms
    #
    # def tf_idf_champion_list(self):
    #     for term, list_postings in self.reduced_terms.items():
    #         for posting in list_postings:
    #             posting["tf_idf"] = self._calc_single_tf_idf(posting, list_postings)
    #             self.doc_terms[posting["doc_id"]][term] = posting["tf_idf"]
    #         self.reduced_terms[term] = sorted(list_postings,
    #                                           key=lambda p: -p["tf_idf"])
    #     return self.reduced_terms

    def _calc_single_tf_idf(self, posting, term_count):
        return tf_idf(posting["freq"], len(self.tok_docs), term_count)

