import pickle
from corus import load_corpora
import tqdm
import time
 
 
class UnigramMorphAnalyzer:
    def __init__(self):
        self.endings_stat = {}
        self.count_words = 0
        
    def train_abc(self, word, wtype, count):
        if len(word) >= count:
            cur_end = word[-count:]
            if cur_end in self.endings_stat.keys():
                pass
            else:
                self.endings_stat[cur_end] = {}
            if wtype in self.endings_stat[cur_end].keys():
                self.endings_stat[cur_end][wtype] += 1
            else:
                self.endings_stat[cur_end][wtype] = 1

    def train_word(self, word, wtype):
        self.train_abc(word, wtype, 4)
        self.train_abc(word, wtype, 3)
        self.train_abc(word, wtype, 2)
        self.train_abc(word, wtype, 1)

    def predict(self, ending):
        if ending in self.endings_stat:
            this = self.endings_stat[ending]
            count_all = 0
            for count in this.values():
                count_all += count
            items = list(this.items())
            items = sorted(items, key=lambda x: x[1], reverse=True)
            for key, value in items:
                prob = round(value/count_all, ndigits=6)
                print(f"{key}: {prob}")
        else:
            print("No data")

    def __getitem__(self, item):
        this_dict = self.endings_stat[item]
        for key, value in this_dict.items():
            print(f"{key}: {value}")

    def save(self, file_name):
        with open(file_name, 'wb') as output:
            pickle.dump(object1, output, pickle.HIGHEST_PROTOCOL)

    def load(self, file_name):
        with open(file_name, 'rb') as input:
            load = pickle.load(input)
            self.endings_stat = load.endings_stat
            self.count_words = load.count_words

    def train(self, zip_file):
        records = load_corpora(zip_file)
        for rec in tqdm.tqdm(records):
            for par in rec.pars:
                for sent in par.sents:
                    for token in sent.tokens:
                        object1.train_word(token.text, token.forms[0].grams[0])
                        self.count_words += 1
        print(f"At all: {self.count_words}")

    def max_value_key(self, ending):
        max_key = None
        max_value = 0
        for key, value in self.endings_stat[ending].items():
            if value > max_value:
                max_key = key
                max_value = value
        return max_key

    def eval(self, zip_file):
        count_error = 0
        count_all = 0
        records = load_corpora(zip_file)
        for rec in tqdm.tqdm(records):
            for par in rec.pars:
                for sent in par.sents:
                    for token in sent.tokens:
                        word = token.text
                        word_type = token.forms[0].grams[0]
                        if word[-4:] in self.endings_stat:
                            if self.max_value_key(word[-4:]) != word_type:
                                count_error += 1
                        elif word[-3:] in self.endings_stat:
                            if self.max_value_key(word[-3:]) != word_type:
                                count_error += 1
                        elif word[-2:] in self.endings_stat:
                            if self.max_value_key(word[-2:]) != word_type:
                                count_error += 1
                        elif word[-1:] in self.endings_stat:
                            if self.max_value_key(word[-1:]) != word_type:
                                count_error += 1
                        count_all += 1
        print(f"Eval result: {(count_all - count_error)*100//count_all}%")