from tokenize_document import TokenizeDocument
from document_vector import DocumentVector
from collections import Counter
from retrieval_math import tf_idf
from collections import defaultdict
import pandas as pd
import numpy as np
from handle_db import HandleDB

class Query(object):
    def __init__(self, query_string="", db_connection_object=None):
        print(type(db_connection_object))
        if type(db_connection_object) is HandleDB:
            self.handle_db = db_connection_object.database
        else:
            self.handle_db = db_connection_object
        self.query_string = query_string
        self.tok_doc = None
        self.document_vector = None

    def handle(self):
        self.tok_doc = TokenizeDocument(text=self.query_string)
        self.tok_doc.tokenize()
        for token in self.tok_doc.tokens_freq:
            if self.invalid_token(token):
                return None
        if self.tok_doc.tokens_found == 1:
            top_docs = self.handle_db["reduced_terms"].find_one(
                {"term": self.tok_doc.tokens_freq.keys()[0]})[u'posting'][:10]
            return [doc["doc_id"] for doc in top_docs]
        return self.cosine_similarity()

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

    def cosine_similarity(self):
        self.make_document_vector()
        doc_list = []
        for token in self.tok_doc.tokens_freq:
            doc_list.extend(self.get_top_doc_matches(token))
        doc_cos = []
        for doc in doc_list:
            terms = self.handle_db["document_vector"].find_one({"doc_id": doc["doc_id"]})["term"]
            vector = self.handle_db["document_vector"].find_one({"doc_id": doc["doc_id"]})["tf_idf"]
            df = pd.DataFrame({"term": terms, "tf_idf": vector})
            merged = pd.merge(df, self.document_vector.vector_frame,
                              how="outer", on="term",suffixes=["","q"]).fillna(0)
            # merged = merged.drop(merged.columns[0], axis=1)
            dp = np.dot(merged["tf_idf"], merged["tf_idfq"])
            doc_cos.append((doc, dp))
        doc_cos.sort(key=lambda x: -x[1])
        return [d[0]["doc_id"] for d in doc_cos[:10]]

    def get_top_doc_matches(self, token, number=30):
        return self.handle_db["reduced_terms"].find_one({"term": token})["posting"][:number]

    def invalid_token(self, token):
        valid = self.handle_db["reduced_terms"].find_one({"term": token})
        return valid is None

        #     for term, list_postings in new_reduced_terms.items():
        #         for posting in list_postings:
        #             posting["tf_idf"] = self._calc_single_tf_idf(posting, self.reduced_terms[term])
        #             new_doc_terms[term] = posting["tf_idf"]
