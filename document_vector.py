import pandas as pd
import numpy as np


class DocumentVector(object):
    def __init__(self, doc_id, terms, vector):
        self.doc_id = doc_id
        self.terms = terms
        self.vector = vector
        self.vector_frame = None

    def make_vector_frame(self):
        self.vector_frame = pd.DataFrame({"term": self.terms,
                                          "tf_idf": self.vector})
        return self.vector_frame

    def normalize(self):
        self.vector_frame["tf_idf"] = self.vector_frame["tf_idf"].apply(
            lambda v: np.true_divide(v, np.linalg.norm(self.vector_frame["tf_idf"])))
        return self.vector_frame

    def __hash__(self):
        return hash(self.doc_id)
