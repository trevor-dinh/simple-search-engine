import os
import re
from collections import defaultdict
from lxml import html
from bs4 import BeautifulSoup


def tokenize(line):
    pattern = re.compile("[0-9a-z]+")
    m = re.findall(pattern, line.lower())
    return m


class ParseWebPage(object):
    def __init__(self, file_name, doc_id):
        self.file_name = file_name
        self.doc_id = doc_id
        self.contents = None
        self.text = None
        self.count = defaultdict(int)

    def get_contents(self):
        with open(self.file_name) as file:
            contents = file.read()
        self.contents = contents
        return self.contents

    def get_text(self):
        soup = BeautifulSoup(self.contents, "html.parser")
        self.text = soup.get_text()
        return self.text

    def count_words(self):
        for line in self.text.split("\n"):
            self._count_words_in_line(line)

    def _count_words_in_line(self, line):
        for word in line:
            self.count[word] += 1



# if __name__ == "__main__":
#     ## set current working directory
#     os.chdir("/Users/***REMOVED******REMOVED***/Documents/UCI17-18/INF141/Assignments/simple-search-engine")
#     txt = get_contents("/Users/***REMOVED******REMOVED***/Documents/UCI17-18/INF141/Assignments/simple-search-engine/WEBPAGES_RAW/0/6")
#     t = get_text(txt)
#     for l in t:
#         tk = tokenize(l)
#         if tk:
#             print(tk)
#             print(tk[0])
#             print(str(tk[0]))