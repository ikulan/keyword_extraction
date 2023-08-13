# Keyword Extraction

This is a small project of my previous work. Performing keyword extraction task in Chinese and Japanese text using tf-idf.

## Library

* [Jieba](https://github.com/fxsjy/jieba): Chinese tokenizer & analyzer

* [kuromoji](https://www.elastic.co/guide/en/elasticsearch/plugins/current/analysis-kuromoji.html): Japanese tokenizer & analyzer
  * We were using Elasticsearch for indexing and searching system, so I chose to use kuromoji through Elasticsearch service to unify the tokenization results.

* [OpenCC](https://github.com/BYVoid/OpenCC): Conversion between Traditional and Simplified Chinese
  * Only used when you want to build Chinese custom dictionaries and stopwords in [resource/zh](resource/zh)


### Installation

Run in virtual environment
```shell
virtualenv env
source env/bin/activate
```

For a local install:
```shell
pip3 install -r requirements.txt
```

Install kuromoji plugin on Elasticsearch for Japanese analysis.
```shell
sudo bin/elasticsearch-plugin install analysis-kuromoji
```


### Console

```shell
make console
```

In console, you can test following functions
```python
# do language detection and decide which keyword extractor to call
extractor = UniversalExtractor()
extractor.extract(text)

# Chinese keyword extractor
extractor = KeywordExtractorZH()
extractor.extract("這是一個測試谷歌")

# Japanese keyword extractor
extractor = KeywordExtractorJA()
extractor.extract("日本航空株式会社は日本で最も長い航空会社としての歴史を持つ。")

# Japanese Analyzer
analyzer = AnalyzerJA()
analyzer.analyze(text)
AnalyzerJA.get_stop_words() # show stop words
AnalyzerJA.get_stop_tags()  # show stop tags

# generate Japanese IDF file
gen_japanese_idf(infile_path, outfile_path, filter_freq=5)
```


### Test

Run unit tests
```shell
make test
```

Make sure you have a test Elasticsearch instance running with Kuromoji plugin installed:

```shell
elasticsearch \
  -E http.port=9250 \
  -E transport.tcp.port=9351 \
  -E path.data=/tmp/es
```

```shell
elasticsearch-plugin install analysis-kuromoji
```
