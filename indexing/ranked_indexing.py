from math import log10 as log, sqrt

from nlp.doc import extract_words_from_text
from datastructures.heap import build_max_heap, pick_max


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


def convert_to_vector(text, idf_dict, dictionary, mode):
    words = extract_words_from_text(text, mode)
    word_counts = {}
    for word in words:
        word_counts[word] = word_counts.get(word, 0) + 1

    doc_vector = {}
    for word in words:
        word_id = dictionary.get(word)
        if word_id is None:
            continue
        tf = word_counts[word]
        weight = (1 + log(tf)) * idf_dict[word_id]
        doc_vector[word_id] = weight
    return doc_vector


def size_of_doc_vector(doc_vector):
    sum_of_square_weights = 0
    for word_id in doc_vector.keys():
        sum_of_square_weights += doc_vector[word_id] * doc_vector[word_id]
    return sqrt(sum_of_square_weights)


def calculate_cosine_similarity(doc_vector1, doc_vector2):
    size1 = size_of_doc_vector(doc_vector1)
    size2 = size_of_doc_vector(doc_vector2)

    dot_result = 0
    for word_id in doc_vector1:
        dot_result += doc_vector1[word_id] * doc_vector2.get(word_id, 0)
    return dot_result / (size1 * size2)


# TODO: Index elimination (partially done)!
class RankedIndex:
    def __init__(self, inverted_index, idf_index_elimination_threshold, count_of_words_in_common_threshold):
        # Index elimination parameters.
        self.idf_threshold = idf_index_elimination_threshold
        self.word_count_threshold = count_of_words_in_common_threshold

        self.inverted_index = inverted_index
        # Represent docs as vectors and remove zero vectors!
        self.docs_vectors = []
        docs = self.inverted_index.docs
        idf_dict = find_idf(self.inverted_index.postings_lists, len(docs))
        self.idf_dict = idf_dict
        for doc_id in range(len(docs)):
            doc_vector = {}  # [0 for i in range(len(idf_dict.keys()))]
            for word_id in idf_dict:
                tf = self.inverted_index.get_token_per_doc_frequency(word_id, doc_id)
                if tf != 0:
                    weight = (1 + log(tf)) * idf_dict[word_id]
                    doc_vector[word_id] = weight
            if len(doc_vector) != 0:
                self.docs_vectors.append(doc_vector)
        print('Done!')

    # Used for testing the tf-idf measure informally.
    def temp_doc_title_top_5_words(self, ind):
        if 0 <= ind < len(self.inverted_index.docs):
            doc = self.inverted_index.docs[ind]
            doc_vector = self.docs_vectors[ind]

            top_5_max = []
            top_5_min = []

            for word in self.inverted_index.dictionary:
                score = doc_vector.get(self.inverted_index.dictionary[word], 0)

                # Top five min  [ 10, 9, 5, 0, 0]
                added = False
                if score == 0:
                    # top_5_min.append((word, 0))
                    added = True
                if not added:
                    for i in range(len(top_5_min)):
                        if score >= top_5_min[i][1]:
                            if i == 0 and len(top_5_min) == 5:
                                added = True
                                break
                            top_5_min.insert(i, (word, score))
                            added = True
                            break

                if not added:
                    top_5_min.append((word, score))

                # Top five max  [ 10, 9 , 6 , 5, 3]
                added = False
                for i in range(len(top_5_max)):
                    if score >= top_5_max[i][1]:
                        top_5_max.insert(i, (word, score))
                        added = True
                        break

                if not added:
                    top_5_max.append((word, score))

                if len(top_5_min) > 5:
                    top_5_min.pop(0)
                if len(top_5_max) > 5:
                    top_5_max.pop(len(top_5_max) - 1)
                # print(top_5_min,top_5_max)
                # print(word)
                # print(score)
                # input('continue?')

            return doc[1], top_5_max, top_5_min

    def search(self, query, k=10):
        query_vector = convert_to_vector(query, self.idf_dict, self.inverted_index.dictionary, self.inverted_index.mode)
        results = []
        docs_set = set()
        docs_words_in_common_count = {}
        for word_id in query_vector.keys():
            if self.idf_dict[word_id] < self.idf_threshold:  # Index elimination for words with idf below threshold
                continue
            postings = self.inverted_index.postings_lists[word_id].next_posting
            while postings is not None:
                docs_words_in_common_count[postings.doc_id] = docs_words_in_common_count.get(postings.doc_id, 0) + 1
                docs_set.add(postings.doc_id)
                postings = postings.next
        for doc_id in docs_set:
            # Index elimination for docs with number of words in common with query below the threshold
            if docs_words_in_common_count.get(doc_id, 0) < self.word_count_threshold:
                continue
            score = calculate_cosine_similarity(query_vector, self.docs_vectors[doc_id])
            results.append((doc_id, score))

        def score_function(result_tuple):
            return result_tuple[1]

        build_max_heap(results, score_function)

        ranked_results = []
        for i in range(k):
            ranked_results.append(pick_max(results, score_function, (-1, 0)))

        final_results = []
        for res in ranked_results:
            if res[0] != -1:
                final_results.append((self.inverted_index.docs[res[0]], res[1]))
        return final_results
