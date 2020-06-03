from nlp.tokenization import get_stopwords, get_character_stopwords, simple_tokenize
from nlp.text import html_filter, stop_word_filter
import sys
import csv

csv.field_size_limit(sys.maxsize)

with open('dataset/ir-news-0-2.csv', newline='') as f:
    reader = csv.reader(f)
    data = list(reader)

# print(data[0])
# print(data[200][5]) #1,3,5,6
print(data[200][6])
print()
tokens = simple_tokenize(str(stop_word_filter(html_filter(data[200][6]), get_character_stopwords())), ' ')

print(tokens)
print(len(tokens))
print()
tokens = stop_word_filter(tokens, get_stopwords())
print(tokens)
print(len(tokens))

# print(len(data))
# print(get_stopwords())
