import re
from collections import defaultdict
import io
import nltk
from bs4 import BeautifulSoup, Comment


def tokenize(line):
    pattern = re.compile("[0-9a-z]+")
    m = re.findall(pattern, line.lower())
    return m


class TokenizeDocument(object):

    def __init__(self, document):
        self.document = document
        self.contents = None
        self.text = None
        self.tokens_found = 0
        self.tokens_freq = defaultdict(int)
        self.tokens_occ = defaultdict(list)

    def parse(self):
        self.get_contents()
        self.get_text()
        # self.count_tokens()
        self.tokenize()

    def print_tokens(self, count=None):
        to_print = []
        for token, frequency in sorted(self.tokens_freq.items(),
                                       key=lambda p: (-p[1], p[0])):
            to_print.append(u"{}: {}".format(token, frequency).encode('utf-8'))
        for line in to_print[:count]:
            print(line)

    def get_contents(self):
        with io.open(self.document.file_path,
                     encoding='utf-8', errors='ignore') as file:
            contents = file.read()
        self.contents = contents
        return self.contents

    def get_text(self):
        soup = BeautifulSoup(self.contents, "html.parser")
        comments = soup.findAll(text=lambda text: isinstance(text, Comment))
        #https://stackoverflow.com/questions/23299557/beautifulsoup-4-remove-comment-tag-and-its-content
        for c in comments:
            c.extract()
        self.text = soup.get_text("\n")
        return self.text

    def tokenize(self):
        #alphanumeric_tokens = [t for t in nltk.word_tokenize(self.text) if t.isalpha()]
        for i, token in enumerate(nltk.word_tokenize(self.text)):
            # if token in nltk.corpus.stopwords.words('english'):
            #     continue
            self.tokens_freq[token] += 1
            self.tokens_occ[token].append(i)

    def count_tokens(self):
        for line in self.text.split("\n"):
            self._count_tokens_in_line(nltk.word_tokenize(line))

    def _count_tokens_in_line(self, line):
        for token in line:
            self.tokens_freq[token] += 1
            self.tokens_occ[token].append(self.tokens_found)
            self.tokens_found += 1

    def __str__(self):
        return "TokenizeDocument({})".format(self.document)

    def __repr__(self):
        return "TokenizeDocument({})".format(self.document)
