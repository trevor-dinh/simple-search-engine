from doc_id import DocID
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
    def __init__(self, file_name):
        self.file_name = file_name
        self.doc_id = None
        self.contents = None
        self.text = None
        self.tokens = defaultdict(int)

    def parse(self):
        self.get_doc_id()
        self.get_contents()
        self.get_text()
        self.count_tokens()

    def get_doc_id(self):
        names = self.file_name.split("/")
        self.doc_id = DocID("{}/{}".format(names[-2], names[-1]))
        return self.doc_id

    def get_contents(self):
        with open(self.file_name) as file:
            contents = file.read()
        self.contents = contents
        return self.contents

    def get_text(self):
        soup = BeautifulSoup(self.contents, "html.parser")
        self.text = soup.get_text()
        return self.text

    def count_tokens(self):
        for line in self.text.split("\n"):
            self._count_tokens_in_line(tokenize(line))

    def _count_tokens_in_line(self, line):
        for token in line:
            self.tokens[token] += 1




if __name__ == "__main__":
    ## set current working directory
    os.chdir("/Users/***REMOVED******REMOVED***/Documents/UCI17-18/INF141/Assignments/simple-search-engine")
    parsed = ParseWebPage("/Users/***REMOVED******REMOVED***/Documents/UCI17-18/INF141/Assignments/simple-search-engine/WEBPAGES_RAW/0/6")
    parsed.parse()
    for k, v in sorted(parsed.tokens.items(), key=lambda p: -p[1]):
        print("{}: {}".format(k, v))
    print(parsed.text)
#     txt = get_contents("/Users/***REMOVED******REMOVED***/Documents/UCI17-18/INF141/Assignments/simple-search-engine/WEBPAGES_RAW/0/6")
#     t = get_text(txt)
#     for l in t:
#         tk = tokenize(l)
#         if tk:
#             print(tk)
#             print(tk[0])
#             print(str(tk[0]))