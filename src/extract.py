#!/usr/bin/env python3
import re
import jieba
import jieba.analyse
import logging
import pycld2
from abc import ABCMeta, abstractmethod
from src.tfidf.tfidf import TFIDF_JA

SUPPORTED_LANGUAGES = {
    "chinese": 'zh',   # simplified Chinese
    "chineset": 'zh',  # tranditional Chinese
    "japanese": 'ja'
}

class UniversalExtractor:

    def __init__(self):
        self._extractors = self.load_extractors()

    def load_extractors(self):
        extractors = {}
        extractors['zh'] = KeywordExtractorZH()
        extractors['ja'] = KeywordExtractorJA()
        return extractors

    def extract(self, content):
        lang = self.detect_language(content)
        if lang in SUPPORTED_LANGUAGES:
            extractor = self._extractors.get(SUPPORTED_LANGUAGES[lang])
            return lang, extractor.extract(content)
        else:
            return lang, []

    def detect_language(self, content):
        if not content: return 'unknown'

        try:
            res = pycld2.detect(content)
            if res[0]:
                return res[2][0][0].lower()
            else: # no reliable result
                return 'unknown'
        except pycld2.error: # most likely UTF8 error, skipping for now
            return 'unknown'


class KeywordExtractor(metaclass=ABCMeta):

    URL_MATCH = re.compile(r'https?:\/\/[a-zA-Z0-9\.\-\/]+')

    @abstractmethod
    def pre_process(self, content):
        pass

    @abstractmethod
    def extract(self, content):
        pass


class KeywordExtractorZH(KeywordExtractor):

    DEFAULT_DICT_ZH   = "resource/zh/dict.txt.big"     # better support for Traditional Chinese
    USER_DICT_ZH      = "resource/zh/userdict.txt"
    STOP_WORDS_ZH     = "resource/zh/stop_words.txt"
    WEIBO_IDF         = "resource/zh/idf.weibo.big.txt"
    KEYWORD_ALLOW_POS = ['n', 'ng', 'nr', 'nrfg', 'nrt', 'ns', 'nt', 'nz', 'eng']

    def __init__(self):
        #suppress jieba messages
        logger = logging.getLogger('jieba')
        if logger: logger.setLevel(0)
        self.load()

    def load(self):
        jieba.set_dictionary(self.DEFAULT_DICT_ZH)
        jieba.load_userdict(self.USER_DICT_ZH)
        jieba.analyse.set_stop_words(self.STOP_WORDS_ZH)
        jieba.analyse.set_idf_path(self.WEIBO_IDF)


    def pre_process(self, content):
        # remove control characters
        content = content.replace('\u200b', '').replace('\u200d', '').strip()
        # remove url
        content = re.sub(self.URL_MATCH, ' ', content)
        content = content.strip().lower()
        return content


    def extract(self, content):
        content = self.pre_process(content)

        keywords = jieba.analyse.extract_tags(
            content,
            topK = 30,
            withWeight = False,
            allowPOS = self.KEYWORD_ALLOW_POS
        )

        return keywords


class KeywordExtractorJA(KeywordExtractor):

    JA_IDF  = "resource/ja/idf.ja.txt"

    def __init__(self):
        self.tfidf_ja = TFIDF_JA(self.JA_IDF)

    def pre_process(self, content):
        # remove lines with only 1 character
        # remove url
        content = re.sub(self.URL_MATCH, ' ', content)
        content = content.strip().lower()
        return content


    def extract(self, content):
        if not content: return []

        content = self.pre_process(content)

        keywords = self.tfidf_ja.extract(
            content,
            topK = 30,
            withWeight = False
        )

        return keywords
