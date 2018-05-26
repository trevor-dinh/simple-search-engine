import pandas as pd
import numpy as np


class DocumentVector(object):
    def __init__(self, doc_id, term_dict):
        self.doc_id = doc_id
        self.term_dict = term_dict
        self.vector_frame = None

    def make_vector_frame(self):
        self.vector_frame = pd.DataFrame({self.doc_id: self.term_dict})
        return self.vector_frame

    def normalize(self):
        self.vector_frame = self.vector_frame.apply(
            lambda v: np.true_divide(v, np.linalg.norm(v)), axis=0)

        return self.vector_frame

    def __hash__(self):
        return hash(self.doc_id)
