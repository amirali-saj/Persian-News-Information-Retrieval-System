from util.file import fetch_docs_from_file
from indexing.ranked_indexing import RankedIndex
from math import log10 as log
from time import time

doc_paths = ['../dataset/ir-news-0-2.csv', '../dataset/ir-news-2-4.csv',
             '../dataset/ir-news-4-6.csv', '../dataset/ir-news-6-8.csv',
             '../dataset/ir-news-8-10.csv', '../dataset/ir-news-10-12.csv']

all_docs = []

for doc_path in doc_paths:
    docs = fetch_docs_from_file(doc_path)
    i = 0
    for doc in docs:
        i += 1
        if i % 50 == 0:
            print(doc_path, i, '/', str((len(docs) - 1)))
        all_docs.append(doc)

ranked_index = RankedIndex(None, log(10 / 4), 0, False)

ranked_index.load_index_from_file(False, all_docs, 0)
ranked_index.load_champions_list()
x = 'initial'
use_champions = False
while x != 'exit':
    x = input('>')
    if x == 'champions':
        use_champions = not use_champions
        print('Champions list activation: ', use_champions)
        continue
    elif x == 'thresh':
        n = input('>')
        try:
            ranked_index.common_word_threshold = float(n)
        except ValueError:
            print('Not a number!')
        continue
    now = time()
    results = ranked_index.search(x, 10, use_champions)
    duration = time() - now
    i = 1
    for result in results:
        print(i, '.', result[0][1])
        print('score:', result[1])
        print('\n', result[0][6])
        print('==================================================================================================')
        i += 1
    print(len(results), 'Results found in', duration, 'seconds.')
