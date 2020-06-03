stopwords = None


def get_stopwords():
    global stopwords
    if stopwords is None:
        stopwords = []

        f = open('files/stop_words.txt', 'r')
        # txt = f.read()
        # txt2 = txt.split('\r')
        word = 'not none'
        # for word in txt2:
        #     stopwords.append(word)
        while word is not None and word != '':
            word = f.readline()
            word = word[:-1]
            if word != '':
                stopwords.append(word)
    return stopwords
