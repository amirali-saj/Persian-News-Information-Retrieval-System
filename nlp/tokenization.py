# from __future__ import unicode_literals

from hazm import word_tokenize
from nlp.text import normalize

stopwords = None
character_stopwords = None


def get_stopwords():
    global stopwords
    if stopwords is None:
        stopwords = fetch_stop_words('files/stop_words.txt')
    return stopwords


def get_character_stopwords_phase2():
    global character_stopwords
    if character_stopwords is None:
        character_stopwords = fetch_stop_words('files/character_stop_words_phase2.txt')
        character_stopwords.append('\n')
        character_stopwords.append('\r')
    return character_stopwords


def get_character_stopwords():
    global character_stopwords
    if character_stopwords is None:
        character_stopwords = fetch_stop_words('files/character_stop_words.txt')
        character_stopwords.append('\n')
        character_stopwords.append('\r')
    return character_stopwords


def get_character_numeral_stopwords():
    global character_stopwords
    if character_stopwords is None:
        character_stopwords = fetch_stop_words('files/character_and_number_stop_words.txt')
        character_stopwords.append('\n')
        character_stopwords.append('\r')
    return character_stopwords


def fetch_stop_words(path):
    words = []
    f = open(path, 'r')
    word = 'not none'
    while word is not None and word != '':
        word = f.readline()
        word = word[:-1]
        if word != '':
            words.append(word)
    return words


def simple_tokenize(text, separator):
    initial_result = text.split(separator)
    result = []
    for token in initial_result:
        if token != '':
            result.append(token)
    return result


def complex_tokenize(text):
    initial_tokens = word_tokenize(text)
    result = []
    half_words = ['می']
    word = ''
    word_incomplete = False
    for token in initial_tokens:
        token = token.replace('_', '\u200c')
        if token in half_words:
            word += token + '\u200c'
            word_incomplete = True
            continue

        if word_incomplete:
            result.append(word)
            word = ''
            word_incomplete = False
            continue
        result.append(token)

    return result
