from nlp.tokenization import get_stopwords, get_character_stopwords, get_character_numeral_stopwords, simple_tokenize
from nlp.text import stop_word_filter, html_filter
from util.lists import append_lists


def extract_words_from_text(text, mode):
    if mode == 1:
        tokens = simple_tokenize(str(stop_word_filter(html_filter(text), get_character_numeral_stopwords())), ' ')
        # print(tokens)
        print(len(tokens))
        tokens = stop_word_filter(tokens, get_stopwords())
        print(len(tokens))
        return tokens
    else:
        return None


def extract_words_from_document(doc, mode=1):
    content_text = doc[6]
    tokens = extract_words_from_text(content_text, mode)
    return tokens
