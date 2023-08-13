#!/usr/bin/env python3
import os
import re
from operator import itemgetter
from src.analyzer import AnalyzerJA

_get_abs_path = lambda path: os.path.normpath(os.path.join(os.getcwd(), path))

class TFIDF(object):

    def __init__(self, idf_path, stopword_path=None):
        self.stop_words = []
        self.idf_freq = {}

        self.set_stop_words(stopword_path)
        self.load_idf(idf_path)


    def set_stop_words(self, stop_words_path):
        if not stop_words_path: return

        abs_path = _get_abs_path(stop_words_path)
        with open(abs_path, 'r') as infile:
            for line in infile:
                self.stop_words.add(line.strip())


    def load_idf(self, idf_path):
        with open(idf_path, 'r') as infile:
            for line in infile:
                word, freq = line.strip().split(' ')
                self.idf_freq[word] = float(freq)
        self.max_idf = max(self.idf_freq.values())

    def extract(self, sentence, topK=20, withWeight=False):
        raise NotImplementedError


class TFIDF_JA(TFIDF):
    SINGLE_LATIN = re.compile(r'[a-zA-Z]')

    def __init__(self, idf_path, stopword_path=None):
        super().__init__(idf_path, stopword_path)
        self.analyzer = AnalyzerJA()

    def extract(self, sentence, topK=20, withWeight=False):
        words = self.analyzer.analyze(sentence)

        freq = {}
        for w in words:
            if w.lower() in self.stop_words:
                continue
            elif len(w)==1 and re.match(self.SINGLE_LATIN, w):
                continue
            freq[w] = freq.get(w, 0.0) + 1.0

        total = sum(freq.values())
        for k in freq:
            freq[k] *= self.idf_freq.get(k, self.max_idf) / total

        if withWeight:
            tags = sorted(freq.items(), key=itemgetter(1), reverse=True)
        else:
            tags = sorted(freq, key=freq.__getitem__, reverse=True)
        if topK:
            return tags[:topK]
        else:
            return tags
