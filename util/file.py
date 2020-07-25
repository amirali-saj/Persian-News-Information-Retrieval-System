import sys
import csv
import re
import os


def write_docs_vectors_to_file(docs_vectors, path):
    csv_string = ''
    for doc_id in range(len(docs_vectors)):
        if len(docs_vectors[doc_id].keys()) != 0:
            for word_id in docs_vectors[doc_id].keys():
                csv_string += str(word_id) + ':' + str(docs_vectors[doc_id][word_id]) + ','
            csv_string = csv_string[:-1]
        csv_string += '\n'
    write_to_file(path, csv_string)


def read_docs_vectors_fom_file(path):
    docs_vectors = []
    results = fetch_csv_from_file(path)
    for i in range(len(results)):
        res = results[i]
        doc_vector = {}
        for field in res:
            tokens = field.split(':')
            doc_vector[int(tokens[0])] = float(tokens[1])
        docs_vectors.append(doc_vector)
    return docs_vectors


def read_text_file():
    file = open('../files/stop_words.txt', 'r')
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


def add_all_posting_lists_from_file(inverted_index):
    files = os.listdir('../files/export/postings')
    posting_files = []
    for file_name in files:
        if re.match('^postings\([0-1]\)\d+\-\d+[\.]csv$', file_name) is not None:
            posting_files.append('../files/export/postings/' + file_name)

    for file_name in posting_files:
        posting_lists = fetch_csv_from_file(file_name)

        for posting_list in posting_lists:
            word_id = int(posting_list[0])
            for i in range(len(posting_list)):
                if i < 1:
                    continue
                inverted_index.add_term_by_id(word_id, int(posting_list[i]))


def add_posting_list_from_file(word_id, inverted_index):
    file_name = find_word_id_file_name(word_id, inverted_index.mode)
    posting_lists = fetch_csv_from_file(file_name)
    for posting_list in posting_lists:
        word_id = int(posting_list[0])
        for i in range(len(posting_list)):
            if i < 1:
                continue
            inverted_index.add_term_by_id(word_id, int(posting_list[i]))


def find_word_id_file_name(word_id, mode=1):
    index = (word_id // 2000) * 2000
    name = '../files/export/postings/postings(' + str(mode) + ')' + str(index) + '-' + str((index + 2000)) + '.csv'
    return name


def write_to_file(path, content):
    f = open(path, 'w')
    f.write(content)
    f.close()


def write_postings_lists_to_file(inverted_index):
    csv_string = ''
    for word_id in range(len(inverted_index.dictionary)):
        term = inverted_index.postings_lists.get(word_id, None)
        csv_string += str(word_id)

        p = term.next_posting
        while p is not None:
            csv_string += ',' + str(p.doc_id)
            p = p.next

        csv_string += '\n'

        if word_id % 2000 == 1999:
            write_to_file(find_word_id_file_name(word_id, inverted_index.mode), csv_string)
            csv_string = ''

    if csv_string != '':
        write_to_file(find_word_id_file_name(word_id, inverted_index.mode), csv_string)


def write_dictionary_to_file(dictionary, path, non_string_key=False):
    csv_string = ''
    if not non_string_key:
        for word in dictionary.keys():
            csv_string += word + ',' + str(dictionary[word]) + '\n'
    else:
        for word in dictionary.keys():
            csv_string += str(word) + ',' + str(dictionary[word]) + '\n'
    write_to_file(path, csv_string)


def read_dictionary_from_file(path, value_type, key_type=str):
    dictionary = {}
    result = fetch_csv_from_file(path)
    for pair in result:
        dictionary[key_type(pair[0])] = value_type(pair[1])
    return dictionary
