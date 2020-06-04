from nlp.doc import extract_words_from_document


class Posting:
    def __init__(self, doc_id):
        self.doc_id = doc_id
        self.next = None

    def append_posting(self, posting):
        if self.next is None:
            self.next = posting
        else:
            self.next.append_posting(posting)

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
        self.postings_lists = {}
        self.docs = []
        self.mode = mode

    def add_posting(self, word, doc_id):
        term = self.postings_lists.get(word, None)
        if term is None:
            return False
        term.add_posting(doc_id)
        return True

    def add_term(self, word, doc_id):
        term = self.postings_lists.get(word, None)
        if term is None:
            self.postings_lists[word] = Term(1)
            self.postings_lists[word].add_posting(doc_id)
            return
        term.frequency += 1
        term.add_posting(doc_id)

    def add_document(self, doc):
        doc_id = len(self.docs)
        self.docs.append(doc)
        tokens = extract_words_from_document(doc, self.mode)

        for token in tokens:
            self.add_term(token, doc_id)
