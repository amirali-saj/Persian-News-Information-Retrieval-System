from nlp.tokenization import get_stopwords, get_character_numeral_stopwords, \
    simple_tokenize, complex_tokenize
from nlp.text import stop_word_filter, html_filter, fast_stem, normalize


def extract_words_from_text(text, mode):
    if mode == 1:
        tokens = simple_tokenize(str(stop_word_filter(html_filter(text), get_character_numeral_stopwords())), ' ')

        tokens = stop_word_filter(tokens, get_stopwords())
        return tokens
    else:
        tokens = complex_tokenize(normalize(html_filter(text)))
        for i in range(len(tokens)):
            tokens[i] = fast_stem(tokens[i])
        tokens = stop_word_filter(tokens, get_stopwords())

        return tokens


def extract_words_from_document(doc, mode=1):
    content_text = doc[6]
    tokens = extract_words_from_text(content_text, mode)
    return tokens


def extract_characters_from_text(text):
    characters = {}
    for c in text:
        characters[c] = True
    return characters
