import os


def get_docs_in_dir(doc_dir):
    return [os.path.join(doc_dir, doc) for doc in os.listdir(doc_dir)]


def get_all_docs(directory):
    all_docs = []
    for sub_dir in os.listdir(directory):
        sub_dir = os.path.join(directory, sub_dir)
        if os.path.isdir(sub_dir):
            all_docs.append(get_docs_in_dir(sub_dir))
    return all_docs

if __name__ == "__main__":
    # get_docs_in_dir("/Users/***REMOVED******REMOVED***/Documents/UCI17-18/INF141/Assignments/simple-search-engine/WEBPAGES_RAW/0")
    for d in get_all_docs("/Users/***REMOVED******REMOVED***/Documents/UCI17-18/INF141/Assignments/simple-search-engine/WEBPAGES_RAW"):
        print(d)