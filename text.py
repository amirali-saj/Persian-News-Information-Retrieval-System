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
