import re
from PersianStemmer import PersianStemmer
from hazm import Lemmatizer, Stemmer


def html_filter(html_content):
    html_stuff = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
    return re.sub(html_stuff, ' ', html_content)


# What this function does is not necessary, and this issue can be handled more efficiently by taking 'ها' as an stop word!
# This function is merely added so tokenizing phase output matches what project specification demands.

def stick_ha_to_plural_words(text):
    ha_plural_wrong_format_regex = re.compile('[\s]*ها[\s]*')
    return re.sub(ha_plural_wrong_format_regex, '\u200cها ', text)


def stop_word_filter(content, stop_words):
    if type(content) is str:
        for stop_word in stop_words:
            content = content.replace(stop_word, ' ')
        return content
    else:
        result = []
        for word in content:
            if word not in stop_words:
                result.append(word)
        return result


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
    (['َ', '“', 'ّ,', 'ً', '؛', 'ٔ', '؟', ',', 'ِ', '”', 'ُ', '\u200f', '\u200e', '\u200d', '\u202c', '\u200a',
      '\u202b'], ''),
    (['\u1680', '\u2005', '\u2006', '\u2009', '\u200A', '\u200B', '\u202F', '\uFEFF'], '\u200c')
]

for x in normalization_list_table:
    for char in x[0]:
        normalization_table[char] = x[1]


def normalize(text):
    new_text = ''
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


def stem(word):
    result = word.replace('\u200c', ' ')
    result_tokens = result.split(' ')

    word_tokens = []
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

    if result in tracked_stems:
        if result in tracked_stems:
            stems[result] = stems.get(result, [])
            if word not in stems[result]:
                stems[result].append(word)
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
    '',
    '',
    '',
    '',
    ''
]
special_phrases_re = []

for s in special_phrases:
    parts = s.split(' ')
    regex = r'.*'
    for part in parts:
        regex += r'[\s\u200c]*' + part
    regex += '.*'
    special_phrases_re.append([re.compile(regex), s])


def special_phrases_search(text):
    result = []
    for phrase in special_phrases_re:
        if phrase[0].match(text) is not None:
            result.append(phrase[1])
    return result
