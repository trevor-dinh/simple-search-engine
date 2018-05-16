from doc_id import DocID
import nltk
import os
import re
from collections import defaultdict
from lxml import html
from bs4 import BeautifulSoup


def tokenize(line):
    pattern = re.compile("[0-9a-z]+")
    m = re.findall(pattern, line.lower())
    return m


class TokenizeDocument(object):

    def __init__(self, file_name):
        self.file_name = file_name
        self.doc_id = None
        self.contents = None
        self.text = None
        self.tokens_found = 0
        self.tokens_freq = defaultdict(int)
        self.tokens_occ = defaultdict(list)

    def parse(self):
        self.get_doc_id()
        self.get_contents()
        self.get_text()
        self.count_tokens()

    def print_tokens(self, count=None):
        to_print = []
        for token, frequency in sorted(self.tokens_freq.items(),
                                       key=lambda p: (-p[1], p[0])):
            to_print.append(u"{}: {}".format(token, frequency).encode('utf-8'))
        for line in to_print[:count]:
            print(line)

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
        self.text = soup.get_text("\n")
        return self.text

    def count_tokens(self):
        for line in self.text.split("\n"):
            self._count_tokens_in_line(nltk.word_tokenize(line))

    def _count_tokens_in_line(self, line):
        for token in line:
            self.tokens_freq[token] += 1
            self.tokens_occ[token].append(self.tokens_found)
            self.tokens_found += 1

    def __str__(self):
        return "'{}' | {}".format(self.file_name, self.doc_id)
