import unittest
from src.extract import KeywordExtractorZH, KeywordExtractorJA

class TestKeywordExtractorZH(unittest.TestCase):
    def setUp(self):
        self.extractor = KeywordExtractorZH()

    def test_pre_process(self):
        # url should be removed
        self.assertEqual(
          self.extractor.pre_process('测试，很好http://t.cn/EwR6eqC。Test, OK?'),
          '测试，很好 。test, ok?')

    def test_extract(self):
        # able to extract keywords
        text = '练完瑜伽🧘 ♀️，今天该教宝贝们认识水果啦🤗🤗[太阳][太阳]'
        self.assertTrue(len(self.extractor.extract(text)) > 0)


class TestKeywordExtractorJA(unittest.TestCase):
    def setUp(self):
        self.extractor = KeywordExtractorJA()

    def test_pre_process_downcase(self):
        text_ori = '#ELLEfashion @repetto_japan の 2019Spring&Summerコレクションは、プレイフルなカラーバレエシューズがお目見え💘 春が待ち遠しい😊'
        text_res = '#ellefashion @repetto_japan の 2019spring&summerコレクションは、プレイフルなカラーバレエシューズがお目見え💘 春が待ち遠しい😊'
        self.assertEqual(self.extractor.pre_process(text_ori), text_res)

    def test_pre_process_url(self):
        text_ori = "今回発表されたコラボコレクションは、2018年11月8日（木）に世界同時発売❤️\n \
          https://www.elle.com/jp/fashion/a24465871/moschino-tv-hm18-1101/"
        text_res = '今回発表されたコラボコレクションは、2018年11月8日（木）に世界同時発売❤️'
        self.assertEqual(self.extractor.pre_process(text_ori), text_res)

    def test_extract(self):
        text = '#ELLEfashion @repetto_japan の 2019Spring&Summerコレクションは、プレイフルなカラーバレエシューズがお目見え💘 春が待ち遠しい😊'
        self.assertTrue(len(self.extractor.extract(text)) > 0)

