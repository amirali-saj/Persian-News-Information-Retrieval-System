import sys
import csv
from indexing.inverted_index import InvertedIndex


def read_text_file():
    file = open('files/stop_words.txt', 'r')
    return file.read()


def fetch_csv_from_file(path):
    csv.field_size_limit(sys.maxsize)
    with open(path, newline='') as f:
        reader = csv.reader(f)
        result = list(reader)
    return result


def fetch_docs_from_file(path):
    docs = fetch_csv_from_file(path)
    return docs[1:]


def add_posting_list_from_file(word_id, inverted_index):
    file_name = find_word_id_file_name(word_id, inverted_index.mode)
    posting_lists = fetch_csv_from_file(file_name)
    for posting_list in posting_lists:
        word_id = posting_list[0]
        for i in range(len(posting_list)):
            if i < 1:
                continue
            inverted_index.add_term_by_id(word_id, posting_list[i])
    return inverted_index


def find_word_id_file_name(word_id, mode=1):
    index = word_id % 2000
    name = 'files/postings/postings{' + str(mode)+'}'+str(index) + '-' + str((index + 2000)) + '.csv'
    return name
