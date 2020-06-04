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
    title = doc[1]
    summary_text = doc[3]
    meta_tags = doc[5]
    content_text = doc[6]

    tokens = extract_words_from_text(title, mode)
    summary_tokens = extract_words_from_text(summary_text, mode)

    # meta_tags_tokens = []

    meta_tags_tokens = meta_tags  # Here I used meta tags as distinct Terms as well as using their processed text

    for tag in meta_tags:
        tag_tokens = extract_words_from_text(tag, mode)
        append_lists(meta_tags_tokens, tag_tokens)

    content_tokens = extract_words_from_text(content_text, mode)

    tokens = append_lists(tokens, summary_tokens)
    tokens = append_lists(tokens, meta_tags_tokens)
    tokens = append_lists(tokens, content_tokens)

    return tokens
