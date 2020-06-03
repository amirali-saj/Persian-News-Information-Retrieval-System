stopwords = None
character_stopwords = None


def get_stopwords():
    global stopwords
    if stopwords is None:
        stopwords = fetch_stop_words('files/stop_words.txt')
    return stopwords


def get_character_stopwords():
    global character_stopwords
    if character_stopwords is None:
        character_stopwords = fetch_stop_words('files/character_stop_words.txt')
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
