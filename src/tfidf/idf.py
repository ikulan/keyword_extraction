import math
import re
import time
from collections import OrderedDict
from src.analyzer import AnalyzerJA

class IDFGenerator(object):

    def __init__(self):
        self.total_doc_num = 0
        self.words = {}

    def add_doc(self, doc_id, word_list):
        self.total_doc_num += 1
        word_list = list(set(word_list)) # dedup
        for word in word_list:
            word = word.strip()
            if word in self.words:
                self.words[word].append(doc_id)
            else:
                self.words[word] = [doc_id]

    def output(self, file_path, filter_freq=5):
        d = { word:len(docs)
          for word, docs in self.words.items() if len(docs)>filter_freq }
        print('Filter freq: ' + str(filter_freq))
        print('# of Words: ' + str(len(d)))

        words_df = OrderedDict(sorted(d.items(), key=lambda t: t[1]))
        with open(file_path, 'w') as outfile:
            for word, df in words_df.items():
                idf = math.log( self.total_doc_num / (1 + df) )
                outfile.write('%s %f\n' % (word, idf))


URL_MATCH = re.compile(r'https?:\/\/[a-zA-Z0-9\.-\/]+')

def gen_japanese_idf(infile_path, outfile_path, filter_freq=5):
    analyzer = AnalyzerJA()
    generator = IDFGenerator()

    start = time.perf_counter()
    with open(infile_path, 'r') as infile:
        text = ''
        doc_id = 0
        for line in infile:
            if line.strip() != "==========":
                text += line
                continue

            # pre-process
            text = re.sub(URL_MATCH, ' ', text)
            text = text.strip().lower()
            if len(text)<1:
                continue

            # tokenize
            word_list = analyzer.analyze(text)
            generator.add_doc(doc_id, word_list)

            # next post
            text = ''
            doc_id += 1

    end = time.perf_counter()
    print("Finished processing %d docs by %d s"%(doc_id, end-start))

    print("\nOutput...")
    generator.output(outfile_path, filter_freq)

