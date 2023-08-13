#!/usr/bin/env python3
import os
from elasticsearch import Elasticsearch
from elasticsearch import ElasticsearchException

class AnalyzerJA(object):

    ANALYSIS_INDEX  = 'kuromoji_sample'
    ANALYZER_NAME   = 'ja_analyzer'

    STOP_TAGS_PATH  = 'resource/ja/stoptags.txt'
    STOP_WORDS_PATH = 'resource/ja/stopwords.txt'

    NOUN_SUFFIXES = ['感', '性', '系', '力', '派', '会', '風']

    def __init__(self):
        self._es_service = Elasticsearch(
            hosts=[os.environ['ES_KUROMOJI_URL']],
            verify_certs=False
        )
        self._analyzer   = self.ANALYZER_NAME
        self.set_setting()

    def analyze(self, text):
        results = self._es_service.indices.analyze(
            index=self.ANALYSIS_INDEX,
            body={"analyzer": self._analyzer, "text": text}
        )
        if 'tokens' in results:
            return self.__merge_noun_suffix(results['tokens'])
        else:
            return []

    # merge noun suffix because some suffixes are meaningless solely
    # ex. '安定', '感' => '安定感'
    # ex. '大人', '系' => '大人系'
    def __merge_noun_suffix(self, tokens):
        merges = []
        for i in range(1, len(tokens)):
            if (tokens[i]['token'] in self.NOUN_SUFFIXES) and \
                (tokens[i]['position'] == tokens[i-1]['position'] + 1):
                word = tokens[i-1]['token'] + tokens[i]['token']
                merges.append([i-1, word])

        words = [d['token'] for d in tokens]

        skip = 0
        for idx, w in merges:
            words[idx-skip] = w   # replace
            words.pop(idx+1-skip) # remove suffix token
            skip += 1
        return words


    @classmethod
    def get_stop_tags(cls):
        with open(cls.STOP_TAGS_PATH, 'r') as infile:
            stoptags = [l.strip() for l in infile if l.strip() and not l.startswith('#')]
        return stoptags


    @classmethod
    def get_stop_words(cls):
        stopwords = []
        with open(cls.STOP_WORDS_PATH, 'r') as infile:
                stopwords = [l.strip() for l in infile if l.strip() and not l.startswith('#')]
        return stopwords


    def set_setting(self):
        stoptags = self.get_stop_tags()
        stopwords = self.get_stop_words() + ['_japanese_']
        setting_body = {
            "settings": { "index": { "analysis": {
                "tokenizer": {
                    "kuromoji_normal": {
                        "type": "kuromoji_tokenizer",
                        "mode": "normal"
                    }
                },
                "analyzer": {
                    "ja_analyzer": {
                        "tokenizer": "kuromoji_normal",
                        "filter": ["ja_posfilter", "kuromoji_baseform", "ja_stop"]
                    }
                },
                "filter": {
                    "ja_stop": {
                        "type": "ja_stop",
                        "stopwords": stopwords
                    },
                    "ja_posfilter": {
                        "type": "kuromoji_part_of_speech",
                        "stoptags": stoptags
                    }
                }
        }}}}

        # delete exist settings to avoid conflict
        try:
            self._es_service.indices.delete(index=self.ANALYSIS_INDEX)
            self._es_service.indices.refresh(index=self.ANALYSIS_INDEX)
        except Exception as e:
            pass

        # set setting
        res = self._es_service.indices.create(
              index=self.ANALYSIS_INDEX,
              body=setting_body
            )
        return res
