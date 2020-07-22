import sys
import csv
import re
import os


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


def add_all_posting_lists_from_file(inverted_index):
    files = os.listdir('files/postings')
    posting_files = []
    for file_name in files:
        if re.match('^postings\([0-1]\)\d+\-\d+[\.]csv$', file_name) is not None:
            posting_files.append('files/postings/' + file_name)

    for file_name in posting_files:
        posting_lists = fetch_csv_from_file(file_name)
        print(file_name,'::>')
        print(posting_lists)

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
    name = 'files/postings/postings(' + str(mode) + ')' + str(index) + '-' + str((index + 2000)) + '.csv'
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
            print(find_word_id_file_name(word_id, inverted_index.mode), ':>')
            print(csv_string)
            write_to_file(find_word_id_file_name(word_id, inverted_index.mode), csv_string)
            csv_string = ''
    if csv_string != '':
        print(find_word_id_file_name(word_id, inverted_index.mode), ':>')
        print(csv_string)
        write_to_file(find_word_id_file_name(word_id, inverted_index.mode), csv_string)


def write_dictionary_to_file(dictionary, path):
    csv_string = ''
    for word in dictionary.keys():
        csv_string += word + ',' + str(dictionary[word]) + '\n'
    write_to_file(path, csv_string)


def read_dictionary_from_file(path):
    dictionary = {}
    result = fetch_csv_from_file(path)
    for pair in result:
        dictionary[pair[0]] = int(pair[1])
    return dictionary
