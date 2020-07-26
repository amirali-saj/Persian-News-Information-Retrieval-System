from PersianStemmer import PersianStemmer
from hazm import Lemmatizer

lemmatizer = Lemmatizer()
ps = PersianStemmer()


def fast_stem(word):
    verb_stem = lemmatizer.lemmatize(word)
    if '#' in verb_stem:
        parts = verb_stem.split('#')
        if parts[0] in word and parts[0] != '':
            return parts[0]
        else:
            return parts[1]
    stem = ps.run(word)
    if stem.endswith('ه'):
        stem2 = stem[:-1] + 'م'
    else:
        stem2 = stem
    word2 = stem2.replace(' ', '\u200c')
    verb_stem = lemmatizer.lemmatize(word2)
    if '#' in verb_stem:
        parts = verb_stem.split('#')
        if parts[0] in word and parts[0] != '':
            return parts[0]
        else:
            return parts[1]
    else:
        return stem



from nlp.doc import extract_words_from_text


print(extract_words_from_text('ترکیه ای',0))
