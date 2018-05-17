from doc_id import DocID
from doc_url import DocURL
import os

class Document(object):
    def __init__(self, doc_id, doc_url=None, file_path=None):
        self.doc_id = doc_id
        self.doc_url = doc_url
        self.file_path = file_path

        if self.file_path is None:
            self.file_path = os.path.join(os.getcwd(), 'WEBPAGES_RAW', self.doc_id.doc_id)

    def __str__(self):
        return repr(self)

    def __repr__(self):
        s = ", ".join("{}: {}".format(k, v) for k, v in self.__dict__.items())
        return "Document({})".format(s)
