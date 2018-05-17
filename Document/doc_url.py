class DocURL(object):
    def __init__(self, doc_url=None):
        self.doc_url = doc_url

    def __str__(self):
        return "{}".format(self.doc_url)

    def __repr__(self):
        return "DocURL({})".format(self.doc_url)
