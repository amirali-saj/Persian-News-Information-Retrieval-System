import re


def html_filter(html_content):
    html_stuff = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
    return re.sub(html_stuff, ' ', html_content)


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
    (['َ', '“', 'ّ,', 'ً', '؛', 'ُ', 'ٔ', '؟', ',', 'ِ', '”', '\u200f', '\u200e', '\u200d', '\u202c', '\u200a',
      '\u202b'], ''),
    (['\u1680', '\u2005', '\u2006', '\u2009', '\u200A', '\u200B', '\u202F', '\uFEFF'], '\u200c')
]

for x in normalization_list_table:
    print(x[0])
    for char in x[0]:
        normalization_table[char] = x[1]
        print(char, '\n', x[1])
        print('\n\n')


def normalize(text):
    new_text = ''
    for c in text:
        replacement = normalization_table.get(c, c)
        new_text += replacement
    return text

