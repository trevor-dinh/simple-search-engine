from pymongo import MongoClient

MONGODB_CONNECTION_STRING = 'mongodb://{user}:{password}@{ip}/invertedIndex'


def convert_to_json_objects(d, key, value):
    '''takes a dict of reduced doc_terms and converts it into a list of JSON objects
    where each object is defined as
    {"term": <key>, "posting_list": posting list of term}
    '''
    json_objects = []
    for k, v in d.items():
        json_objects.append({"{}".format(key) : k, "{}".format(value): v})
    return json_objects


def chunker(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]


class HandleDB(object):
    def __init__(self, user="***REDACTED***", password="***REDACTED***", ip="***REDACTED***"):
        self.user = user
        self.password = password
        self.ip = ip
        self.connect_str = MONGODB_CONNECTION_STRING.format(user=self.user,
                                                            password=self.password,
                                                            ip=self.ip)
        self.database = MongoClient(self.connect_str).invertedIndex

    def insert_dict(self, d, key, value, collection, chunksize=1000):
        dict_list = convert_to_json_objects(d, key, value)
        for chunk in chunker(dict_list, chunksize):
            self.database[collection].insert_many(chunk)

    def insert_list(self, l, collection, chunksize=1000):
        for chunk in chunker(l, chunksize):
            self.database[collection].insert_many(chunk)


