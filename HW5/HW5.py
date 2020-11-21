1. MinStack

class MinStack:
 
    def __init__(self):
        self.arr = []
        self.min = []
 
    def push(self, x: int) -> None:
        self.arr.append(x)
        if len(self.min) == 0:
            self.min.append(x)
        else:
            if x < self.min[-1]:
                self.min.append(x)
            else:
                self.min.append(self.min[-1])
 
    def pop(self) -> None:
        del self.arr[-1]
        del self.min[-1]
        
 
    def top(self) -> int:
        return self.arr[-1]
 
    def getMin(self) -> int:
        return self.min[-1]

2. Сортировка строки

from collections import defaultdict, Counter
 
 
string = "Theredforjumpedoverthefenceandrantothezooforfood"
 
d = defaultdict(int)
# d = Counter()
for a in string:
    d[a] += 1
 
for i in range(len(d.keys())):
    min_key = None
    for key in d.keys():
        if min_key == None or key.lower() < min_key.lower():
            min_key = key
    print(min_key * d[min_key], end="")
    del d[min_key]

3. Коллокации

import itertools
import random
 
import pymorphy2
import tqdm
 
if __name__ == '__main__':
    morph = pymorphy2.MorphAnalyzer()
    nouns = []
    adjfs = []
    file = open("rus_shuffled.txt", "r", encoding="utf-8")
    for line in tqdm.tqdm(file.readlines()[:100]):
        word = line[:len(line) - 1]
        obj = morph.parse(word)[0]
        obj_pos = obj.tag.POS
        if obj.score > 0.8:
            if obj_pos == "NOUN":
                nouns.append(obj)
            elif obj_pos == "ADJF":
                adjfs.append(obj)
    file.close()
 
    pairs = []
    for pair in itertools.product(nouns, adjfs):
        noun, adjf = pair
        gender = noun.tag.gender
        adjf = morph.parse(adjf.normal_form)[0]
        adjf = adjf.inflect({gender})
        pairs.append(f"{adjf.word} {noun.normal_form}")
    random.shuffle(pairs)
    for pair in pairs:
        print(pair)
 