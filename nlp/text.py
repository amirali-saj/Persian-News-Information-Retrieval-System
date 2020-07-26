import re
from PersianStemmer import PersianStemmer
from hazm import Lemmatizer, Stemmer
from nlp.tokenization import get_character_stopwords_phase2

html_stuff = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')


def html_filter(html_content):
    return re.sub(html_stuff, ' ', html_content)


# What this function does is not necessary, and this issue can be handled more efficiently by taking 'ها' as an stop word!
# This function is merely added so tokenizing phase output matches what project specification demands.

def stick_ha_to_plural_words(text):
    ha_plural_wrong_format_regex = re.compile('[\s]*ها[\s]*')
    return re.sub(ha_plural_wrong_format_regex, '\u200cها ', text)


def stop_word_filter(content, stop_words):
    result = []
    for word in content:
        if word not in stop_words:
            result.append(word)
    return result

    # if type(content) is str:
    #     for stop_word in stop_words:
    #         content = content.replace(stop_word, ' ')
    #     return content
    # else:
    #     result = []
    #     for word in content:
    #         if word not in stop_words:
    #             result.append(word)
    #     return result


normalization_table = {}

normalization_list_table = [
    (['ب', 'ﺒ', 'ﺐ', 'ﺑ'], 'ب'),
    (['ء', 'ئ', 'ﻰ', 'ﯾ', 'ﯿ', 'ئ', 'ي'], 'ی'),
    (['ك''ﮐ', 'ک'], 'ک'),
    (['ﻨ', 'ﻦ', 'ﻧ'], 'ن'),
    (['ﺻ'], 'ص'),
    (['ﻀ'], 'ض'),
    (['ﻘ'], 'ق'),
    (['ﺶ', 'ﺸ', 'ﺷ'], 'ش'),
    (['ﺛ'], 'ث'),
    (['ف'], 'ف'),
    (['ﮔ', 'ﮕ'], 'گ'),
    (['ﻪ', 'ﻬ', 'ﻫ', 'ة'], 'ه'),
    (['ﺖ', 'ﺘ', 'ﺗ'], 'ت'),
    (['ﻤ', 'ﻣ'], 'م'),
    (['ﺨ', 'ﺧ'], 'خ'),
    (['ﺴ', 'ﺳ', 'ﺲ'], 'س'),
    (['ﺣ'], 'ح'),
    (['ﻌ'], 'ع'),
    (['ﻮ', 'ﻓ', 'ؤ'], 'و'),
    (['ﺪ'], 'د'),
    (['ﺮ'], 'ر'),
    (['إ', 'أ', 'آ'], 'ا'),
    (['َ', '“', 'ّ,', 'ً', '؛', 'ٔ', '؟', ',', 'ِ', '”', 'ُ', 'ٕ', 'ٔ', 'ٓ', 'ْ', '', 'ّ', 'ِ', 'ُ', 'َ', 'ٍ', 'ٌ', 'ً'
                                                                                                                    '\u200f',
      '\u200e', '\u200d', '\u202c', '\u200a',
      '\u202b'], ''),
    (['+', '-,''٬', '9', '8', '7', '6', '5', '4', '3', '2', '1', '0',
      '۹', '۱', '۲', '۳', '٤', '۴', '۵', '۶', '۷', '۸'], ' '),
    (['\u1680', '\u2005', '\u2006', '\u2009', '\u200A', '\u200B', '\u202F', '\uFEFF'], '\u200c')
]

for x in normalization_list_table:
    for char in x[0]:
        normalization_table[char] = x[1]

for c in get_character_stopwords_phase2():
    normalization_table[c] = ' '


def normalize(text):
    new_text = ''
    # next_text = text
    # for bad_char in normalization_table.keys():
    #     next_text = next_text.replace(bad_char, normalization_table[bad_char])
    for c in text:
        replacement = normalization_table.get(c, c)
        new_text += replacement
    return new_text


ps = PersianStemmer()

stems = {}

tracked_stems = ['گفت', 'گو', 'رود', 'خواه', 'سپاس', 'هنر', 'شریف', 'دوست', 'یاد', 'توان', 'شنو', 'کرد', 'ساز', 'دان']

lemmatizer = Lemmatizer()


def lemmatize(word):
    result = lemmatizer.lemmatize(word)
    if '#' in result:
        parts = result.split('#')
        if parts[0] in word and parts[0] != '':
            result = parts[0]
        else:
            result = parts[1]
    return result


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


def stem(word):
    result = word.replace('\u200c', ' ')
    result_tokens = result.split(' ')

    word_tokens = []

    # Uncomment this section to increase speed at cost of accuracy!

    # temp_res = ''
    # for t in result_tokens:
    # temp_res += lemmatize(ps.run(t)) + ' '
    # return temp_res[:-1]

    for t in result_tokens:
        word_tokens.append(lemmatize(ps.run(t)))

    result = None
    if len(word_tokens) == 1:
        result = lemmatize(ps.run(word_tokens[0]))
    elif len(word_tokens) == 2:
        if word_tokens[0] == 'نم' or word_tokens[0] == 'می':
            result = lemmatize('می\u200c' + word_tokens[1] + 'م')
        elif word_tokens[1] in ['بود', 'باش', 'ام', 'اید', 'است', 'ای', 'ایم', 'اند'] and word_tokens[0].endswith(
                'ه') and word_tokens[0] != 'خواه':
            result = lemmatize(word_tokens[0] + '\u200cام')
        elif word_tokens[0] == 'خواه':
            result = word_tokens[1]
    elif len(word_tokens) == 3:
        if word_tokens[0] == 'نم' or word_tokens[0] == 'می' and word_tokens[1].endswith('ه'):
            result = lemmatize(word_tokens[1] + '\u200cام')
        elif word_tokens[1] in ['نم', 'می'] and word_tokens[0] in ['داشت', 'دار']:
            result = lemmatize('می\u200c' + word_tokens[2] + 'م')

    if result is None:
        result = ps.run(word)

    # if result in tracked_stems:
    #     if result in tracked_stems:
    #         stems[result] = stems.get(result, [])
    #         if word not in stems[result]:
    #             stems[result].append(word)
    return result
