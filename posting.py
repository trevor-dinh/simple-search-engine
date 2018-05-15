

class Posting(object):
    def __init__(self, doc_id, freq=None, occ=None, tf_idf=None):
        self.doc_id = doc_id
        self.freq = freq
        self.occ = occ
        self.tf_idf = tf_idf

    def __str__(self):
        return "ID: {} | Freq: {} | Occ: {} | TF_IDF: {}".format(self.doc_id,
                                                                 self.freq,
                                                                 self.occ,
                                                                 self.tf_idf)

    def __repr__(self):
        return "Posting({}, {}, {}, {})".format(self.doc_id,
                                                self.freq,
                                                self.occ,
                                                self.tf_idf)
