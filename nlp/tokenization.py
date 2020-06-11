from hazm import word_tokenize

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


special_phrases = [
    'فی ما بین',
    'چنان چه',
    'مع ذلک',
    'بنا بر این',
    'جست و جو',
    'گفت و گو',
    'نشست و برخاست',
    'گفت و شنود',
    'حضرت عالی',
    'جناب عالی',
    'به نحو احسن',
    'بلا درنگ',
    'در مجموع',
    'در کل',
    'صلاح دید',
    'فی الواقع',
    'از این رو',
    'ما حصل',
    'در واقع',
    'علی القاعده'
]

special_phrases_parts = []
for s in special_phrases:
    special_phrases_parts.append(s.split(' '))


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
        if word == 'ها':
            result[-1] = result[-1] + '\u200cها'
        else:
            for parts in special_phrases_parts:
                i = len(parts) - 1
                check = True
                if len(result) < len(parts):
                    continue

                while i != -1:
                    i2 = len(parts) - 1 - i
                    if result[-1 - i2] != parts[i]:
                        check = False
                        break
                    i -= 1
                if check:
                    for i in range(len(parts)):
                        result.pop(len(result) - 1)
                    result.append(' '.join(parts))

            result.append(token)

    return result
