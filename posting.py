class Posting(object):
    def __init__(self, doc_id, freq=None, occ=None, tf_idf=None):
        self.doc_id = doc_id
        self.freq = freq
        self.occ = occ
        self.tf_idf = tf_idf

    def __str__(self):
        l = ["{}: {}".format(k, v) for k, v in self.__dict__.items()]
        return " | ".join(l)

    def __repr__(self):
        s = ", ".join(str(v) for k, v in self.__dict__.items())
        return "Posting({})".format(s)