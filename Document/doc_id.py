class DocID(object):
    def __init__(self, doc_id=None):
        self.doc_id = doc_id

    def __str__(self):
        return "{}".format(self.doc_id)

    def __repr__(self):
        return "DocID({})".format(self.doc_id)

    def __hash__(self):
        return hash(self.doc_id)
