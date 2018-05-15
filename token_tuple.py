

class TokenTuple(object):
    def __init__(self, doc_id, frequency):
        self.doc_id = doc_id
        self.frequency = frequency

    def __hash__(self):
        return hash(self.token)
