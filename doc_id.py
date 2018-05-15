

class DocID(object):
    def __init__(self, doc_id):
        self.doc_id = doc_id

    def __str__(self):
        return "{}".format(self.doc_id)

    def __repr__(self):
        return "DocID({})".format(self.doc_id)