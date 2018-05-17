

class DocPath(object):
    def __init__(self, doc_path):
        self.doc_path = doc_path

    def __str__(self):
        return "{}".format(self.doc_path)

    def __repr__(self):
        return "DocPath({})".format(self.doc_path)
