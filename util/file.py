import sys
import csv


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
