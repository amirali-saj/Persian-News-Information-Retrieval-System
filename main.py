from indexing.inverted_index import InvertedIndex
from util.file import fetch_docs_from_file

invertedIndex = InvertedIndex(mode=1)

doc_paths = ['dataset/ir-news-0-2.csv', 'dataset/ir-news-2-4.csv',
             'dataset/ir-news-4-6.csv', 'dataset/ir-news-6-8.csv',
             'dataset/ir-news-8-10.csv', 'dataset/ir-news-10-12.csv']

for doc_path in doc_paths:
    docs = fetch_docs_from_file(doc_path)
    i = 0
    for doc in docs:
        i += 1
        if i % 50 == 0:
            print(doc_path,i, '/', str((len(docs) - 1)))
        invertedIndex.add_document(doc)

x = 'hh'
while x != 'exit':
    x = input('>')
    result = invertedIndex.search(x)
    i = 1
    for doc in result:
        print(str(i) + '.' + doc[1] + '\n' + doc[6])
        i += 1
