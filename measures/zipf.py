# Calculate and draw zipf

from math import log10
from measures.plot import draw_prediction_line_with_actual_points

from util.file import read_dictionary_from_file


def get_frequency(pair):
    return pair[1]


def draw_zipf_plot(dictionary,threshold):
    term_list = []
    for key in dictionary:
        term_list.append((key, dictionary[key]))
    term_list.sort(key=get_frequency, reverse=True)
    cf1 = term_list[0][1]
    cf2 = term_list[1][1]
    m = -1
    b = log10(cf2) + log10(2)

    points = []
    for i in range(len(term_list)):
        if term_list[i][1] == 0:
            break
        if i > 100:
            if i % 50 != 0:
                continue
        points.append((log10(i+1), log10(term_list[i][1])))

    draw_prediction_line_with_actual_points(0, threshold, m, b, 'Zipf law', points,'log10 rank','log10 cf')


d0 = read_dictionary_from_file('../dictionary.txt')

d1 = read_dictionary_from_file('../dictionary_2.txt')
draw_zipf_plot(d0,20)
draw_zipf_plot(d1,20)
