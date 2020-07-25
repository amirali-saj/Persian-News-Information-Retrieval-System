from random import randint

from indexing.inverted_index import InvertedIndex
from util.file import fetch_docs_from_file
from nlp.text import stems

# doc_paths = ['../dataset/ir-news-0-2.csv', '../dataset/ir-news-2-4.csv',
#              '../dataset/ir-news-4-6.csv', '../dataset/ir-news-6-8.csv',
#              '../dataset/ir-news-8-10.csv', '../dataset/ir-news-10-12.csv']

doc_paths = ['../dataset/ir-news-0-2.csv']

all_docs = []

for doc_path in doc_paths:
    docs = fetch_docs_from_file(doc_path)
    i = 0
    for doc in docs:
        i += 1
        if i % 50 == 0:
            print(doc_path, i, '/', str((len(docs) - 1)))
        all_docs.append(doc)


def pick_random_docs(dataset, number):
    result = []
    for i in range(number):
        index = randint(0, len(dataset) - 1)
        result.append(dataset[index])
    return result


def build_inverted_index(documents, mode=1):
    inverted_index = InvertedIndex(mode=mode)
    i = 0
    for document in documents:
        i += 1
        inverted_index.add_document(document)
        if i % 50 == 0:
            print('indexing(', i, '/', str(len(documents)), ')')

    return inverted_index


iv = build_inverted_index(all_docs[:1000], 0)
print('bef-here3')

# iv.store_index_to_file('../files/main_dictionary.csv')

print('bef-here2')
from indexing.ranked_indexing import RankedIndex

from math import log10 as log

rx = RankedIndex(iv,log(10/4),1)
print('bef-here1.5')
# rx.store_index_to_file()

# rx2 = RankedIndex(None,log(10/4),1)
#
# rx2.load_index_from_file(docs=all_docs[:1000],mode=0)
#
#
# rx = rx2
#


# print(rx.docs_vectors[:2],'\n\ndcs:\n',iv.docs[:2],'\n\ndict:\n')
# for d in iv.dictionary:
#     print(d,iv.dictionary[d])

print('bef-here1')
a, b, c = rx.temp_doc_title_top_5_words(0)
print(a, b, c)
a, b, c = rx.temp_doc_title_top_5_words(5)
print(a, b, c)
a, b, c = rx.temp_doc_title_top_5_words(100)
print(a, b, c)
a, b, c = rx.temp_doc_title_top_5_words(200)
print(a, b, c)
a, b, c = rx.temp_doc_title_top_5_words(257)
print(a, b, c)


print('here')
x = 'hh'
while x != 'exit':
    x = input('>')
    results = rx.search(x, 10)
    for doc in results:
        print('score:', doc[1], '\n\ntext:{', doc[0], '\n}')

exit(5)

stems2 = stems

# index1 = build_inverted_index_for_random_docs(all_docs, 5000, mode=0)

# dc = pick_random_docs(all_docs, len(all_docs)-1)
# index1 = build_inverted_index(all_docs,mode=0)
# print(index1.get_heaps_parameters())
# print(stems)
# index2 = build_inverted_index_for_random_docs(all_docs,15000,mode = 1)

# invertedIndex.store_index_to_file('files/dictionary.csv')

# invertedIndex.load_index_from_file('files/dictionary.csv', docs)


# from nlp.text import stem
#
# x = 'hh'
# while x != 'exit':
#     x = input('>')
#     print(stem(x))
#     result = index1.search(stem(x))
#     i = 1
#     for doc in result:
#         print(str(i) + '.' + doc[1] + '\n' + doc[6])
#         i += 1
