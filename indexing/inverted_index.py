from nlp.doc import extract_words_from_document, extract_words_from_text
from uuid import uuid4
from util.file import add_posting_list_from_file, write_dictionary_to_file, write_postings_lists_to_file, \
    read_dictionary_from_file, add_all_posting_lists_from_file


def generate_random_id():
    return str(uuid4().hex)


class Posting:
    def __init__(self, doc_id):
        self.doc_id = doc_id
        self.next = None

    def append_posting(self, posting):
        p = self
        while p.next is not None:
            if p.doc_id == posting.doc_id:
                return
            p = p.next
        if p.doc_id == posting.doc_id:
            return
        p.next = posting

    def sorted_append_posting(self, posting):
        if self.doc_id <= posting.doc_id:
            if self.next is None:
                self.next = posting
            else:
                self.next = self.next.sorted_append_posting(posting)
            return self
        else:
            posting.next = self
            return posting


class Term:
    def __init__(self, first_doc_id):
        self.postings = [first_doc_id]
        self.frequency = 1

    def add_posting(self, doc_id):
        self.frequency += 1
        if doc_id != self.postings[-1]:
            self.postings.append(doc_id)

    def df(self):  # Document frequency (number of documents containing the term)
        return len(self.postings)


class InvertedIndex:
    def __init__(self, mode):
        self.dictionary = {}  # word -> word_id
        self.postings_lists = {}  # word_id -> Term
        self.docs = []  # doc_id (array index) -> doc
        self.mode = mode
        self.number_of_tokens = 0

        self.token_per_doc_frequency_table = {}  # f(t,d) table

    def get_word(self, word):
        word_id = self.dictionary.get(word, None)

        if word_id is None:
            return None

        posting_list = self.postings_lists.get(word_id, None)
        if posting_list is not None:
            return posting_list
        else:  # Read from file otherwise
            add_posting_list_from_file(word_id, self)
        return self.postings_lists.get(word_id, None)

    def increase_token_per_doc_frequency(self, word_id, doc_id):
        key = str(word_id) + '-' + str(doc_id)
        self.token_per_doc_frequency_table[key] = self.token_per_doc_frequency_table.get(key, 0) + 1

    def get_token_per_doc_frequency(self, word_id, doc_id):
        key = str(word_id) + '-' + str(doc_id)
        return self.token_per_doc_frequency_table.get(key, 0)

    def add_term(self, word, doc_id):

        term = self.postings_lists.get(self.dictionary.get(word))

        if term is None:
            word_id = len(self.dictionary)
            self.increase_token_per_doc_frequency(word_id, doc_id)
            self.dictionary[word] = word_id
            self.postings_lists[word_id] = Term(doc_id)
            return
        self.increase_token_per_doc_frequency(self.dictionary[word], doc_id)
        term.add_posting(doc_id)

    def add_term_by_id(self, word_id, doc_id):
        term = self.postings_lists.get(word_id, None)
        if term is None:
            self.postings_lists[word_id] = Term(doc_id)
        else:
            term.add_posting(doc_id)

    def add_document(self, doc):
        doc_id = len(self.docs)
        self.docs.append(doc)
        tokens = extract_words_from_document(doc, self.mode)

        self.number_of_tokens += len(tokens)  # For heaps measure
        for token in tokens:
            self.add_term(token, doc_id)

    def get_heaps_parameters(self):
        return self.number_of_tokens, len(self.dictionary)

    def search(self, word):
        if word == '':
            return []
        words = extract_words_from_text(word, 0)
        if len(words) == 0:
            return []
        word = words[0]
        term = self.get_word(word)

        if term is None:
            return []

        result_docs = term.postings
        return result_docs

    def store_index_to_file(self):
        write_dictionary_to_file(self.dictionary, '../files/export/dictionary.csv')
        write_dictionary_to_file(self.token_per_doc_frequency_table, '../files/export/term_doc_freq.csv')
        print('stored dictionary and token_per_doc table!')
        write_postings_lists_to_file(self)
        print('stored postings lists')

    def load_index_from_file(self, docs):
        self.docs = docs
        self.dictionary = read_dictionary_from_file('../files/export/dictionary.csv', int)
        print('Read dictionary')
        self.token_per_doc_frequency_table = read_dictionary_from_file('../files/export/term_doc_freq.csv', int)
        print('Read tdf (token_per_doc table)')
        add_all_posting_lists_from_file(self)
