from nlp.doc import extract_words_from_document
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
        # if self.next is None:
        #     self.next = posting
        # else:
        #     try:
        #         self.next.append_posting(posting)

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
    def __init__(self, frequency):
        self.frequency = frequency
        self.next_posting = None

    def add_posting(self, doc_id):
        posting = Posting(doc_id)
        if self.next_posting is None:
            self.next_posting = posting
        else:
            self.next_posting.append_posting(posting)


class InvertedIndex:
    def __init__(self, mode):
        self.dictionary = {}  # word -> word_id
        self.postings_lists = {}  # word_id -> Term
        self.docs = []  # doc_id (array index) -> doc
        self.mode = mode

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

    # def add_posting(self, word, doc_id):
    #     term = self.get_word(word)
    #     if term is None:
    #         return False
    #     term.add_posting(doc_id)
    #     return True

    def add_term(self, word, doc_id):
        term = self.get_word(word)
        if term is None:
            word_id = len(self.dictionary)
            self.dictionary[word] = word_id
            self.postings_lists[word_id] = Term(1)
            self.postings_lists[word_id].add_posting(doc_id)
            return
        term.frequency += 1
        term.add_posting(doc_id)

    def add_term_by_id(self, word_id, doc_id):
        term = self.postings_lists.get(word_id, None)
        if term is None:
            term = self.postings_lists[word_id] = Term(0)
        term.frequency += 1
        term.add_posting(doc_id)

    def add_document(self, doc):
        doc_id = len(self.docs)
        self.docs.append(doc)
        tokens = extract_words_from_document(doc, self.mode)

        for token in tokens:
            self.add_term(token, doc_id)

    def search(self, word):
        term = self.get_word(word)

        if term is None:
            return []

        result_docs = []

        posting = term.next_posting

        while posting is not None:
            result_docs.append(self.docs[posting.doc_id])
            posting = posting.next

        return result_docs

    def store_index_to_file(self, dictionary_path):
        write_dictionary_to_file(self.dictionary, dictionary_path)
        write_postings_lists_to_file(self)

    def load_index_from_file(self, dictionary_path,docs):
        self.docs = docs
        self.dictionary = read_dictionary_from_file(dictionary_path)
        add_all_posting_lists_from_file(self)
