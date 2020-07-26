from math import log10 as log, sqrt
import numpy as np

from nlp.doc import extract_words_from_text
from datastructures.heap import build_max_heap, pick_max

from indexing.inverted_index import InvertedIndex
from util.file import write_compressed_docs_vectors_to_file, read_compressed_docs_vectors_fom_file, \
    write_dictionary_to_file, \
    read_dictionary_from_file, write_array_to_file, read_array_from_file


def doc_array_to_dict(doc_array):
    doc_dict = {}
    for i in range(doc_array.size):
        if doc_array[i] != 0:
            doc_dict[i] = doc_array[i]
    return doc_dict


def doc_dict_to_array(doc_dict, size_of_array):
    doc_array = np.zeros(shape=size_of_array)
    for key in doc_dict.keys():
        doc_array[key] = doc_dict[key]
    return doc_array


def find_idf(postings_list, docs_count):
    result = np.zeros(shape=len(postings_list))
    for word_id in postings_list:
        result[word_id] = log(docs_count / postings_list[word_id].df())
    return result


def convert_to_vector(text, idf_dict, dictionary, mode):
    words = extract_words_from_text(text, mode)
    word_counts = {}
    for word in words:
        word_counts[word] = word_counts.get(word, 0) + 1

    doc_vector = np.zeros(shape=(len(dictionary)))
    for word in words:
        word_id = dictionary.get(word)
        if word_id is None:
            continue
        tf = word_counts[word]
        weight = (1 + log(tf)) * idf_dict[word_id]
        doc_vector[word_id] = weight
    return doc_vector


def size_of_doc_vector(doc_vector):
    return np.linalg.norm(doc_vector)


def calculate_cosine_similarity(doc_vector1, doc_vector2):
    size1 = size_of_doc_vector(doc_vector1)
    size2 = size_of_doc_vector(doc_vector2)
    if size2 == 0 or size1 == 0:
        return 0
    return np.dot(doc_vector1, doc_vector2) / (size1 * size2)


# TODO: Index elimination (partially done)!
class RankedIndex:
    def __init__(self, inverted_index, idf_index_elimination_threshold, common_word_threshold, low_memory=False):
        # Index elimination parameters.
        self.vector_type = 'dict'
        self.idf_threshold = idf_index_elimination_threshold
        self.common_word_threshold = common_word_threshold

        # Represent docs as vectors!
        self.docs_vectors = []
        self.inverted_index = inverted_index
        self.idf_array = None
        if inverted_index is not None:
            self.inverted_index = inverted_index
            docs = self.inverted_index.docs
            idf_array = find_idf(self.inverted_index.postings_lists, len(docs))
            self.idf_array = idf_array

            # if low_memory:
            #     inverted_index.postings_lists = None
            # for key in inverted_index.token_per_doc_frequency_table.keys():
            #     inverted_index.token_per_doc_frequency_table.get(key)
            # tf_matrix =

            self.docs_vectors = []
            for doc_id in range(len(docs)):
                self.docs_vectors.append({})

            for word_id in self.inverted_index.postings_lists:
                for doc_id in self.inverted_index.postings_lists[word_id].postings:
                    tf = self.inverted_index.get_token_per_doc_frequency(word_id, doc_id)
                    if tf != 0:
                        self.docs_vectors[doc_id][word_id] = (1 + log(tf)) * idf_array[word_id]
                print(word_id, '(', len(self.inverted_index.postings_lists[word_id].postings), ')', '/',
                      len(self.inverted_index.postings_lists))
            self.store_index_to_file(exclude_inverted_index=True, vector_type='dict')

        else:
            print('Postponed!')
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

            return doc[1], top_5_max, top_5_min

    def search(self, query, k=10):
        query_vector = convert_to_vector(query, self.idf_array, self.inverted_index.dictionary,
                                         self.inverted_index.mode)
        results = []
        docs_set = set()

        high_idf_terms_indices = ((self.idf_array > self.idf_threshold) * query_vector).nonzero()[0]
        for word_id in high_idf_terms_indices:
            print('wid', word_id)
            for doc_id in self.inverted_index.postings_lists[word_id].postings:
                # if ((query_vector * self.docs_vectors[doc_id] > 0).nonzero()[
                #     0].size)*1. / high_idf_terms_indices.size < self.common_word_threshold:
                #     continue
                docs_set.add(doc_id)
        print(docs_set)
        for doc_id in docs_set:
            score = calculate_cosine_similarity(query_vector, doc_dict_to_array(self.docs_vectors[doc_id],len(self.inverted_index.dictionary)))
            results.append((doc_id, score))
        print(results)

        # if len(results) < k:
        #     final_results = []
        #     for res in results:
        #         if res[0] != -1:
        #             final_results.append((self.inverted_index.docs[res[0]], res[1]))
        #     return final_results

        def score_function(result_tuple):
            return result_tuple[1]

        build_max_heap(results, score_function)
        print(results, 'post heap')

        ranked_results = []
        for i in range(k):
            if len(results) > 0:
                ranked_results.append(pick_max(results, score_function, (-1, 0)))
                print(i, '>', ranked_results[-1])
        final_results = []
        print(ranked_results)

        for res in ranked_results:
            if res[0] != -1:
                final_results.append((self.inverted_index.docs[res[0]], res[1]))
        print(final_results)
        return final_results

    def store_index_to_file(self, exclude_inverted_index=False, vector_type='numpy'):
        if not exclude_inverted_index:
            self.inverted_index.store_index_to_file()
            print('inverted index saved')
        write_array_to_file('../files/export/idf.csv', self.idf_array)
        print('idf saved')

        def identity_function(x):
            return x

        if vector_type == 'dict':
            compression_function = identity_function
        else:
            compression_function = doc_array_to_dict
        write_compressed_docs_vectors_to_file(self.docs_vectors, compression_function,
                                              '../files/export/doc_vectors.csv')
        print('doc vectors saved!')

    def load_index_from_file(self, exclude_inverted_index=False, docs=None, mode=0):
        if not exclude_inverted_index:
            self.inverted_index = InvertedIndex(mode)
            self.inverted_index.load_index_from_file(docs)
        self.idf_array = read_array_from_file('../files/export/idf.csv', float)

        def identity_fucntion(x, y):
            return x

        self.docs_vectors = read_compressed_docs_vectors_fom_file('../files/export/doc_vectors.csv', identity_fucntion,
                                                                  len(self.inverted_index.dictionary))
