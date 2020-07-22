from math import log10 as log

from indexing.inverted_index import InvertedIndex


def find_idf(postings_list, docs_count):
    result = {}
    for word_id in postings_list:
        p = postings_list[word_id].next_posting
        df = 0
        while p is not None:
            df += 1
            p = p.next
        result[word_id] = log(docs_count / df)
    return result


class RankedIndex:
    def __init__(self, inverted_index):
        self.inverted_index = inverted_index


        # Represent docs as vectors and remove zero vectors!
        self.docs_vectors = []
        docs = self.inverted_index.docs
        idf_dict = find_idf(self.inverted_index.postings_lists, len(docs))

        for doc_id in range(len(docs)):
            doc_vector = [0 for i in range(len(idf_dict.keys()))]
            all_entries_zero = True
            for word_id in idf_dict:
                tf = self.inverted_index.get_token_per_doc_frequency(word_id, doc_id)
                weight = log(1 + tf) * idf_dict[word_id]
                if weight != 0:
                    doc_vector[word_id] = weight
                    all_entries_zero = False
            if not all_entries_zero:
                self.docs_vectors.append(doc_vector)
