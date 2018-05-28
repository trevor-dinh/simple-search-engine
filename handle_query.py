from tokenize_document import TokenizeDocument
from document_vector import DocumentVector
from collections import Counter
from retrieval_math import tf_idf
from collections import defaultdict
import pandas as pd
import numpy as np
from handle_db import HandleDB


def unique_list(l):
    new_l = []
    check = set()
    for item in l:
        if item not in check:
            new_l.append(item)
            check.add(item)
    return new_l


class Query(object):
    def __init__(self, query_string="", db_connection_object=None):
        if type(db_connection_object) is HandleDB:
            self.handle_db = db_connection_object.database
        else:
            self.handle_db = db_connection_object
        self.query_string = query_string
        self.num_times_queried = 0
        self.docs_found = 0
        self.tok_doc = None
        self.document_vector = None

    def handle(self):
        self.tok_doc = TokenizeDocument(text=self.query_string)
        self.tok_doc.tokenize()
        if not self.tok_doc.tokens_found:
            return None
        for token in self.tok_doc.tokens_freq:
            if self.invalid_token(token):
                return None
        if self.tok_doc.tokens_found == 1:
            top_docs = self.handle_db["reduced_terms"].find_one(
                {"term": self.tok_doc.tokens_freq.keys()[0]})[u'posting'][:10]
            return [doc["doc_id"] for doc in top_docs]
        self.num_times_queried = self.times_queried()
        return self.calc_similarity()

    def make_document_vector(self):
        tokens = []
        metrics = []
        n = self.handle_db["reduced_terms"].count()
        for token, freq in self.tok_doc.tokens_freq.items():
            df = self.handle_db["term_count"].find_one({"term": token})["count"]
            tokens.append(token)
            metrics.append(tf_idf(freq, n, df))
        self.document_vector = DocumentVector("query", tokens, metrics)
        self.document_vector.make_vector_frame()
        self.document_vector.normalize()
        return self.document_vector

    def calc_similarity(self):
        self.make_document_vector()
        doc_list = []
        docs_to_find = int(160 / self.tok_doc.tokens_found)
        for token in self.tok_doc.tokens_freq:
            doc_list = unique_list(self.get_top_doc_matches(token, docs_to_find))
        self.docs_found = len(doc_list)
        doc_cos = []
        for doc_id in doc_list:
            dp = self.cosine_similarity(doc_id)
            doc_cos.append((doc_id, dp))
        doc_cos.sort(key=lambda x: -x[1])
        doc_id_results = [d[0] for d in doc_cos[:10]]
        cos_results = [d[1] for d in doc_cos[:10]]
        self.cache_results(doc_id_results, cos_results)
        return doc_id_results

    def get_top_doc_matches(self, token, number=75):
        return self.handle_db["reduced_terms"].find_one({"term": token})["posting"][:number]

    def get_next_doc_matches(self, token, number=75):
        docs = self.handle_db["reduced_terms"].find_one({"term": token})["posting"]
        if number * self.num_times_queried > len(docs):
            return None
        return docs[self.num_times_queried * number: (self.num_times_queried * number) + number]

    def invalid_token(self, token):
        valid = self.handle_db["reduced_terms"].find_one({"term": token})
        return valid is None

    def times_queried(self):
        results = self.handle_db["search_results"].find_one({"query": self.query_string})
        if results is not None:
            return results["times"]
        return 0

    def cache_results(self, doc_id_results, cos_results):
        if self.num_times_queried:
            self.handle_db["search_results"].update_one(
                {"query": self.query_string},
                {"doc_id_results": doc_id_results,
                 "cos_results": cos_results,
                 "$inc": {"times": 1}})
        else:
            self.handle_db["search_results"].insert_one(
                {"query": self.query_string,
                 "times": 1,
                 "doc_id_results": doc_id_results,
                 "cos_results": cos_results})

    def cosine_similarity(self, doc_id):
        terms = self.handle_db["document_vector"].find_one({"doc_id": doc_id})["term"]
        vector = self.handle_db["document_vector"].find_one({"doc_id": doc_id})["tf_idf"]
        df = pd.DataFrame({"term": terms, "tf_idf": vector})
        merged = pd.merge(df, self.document_vector.vector_frame,
                          how="outer", on="term", suffixes=["", "q"]).fillna(0)
        return np.dot(merged["tf_idf"], merged["tf_idfq"])

        #     for term, list_postings in new_reduced_terms.items():
        #         for posting in list_postings:
        #             posting["tf_idf"] = self._calc_single_tf_idf(posting, self.reduced_terms[term])
        #             new_doc_terms[term] = posting["tf_idf"]
