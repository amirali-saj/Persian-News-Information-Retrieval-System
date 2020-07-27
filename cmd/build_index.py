from random import randint

from indexing.inverted_index import InvertedIndex
from util.file import fetch_docs_from_file
from indexing.ranked_indexing import RankedIndex
from math import log10 as log

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


def pick_random_docs(dataset, number):  # Was used in phase 1
    result = []
    for j in range(number):
        index = randint(0, len(dataset) - 1)
        result.append(dataset[index])
    return result


# Builds an inverted index
def build_inverted_index(documents, mode=1):
    inv_ind = InvertedIndex(mode=mode)
    j = 0
    for document in documents:
        j += 1
        inv_ind.add_document(document)
        if j % 50 == 0:
            print('indexing(', j, '/', str(len(documents)), ')')

    return inv_ind


inverted_index = build_inverted_index(all_docs, 0)
print('Inverted Index built!')

inverted_index.store_index_to_file()
print('Inverted Index stored in file!')

ranked_index = RankedIndex(inverted_index, log(10 / 4), 1, False)
print('Ranked Index stored in file!')
